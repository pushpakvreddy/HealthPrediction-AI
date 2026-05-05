# HealthSync AI 🏥✨

HealthSync AI is a cutting-edge, full-stack disease prediction and health analytics platform. It leverages a hybrid intelligence approach, combining Classical Machine Learning (ML), Deep Learning (DL), and Quantum Machine Learning (QML) to provide high-precision diagnostics and treatment recommendations.

## 🚀 Key Features

- **Hybrid AI Engine**: Integrates Random Forest, XGBoost, CNNs (ResNet50), LSTMs with Attention, and Quantum Variational Circuits.
- **Quantum-Ready**: Includes QML modules using PennyLane for drug efficacy and treatment optimization (QAOA).
- **Medical Imaging**: Automated classification of X-rays and medical images using transfer learning.
- **Real-time Analytics**: Dynamic dashboard with glassmorphism UI, interactive charts, and risk score visualizations.
- **Production-Ready**: Fully containerized with Docker and orchestrated with Docker Compose.

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Scikit-learn, TensorFlow, PyTorch, PennyLane.
- **Frontend**: React, Vite, Tailwind CSS, Plotly.js, Lucide Icons.
- **Infrastructure**: Docker, Docker Compose, Nginx.

## 📦 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js (for local frontend development)
- Python 3.9+ (for local backend development)

### Running with Docker (Recommended)
1. Clone the repository.
2. Create a `.env` file in the root (use `.env.example` as a template).
3. Run the following command:
   ```bash
   docker-compose up --build
   ```
4. Access the application:
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8001/docs
   - **pgAdmin**: http://localhost:5050

## 📂 Project Structure

```
.
├── backend/            # FastAPI Application
│   ├── app/            # Core API logic (models, routes, schemas)
│   ├── models/         # ML and DL model definitions
│   ├── qml/            # Quantum Machine Learning modules
│   └── saved_models/   # Persistent storage for trained models
├── frontend/           # React Application
│   ├── src/
│   │   ├── components/ # Reusable UI components
│   │   ├── pages/      # Application views
│   │   └── services/   # API interaction layer
└── docker-compose.yml  # Orchestration configuration
```

## 📜 License
This project is licensed under the MIT License.
