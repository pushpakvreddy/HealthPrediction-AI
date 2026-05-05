from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
import pandas as pd
import numpy as np
from ..database import get_db
from ..models import models
from ..schemas import schemas
from ...inference_ml import MLInference
from ...inference_dl import DLInference
from ...qml_inference import QMLInference
from ..config import settings

router = APIRouter(
    prefix="/predict",
    tags=["predictions"]
)

# Initialize inference engines (assuming models are in settings.MODEL_DIR)
ml_engine = MLInference(settings.MODEL_DIR)
dl_engine = DLInference(settings.MODEL_DIR)
qml_engine = QMLInference(settings.MODEL_DIR)

@router.post("/ml", response_model=schemas.Prediction)
def predict_ml(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Prepare data for ML
    df_input = pd.DataFrame([{
        "age": patient.age,
        "bmi": patient.bmi,
        # Add other fields as needed
    }])
    
    result = ml_engine.predict(df_input)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    prediction = models.Prediction(
        patient_id=patient_id,
        model_type="ML",
        disease="Predicted Disease", # Simplified
        risk_score=result["probability"],
        confidence=result["probability"],
        details_json=json.dumps(result["contributions"])
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction

@router.post("/dl", response_model=schemas.Prediction)
def predict_dl(patient_id: int, image_id: int, db: Session = Depends(get_db)):
    image = db.query(models.MedicalImage).filter(models.MedicalImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    result = dl_engine.predict_image(image.image_path)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    prediction = models.Prediction(
        patient_id=patient_id,
        model_type="DL",
        disease=result["prediction"],
        risk_score=result["confidence"],
        confidence=result["confidence"],
        details_json="{}"
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction

@router.post("/qml", response_model=schemas.Prediction)
def predict_qml(patient_id: int, drug_features: dict, db: Session = Depends(get_db)):
    result = qml_engine.predict_drug_efficacy(drug_features)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    prediction = models.Prediction(
        patient_id=patient_id,
        model_type="QML",
        disease="Drug Efficacy Analysis",
        risk_score=result["efficacy_score"],
        confidence=result["confidence"],
        details_json=result["explanation"]
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction
