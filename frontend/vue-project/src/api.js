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
