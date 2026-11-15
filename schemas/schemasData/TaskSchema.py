from schemas.Validator import FieldValidatorClass
from typing import Optional
from datetime import datetime, date


class TaskRequest(FieldValidatorClass):
    project_id : int
    title: str
    description:str
    priority: int
    status:int
    start_date:date
    end_date:date

class TaskResponse(FieldValidatorClass):
    task_id:int
    project_id:int
    assigned_to: int
    created_by:int
    title:str
    description:str
    priority:int
    status:int
    start_date:date
    end_date:date
    created_at:datetime
    updated_at:datetime

class TaskUpdaterequest(FieldValidatorClass):
    project_id: Optional[int]= None
    assigned_to: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    priority:Optional[int] = None
    status:Optional[int] = None
    start_date:Optional[date] = None
    end_date:Optional[date] = None


class TaskCommentsrequest(FieldValidatorClass):
    task_id : int
    comment_text: str

class TaskCommentResponse(FieldValidatorClass):
    comment_id:int
    task_id :int
    user_id : int
    comment_text :str
    created_at : datetime
    updated_at :datetime