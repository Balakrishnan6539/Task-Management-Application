from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Database.DB_connection import get_db, get_db_and_user_id
from schemas.schemasData.ProjectSchema import ProjectRequest , ProjectReponse, ProjectUpdateRequest,MemberRequest, ProjectStatResponse
from schemas.schemasData.MessageResponseSchema import MessageResponse
from service import ProjectService
from Security.JWTAuth import is_valid_user
from Constant.EnumConstant import TeamRole


projectRouter=APIRouter( tags= ["Project Router"])

@projectRouter.post("/project/create", response_model=MessageResponse)
def createProject(project_data: ProjectRequest,
                  db : Session = Depends(get_db),
                  session_user_id : int = Depends(is_valid_user([TeamRole.ADMIN]))):
    return ProjectService.create_project(project_data,db,session_user_id)



@projectRouter.get("/project/get/{project_id}",response_model=ProjectReponse)
def getProjectById(project_id : int,
                   db: Session = Depends(get_db),
                   session_user_id : int = Depends(is_valid_user([TeamRole.PM,TeamRole.TM, TeamRole.ADMIN]))):
    return ProjectService.get_project_by_id(project_id,db)



@projectRouter.get("/project/getall", response_model=list[ProjectReponse])
def getAllProject(db : Session =Depends(get_db),
                  session_user_id : int = Depends(is_valid_user([TeamRole.ADMIN]))):
    return ProjectService.get_all_projects(db)



@projectRouter.patch("/project/update/{project_id}", response_model=ProjectReponse)
def updateProject(project_id: int,
                  project_data: ProjectUpdateRequest ,
                  db: Session = Depends(get_db),
                  session_user_id : int = Depends(is_valid_user([TeamRole.ADMIN,TeamRole.PM]))):
    return ProjectService.update_project(project_id,project_data,db)



@projectRouter.delete("/project/remove/{project_id}",response_model=MessageResponse)
def deleteProject(project_id: int,
                  db : Session = Depends(get_db),
                  session_user_id: int = Depends(is_valid_user([TeamRole.ADMIN]))):
    return ProjectService.delete_project(project_id,db)



@projectRouter.patch("/project/status/{project_id}/{status_id}", response_model=MessageResponse)
def changeStatusForProject(project_id: int,
                           status_id: int,
                           db: Session = Depends(get_db),
                           session_user_id : int = Depends(is_valid_user([TeamRole.PM,TeamRole.ADMIN]))):
    return ProjectService.ChangeStatus(project_id,status_id,db)



@projectRouter.post("/project/assign", response_model=MessageResponse)
def assignMemberToProject(data : MemberRequest,
                          db : Session = Depends(get_db),
                          session_user_id : int = Depends(is_valid_user([TeamRole.PM,TeamRole.ADMIN]))):
    return ProjectService.AssignMemberToProject(data.project_id,data.member_id,db)



@projectRouter.delete("/project/remove", response_model=MessageResponse)
def removeMemberFromProject(data: MemberRequest,
                            db : Session = Depends(get_db),
                            session_user_id : int = Depends(is_valid_user([TeamRole.ADMIN,TeamRole.PM]))):
    return ProjectService.RemoveMemberFromProject(data.project_id,data.member_id,db)



@projectRouter.get("/project/progress/{project_id}", response_model= MessageResponse)
def projectProgress(project_id: int ,
                    db : Session = Depends(get_db),
                    session_user_id : int = Depends(is_valid_user([TeamRole.ADMIN,TeamRole.PM]))):
    return ProjectService.ProjectProgress(project_id,db)



@projectRouter.get("/project/stat", response_model= list[ProjectStatResponse])
def projectWiseStat(db: Session = Depends(get_db),
                    session_user_id : int = Depends(is_valid_user([TeamRole.ADMIN,TeamRole.PM]))):
    return ProjectService.ProjectWiseStat(db)