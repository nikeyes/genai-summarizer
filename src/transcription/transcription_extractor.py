import os
import subprocess
import re
import tempfile
import uuid
from urllib.parse import urlparse, parse_qs
import moviepy.editor as mp
from groq import Groq
from pytubefix import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from helpers.config import TMP_FOLDER


class TranscriptionExtractor:

    def __init__(self):
        self.tmp_folder = TMP_FOLDER

    def extract(self, filename: str, context: str, audio_language: str, output_filename: str = None) -> tuple[str, str]:
        file_type = self.__get_file_type(filename)

        if output_filename is None or output_filename == "":
            output_filename = self.get_transcription_file_name(filename)

        if file_type == "Video":
            audio_file = self.__extract_audio_from_video(filename)
            transcription_text = self.__get_transcription_from_audio(audio_file, context, audio_language, output_filename)
        elif file_type == "YouTube":
            transcription_text = self.__get_transcript_from_youtube_video(filename, audio_language, output_filename)
            if transcription_text is None:
                audio_file = self.__extract_audio_from_youtube(filename)
                transcription_text = self.__get_transcription_from_audio(audio_file, context, audio_language, output_filename)
        elif file_type == "Audio":
            audio_file = filename
            transcription_text = self.__get_transcription_from_audio(audio_file, context, audio_language, output_filename)
        else:
            raise Exception(
                """
            Formato de archivo no soportado. Solo soportamos: 
                - URLs de Youtube
                - Audio: mp3, wav, aac, flac, ogg, m4a
                - Video: mp4, mkv, avi, mov, wmv, flv
                """
            )
        return output_filename, transcription_text

    def __get_transcription_from_audio(self, audio_file, context, audio_language, output_filename) -> str:
        audio_file_compressed = self.__compress_audio(audio_file)
        print(f"Audio guardado en: {audio_file_compressed}")
        self.__check_audio_file_size(audio_file_compressed)
        transcription_text = self.__transcript_audio(audio_file_compressed, context, audio_language, output_filename)
        print(f"Transcripción guardada en: {output_filename}")
        return transcription_text

    def __extract_audio_from_video(self, filename_input: str) -> str:
        with tempfile.NamedTemporaryFile(suffix=".mp3", dir=self.tmp_folder, delete=False) as temp_file:
            output_filename = temp_file.name
            clip = mp.VideoFileClip(filename_input)
            clip.audio.write_audiofile(output_filename)
            clip.close()
        return output_filename

    def __extract_audio_from_youtube(self, url: str) -> str:
        yt = YouTube(url)
        yt.check_availability()
        audio = yt.streams.filter(only_audio=True).first()

        output_filename = f"{uuid.uuid4()}.mp3"
        downloaded_file_path = audio.download(output_path=self.tmp_folder, filename=output_filename)

        return downloaded_file_path

    def __compress_audio(self, file_name_mp3: str):
        with tempfile.NamedTemporaryFile(suffix=".mp3", dir=self.tmp_folder, delete=False) as temp_file:
            output_filename = temp_file.name
            command = [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                file_name_mp3,
                "-ar",
                "16000",
                "-ac",
                "1",
                "-map",
                "0:a:",
                output_filename,
                "-y",
            ]
            subprocess.run(command, check=True)
        return output_filename

    def __check_audio_file_size(self, file_name_compress_mp3: str):
        file_size = os.path.getsize(file_name_compress_mp3)

        # 25MB en bytes
        size_limit = 25 * 1024 * 1024

        file_size_mb = round(file_size / (1024 * 1024))

        if file_size > size_limit:
            print(f"El fichero {file_name_compress_mp3} es más grande de 25MB ({file_size_mb}MB).")
            raise Exception("Tamaño máximo del fichero 25MB")

    def __transcript_audio(self, file_name_compress_mp3: str, context: str, audio_language: str, output_filename: str) -> str:

        client = Groq()
        filename = file_name_compress_mp3

        with open(filename, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(filename, file.read()),
                model="whisper-large-v3-turbo",
                response_format="json",
                prompt=context,
                language=audio_language,
                temperature=0.0,
            )

        with open(output_filename, mode="w", encoding="utf-8") as temp_file:
            temp_file.write(transcription.text)

        return transcription.text

    def __get_file_type(self, string: str) -> str:
        youtube_pattern = re.compile(r'(https?://)?(www.)?(youtube|youtu.be)(.com)?/.*')
        audio_pattern = re.compile(r'.*\.(mp3|wav|aac|flac|ogg|m4a)$', re.IGNORECASE)
        video_pattern = re.compile(r'.*\.(mp4|mkv|avi|mov|wmv|flv)$', re.IGNORECASE)

        if youtube_pattern.match(string):
            return "YouTube"
        if audio_pattern.match(string):
            return "Audio"
        if video_pattern.match(string):
            return "Video"

        return "Otros"

    def get_transcription_file_name(self, url_or_filename):
        if self.__get_file_type(url_or_filename) == "YouTube":
            filename = self.__extract_video_id_from_youtube_url(url_or_filename)
        else:
            filename = os.path.basename(url_or_filename)
        filename_with_path = os.path.join(self.tmp_folder, filename + ".txt")
        return filename_with_path

    def __extract_video_id_from_youtube_url(self, url: str) -> str:

        parsed_url = urlparse(url)

        if parsed_url.netloc in ('youtu.be', 'www.youtu.be'):
            # Para URLs cortas de youtu.be
            return parsed_url.path[1:]

        elif parsed_url.netloc in ('youtube.com', 'www.youtube.com'):
            if parsed_url.path == '/watch':
                # Para URLs de tipo youtube.com/watch?v=VIDEO_ID
                query = parse_qs(parsed_url.query)
                return query.get('v', [None])[0]

            elif parsed_url.path.startswith('/embed/'):
                # Para URLs de tipo youtube.com/embed/VIDEO_ID
                return parsed_url.path.split('/')[2]

            elif parsed_url.path.startswith('/v/'):
                # Para URLs de tipo youtube.com/v/VIDEO_ID
                return parsed_url.path.split('/')[2]
            elif parsed_url.path.startswith('/shorts/'):
                # Para URLs de tipo youtube.com/shorts/VIDEO_ID
                return parsed_url.path.split('/')[2]

        # Si no se pudo extraer el ID, devolver None
        return None

    def __get_transcript_from_youtube_video(self, url: str, language: str, output_filename: str) -> str:
        video_id = self.__extract_video_id_from_youtube_url(url)
        if video_id is None:
            return None, None

        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language], preserve_formatting=True)
        formatter = TextFormatter()

        text_transcript = formatter.format_transcript(transcript)

        with open(output_filename, mode="w", encoding="utf-8") as temp_file:
            temp_file.write(text_transcript)

        return text_transcript
