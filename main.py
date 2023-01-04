from fastapi import FastAPI
from routers import user, auth
from fastapi.exceptions import RequestValidationError, ValidationError
import json
from starlette.responses import JSONResponse



app = FastAPI()
app.include_router(user.api)
app.include_router(auth.auth)


@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
async def valdtion_handeler(request, exec):
    exc_json = json.loads(exec.json())
    response = {"status": False, "data": None, "message":{"data":[]}}
    print(exc_json)
    for error in exc_json:
        print(response)
        response["message"]["data"].append({error['loc'][1]:error['msg']})
    return JSONResponse(response, status_code=422)