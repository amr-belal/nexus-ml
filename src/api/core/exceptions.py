from fastapi import HTTPException


class ModelNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Model not found")

class PredictionError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=f"Prediction error: {detail}")

class ValidationError(HTTPException):
    def __init__(self, detail:str):
        super().__init__(status_code=422, detail=f"Validation error: {detail}")