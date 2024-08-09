# -- coding: utf-8 --

from my_logger import *
from fastapi import FastAPI, HTTPException, Request
from pipeline import InterfaceException
from pydantic import BaseModel
from pipeline import intent_classify_service
import uvicorn
from config import API_SERVICE_CONFIG

app = FastAPI()

class ProcessRequestModel(BaseModel):
    content: str

@app.post("/process_request/")
async def process_api_request(request: Request, request_body: ProcessRequestModel):
    try:
        # 记录请求的header
        headers = dict(request.headers)
        logger.info(f"Request Headers: {headers}")

        # 记录请求的body
        body = dict(request_body)
        logger.info(f"Request Body: {body}")

        # 从请求中抽取content内容
        query = request_body.content
        response = intent_classify_service(query)

        # 将响应内容写入日志
        logger.info(f"Response content: {response}")

        return response
    except KeyError:
        # 如果请求体缺少必要的键
        raise HTTPException(status_code=400, detail={
            "errorcode": "0",
            "result": "1000",
            "data": None,
            "msg": "There is an error in the request parameter"
        })
    except InterfaceException as e:
        # 处理接口异常
        raise HTTPException(status_code=500, detail={
            "errorcode": "0",
            "result": "108",
            "data": None,
            "msg": "The atomic service is running abnormally"
        })
    except Exception as e:
        # 捕捉其他所有异常
        raise HTTPException(status_code=500, detail={
            "errorcode": "0",
            "result": "1099",
            "data": None,
            "msg": "Program running exception"
        })

if __name__ == "__main__":
    uvicorn.run(app, host=API_SERVICE_CONFIG['host'], port=API_SERVICE_CONFIG['port'])
