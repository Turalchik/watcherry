import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api'; // Замените на ваш URL API

export const fetchPopularAndNewMovies = async () => {
    const response = await axios.get(`${API_BASE_URL}/movies/`);
    return response.data;
};

export const fetchMovieDetails = async (titleId) => {
    const token = localStorage.getItem('token');
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    
    const response = await axios.get(`${API_BASE_URL}/movies/${titleId}/`, {
      headers,
    });
  
    return response.data;
};

export const searchMovies = async (movieTitle, rating, movieGenre) => {
    if (!movieTitle || movieTitle.trim() === '') {
        throw new Error('Title is required for the search query.');
    }
    const response = await axios.get(`${API_BASE_URL}/search/`, {
        params: { title: movieTitle, min_rating: rating, genre: movieGenre },
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

export const fetchUserProfile = async (token) => {
    if (!token) {
        return;
    }
    try {
        const response = await axios.get(`${API_BASE_URL}/profile/`, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    } catch (error) {
        throw error;
    }
};

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


export const fetchGenres = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/genres/`);
        return response.data;
    } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message;
        alert(`Ошибка при получении жанров: ${errorMessage}`);
        throw error;
    }
};