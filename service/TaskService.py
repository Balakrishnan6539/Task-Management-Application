from sqlalchemy.orm import Session
from Database.Models import Task,Status,Project,User,Priorities,Task_Comments
from fastapi import HTTPException


def CreateTask(task : Task, db: Session, sesion_user_id : int):

    existing_task=db.query(Task).filter(Task.title==task.title,Task.project_id==task.project_id).first()
    if existing_task:
        raise HTTPException(status_code=403, detail="task title alread")
    new_task=Task(
        project_id=task.project_id,
        assigned_to = task.assigned_to,
        title = task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        start_date=task.start_date,
        end_date=task.end_date,
        created_by=sesion_user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"message": "task created successfully"}

def getTaskById(task_id: int, db : Session ):
    task= db.query(Task).filter(Task.task_id==task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

def getAllTaskInProject(project_id : int, db : Session ):

    checkProject=db.query(Project).filter(Project.project_id==project_id).first()
    if not checkProject:
        raise HTTPException(status_code=404, detail="there is no project in this id")

    tasks=db.query(Task).filter(Task.project_id==project_id).all()

    if not tasks:
        raise HTTPException(status_code=404, detail="there are no task in this project")

    return tasks

def updateTask(update_data: Task, task_id : int, db : Session ):

    task=db.query(Task).filter(Task.task_id==task_id).first()

    if not task:
        raise HTTPException(status_code=404 , detail="Task not found in the application")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task

def deleteTask(task_id : int, db : Session):
    task=db.query(Task).filter(task_id==Task.task_id).first()
    if not task:
        raise HTTPException(status_code=404 , detail="task not found")

    db.delete(task)
    db.commit()

    return {"message":"Task deleted successfully"}

def assignTaskToUser(task_id : int , user_id : int , db: Session):
    task = db.query(Task).filter(Task.task_id==task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not fount or incorrect task id")

    setattr(task,"assigned_to",user_id)
    db.commit()
    db.refresh(task)

    return {"message": f"{task.title} is assigned to {task.assigned_user.username}"}

def getAllTaskOfUser(user_id : int, db : Session):
    user=db.query(User).filter(User.user_id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="metioned user is not found or invalid")
    tasks=db.query(Task).filter(Task.assigned_to==user_id).all()

    if not tasks:
        raise HTTPException(status_code=400 , detail="there is no task unser this user")

    return tasks


def getTaskByPriority(priority_id : int, db : Session):

    priority=db.query(Priorities).filter(Priorities.priority_id==priority_id).first()

    if not priority:
        raise HTTPException(status_code=404 , detail="there is no priority like you mentioned")

    tasks=db.query(Task).filter(Task.priority==priority_id).all()

    if not tasks:
        raise HTTPException(status_code=400 , detail="there is no task with this priority")

    return tasks

def getTaskByStatus(status_id : int, db : Session):

    status=db.query(Status).filter(Status.status_id==status_id).first()

    if not status:
        raise HTTPException(status_code=404 , detail="there is no status like you mentioned")

    tasks=db.query(Task).filter(Task.status==status_id).all()

    if not tasks:
        raise HTTPException(status_code=400 , detail="there is no task with this status")

    return tasks

def getAllTaskOfCurrentUser(session_user_id: int, db: Session):
    tasks=db.query(Task).filter(Task.assigned_to==session_user_id).all()

    if not tasks:
        raise HTTPException(status_code=400 , detail="there is no task under you")

    return tasks

def saveTaskComments(session_user_id: int, comment_data: Task_Comments, db : Session ):

    new_comment= Task_Comments(
        task_id=comment_data.task_id,
        comment_text=comment_data.comment_text,
        user_id=session_user_id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {"message":"Comment saved successfully"}

def getComment(comment_id : int,db : Session):
    comment=db.query(Task_Comments).filter(Task_Comments.comment_id==comment_id).first()
    if not comment:
        raise HTTPException(status_code=404,detail="comment not found")
    return comment

def getTaskCommentByTask(task_id:int , db: Session):

    task=db.query(Task).filter(Task.task_id).first()
    if not task:
        raise HTTPException(status_code=400, detail="there is no task like you metioned")


    taskComments=db.query(Task_Comments).filter(Task_Comments.task_id==task_id).all()

    if not taskComments:
        raise HTTPException(status_code=404 , detail="there is no comment for this task")

    return taskComments