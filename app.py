from fastapi import FastAPI
from azure_get_token import router as azure_router
import uvicorn

app = FastAPI()

app.include_router(azure_router,prefix='/azure',tags=['Azure AD'])



if __name__ == '__main__':
    
    uvicorn.run(app, host='0.0.0.0', port=8080)