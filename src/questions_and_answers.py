import argparse
from bedrock_client import BedrockClient


class QuestionsAndAnswers:

    def __init__(self):
        self.tmp_folder = 'src/tmp/'
        self.model_id = "anthropic.claude-3-haiku-20240307-v1:0"
        # self.model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
        # self.model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    def ask_things(self, transcription_file: str, summary_language: str, question: str) -> str:
        bedrock_client = BedrockClient()

        with open(transcription_file, "r", encoding="utf-8") as file:
            transcript = file.read()

        SYSTEM_PROMPT = f"""
        You are responsible for answering questions accurately from the <transcript>.

        <transcript>
        {transcript}
        </transcript>

        Answers the following question: 
        <question>
        {question}
        </question>

        Write the answer in {summary_language}

        Don't hallucinate. Don't make up truthful information.
        """
        SYSTEM_PROMPT = f"""
        You are an expert research assistant. Here is a document you will answer questions about:

        <document>
        {transcript}
        </document>

        First, find the quotes from the document that are most relevant to answering the question, and then print them in numbered order. 
        Quotes should be relatively short.

        If there are no relevant quotes, write "No relevant quotes" instead.

        Then, answer the question, starting with "Answer:". Do not include or reference quoted content verbatim in the answer. 
        Don't say "According to Quote [1]" when answering. 
        Instead make references to quotes relevant to each section of the answer solely by adding their bracketed numbers at the end of relevant sentences.

        Thus, the format of your overall response should look like what's shown between the <example></example> tags. 
        Make sure to follow the formatting and spacing exactly.

        <example>
        <quotes>
        [1] "Company X reported revenue of $12 million in 2021."
        [2] "Almost 90% of revene came from widget sales, with gadget sales making up the remaining 10%."
        </quotes>

        <answer>
        Company X earned $12 million. [1]  Almost 90% of it was from widget sales. [2]
        </answer>
        </example>

        Answers the following question: 
        <question>
        {question}
        </question>

        Write the answer in {summary_language}

        If the question cannot be answered by the document, say so.
        Don't hallucinate. Don't make up truthful information.

        Answer the question immediately without preamble.
        """

        completion = bedrock_client.invoke_model(self.model_id, system_prompt="", user_prompt=SYSTEM_PROMPT)

        response_text = completion.get("content")[0]["text"]
        return response_text


def main():
    parser = argparse.ArgumentParser(description="Questions And Answers CLI")
    parser.add_argument(
        "--transcription", type=str, required=False, default='src/tmp/transcription.txt', help="Ruta al fichero de la transcripción"
    )
    parser.add_argument("--question", type=str, required=True, help="Idioma de las respuestas")
    parser.add_argument("--response_language", type=str, required=False, default='Spanish', help="Idioma de las respuestas")

    args = parser.parse_args()

    qa = QuestionsAndAnswers()
    print(qa.ask_things(args.transcription, args.response_language, args.question))


if __name__ == "__main__":
    main()
