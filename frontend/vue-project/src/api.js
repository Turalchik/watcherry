import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api'; // Замените на ваш URL API

export const fetchPopularAndNewMovies = async () => {
    const response = await axios.get(`${API_BASE_URL}/movies/`);
    return response.data;
};

export const fetchMovieDetails = async (titleId) => {
    const token = localStorage.getItem('token'); // Получаем токен из localStorage
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    
    const response = await axios.get(`${API_BASE_URL}/movies/${titleId}/`, {
      headers,
    });
  
    return response.data;
};

export const searchMovies = async (query) => {
    const response = await axios.get(`${API_BASE_URL}/search/`, {
        params: { q: query },
    });
    return response.data;
};

export const fetchReviews = async (titleId) => {
    const response = await axios.get(`${API_BASE_URL}/movies/${titleId}/reviews/`);
    return response.data;
};

// Функция для отправки отзыва
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

// Функция для отправки комментария
export const postComment = async (reviewId, data, token) => {
    const response = await axios.post(
        `${API_BASE_URL}/reviews/${reviewId}/comments/`,
        data,
        {
            headers: { Authorization: `Bearer ${token}` },
        }
    );
    return response.data;
};

export const toggleLike = async (titleId, token) => {
    const response = await axios.post(
        `${API_BASE_URL}/movies/${titleId}/toggle_like/`,
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
        return response.data;
    } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message;
        alert(`Ошибка: ${errorMessage}`);
        throw error;
    }
};

// Регистрация пользователя
export const registerUser = async (userData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/register/`, userData);
        return response.data;
    } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message;
        alert(`Ошибка: ${errorMessage}`);
        throw error;
    }
};

// Получение профиля пользователя
export const fetchUserProfile = async (token) => {
    if (!token) {
        alert("Токен не найден");
        return;
    }
    try {
        const response = await axios.get(`${API_BASE_URL}/profile/`, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message;
        alert(`Ошибка: ${errorMessage}`);
        throw error;
    }
};

// Обновление профиля пользователя
export const updateUserProfile = async (profileData, token) => {
    try {
        const response = await axios.put(`${API_BASE_URL}/profile/`, profileData, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message;
        alert(`Ошибка: ${errorMessage}`);
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
        const errorMessage = error.response?.data?.detail || error.message;
        alert(`Ошибка: ${errorMessage}`);
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
        const errorMessage = error.response?.data?.detail || error.message;
        alert(`Ошибка: ${errorMessage}`);
        throw error;
    }
};