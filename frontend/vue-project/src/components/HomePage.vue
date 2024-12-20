<!-- frontend/src/components/HomePage.vue -->
<template>
  <div>
    <Navbar />

    <h1>Популярные фильмы</h1>
    <div v-if="isLoading">Загрузка...</div>
    <div v-else-if="error">
      <p>Не удалось загрузить данные. Попробуйте позже.</p>
    </div>
    <ul v-else class="movie-list">
      <li v-for="movie in popularMovies" :key="movie.id" class="movie-item">
        <router-link :to="`/movie/${movie.title_id}`">
          <img :src="movie.poster_url" :alt="movie.title" class="movie-poster" />
          <span>{{ movie.title }} ({{ movie.release_year }})</span>
        </router-link>
      </li>
    </ul>

    <h1>Новые фильмы</h1>
    <div v-if="isLoading">Загрузка...</div>
    <div v-else-if="error">
      <p>Не удалось загрузить данные. Попробуйте позже.</p>
    </div>
    <ul v-else class="movie-list">
      <li v-for="movie in newMovies" :key="movie.id" class="movie-item">
        <router-link :to="`/movie/${movie.title_id}`">
          <img :src="movie.poster_url" :alt="movie.title" class="movie-poster" />
          <span>{{ movie.title }} ({{ movie.release_year }})</span>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import Navbar from './Navbar.vue';
import { fetchPopularAndNewMovies } from '../api';

export default {
  components: {
    Navbar,
  },
  data() {
    return {
      popularMovies: [],
      newMovies: [],
      isLoading: true,
      error: null,
    };
  },
  async created() {
    try {
      const data = await fetchPopularAndNewMovies();
      console.log("Полученные данные:", data);
      this.popularMovies = data.popular_movies || [];
      this.newMovies = data.new_movies || [];
    } catch (error) {
      console.error("Ошибка при загрузке фильмов:", error);
      this.error = "Ошибка при загрузке данных.";
    } finally {
      this.isLoading = false;
    }
  },
};
</script>

<style scoped>
h1 {
  font-size: 1.8em;
  margin-bottom: 10px;
}

.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 0;
  list-style: none;
}

.movie-item {
  width: 150px;
  text-align: center;
}

.movie-poster {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

a {
  text-decoration: none;
  color: #2c3e50;
}

a:hover span {
  text-decoration: underline;
}
</style>
