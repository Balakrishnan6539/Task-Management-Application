from fastapi import APIRouter,Depends,HTTPException,Response
from sqlalchemy.orm import Session
from Database.DB_connection import get_db
from Security.JWTAuth import is_valid_user
from Constant.EnumConstant import TeamRole
from schemas.schemasData.MessageResponseSchema import MessageResponse
from schemas.schemasData.TaskSchema import TaskCommentResponse,TaskCommentsrequest,TaskRequest,TaskResponse,TaskUpdaterequest
from service import TaskService


taskRouter=APIRouter(tags="Task Router")

@taskRouter.post("/task/create", response_model=MessageResponse)
def CreateTask(Task_data: TaskRequest,session_user_id: int =Depends(is_valid_user([TeamRole.PM])),db : Session = Depends(get_db)):
    return TaskService.CreateTask(Task_data,db,session_user_id)

@taskRouter.get("/task/get/{task_id}",response_model=TaskResponse)
def getTaskById(task_id:int,session_user_id:int = Depends(is_valid_user([TeamRole.ADMIN,TeamRole.PM,TeamRole.TM])),db : Session = Depends(get_db)):
    return TaskService.getTaskById(task_id,db)

@taskRouter.get("/task/projecttask/{project_id}", response_model=list[TaskResponse])
def getAllTaskInProject(project_id : int , session_user_id : int = Depends(is_valid_user([TeamRole.ADMIN,TeamRole.PM])),db : Session = Depends(get_db)):
    return TaskService.getAllTaskInProject(project_id,db)

@taskRouter.patch("/task/update/{task_id}",response_model=MessageResponse)
def updateTask(task_id:int,task_data:TaskUpdaterequest,session_user_id:int = Depends(is_valid_user([TeamRole.ADMIN,TeamRole.PM])),db : Session= Depends(get_db)):
    return TaskService.updateTask(task_data,task_id,db)

@taskRouter.delete("/task/delete/{task_id}", response_model=MessageResponse)
def deleteTask(task_id: int , session_user_id: int = Depends(is_valid_user(TeamRole.ADMIN,TeamRole.PM)),db : Session = Depends(get_db)):
    return TaskService.deleteTask(task_id,db)

@taskRouter.patch("/task/assign/{task_id}/{user_id}", response_model=MessageResponse)
def AssignTaskToUser(task_id : int, user_id:int, session_user_id: int = Depends(is_valid_user([TeamRole.PM])),db: Session = Depends(get_db)):
    return TaskService.assignTaskToUser(task_id,user_id,db)

@taskRouter.get("/task/getAllTaskInUser/{user_id}", response_model=list[TaskResponse])
def getAllTaskInUser(user_id: int, session_user_id:int = Depends(is_valid_user([TeamRole.ADMIN,TeamRole.PM,TeamRole.TM])),db: Session = Depends(get_db)):
    return TaskService.getAllTaskOfUser(user_id,db)

@taskRouter.get("/task/priority/{priority_id}",response_model=list[TaskResponse])
def getTaskByPriority(priority_id:int ,session_user_id:int = Depends(is_valid_user([TeamRole.ADMIN,TeamRole.PM])),db : Session = Depends(get_db)):
    return TaskService.getTaskByPriority(priority_id,db)

@taskRouter.get("/task/status/{status_id}",response_model=list[TaskResponse])
def getTaskByPriority(status_id:int ,session_user_id:int = Depends(is_valid_user([TeamRole.ADMIN,TeamRole.PM])),db : Session = Depends(get_db)):
    return TaskService.getTaskByStatus(status_id,db)

@taskRouter.get("/task/currentusertask", response_model=list[TaskResponse])
def getAllTaskOfCurrentUser(session_user_id: int = Depends(is_valid_user([TeamRole.PM,TeamRole.TM])),db : Session = Depends(get_db)):
    return TaskService.getAllTaskOfCurrentUser(session_user_id,db)

@taskRouter.post("/task/savecomments", response_model=MessageResponse)
def saveTaskComments(comment_data: TaskCommentsrequest,session_user_id : int = Depends(is_valid_user([TeamRole.PM,TeamRole.TM])),db: Session = Depends(get_db)):
    return TaskService.saveTaskComments(session_user_id,comment_data,db)

@taskRouter.get("/task/comments/{comment_id}", response_model=TaskCommentResponse)
def getcomment(comment_id:int,session_user_id:int = Depends(is_valid_user([TeamRole.PM,TeamRole.ADMIN,TeamRole.TM])),db : Session = Depends(get_db)):
    return TaskService.getComment(comment_id,db)

@taskRouter.get("/task/taskComment/{task_id}", response_model=list[TaskCommentResponse])
def getTaskComments(task_id:int, session_user_id:int = Depends(is_valid_user([TeamRole.ADMIN,TeamRole.PM,TeamRole.TM])),db: Session = Depends(get_db)):
    return TaskService.getTaskCommentByTask(task_id,db)
