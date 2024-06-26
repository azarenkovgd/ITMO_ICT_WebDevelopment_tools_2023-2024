from fastapi import HTTPException


class NotAuthException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="User not authorized")

