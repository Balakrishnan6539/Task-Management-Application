from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from Database.DB_connection import get_db
from Security.JWTAuth import is_valid_user
from schemas.schemasData.UserSchema import LoginRequest, tokenResponse , RegisterRequest , UserUpdateRequest
from schemas.schemasData.MessageResponseSchema import MessageResponse
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

@router.patch("/user/deactivate/{user_id}", response_model= MessageResponse)
def deactivateUser(user_id: int, db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin"]))):
    
    return UserService.deactivate_user(user_id, db)

@router.Patch("/user/activate/{user_id}", response_model= MessageResponse)
def activateUser(user_id: int, db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin"]))):
    return UserService.activate_user(user_id, db)

@router.get("/user/get_by_id/{user_id}", response_model= MessageResponse)
def getUserById(user_id: int, db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin","user"]))):
    return UserService.get_user_by_id(user_id, db)

@router.get("/user/get_all", response_model= MessageResponse)
def getAllUsers(db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin"]))):
    
    return UserService.get_all_users(db)

@router.get("/user/get_by_role/{role_name}", response_model= MessageResponse)
def getUsersByRole(role_name: str, db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin"]))):
    
    return UserService.get_users_by_role(role_name, db) 

@router.patch("/user/promote/{user_id}/{role_id}", response_model= MessageResponse)
def promoteUser(user_id: int, role_id: int, db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin"]))):
    return UserService.PromoteUser(user_id, role_id, db)

@router.patch("/user/demote/{user_id}/{role_id}", response_model= MessageResponse)
def demoteUser(user_id: int, role_id: int, db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin"]))):
    return UserService.DemoteUser(user_id, role_id, db)
