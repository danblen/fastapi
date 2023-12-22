#!/bin/bash

# 启动 FastAPI 应用
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

