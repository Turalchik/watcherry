<template>
  <div class="profile-container">
    <h2>Личный кабинет</h2>
    
    <!-- Кнопка "Выйти" -->
    <button class="logout-button" @click="logout">Выйти</button>
    
    <!-- Личная информация -->
    <div class="profile-info">
      <img :src="userProfile.avatar_url" alt="Аватар" class="avatar" />
      <p>Никнейм: {{ userProfile.username }}</p>
    </div>

    <!-- Фильмы, которые пользователь комментировал -->
    <div v-if="moviesWithReviews.length" class="movies-section">
      <h3>Фильмы, которые вы комментировали:</h3>
      <ul>
        <li v-for="movie in moviesWithReviews" :key="movie.id">
          <a :href="`/movies/${movie.id}`">{{ movie.title }}</a>
        </li>
      </ul>
    </div>

    <!-- Понравившиеся фильмы -->
    <div v-if="likedMovies.length" class="movies-section">
      <h3>Понравившиеся фильмы:</h3>
      <ul>
        <li v-for="movie in likedMovies" :key="movie.id">
          <a :href="`/movies/${movie.id}`">{{ movie.title }}</a>
        </li>
      </ul>
    </div>

    <!-- Рекомендации -->
    <div v-if="recommendations.length" class="movies-section">
      <h3>Рекомендации для вас:</h3>
      <ul>
        <li v-for="movie in recommendations" :key="movie.id">
          <a :href="`/movies/${movie.id}`">{{ movie.title }}</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { fetchUserProfile } from '../api';

export default {
  data() {
    return {
      userProfile: {},
      moviesWithReviews: [],
      likedMovies: [],
      recommendations: [],
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem('token');
      const profileData = await fetchUserProfile(token);

      // Заполняем данные профиля
      this.userProfile = profileData.profile;
      console.log(this.userProfile)

      // Фильмы, которые пользователь комментировал
      this.moviesWithReviews = profileData.movies_with_reviews;

      // Понравившиеся фильмы
      this.likedMovies = profileData.liked_movies;

      // Рекомендованные фильмы
      this.recommendations = profileData.recommendations;
    } catch (error) {
      console.error('Ошибка получения профиля:', error);
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token'); // Удаляем токен
      authState.setAuth(false); // Обновляем глобальное состояние авторизации
      this.$router.push('/login'); // Перенаправляем на страницу входа
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
</style>
