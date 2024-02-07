# Note: DALL-E 3 requires version 1.0.0 of the openai-python library or later
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import json

load_dotenv()
deployment=os.getenv("AZURE_DALLE3_DEPLOYMENT_NAME")
apiversion=os.getenv("AZURE_DALLE3_VERSION")
apikey=os.getenv("AZURE_DALLE3_KEY")

client = AzureOpenAI(api_version=apiversion,azure_endpoint=deployment,api_key=apikey)

result = client.images.generate(
    model="dalle3", # the name of your DALL-E 3 deployment
    prompt="春天成都人在桃树下打麻将，生成素描画",
    n=1
)

image_url = json.loads(result.model_dump_json())['data'][0]['url']
print(result)
