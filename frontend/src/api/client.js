import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadDataset = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await apiClient.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const loadBenchmarkData = async () => {
  const response = await apiClient.post('/sample-data');
  return response.data;
};

export const runFairnessAnalysis = async (payload) => {
  const response = await apiClient.post('/analyze', payload);
  return response.data;
};

export const getReportHtmlUrl = (analysisId) => `${API_BASE_URL}/report/html/${analysisId}`;
export const getReportPdfUrl = (analysisId) => `${API_BASE_URL}/report/pdf/${analysisId}`;
