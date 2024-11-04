from helpers.bedrock_client import BedrockClient
from helpers.config import TMP_FOLDER, MODEL_ID


class Summarizer:

    def __init__(self):
        self.tmp_folder = TMP_FOLDER
        self.model_id = MODEL_ID

    def summarize(self, transcription_file: str, summary_language: str):
        summary = self.summarize_with_llm(transcription_file, summary_language)
        return summary

    def summarize_with_llm(self, transcript_file_name: str, summary_language: str) -> str:
        bedrock_client = BedrockClient()

        with open(transcript_file_name, "r", encoding="utf-8") as file:
            transcript = file.read()

        MEETING_MINUTES_PROMPT = f"""You are responsible for accurately summarizing the meeting <transcript>.

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

        completion = bedrock_client.invoke_model(self.model_id, system_prompt="", user_prompt=MEETING_MINUTES_PROMPT)

        response_text = completion.get("content")[0]["text"]
        return response_text
