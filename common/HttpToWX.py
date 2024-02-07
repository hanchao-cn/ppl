import os

import requests
from dotenv import load_dotenv


#登陆时获取openid和session_key
def wxLogin(appid,code):
    load_dotenv()
    Key=os.environ.get("WEIXIN_APP_KEY")
    url=f"https://api.weixin.qq.com/sns/jscode2session?appid="+appid+"&secret="+Key+"&js_code="+code+"&grant_type=authorization_code"
    r=requests.get(url=url)
    if r.status_code==200:
          return r             
    else:
          if r.json()['errcode']==-1:
               print("系统繁忙，稍候再试")
          elif r.json()['errcode']==40029:
               print("code 无效")
          elif r.json()['errcode']==45011:
               print("频率限制，每个用户每分钟100次")
          elif r.json()['errcode']==40226:
               print("高风险等级用户，小程序登录拦截 。") 
          
          print("获取openai和sessionkey失败："+r.status_code)
          return r
     
