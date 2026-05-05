from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

# Patient Schemas
class PatientBase(BaseModel):
    name: str
    age: int
    gender: str
    bmi: float
    medical_history: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Prediction Schemas
class PredictionBase(BaseModel):
    model_type: str
    disease: str
    risk_score: float
    confidence: float
    details_json: str

class PredictionCreate(PredictionBase):
    patient_id: int

class Prediction(PredictionBase):
    id: int
    patient_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Image Schemas
class ImageBase(BaseModel):
    image_path: str
    image_type: str

class ImageCreate(ImageBase):
    patient_id: int

class MedicalImage(ImageBase):
    id: int
    patient_id: int
    analysis_result: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Auth Schemas
class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
