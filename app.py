import boto3
from datetime import datetime
#from boto3.exceptions import ClientError

def get_client(service_name:str, region:str):
    client = boto3.client(service_name,region_name=region)

    return client


model_id = "meta.llama3-8b-instruct-v1:0"
service_name = "bedrock-runtime"
region = "us-east-1"



def generate_details(client,topic):
    query = f" {topic}"
    conversation = [
        {
            "role": "user",
            "content": [{"text": query}],
        }
    ]
    return  f"Information about {topic}"
    try:
        response = client.converse(modelId=model_id, messages=conversation,inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9})
        response_text = response["output"]["message"]["content"][0]["text"]

    except Exception as e:
       
        return e

    return response_text

def save_data(s3_key,s3_bucket, payload):
    s3 = boto3.client('s3')

    try:
        s3.put_object(Bucket = s3_bucket, Key = s3_key, Body = payload)
       
    except Exception as e:
        print(f"Something went wrong {e}")
    
client = get_client(service_name, region)

def lambda_handler(event,context):
    topic = event["body"]
    global client
    data = generate_details(client,topic)
    if data is None:
        print("Something went wrong ! Could not fetch data")
        return None
    
    
    current_time = datetime.now().strftime('%H%M%S')
    s3_key = f"outputs/{current_time}.txt"
    s3_bucket = "geni-bedrock"
    save_data(s3_key=s3_key,s3_bucket=s3_bucket,payload=data)
    return {"status_code ":200,"message":data}

    

lambda_handler({"body":"indian cricket team"},None)