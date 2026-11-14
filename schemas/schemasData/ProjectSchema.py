from schemas.Validator import FieldValidatorClass
from typing import Optional
from datetime import date,datetime

class ProjectRequest(FieldValidatorClass):
    project_name : str
    description: str
    start_date: date
    end_date: date


class ProjectReponse(FieldValidatorClass):
    project_id: int
    project_name: str
    description:str
    start_date: date
    end_date: date
    status: int
    created_by : int
    created_at : datetime
    updated_at : datetime


class ProjectUpdateRequest(FieldValidatorClass):
    project_name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[int] = None

class MemberRequest(FieldValidatorClass):
    project_id : int
    member_id: int


class ProjectStatResponse(FieldValidatorClass):
    project_id: int
    project_name: str
    totak_task: int
    completed : int
    progress : int
    not_started : int
    progress_percent : int
