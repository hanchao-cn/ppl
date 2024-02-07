import contextvars
from dotenv import load_dotenv
from openai import AzureOpenAI
import os
from semantic_kernel import ContextVariables
from semantic_kernel.skill_definition import sk_function


class Dalle3:
    @sk_function(
        description="Generates an with DALL-E 3 model based on a prompt",
        name="ImageFromPrompt",
        input_description="The prompt used to generate the image",
    )
    def ImageFromPrompt(self, input:str) -> str:
        load_dotenv()
        #client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        deployment=os.getenv("AZURE_DALLE3_DEPLOYMENT_NAME")
        apiversion=os.getenv("AZURE_DALLE3_VERSION")
        apikey=os.getenv("AZURE_DALLE3_KEY")
        
        client = AzureOpenAI(api_version=apiversion,azure_endpoint=deployment,api_key=apikey)
        response = client.images.generate(
            model="dalle3",
            prompt=input,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url