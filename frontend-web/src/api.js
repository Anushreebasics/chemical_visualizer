import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add token to requests
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Token ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export const authAPI = {
    register: (username, email, password, firstName = '', lastName = '') =>
        api.post('/auth/register/', { username, email, password, first_name: firstName, last_name: lastName }),
    login: (username, password) =>
        api.post('/auth/login/', { username, password }),
    logout: () =>
        api.post('/auth/logout/'),
};

export const equipmentAPI = {
    getAll: () =>
        api.get('/equipment/'),
    uploadCSV: (file) => {
        const formData = new FormData();
        formData.append('file', file);
        return api.post('/upload-csv/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
    },
    getSummary: () =>
        api.get('/summary/'),
    getHistory: () =>
        api.get('/history/'),
    generatePDF: (uploadId = null) =>
        api.post('/generate-pdf/', uploadId ? { upload_id: uploadId } : {}),
};

export default api;
