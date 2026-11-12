from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from Database.DB_connection import get_db
from Security.JWTAuth import is_valid_user
from schemas.schemasData.UserSchema import LoginRequest, tokenResponse , RegisterRequest , UserUpdateRequest, UserResponse, UserRoleRequest
from schemas.schemasData.MessageResponseSchema import MessageResponse
from service import UserService


userRouter = APIRouter()

@userRouter.post("/user/login", response_model= tokenResponse)
def Login(login_data: LoginRequest,db : Session = Depends(get_db)):

    if not login_data.mobilenumber or not login_data.password:
        raise HTTPException(status_code=400, detail="Mobile number and password are required")

    return UserService.Login(login_data,db)

@userRouter.post("/user/register", response_model= MessageResponse)
def Register(register_data: RegisterRequest,db : Session = Depends(get_db)):

    if not register_data.username or not register_data.mobile_number or not register_data.email or not register_data.password:
        raise HTTPException(status_code=400, detail="All fields are required")

    return UserService.Register(register_data,db)

@userRouter.patch("/user/update/{user_id}", response_model= UserResponse)
def updateUser(user_id: int, update_data: UserUpdateRequest , db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin","user"]))):
    
    return UserService.UpdateUser(user_id, update_data, db, session_user_id)

@userRouter.delete("/user/delete/{user_id}", response_model= MessageResponse)
def deleteUser(user_id: int, db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin"]))):
    
    return UserService.DeleteUser(user_id, db)

@userRouter.patch("/user/deactivate/{user_id}", response_model= MessageResponse)
def deactivateUser(user_id: int, db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin"]))):
    
    return UserService.deactivate_user(user_id, db)

@userRouter.patch("/user/activate/{user_id}", response_model= MessageResponse)
def activateUser(user_id: int, db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin"]))):
    return UserService.activate_user(user_id, db)

@userRouter.get("/user/get_by_id/{user_id}", response_model= UserResponse)
def getUserById(user_id: int, db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin","user"]))):
    return UserService.get_user_by_id(user_id, db)

@userRouter.get("/user/get_all", response_model= list[UserResponse])
def getAllUsers(db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin"]))):
    
    return UserService.get_all_users(db)

@userRouter.get("/user/get_by_role/{role_name}", response_model= list[UserResponse])
def getUsersByRole(role_name: str, db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin"]))):
    
    return UserService.get_users_by_role(role_name, db) 

@userRouter.patch("/user/promote", response_model= MessageResponse)
def promoteUser(data : UserRoleRequest, db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin"]))):
    return UserService.PromoteUser(data.user_id, data.role_id, db)

@userRouter.patch("/user/demote", response_model= MessageResponse)
def demoteUser(data : UserRoleRequest, db: Session = Depends(get_db), session_user_id: int = Depends(is_valid_user(required_role=["admin"]))):
    return UserService.DemoteUser(data.user_id, data.role_id, db)

@userRouter.patch("/user/assignrole", response_model=MessageResponse)
def assignRoleToUser(data: UserRoleRequest, db: Session = Depends(get_db),session_user_id: int = Depends(is_valid_user(required_role=["admin"]))):
    return UserService.assign_role_to_user(data.user_id,data.role_id,db)