import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api/v1';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const patientService = {
    getAll: () => api.get('/patients/'),
    getById: (id) => api.get(`/patients/${id}`),
    create: (data) => api.post('/patients/', data),
};

export const predictionService = {
    predictML: (patientId) => api.post(`/predict/ml?patient_id=${patientId}`),
    predictDL: (patientId, imageId) => api.post(`/predict/dl?patient_id=${patientId}&image_id=${imageId}`),
    predictQML: (patientId, drugFeatures) => api.post(`/predict/qml?patient_id=${patientId}`, drugFeatures),
};

export const imageService = {
    upload: (patientId, imageType, file) => {
        const formData = new FormData();
        formData.append('file', file);
        return api.post(`/images/upload?patient_id=${patientId}&image_type=${imageType}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
    },
    getById: (id) => api.get(`/images/${id}`),
};

export default api;
