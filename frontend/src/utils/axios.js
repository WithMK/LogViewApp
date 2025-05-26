import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    },
    timeout: 10000, // 10초 타임아웃
});

// 요청 인터셉터
api.interceptors.request.use(
    (config) => {
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 응답 인터셉터
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (!error.response) {
            // 네트워크 에러 처리
            throw new Error('서버와의 연결이 실패했습니다. 서버가 실행 중인지 확인해주세요.');
        }
        return Promise.reject(error);
    }
);

export default api;
