from schemas.Validator import FieldValidatorClass
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


class tokenResponse(FieldValidatorClass):
    token: str


class MessageResponse(FieldValidatorClass):
    message: str

