from fastapi import FastAPI, Depends, Request, Header, status, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer ,OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials, HTTPBearer
from typing import Optional

app = FastAPI()

oauth = HTTPBearer(auto_error=False)
security = HTTPBasic()


def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if not credentials:
        return False
    print(f'Basic auth credentials: {credentials.username}:{credentials.password}')
    return credentials.username


def bearer_auth(token: str = Depends(oauth)):
    if not token:
        return False
    print(f'Bearer auth token: {token.credentials}')
    raise HTTPException(status_code=200)


async def check(
    token: Optional[str] = Depends(bearer_auth),
    credentials: Optional[HTTPBasicCredentials] = Depends(basic_auth),
):
    return True


@app.get("/test_jwt", dependencies=[Depends(check)])
async def test_endpoint(request: Request):
    return True