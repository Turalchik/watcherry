<template>
  <div class="profile-container">
    <h2>Личный кабинет</h2>
    
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
</style>
