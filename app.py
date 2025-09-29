import boto3
#from boto3.exceptions import ClientError

def get_client(service_name:str, region:str):
    client = boto3.client(service_name,region_name=region)

    return client

model_id = "meta.llama3-8b-instruct-v1:0"
service_name = "bedrock-runtime"
region = "us-east-1"

client = get_client(service_name, region)
query = "TEll me world 7 wonders"

conversation = [
    {
        "role": "user",
        "content": [{"text": query}],
    }
]

try:
    response = client.converse(modelId=model_id, messages=conversation,inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9})
    response_text = response["output"]["message"]["content"][0]["text"]
    print(response_text)

except Exception as e:
    print(f"Error: {e}")