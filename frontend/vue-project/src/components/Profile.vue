<template>
  <div class="profile-container">
    <a href="/" class="back-to-home">← На главную</a>

    <h2>Личный кабинет</h2>
    
    <button class="logout-button" @click="logout">Выйти</button>
    
    <div class="profile-info">
      <img :src="userProfile.avatar_url" alt="Аватар" class="avatar" />
      <p>Никнейм: {{ userProfile.username }}</p>
    </div>

    <div v-if="moviesWithReviews.length" class="movies-section">
      <h3>Фильмы, которые вы комментировали:</h3>
      <ul>
        <li v-for="movie in moviesWithReviews" :key="movie.id">
          <a :href="`/movie/${movie.title_id}`">{{ movie.title }}</a>
        </li>
      </ul>
    </div>

    <div v-if="likedMovies.length" class="movies-section">
      <h3>Понравившиеся фильмы:</h3>
      <ul>
        <li v-for="movie in likedMovies" :key="movie.id">
          <a :href="`/movie/${movie.title_id}`">{{ movie.title }}</a>
        </li>
      </ul>
    </div>

    <div v-if="recommendations.length" class="movies-section">
      <h3>Рекомендации для вас:</h3>
      <ul>
        <li v-for="movie in recommendations" :key="movie.id">
          <a :href="`/movie/${movie.title_id}`">{{ movie.title }}</a>
        </li>
      </ul>
    </div>

     <div class="change-password-section">
      <h3>Сменить пароль</h3>
      <form @submit.prevent="changePassword">
        <input v-model="passwordData.current_password" type="password" placeholder="Текущий пароль" />
        <input v-model="passwordData.new_password" type="password" placeholder="Новый пароль" />
        <input v-model="passwordData.new_password_confirm" type="password" placeholder="Подтверждение нового пароля" />
        <button type="submit">Изменить пароль</button>
      </form>
      <p v-if="passwordError" class="error">{{ passwordError }}</p>
      <p v-if="passwordSuccess" class="success">{{ passwordSuccess }}</p>
    </div>

  </div>
</template>

<script>
import { fetchUserProfile } from '../api';
import { authState } from '../auth.js'
import { changePassword } from '../api';
import axios from "axios";

export default {
  data() {
    return {
      userProfile: {},
      moviesWithReviews: [],
      likedMovies: [],
      recommendations: [],

      passwordData: {
        current_password: '',
        new_password: '',
        new_password_confirm: '',
      },
      passwordError: '',
      passwordSuccess: '',

      selectedFile: null,
      avatarUrl: null,

    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem('token');
      const profileData = await fetchUserProfile(token);

      this.userProfile = profileData.profile;

      this.moviesWithReviews = profileData.movies_with_reviews;

      this.likedMovies = profileData.liked_movies;

      this.recommendations = profileData.recommendations;
    } catch (error) {
      console.error('Ошибка получения профиля:', error);
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      authState.setAuth(false);
      this.$router.push('/');
    },

    async changePassword() {
      try {
        const token = localStorage.getItem('token');
        const response = await changePassword(this.passwordData, token);
        this.passwordSuccess = response.success || 'Пароль успешно изменён!';
        this.passwordError = '';
        this.resetPasswordForm();
      } catch (error) {
        this.passwordError = error.response?.data?.error || 'Ошибка при смене пароля';
        this.passwordSuccess = '';
      }
    },
    resetPasswordForm() {
      this.passwordData = {
        current_password: '',
        new_password: '',
        new_password_confirm: '',
      };
    },    

  },
};
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
}
.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}
.movies-section {
  margin-top: 20px;
}
.logout-button {
  background-color: #ff4d4f;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 20px;
}
.logout-button:hover {
  background-color: #ff7875;
}
.back-to-home {
  display: inline-block;
  margin-bottom: 20px;
  color: #1890ff;
  text-decoration: none;
  font-size: 16px;
}
.back-to-home:hover {
  text-decoration: underline;
}
</style>
