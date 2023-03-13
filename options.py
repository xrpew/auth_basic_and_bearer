from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import  HTTPBasic, HTTPBearer,HTTPBasicCredentials,OAuth2PasswordRequestForm
from typing import Optional
from jose import jwt
import datetime

app = FastAPI()

oauth2 = HTTPBearer(auto_error=False)
security = HTTPBasic(auto_error=False)

def basic_auth(credentials: Optional[HTTPBasicCredentials] = Depends(security)):
    try:
        return credentials
    except:
        return None

def bearer_auth(token:Optional[str] =Depends(oauth2)):
    try:
        decode = jwt.decode(token.credentials, "secret", algorithms=["HS256"])
        return decode
    except:
        return None

def create_jwt_token(username: str) -> str:
    payload = {"name": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
    token = jwt.encode(payload, 'secret', algorithm="HS256")
    return token

def get_type_auth(
        token: Optional[str] = Depends(bearer_auth),
        credentials:Optional[HTTPBasicCredentials] = Depends(basic_auth),
        ):
    if token is not None:
        print('3')
        print(token, 'get_type')
        return token
    if credentials is not None:
        print('3')
        print(credentials, 'get_type')
        return credentials
    raise HTTPException(status_code=401, detail="No autenticado")



@app.get("/")
async def read_root(current_user:str = Depends(get_type_auth)):
    return current_user

@app.post('/token')
async def tok(form_data: OAuth2PasswordRequestForm = Depends()):
    token = create_jwt_token(form_data.username)
    return token
