from pwdlib import PasswordHash


def HashPassword(pwd : str) -> str:
    return PasswordHash.recommended().hash(pwd)

def VerifyPassword(pwd : str, hashed_pwd : str) -> bool:
    return PasswordHash.recommended().verify(pwd, hashed_pwd)