from sqlalchemy.orm import Session
from Database.Models import Activity_log, Priorities, Project, Project_Member, Role, Status, Task, Task_Comments, User
from fastapi import HTTPException
from Security.JWTAuth import create_jwt_token
from Security.PasswordHash import HashPassword , VerifyPassword

def Login(login_data: User, db: Session):

    user =db.query(User).filter(User.mobile_number == login_data.mobilenumber).first()
    if not user or not VerifyPassword(login_data.password,user.password):
        raise HTTPException(status_code=400, detail= "Mobile number or Password is incorrect. Kindly provide the valid data")
    return create_jwt_token(user.user_id,user.role.role_name)

def Register(register_data: User, db: Session):
    existing_user = db.query(User).filter((User.mobile_number == register_data.mobile_number) | (User.email == register_data.email) ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="mobile number or email already exists")

    hashed_password = HashPassword(register_data.password)
    new_user = User(
        username=register_data.username,
        mobile_number=register_data.mobile_number,
        email=register_data.email,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

def UpdateUser(user_id: int, update_data: User, db: Session, session_user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(user, key, value)

    user.updated_by = session_user_id
    
    db.commit()
    db.refresh(user)
    return user

def DeleteUser(user_id: int, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


def deactivate_user(user_id: int, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False
    db.commit()
    db.refresh(user)
    return {"message": "User deactivated successfully"}

def activate_user(user_id: int, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    db.commit()
    db.refresh(user)
    return {"message": "User activated successfully"}

def assign_role_to_user(user_id: int, role_id: int, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role = db.query(Role).filter(Role.role_id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    user.role_id = role_id
    db.commit()
    db.refresh(user)
    return {"message": f"Role '{role.role_name}' assigned to user '{user.username}' successfully"}

def get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_all_users(db: Session):
    users = db.query(User).all()
    return users

def get_users_by_role(role_name: str, db: Session):
    role = db.query(Role).filter(Role.role_name == role_name).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    users = db.query(User).filter(User.role_id == role.role_id).all()
    return users

def PromoteUser(user_id: int, db: Session , role_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role = db.query(Role).filter(Role.role_id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    user.role_id = role_id
    db.commit()
    db.refresh(user)
    return {"message": f"User '{user.username}' promoted to role '{role.role_name}' successfully"}

def DemoteUser(user_id: int, db: Session , role_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role = db.query(Role).filter(Role.role_id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    user.role_id = role_id
    db.commit()
    db.refresh(user)
    return {"message": f"User '{user.username}' demoted to role '{role.role_name}' successfully"}
