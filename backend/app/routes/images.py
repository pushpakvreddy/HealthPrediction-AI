from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os
import shutil
from ..database import get_db
from ..models import models
from ..schemas import schemas
from ..config import settings

router = APIRouter(
    prefix="/images",
    tags=["images"]
)

@router.post("/upload", response_model=schemas.MedicalImage)
async def upload_image(patient_id: int, image_type: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, f"{patient_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    db_image = models.MedicalImage(
        patient_id=patient_id,
        image_path=file_path,
        image_type=image_type
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

@router.get("/{image_id}", response_model=schemas.MedicalImage)
def get_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(models.MedicalImage).filter(models.MedicalImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image
