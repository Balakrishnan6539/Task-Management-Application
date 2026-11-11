from fastapi import APIRouter,Depends,Cookie,Response,Request,HTTPException
from sqlalchemy.orm import Session
from Database.DB_connection import get_db
from Security.JWTAuth import is_valid_user
from schemas.schemasData.UserSchema import LoginRequest, tokenResponse , RegisterRequest ,MessageResponse, UserUpdateRequest
from service import UserService


router = APIRouter()

@router.post("/user/login", response_model= tokenResponse)
def Login(login_data: LoginRequest,db : Session = Depends(get_db)):

    if not login_data.mobilenumber or not login_data.password:
        raise HTTPException(status_code=400, detail="Mobile number and password are required")

    return UserService.Login(login_data,db)

@router.post("/user/register", response_model= MessageResponse)
def Register(register_data: RegisterRequest,db : Session = Depends(get_db)):

    if not register_data.username or not register_data.mobile_number or not register_data.email or not register_data.password:
        raise HTTPException(status_code=400, detail="All fields are required")

    return UserService.Register(register_data,db)

@router.patch("/user/update/{user_id}", response_model= MessageResponse)
def updateUser(user_id: int, update_data: UserUpdateRequest , db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin","user"]))):
    
    return UserService.UpdateUser(user_id, update_data, db, session_user_id)

@router.delete("/user/delete/{user_id}", response_model= MessageResponse)
def deleteUser(user_id: int, db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin"]))):
    
    return UserService.DeleteUser(user_id, db)
