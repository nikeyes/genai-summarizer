from helpers.bedrock_client import BedrockClient
from helpers.config import MODEL_ID, TMP_FOLDER


class Summarizer:
    def __init__(self):
        self.tmp_folder = TMP_FOLDER
        self.model_id = MODEL_ID

    def summarize(self, transcription_file: str, summary_language: str):
        summary = self.summarize_with_llm(transcription_file, summary_language)
        return summary

    def summarize_with_llm(
        self, transcript_file_name: str, summary_language: str
    ) -> str:
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

        ##########################################
        # Optimized version by Anthropic console #
        ##########################################
        # MEETING_MINUTES_PROMPT = f"""You are an expert meeting summarizer. Your task is to accurately summarize a meeting transcript and provide key takeaways. Here's the transcript you need to analyze:

        # <transcript>
        # {transcript}
        # </transcript>

        # Please follow these steps to create an accurate and useful summary:

        # 1. Carefully read and analyze the transcript.
        # 2. In the <analysis> section, identify the main topics discussed, key decisions made, action items assigned, and the people responsible for those actions. Also, extract and list key quotes from the transcript that support each decision, action item, and owner assignment.
        # 3. Create a structured list in the <sketchpad> section with the following components:
        # - <main_topics>: List the main topics discussed during the meeting
        # - <decisions>: List the important decisions made during the meeting
        # - <action_items>: List the tasks or actions that were assigned
        # - <owners>: For each action item, specify who is responsible for it

        # 4. Double-check that all items in your <sketchpad> are factually consistent with the information provided in the transcript. Do not include any information that isn't explicitly stated or directly implied by the transcript.

        # 5. Based on your <sketchpad>, create a concise <summary> of the meeting, highlighting the most important points.

        # 6. Ensure that both your <sketchpad> and <summary> are written in {summary_language}.

        # Important guidelines:
        # - Do not invent or assume any information not present in the transcript.
        # - Be objective and accurate in your summary.
        # - Keep your summary concise but informative.

        # Here's an example of how your output should be structured (use this format, but replace the content with information from the actual transcript):

        # <sketchpad>
        # <main_topics>
        # 1. Project X budget
        # 2. Staffing decisions
        # 3. Q3 financial report
        # </main_topics>

        # <decisions>
        # 1. Approved budget for Project X
        # 2. Postponed decision on new hire until next quarter
        # </decisions>

        # <action_items>
        # 1. Update project timeline
        # 2. Prepare financial report for Q3
        # 3. Schedule follow-up meeting with Team Y
        # </action_items>

        # <owners>
        # 1. John Doe (Project Manager) - Update project timeline
        # 2. Jane Smith (Finance Lead) - Prepare financial report
        # 3. Alice Johnson (Team Lead) - Schedule follow-up meeting
        # </owners>
        # </sketchpad>

        # <summary>
        # The meeting focused on Project X's budget approval and staffing decisions. Key outcomes include the approval of Project X's budget and the postponement of a new hire decision. Action items were assigned to update the project timeline, prepare a Q3 financial report, and schedule a follow-up meeting with Team Y.
        # </summary>

        # Please proceed with your analysis and summary of the provided transcript. """

        ################################
        # Created by Anthropic console #
        ################################
        # MEETING_MINUTES_PROMPT = f"""You are tasked with summarizing an important meeting. The meeting transcript will be provided to you, and your job is to extract and organize key information from it. Here is the meeting transcript:
        # <meeting_transcript>
        # {transcript}
        # </meeting_transcript>

        # Your task is to summarize this meeting by identifying and organizing the following components:

        # 1. Main topics discussed
        # 2. Decisions made
        # 3. Action items agreed upon
        # 4. Owners assigned to action items

        # Please follow these steps to complete the task:

        # 1. Carefully read through the entire meeting transcript.

        # 2. Use a scratchpad to analyze the transcript and identify the key components. In your scratchpad, you can make notes, list potential main topics, decisions, action items, and owners as you find them in the transcript.

        # 3. After your analysis, create a structured summary of the meeting with the following format:

        # <summary>
        # <main_topics>
        # - List the main topics discussed in the meeting
        # - Use bullet points for each topic
        # </main_topics>

        # <decisions>
        # - List the key decisions made during the meeting
        # - Use bullet points for each decision
        # </decisions>

        # <action_items>
        # - List the action items agreed upon in the meeting
        # - Use bullet points for each action item
        # - Include the owner of each action item in parentheses after the item
        # </action_items>
        # </summary>

        # 4. When identifying main topics, look for recurring themes or subjects that took up significant discussion time.

        # 5. For decisions, focus on clear conclusions or agreements reached by the meeting participants.

        # 6. Action items are typically tasks or next steps that were explicitly stated or agreed upon during the meeting. Pay attention to phrases like "we need to," "let's do," or "who will take care of."

        # 7. Owners are the individuals or teams assigned responsibility for specific action items. Look for names or roles mentioned in connection with tasks or responsibilities.

        # 8. Be concise in your summary, but make sure to capture all important information.

        # 9. If you're unsure about including something, err on the side of inclusion rather than omission.

        # 10. Use your best judgment to interpret and categorize the information if it's not explicitly stated in the transcript.

        # Begin your response with your scratchpad analysis, then provide the final structured summary as specified above.

        # Make sure to write your response in {summary_language}."""

        completion = bedrock_client.invoke_model(
            self.model_id, system_prompt="", user_prompt=MEETING_MINUTES_PROMPT
        )

        response_text = completion.get("content")[0]["text"]
        return response_text
