import semantic_kernel as sk
from plugins.DALLE3 import Dalle3

class Draw:
    def __init__(self):
        self.kernel = sk.Kernel()
        self.skill = self.kernel.import_skill(Dalle3())
    
    async def generateImg(self,prompt:str):

        img_url=await self.kernel.run_async(self.skill['ImageFromPrompt'],input_str=prompt)
        return img_url.result