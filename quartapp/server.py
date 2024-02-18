import json
from aiomysql.log import logger
from click import prompt
from exceptiongroup import catch
from quart import Blueprint, Response, current_app, render_template, request, stream_with_context

from common.HttpToWX import wxLogin
from models.draw import Draw
from models.chat import Chat
from common.views.userinfo import userinfo as userInfo

bp = Blueprint("chat", __name__, template_folder="templates", static_folder="static")

@bp.get("/")
async def index():
    return await render_template("index.html")
#聊天
@bp.post("/chat")
async def chat_handler():
    Openid=request.headers.get('Authoruser')
    userinfo=userInfo()
    count=await userinfo.get_chat_count(Openid)
    if count<=0:
        return Response(status=600,mimetype="application/json")
    else:
        pass
    request_message = (await request.get_json())["message"]
    model=request.headers.get('model')
    skill=(await request.get_json())["skill"]
    history=(await request.get_json())["history"]
    temperature=float((await request.get_json())["temperature"])
    @stream_with_context
    async def response_stream():
        if not skill=='':
            chat_coroutine = Chat(skill,model).send(request_message,history,temperature)
            async for event in await chat_coroutine:
                #yield json.dumps(event, ensure_ascii=False) #+ "\n"
                yield event
    try:
        await userinfo.reduc_chat_count(Openid)
    except Exception as e:
        await userinfo.reduc_chat_count(Openid)
        print(e)
    finally:
        return Response(response_stream(),mimetype="text/event-stream")
    
    
#微信登录
@bp.post('/wxlogin')
async def wxlogin():
   #Unionid=request.headers.get('X-Wx-Unionid')
    Openid=request.headers.get('X-Wx-Openid')
    userinfo=userInfo()
    if Openid is not None:
        if await userinfo.isUserExist(Openid):
            await userinfo.update_login_time(Openid)
            logger.info('user exist')
        else:
            logger.info('user not exist')
            await userinfo.addUser(Openid)
    else:
        return json.dumps({'errcode':-1,'errmsg':'Openid is None'})
    data={'openId':Openid}
    return json.dumps(data)
    
    # request_info= (await request.get_json())
    # openid=request_info['openId']

    # #去微信申请openid和session_key
    # if(openid==''):
    #     appid=request_info['appId']
    #     code=request_info['token']
    #     result=wxLogin(appid,code)
    #     if result.status_code==200:
    #         result_json=result.json()
    #         result_json['session_key']
    #         print(result_json['openid'])
    #         data={'openId':result_json['openid']}
    #         return json.dumps(data)
    #     else:
    #         data={'errcode':result_json['errcode'],'errmsg':result_json['errmsg']}
    #         return json.dumps(data)
        
    # #去查询openid对应的session_key

#获取技能角色列表
@bp.post('/rolesCategory')
async def rolesCategory():
    r=await Chat().get_skills()
    return json.dumps(r)

#获取产品列表
@bp.post('/pay/produceCategory')
async def produceCategory():
    r={"data":[{"productName":"test","chatPlusCount":"100","drawCount":"10","price":"1000"}]}
    return json.dumps(r)
#返回剩余聊天次数
@bp.post('/getChatCount')
async def getChatCount():
    await wxlogin()
    Openid=request.headers.get('X-Wx-Openid')
    userinfo=userInfo()
    chat_count=await userinfo.get_chat_count(Openid)
    voice_count=await userinfo.get_voice_count(Openid)
    img_count=await userinfo.get_img_count(Openid)
    data={'chat_count':chat_count,'voice_count':voice_count,'img_count':img_count}
    return json.dumps(data)

#创建绘图并返回图片的url
@bp.post('/drawCreateTask')
async def drawCreateTask():
    request_info= (await request.get_json())
    Openid=request.headers.get('authU')
    userinfo=userInfo()
    count=await userinfo.get_img_count(Openid)
    if count<=0:
        return Response(status=600,mimetype="application/json")
    else:
        prompt=request_info["prompt"]
        img=Draw()
        img_url= await img.generateImg(prompt)
        try:
            await userinfo.reduc_img_count(Openid)
        except Exception as e:
            print(e)
            await userinfo.reduc_img_count(Openid)
        
        return img_url



#测试api
@bp.post('/test')
async def test():
    # userinfo=userInfo()
    # await userinfo.addUser('test')
    # if await userinfo.isUserExist('test'):
    #     print('user exist')
    # else:
    #     print('user not exist')
    # print("count chat reduc:"+str(await userinfo.reduc_chat_count('test')))
    # print("count chat add:"+str(await userinfo.add_chat_count('test')))
    # print("count img reduc:"+str(await userinfo.reduc_img_count('test')))
    # print("count img add:"+str(await userinfo.add_img_count('test')))
    # print("count voice reduc:"+str(await userinfo.reduc_voice_count('test')))
    # print("count voice add:"+str(await userinfo.add_voice_count('test')))
    # print("get role:"+str(await userinfo.get_role('test')))
    # print("set role:"+str(await userinfo.set_role('test',1)))
    # del userinfo
    print('Unionid:'+request.headers.get('X-Wx-Unionid'))
    print('Openid:'+request.headers.get('X-Wx-Openid'))
    data={'Unionid':request.headers.get('X-Wx-Unionid'),'Openid':request.headers.get('X-Wx-Openid')}
    return data

