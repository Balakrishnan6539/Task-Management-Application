
from sqlalchemy.orm import Session
from Database.Models import  Project, Project_Member, Task,Status
from fastapi import HTTPException


def create_project(project_data: Project, db: Session, session_user_id: int):
    existing_project = db.query(Project).filter(Project.project_name == project_data.project_name).first()
    if existing_project:
        raise HTTPException(status_code=400, detail="Project name already exists")


    new_project = Project(
        project_name=project_data.project_name,
        description=project_data.description,
        start_date=project_data.start_date,
        end_date=project_data.end_date,
        created_by=session_user_id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {"message": "Project created successfully"}

def get_project_by_id(project_id: int, db: Session):
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

def get_all_projects(db: Session):
    projects = db.query(Project).all()
    return projects

def update_project(project_id: int, update_data: Project, db: Session):
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project

def delete_project(project_id: int, db: Session):
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}

def ChangeStatus(project_id: int, status_id: int, db: Session):
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.status_id = status_id
    status=db.query(Status.status_name).filter(Status.status_id== status_id).scalar()
    db.commit()
    db.refresh(project)
    return {"message": f"Project status updated to {status} successfully"}

def AssignMemberToProject(project_id: int, member_id: int, db: Session):
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    existing_member = db.query(Project_Member).filter(Project_Member.project_id == project_id, Project_Member.member_id == member_id).first()
    if existing_member:
        raise HTTPException(status_code=400, detail="Member already assigned to this project")

    new_member = Project_Member(
        project_id=project_id,
        member_id=member_id
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return {"message": "Member assigned to project successfully"}

def RemoveMemberFromProject(project_id: int, member_id: int, db: Session):
    project_member = db.query(Project_Member).filter(Project_Member.project_id == project_id, Project_Member.member_id == member_id).first()
    if not project_member:
        raise HTTPException(status_code=404, detail="Member not found in this project")

    db.delete(project_member)
    db.commit()
    return {"message": "Member removed from project successfully"}


def ProjectProgress(project_id: int, db: Session):
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    total_tasks = db.query(Task).filter(Task.project_id == project_id).count()
    completed_tasks = db.query(Task).filter(Task.project_id == project_id, Task.status == "completed").count()

    if total_tasks == 0:
        return {"project_id": project_id, "message": "there are no tasks in this project"}
    else:
        progress = (completed_tasks / total_tasks) * 100

    return {"message": f"Project progress: {progress:.2f}%"}


def ProjectWiseStat(db: Session):
    projects= db.query(Project).all()

    result=[]

    for project in projects:

        tasks= db.query(Task).filter(Task.project_id == project.project_id)

        total_task= tasks.count()

        completed= tasks.filter(Task.status == 3).count()

        progress = tasks.filter(Task.status == 2).count()

        pending = tasks.filter(Task.status==1).count()


        if total_task>0:
            progress = (completed/total_task)*100
        else:
            progress=0

        result.append(
            {
                "project_id" : project.project_id,
                "project_name": project.project_name,
                "total_task": total_task,
                "completed": completed,
                "progress": progress,
                "not_started": pending,
                "progress_percent": progress
            }
        )

    return result


