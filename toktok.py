from typing import Union, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasic
from pydantic import BaseModel


app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

security = HTTPBasic()

async def get_basic_user(token: Optional[str] = Depends(oauth2_scheme)):
    print(token)
    return token

async def get_bearer_user(credentials: Optional[str] = Depends(security)):
    print(credentials)
    return credentials

async def get_current_active_user(
        user_basic: Optional[str] = Depends(get_basic_user),
        user_bearer: Optional[str] = Depends(get_bearer_user)
          ):
    if not (user_basic or user_bearer):
        return 'ERROR'
    if user_basic != None:
        return user_basic
    elif user_bearer != None:
        return user_bearer
    




@app.get("/users/me")
async def read_users_me(current_user: str = Depends(get_current_active_user)):
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    hashed_password = form_data.password
    if not hashed_password == '123456':
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": form_data.username, "token_type": "bearer"}