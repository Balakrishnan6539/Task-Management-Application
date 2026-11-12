from schemas.Validator import FieldValidatorClass
from typing import Optional
from datetime import datetime

class ProjectRequest(FieldValidatorClass):
    project_name : str
    description: str
    start_date: datetime
    end_date: datetime


class ProjectReponse(FieldValidatorClass):
    project_name: str
    description:str
    start_date: datetime
    end_date: datetime
    status: int
    created_by : int
    created_at : datetime
    updated_at : datetime


class ProjectUpdateRequest(FieldValidatorClass):
    project_name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
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
