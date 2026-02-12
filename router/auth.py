#  login api and sigin api
from fastapi import APIRouter  , Depends , HTTPException
from database.db import get_db
from sqlalchemy.orm import Session
from database.schema import user
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from Businesslogic.auth import create_user , create_access_token , authenticate_user , get_current_user
auth = APIRouter(prefix="/auth" , tags=['auth'])
def require_role(required_roles: list[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in required_roles:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission"
            )
        return current_user
    return role_checker
# for Rabc

@auth.post("/Login")
def login(form_data :Session= Depends(OAuth2PasswordRequestForm) , db : Session = Depends(get_db)):
   user = authenticate_user(form_data.username ,  form_data.password, db)
   token = create_access_token(user_id= user.user_id , username= user.username  , role = user.role , expire_time=timedelta(minutes=20))
   return {
      "access_token": token,
      "token_type": "bearer"
      
   }
@auth.post("/Signin")
def new_user(user:user , db : Session = Depends(get_db)):
 return create_user(user , db)
