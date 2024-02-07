import os
from dotenv import load_dotenv
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from semantic_kernel.utils.settings import azure_openai_settings_from_dot_env as config

class Chat:
    def __init__(self,skill_name="ChatSkill",model="gpt-3.5"):
        self.kernel = sk.Kernel()
        self.deployment, self.api_key, self.endpoint = config()
        if(model=="gpt-3.5"):
            load_dotenv()
            self.deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME_35")
        
        self.chat_service = AzureChatCompletion(deployment_name=self.deployment, api_key=self.api_key,
                                           endpoint=self.endpoint)
        self.kernel.add_chat_service("chat", self.chat_service)
        self.skill_name=skill_name
        self.context = self.kernel.create_new_context()

    async def send(self, msg,history:str="",temperature:float=0.9):
        skill = self.kernel.import_semantic_skill_from_directory("./plugins", "Skills")
        chat_function = skill[self.skill_name]
        chat_function.model_config['temperature']=temperature
        if history:
            self.context["history"] = history
        self.context["input"] = msg
        
        result=self.kernel.run_stream_async(chat_function,input_str=msg,input_context=self.context)
        return result
    
    async def get_skills(self):
        skill = self.kernel.import_semantic_skill_from_directory("./plugins", "Skills")
        data=[]
        for item in skill:
            name=skill[item].description.split('。')[0]
            info=skill[item].description.split('。')[-1]
            data.append({'id':item,'name':name,'info':info})
        return data
