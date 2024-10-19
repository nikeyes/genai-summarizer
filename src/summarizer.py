import os
import sys
import subprocess
import re
import tempfile
import uuid
import moviepy.editor as mp
from groq import Groq
from bedrock_client import BedrockClient
from pytubefix import YouTube


class Summarizer:

    def __init__(self, filename: str, context: str, audio_language: str, summary_language: str):
        self.tmp_folder = 'src/tmp/'
        self.filename = filename
        self.context = context
        self.audio_language = audio_language  # 'en' https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes
        self.summary_language = summary_language

    def summarize(self):
        file_type = self.__get_file_type(self.filename)
        if file_type == "Video":
            audio_file = self.__extract_audio_from_video(self.filename)
        elif file_type == "YouTube":
            audio_file = self.__extract_audio_from_youtube(self.filename)
        elif file_type == "Audio":
            audio_file = self.filename
        else:
            sys.exit(
                """Formato de archivo no soportado. Solo soportamos: 
                - URLs de Youtube
                - Audio: mp3, wav, aac, flac, ogg, m4a
                - Video: mp4, mkv, avi, mov, wmv, flv
                - Ficheros de texto: txt, csv
                     """
            )

        audio_file_compressed = self.__compress_audio(audio_file)
        self.__check_audio_file_size(audio_file_compressed)
        transcription = self.__transcript_audio(
            audio_file_compressed,
            self.context,
            self.audio_language,
        )
        summary = self.__call_llm(transcription, self.summary_language)
        self.__clean_tmp(self.tmp_folder)
        return summary

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

        print(f"Audio descargado exitosamente: {downloaded_file_path}")
        return downloaded_file_path

    def __compress_audio(self, file_name_mp3: str):
        with tempfile.NamedTemporaryFile(suffix=".mp3", dir=self.tmp_folder, delete=False) as temp_file:
            output_filename = temp_file.name
            command = [
                "ffmpeg",
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
            sys.exit("Tamaño máximo del fichero 25MB")

    def __transcript_audio(self, file_name_compress_mp3: str, context: str, audio_language: str) -> str:

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
            print(transcription.text)
        return transcription.text

    def __call_llm(self, transcript: str, summary_language: str) -> str:
        MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
        # MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
        # MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"
        bedrock_client = BedrockClient()

        SUMARIZATION_PROMPT = f"""You are responsible for accurately summarizing the meeting <transcript>.

        <transcript>
        {transcript}
        </transcript>

        Think step by step on how to summarize the <transcript> within the provided <sketchpad>.

        In the <sketchpad>, return a list of <decision>, <action_item>, and <owner>.

        Then, check that <sketchpad> items are factually consistent with the <transcript>.

        Finally, return a short <summary> based on the <sketchpad>.

        Write the answer in {summary_language}

        Don't hallucinate. Don't make up truthful information.
        """

        completion = bedrock_client.invoke_model(MODEL_ID, system_prompt="", user_prompt=SUMARIZATION_PROMPT)

        response_text = completion.get("content")[0]["text"]
        print(response_text)
        return response_text

    def __get_file_type(self, string: str) -> str:
        youtube_pattern = re.compile(r'(https?://)?(www.)?(youtube|youtu.be)(.com)?/.*')
        audio_pattern = re.compile(r'.*\.(mp3|wav|aac|flac|ogg|m4a)$', re.IGNORECASE)
        video_pattern = re.compile(r'.*\.(mp4|mkv|avi|mov|wmv|flv)$', re.IGNORECASE)

        if youtube_pattern.match(string):
            return "YouTube"
        elif audio_pattern.match(string):
            return "Audio"
        elif video_pattern.match(string):
            return "Video"
        else:
            return "Otros"

    def __clean_tmp(self, folder_path: str):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                if filename.lower().endswith(('.mp3', '.txt')):
                    os.remove(file_path)
                    print(f"Deleted: {filename}")


# https://www.youtube.com/watch?v=7iiE-cE03So
# video_youtube.mp4
summarizer = Summarizer('pepeti.gggg', 'reglas del virus', 'es', 'Spanish')
print(summarizer.summarize())
