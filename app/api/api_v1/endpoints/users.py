from fastapi import FastAPI, HTTPException
from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
import pydantic
import requests
from datetime import datetime, date
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import datetime, date
from db.engine import db
from fastapi.responses import JSONResponse
import json

# pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str
# from config.wxConfig import wxConfig


wxConfig = {
    "appid": "wx3e67e2268416075f",
    "secret": "c49ae70f9b671c074c3f684687c27177",
    "url": "https://api.weixin.qq.com/sns/jscode2session",
    "grant_type": "authorization_code",
}

router = APIRouter()


# # 获取所有用户
@router.get("/")
def read_users():
    return "asd"


class WechatLoginData(BaseModel):
    code: str


@router.post("/wechat_login")
def wechat_login(data: WechatLoginData):
    wechat_params = {
        "appid": wxConfig["appid"],
        "secret": wxConfig["secret"],
        "js_code": data.code,
        "grant_type": wxConfig["grant_type"],
    }
    wechat_response = requests.get(wxConfig["url"], params=wechat_params)
    wechat_data = wechat_response.json()

    session_key = wechat_data.get("session_key")
    openid = wechat_data.get("openid")
    users_collection = db.users

    user = users_collection.find_one({"user_id": openid})
    if not user:
        # 用户不存在，创建新用户
        default_user = {
            "user_id": openid,
            "points": 20,
            "is_check": False,
        }
        new_user_id = users_collection.insert_one(default_user).user_id
        user = users_collection.find_one({"user_id": new_user_id})
        print(user)
        response_data = {"code": 200, "session_key": session_key, "data": user}
    else:
        # 用户存在，更新用户信息
        users_collection.update_one(
            {"user_id": user["user_id"]},
            {
                "$set": {
                    "last_check_date": datetime.combine(
                        date.today(), datetime.min.time()
                    )
                }
            },
        )
        user = users_collection.find_one({"_id": user["_id"]})
        response_data = {
            "code": 0,
            "session_key": session_key,
            "data": user,
        }
    response_data = json.loads(dumps(response_data))
    # response_data.pop("_id", None)
    # 假设您有一个方法来处理和返回用户信息
    return response_data


@router.post("/get_user")
async def get_user(user_id: str):
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if user:
        response_data = {
            "code": 0,
            "data": user,
        }
        return json.loads(dumps(response_data))

    else:
        raise HTTPException(status_code=404, detail="User not found")
