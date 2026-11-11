from pydantic import BaseModel,field_validator


class FieldValidatorClass(BaseModel):

    @field_validator("username", check_fields=False)
    @classmethod
    def validate_name(cls, value: str):
        name = value.strip()

        if not name or not name.replace(" ", "").isalpha():
            raise ValueError("Name can contain only letters and spaces")

        return name

    @field_validator("mobilenumber", check_fields=False)
    @classmethod
    def validate_mobilenumber(cls, value: str):
        if len(value) != 10:
            raise ValueError("Mobile number must be a 10-digit number")

        return value

    @field_validator("password", check_fields=False)
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8 and not any(char.isdigit() for char in value) and not any(char.isupper() for char in value):
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        return value

    @field_validator("email", check_fields=False)
    @classmethod
    def validate_email(cls, value: str):
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email address")
        return value