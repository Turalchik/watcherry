import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api'; // Замените на ваш URL API

export const fetchPopularAndNewMovies = async () => {
    const response = await axios.get(`${API_BASE_URL}/movies/`);
    return response.data;
};

export const fetchMovieDetails = async (titleId) => {
    const response = await axios.get(`${API_BASE_URL}/movies/${titleId}/`);
    return response.data;
};

export const searchMovies = async (query) => {
    const response = await axios.get(`${API_BASE_URL}/movies/search/`, {
        params: { q: query },
    });
    return response.data;
};

export const fetchReviews = async (titleId) => {
    const response = await axios.get(`${API_BASE_URL}/movies/${titleId}/reviews/`);
    return response.data;
};

export const postReview = async (titleId, data, token) => {
    const response = await axios.post(
        `${API_BASE_URL}/movies/${titleId}/reviews/`,
        data,
        {
            headers: { Authorization: `Bearer ${token}` },
        }
    );
    return response.data;
};

export const toggleLike = async (titleId, token) => {
    const response = await axios.post(
        `${API_BASE_URL}/movies/${titleId}/like/`,
        {},
        {
            headers: { Authorization: `Bearer ${token}` },
        }
    );
    return response.data;
};

// Вход пользователя
export const loginUser = async (credentials) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/login/`, credentials);
        return response.data; // Возвращает данные пользователя или токен
    } catch (error) {
        console.error("Ошибка входа:", error.response?.data || error.message);
        throw error;
    }
};

// Регистрация пользователя
export const registerUser = async (userData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/register/`, userData);
        return response.data;
    } catch (error) {
        console.error("Ошибка регистрации:", error.response?.data || error.message);
        throw error;
    }
};

// Получение профиля пользователя
export const fetchUserProfile = async (token) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/profile/`, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    } catch (error) {
        console.error("Ошибка получения профиля:", error.response?.data || error.message);
        throw error;
    }
};

// Обновление профиля пользователя
export const updateUserProfile = async (profileData, token) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/profile/`, profileData, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    } catch (error) {
        console.error("Ошибка обновления профиля:", error.response?.data || error.message);
        throw error;
    }
};

// Смена пароля
export const changePassword = async (passwordData, token) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/change-password/`, passwordData, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    } catch (error) {
        console.error("Ошибка смены пароля:", error.response?.data || error.message);
        throw error;
    }
};

// Получение рекомендаций
export const fetchRecommendations = async (token) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/recommendations/`, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    } catch (error) {
        console.error("Ошибка получения рекомендаций:", error.response?.data || error.message);
        throw error;
    }
};