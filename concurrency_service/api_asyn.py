from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pipeline import intent_classify_service_asyn
from my_logger import logger
import json

app = FastAPI()

class InterfaceException(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class ProcessRequestModel(BaseModel):
    content: str

@app.post("/process_request/")
async def process_api_request(request_body: ProcessRequestModel):
    try:
        query = request_body.content
        logger.info(f"Received query: {query}")

        response = await intent_classify_service_asyn(query)

        logger.info(f"Response content: {response}")

        return json.loads(response)
    except KeyError as e:
        logger.error(f"KeyError: {str(e)}")
        raise HTTPException(status_code=400, detail={
            "errorcode": "0",
            "result": "1000",
            "data": None,
            "msg": "There is an error in the request parameter"
        })
    except InterfaceException as e:
        logger.error(f"InterfaceException: {str(e)}")
        raise HTTPException(status_code=500, detail={
            "errorcode": "0",
            "result": "108",
            "data": None,
            "msg": "The atomic service is running abnormally"
        })
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=500, detail={
            "errorcode": "0",
            "result": "1099",
            "data": None,
            "msg": "Program running exception"
        })

if __name__ == "__main__":
    import uvicorn
    from config import API_SERVICE_CONFIG

    uvicorn.run(app, host=API_SERVICE_CONFIG['host'], port=API_SERVICE_CONFIG['port'])
