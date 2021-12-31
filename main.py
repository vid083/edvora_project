from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException, FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi_socketio import SocketManager


users = {"vidya": {"password": "secret1"}, "edvora": {"password": "secret2"}}  #fake users without hash password

# fastapi
app = FastAPI()             
# socketio server
socket_manager = SocketManager(app=app)


# token_path
oauth_scheme = OAuth2PasswordBearer(tokenUrl="tokengen")

# template for client
templates = Jinja2Templates(directory="templates")


@app.post("/tokengen")
async def token_gen(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data) #debug
    if form_data.username not in users: #check for user exist
        raise HTTPException(
            status_code=403, detail="Invalid user or password"
        )
    db_password = users[form_data.username]["password"]
    if not form_data.password == db_password: #password match
        raise HTTPException(
            status_code=403, detail="Invalid user or password"
        )
    return{"access_token": form_data.username, "token_type":"bearer"}


@app.get("/aboutme")
async def aboutme(token: str = Depends(oauth_scheme)):
    print(token)
    return{
        "name": "edvora",
        "type": "project"
    }

@app.sio.event
def connect(sid, environ):
    print("connect ", sid)
    # need to implement auth
    # username = authenticate_user(environ)
    # app.sio.save_session(sid, {'username': username})

@app.sio.on('message')
async def message(sid, data):
    print("message ", data)
    await app.sio.emit('response', 'hi ' + data, broadcast=True)

@app.get("/info")
async def settings(request: Request):
    return templates.TemplateResponse("index.html",context={"request": request})

