from database.db import get_db
from fastapi import Depends  , HTTPException
from sqlalchemy.orm import Session
from Businesslogic.auth import get_current_user 
from database.schema import task  , update_task
from router.auth import require_role
from database.model import Task , User
#  task_id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     description = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)
def create_task(task : task , user :dict =  Depends(require_role(["user"])),  db : Session = Depends(get_db)):
    current_user = db.query(User).filter(User.username == user.get("username")).first()
    
    if not current_user :
        raise HTTPException(status_code=401 , detail="not valid user")
    
    new_task =  Task(
       title = task.title,
       description = task.description,
       created_at = task.created_at,
       owner_id = current_user.user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
def update_task1( id : str, new_task : update_task , user: dict = Depends(require_role(["user"])) ,   db : Session = Depends(get_db)):
    #    particular task - update it   , json.load , json.loads , model.dump , model.dumps
    new_query = db.query(Task).filter(Task.owner_id == user.get("user_id")).filter(Task.task_id == id).first()
    if new_query is None:
        raise HTTPException(status_code=404 , detail="Task is not found")
    for k , v in new_task.model_dump().items():
        setattr(new_query , k , v)

    db.add(new_query)
    db.commit()
    db.refresh(new_query)
    return new_query 

       
def get_task1(user: dict = Depends(require_role(["user"])) ,   db : Session = Depends(get_db)):
    all_task= db.query(Task).filter(Task.owner_id == user.get("user_id")).all()
    return all_task
def delete_task(id : str,  user: dict  ,   db : Session ):
    task = db.query(Task).filter(Task.owner_id == user.get("user_id")).filter(Task.task_id == id).first()
    if task is None:
        raise HTTPException(status_code=404 , detail="Task is not found")
    db.delete(task)
    db.commit()
    return task