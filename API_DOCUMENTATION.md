# HealthSync AI API Documentation 📖

The HealthSync AI API is a RESTful interface built with FastAPI. It provides endpoints for patient management, medical image analysis, and multi-model disease predictions.

## 🔑 Authentication
- **Endpoint**: `/api/v1/login`
- **Method**: `POST`
- **Body**: `username`, `password` (form-data)
- **Response**: `{"access_token": "...", "token_type": "bearer"}`

## 👥 Patient Management

### Create Patient
- **Endpoint**: `/api/v1/patients/`
- **Method**: `POST`
- **Payload**:
  ```json
  {
    "name": "John Doe",
    "age": 45,
    "gender": "Male",
    "bmi": 24.5,
    "medical_history": "None"
  }
  ```

### List Patients
- **Endpoint**: `/api/v1/patients/`
- **Method**: `GET`
- **Params**: `skip` (int), `limit` (int)

## 🧠 Predictions

### ML Ensemble Prediction
- **Endpoint**: `/api/v1/predict/ml`
- **Method**: `POST`
- **Params**: `patient_id` (int)
- **Description**: Runs the Random Forest + XGBoost + SVM ensemble on tabular patient data.

### DL Image Analysis
- **Endpoint**: `/api/v1/predict/dl`
- **Method**: `POST`
- **Params**: `patient_id` (int), `image_id` (int)
- **Description**: Analyzes the specified medical image using the ResNet50 CNN.

### QML Drug Interaction
- **Endpoint**: `/api/v1/predict/qml`
- **Method**: `POST`
- **Params**: `patient_id` (int)
- **Payload**: Drug features dictionary.
- **Description**: Executes a Variational Quantum Circuit to predict drug efficacy.

## 🖼️ Medical Images

### Upload Image
- **Endpoint**: `/api/v1/images/upload`
- **Method**: `POST`
- **Params**: `patient_id` (int), `image_type` (str)
- **Body**: `file` (binary)

## 🛠️ Swagger UI
For interactive documentation and testing, visit:
`http://localhost:8001/docs`
