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

    def summarize(self, transcription_file: str, summary_language: str):
        summary = self.summarize_with_llm(transcription_file, summary_language)
        return summary

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


def main():
    parser = argparse.ArgumentParser(description="Summarizer CLI")
    parser.add_argument("--transcription", type=str, required=True, help="Ruta al fichero de la transcripción")
    parser.add_argument("--summary_language", type=str, required=False, default='Spanish', help="Idioma del resumen")

    args = parser.parse_args()

    summarizer = Summarizer()
    print(summarizer.summarize(args.transcription, args.summary_language))


if __name__ == "__main__":
    main()
