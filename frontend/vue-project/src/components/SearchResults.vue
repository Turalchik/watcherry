<template>
  <div>
    <h1>Результаты поиска</h1>
    <div v-if="query">
      <p>Результаты для запроса: "{{ query }}"</p>
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
  props: {
    query: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      movies: [], // Список фильмов, который будем заполнять из ответа
    };
  },
  watch: {
    query(newQuery) {
      this.fetchMovies(newQuery); // Когда query изменяется, отправляем новый запрос
    },
  },
  methods: {
    async fetchMovies(searchQuery) {
      if (!searchQuery) {
        this.movies = []; // Если query пустое, очищаем список фильмов
        return;
      }
      try {
        const results = await searchMovies(searchQuery); // Запрос к API
        this.movies = results; // Сохраняем фильмы в локальный state
      } catch (error) {
        console.error('Ошибка при поиске фильмов:', error); // Обработка ошибок
        this.movies = []; // Очищаем фильмы в случае ошибки
      }
    },
  },
  mounted() {
    if (this.query) {
      this.fetchMovies(this.query); // Если query есть при монтировании компонента, сразу делаем запрос
    }
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
