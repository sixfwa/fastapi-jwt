import fastapi as _fastapi
import fastapi.security as _security

import sqlalchemy.orm as _orm

import services as _services
import schemas as _schemas

app = _fastapi.FastAPI()

@app.post("/api/users")
async def create_user(user: _schemas.UserCreate, db:_orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.get_user_by_email(email=user.email, db=db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="User with that email already exists")

    user = await _services.create_user(user=user, db=db)

    return await _services.create_token(user=user)

@app.post("/api/token")
async def generate_token(form_data: _security.OAuth2PasswordRequestForm=_fastapi.Depends(), db: _orm.Session=_fastapi.Depends(_services.get_db)):
    user = await _services.authenticate_user(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")