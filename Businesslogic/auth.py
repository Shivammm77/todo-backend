from fastapi import APIRouter  , Depends , HTTPException
from database.db import get_db
from sqlalchemy.orm import Session
from database.schema import user
from database.model import User , role
from jose import jwt , JWTError
from datetime import datetime , timedelta
from  passlib.context import CryptContext
import os 
from dotenv import load_dotenv
load_dotenv()
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer

bycrpt = CryptContext(schemes=['bcrypt'] , deprecated = ['auto'])
algo = os.getenv("alg")
Secret_key = os.getenv("secret")
oauth2 = OAuth2PasswordBearer(tokenUrl="api/v1/auth/Login")
def authenticate_user(username , password , db :Session = Depends(get_db)):
    user  = db.query(User).filter(User.username == username).first()
    if not user :
        raise HTTPException(status_code=401 , detail="user not found")
    if not  bycrpt.verify( password, user.hash_password ):
        raise HTTPException(status_code=401 , detail="password is wrong")
    return user
def create_user(user : user , db : Session = Depends(get_db)): 
    if user.role not in [role.user.value , role.admin.value]:
        raise HTTPException(status_code=403 , detail="given role is not allowed")
    new_user = User(
        
        full_name = user.fullname,
        username = user.username,
        hash_password = bycrpt.hash(user.passowrd),
        student =  user.student,
        role = user.role
)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
def create_access_token( user_id, username , role: role , expire_time : timedelta):
    encode = {'id' : user_id , 'sub' : username , 'role' :role }
    expire = datetime.now() + expire_time
    encode.update({'exp':expire})
    return jwt.encode(encode , Secret_key ,algorithm=algo)
def get_current_user(token:str=Depends(oauth2) ):
    
    try : 
      payload = jwt.decode(token ,  Secret_key , algorithms=[algo])
      username = payload.get("sub") 
      user_id = payload.get("id")
      user_role = payload.get("role")
      if user_role not in [role.user.value , role.admin.value]:
        raise HTTPException(status_code=403 , detail="given role is not allowed") 
      if username is None or user_id is None :
          raise HTTPException(status_code=401 , detail="User is not found")
      return {"username" : username , "user_id" : user_id , "role" : user_role}
    except JWTError:
        raise HTTPException(
            status_code=401, 
            detail="Token is invalid or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )



    

    