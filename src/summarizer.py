import os
import sys
import subprocess
import re
import tempfile
import uuid
import argparse
import moviepy.editor as mp
from groq import Groq
from bedrock_client import BedrockClient
from pytubefix import YouTube


class Summarizer:

    def __init__(self):
        self.tmp_folder = 'src/tmp/'
        self.model_id = "anthropic.claude-3-haiku-20240307-v1:0"
        # self.model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
        # self.model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"


    def summarize(self, filename: str, context: str, audio_language: str, summary_language: str):
        file_type = self.__get_file_type(filename)
        if file_type == "Video":
            audio_file = self.__extract_audio_from_video(filename)
        elif file_type == "YouTube":
            audio_file = self.__extract_audio_from_youtube(filename)
        elif file_type == "Audio":
            audio_file = filename
        else:
            sys.exit(
                """Formato de archivo no soportado. Solo soportamos: 
                - URLs de Youtube
                - Audio: mp3, wav, aac, flac, ogg, m4a
                - Video: mp4, mkv, avi, mov, wmv, flv
                     """
            )

        audio_file_compressed = self.__compress_audio(audio_file)
        self.__check_audio_file_size(audio_file_compressed)
        transcription_file = self.__transcript_audio(
            audio_file_compressed,
            context,
            audio_language,
        )
        summary = self.summarize_with_llm(transcription_file, summary_language)
        return summary

    def ask_things(self, transcription_file: str, summary_language: str) -> str:
        bedrock_client = BedrockClient()

        with open(transcription_file, "r", encoding="utf-8") as file:
            transcript = file.read()

        SUMARIZATION_PROMPT = f"""You are responsible for answering questions accurately from the <transcript>.

        <transcript>
        {transcript}
        </transcript>

        Write the answer in {summary_language}

        Don't hallucinate. Don't make up truthful information.
        """

        completion = bedrock_client.invoke_model(self.model_id, system_prompt="", user_prompt=SUMARIZATION_PROMPT)

        response_text = completion.get("content")[0]["text"]
        return response_text

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

        with tempfile.NamedTemporaryFile(delete=False, dir=self.tmp_folder, suffix=".txt", mode="w", encoding="utf-8") as temp_file:
            temp_file.write(transcription.text)
            temp_file_name = temp_file.name

        print(f"Transcripción guardada en: {temp_file_name}")
        return temp_file_name

    def summarize_with_llm(self, transcript_file_name: str, summary_language: str) -> str:
        bedrock_client = BedrockClient()

        with open(transcript_file_name, "r", encoding="utf-8") as file:
            transcript = file.read()

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

        completion = bedrock_client.invoke_model(self.model_id, system_prompt="", user_prompt=SUMARIZATION_PROMPT)

        response_text = completion.get("content")[0]["text"]
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


def main():
    parser = argparse.ArgumentParser(description="Summarizer CLI")
    parser.add_argument("--url", type=str, required=True, help="URL del contenido a resumir")
    parser.add_argument("--context", type=str, required=False, help="Contexto adicional para la transcripción")
    parser.add_argument("--language", type=str, required=False, default='es', help="Idioma del contenido")
    parser.add_argument("--summary_language", type=str, required=False, default='Spanish', help="Idioma del resumen")

    args = parser.parse_args()

    summarizer = Summarizer()
    print(summarizer.summarize(args.url, args.context, args.language, args.summary_language))


if __name__ == "__main__":
    main()
