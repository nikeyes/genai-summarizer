import json
import boto3
import os


class BedrockClient:
    client: boto3.client = None

    def __init__(self):
        boto3.setup_default_session(profile_name='genai-dev')

        aws_region_paris = 'eu-west-3'
        aws_region_frankfurt = 'eu-central-1'

        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name=aws_region_frankfurt,
        )

    def invoke_model(self, model_id: str, system_prompt: str, user_prompt: str):
        body = json.dumps(
            {
                "system": system_prompt,
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2048,
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": user_prompt}],
                    },
                    {
                        "role": "assistant",
                        "content": "",
                    },
                ],
                "temperature": 0,
                "top_k": 250,
                "top_p": 0.999,
                "stop_sequences": ["\n\nHuman:", "\n\nAssistant", "</function_calls>"],
            }
        )

        accept = 'application/json'
        content_type = 'application/json'

        response = self.client.invoke_model(
            modelId=model_id,
            body=body,
            accept=accept,
            contentType=content_type,
        )

        completion = json.loads(response.get("body").read())
        return completion
