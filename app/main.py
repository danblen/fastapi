from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from api.api_v1.api import api_router

# 创建 FastAPI 实例
app = FastAPI()

# 模拟存储用户数据的数据库
fake_db = []

app.include_router(
    api_router,
)

# # 用户数据模型
# class User(BaseModel):
#     username: str
#     email: str
#     age: Optional[int] = None


# # 创建新用户
# @app.post("/users/", response_model=User)
# def create_user(user: User):
#     fake_db.append(user)
#     return user


# # 获取所有用户
# @app.get("/users/", response_model=List[User])
# def read_users():
#     return fake_db


# # 获取单个用户
# @app.get("/users/{user_id}", response_model=User)
# def read_user(user_id: int):
#     if user_id < len(fake_db):
#         return fake_db[user_id]
#     raise HTTPException(status_code=404, detail="User not found")


# # 更新用户信息
# @app.put("/users/{user_id}", response_model=User)
# def update_user(user_id: int, user: User):
#     if user_id < len(fake_db):
#         fake_db[user_id] = user
#         return user
#     raise HTTPException(status_code=404, detail="User not found")


# # 删除用户
# @app.delete("/users/{user_id}", response_model=User)
# def delete_user(user_id: int):
#     if user_id < len(fake_db):
#         deleted_user = fake_db.pop(user_id)
#         return deleted_user
#     raise HTTPException(status_code=404, detail="User not found")
