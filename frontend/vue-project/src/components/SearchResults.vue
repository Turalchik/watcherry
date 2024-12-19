<template>
  <div>
    <h1>Результаты поиска</h1>
    <div v-if="query">
      <p>Результаты для запроса: "{{ title }}" {{ minRating }}/10</p>
      <div class="movie-list" v-if="movies.length">
        <div class="movie-item" v-for="movie in movies" :key="movie.title_id">
          <a :href="`/movie/${movie.title_id}`">
            <img :src="movie.poster_url" :alt="`${movie.title} poster`" />
          </a>
          <a :href="`/movie/${movie.title_id}`">{{ movie.title }}</a>
        </div>
      </div>
      <p v-else>Фильмы не найдены.</p>
    </div>
    <p v-else>Введите запрос для поиска.</p>
  </div>
</template>

<script>
import { searchMovies } from '../api'; // Импортируем функцию для поиска фильмов

export default {
  name: "SearchResults",
  data() {
    return {
      movies: [],
      title: '',
      minRating: 1,
    };
  },
  computed: {
    query() {
      return this.title || this.minRating;
    },
  },
  watch: {
    '$route.query': {
      immediate: true,
      handler(newQuery) {
        this.title = newQuery.title || '';
        this.minRating = Number(newQuery.minRating) || 1;
        this.fetchMovies({ title: this.title, minRating: this.minRating });
      },
    },
  },
  methods: {
    async fetchMovies(searchQuery) {
      if (!searchQuery.title) {
        console.warn('Поисковой запрос пуст. Пропускаем запрос к API.');
        this.movies = [];
        return;
      }
      try {
        const results = await searchMovies(searchQuery.title, searchQuery.minRating);
        this.movies = results;
      } catch (error) {
        console.error('Ошибка при поиске фильмов:', error);
        this.movies = [];
      }
    },
  },
};
</script>

<style scoped>
.movie-list {
  display: flex;
  flex-wrap: wrap; /* Перенос элементов на новую строку, если они не помещаются */
  gap: 20px; /* Промежуток между элементами */
}

.movie-item {
  text-align: center;
  width: 150px; /* Ограничение ширины каждого элемента */
}

.movie-item img {
  width: 100px;
  height: auto;
  display: block;
  margin: 0 auto;
}

.movie-item a {
  display: block;
  margin-top: 5px;
}
</style>
