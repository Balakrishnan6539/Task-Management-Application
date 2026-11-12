from schemas.Validator import FieldValidatorClass
from datetime import datetime
from typing import Optional


class LoginRequest(FieldValidatorClass):
    mobilenumber: str
    password: str


class RegisterRequest(FieldValidatorClass):
    username : str
    mobile_number : str
    email : str
    password : str


class UserUpdateRequest(FieldValidatorClass):
    username : Optional[str] = None
    mobile_number : Optional[str] = None
    email : Optional[str] = None
    current_password : Optional[str] = None
    new_password : Optional[str] = None


class UserRoleRequest(FieldValidatorClass):
    user_id : str
    role_id : str


class tokenResponse(FieldValidatorClass):
    token: str

class UserResponse(FieldValidatorClass):
    user_id : int
    username : str
    mobile_number : str
    email : str
    password : str
    role_id : int
    is_active : bool
    created_at : datetime
    updated_at : datetime
    updated_by : Optional[int]=None


