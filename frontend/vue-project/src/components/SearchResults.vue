<template>
  <div>
    <h1>Результаты поиска</h1>
    <div v-if="query">
      <p v-if="title && minRating && genre">
        Результаты для запроса: "{{ title }}" с рейтингом от {{ minRating }} и жанром "{{ genre }}"
      </p>
      <p v-else-if="title && minRating">
        Результаты для запроса: "{{ title }}" с рейтингом от {{ minRating }}
      </p>
      <p v-else-if="title && genre">
        Результаты для запроса: "{{ title }}" и жанром "{{ genre }}"
      </p>
      <p v-else-if="title">
        Результаты для запроса: "{{ title }}"
      </p>
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
import { searchMovies } from '../api';

export default {
  name: "SearchResults",
  data() {
    return {
      movies: [],
      title: '',
      minRating: 1,
      genre: '',
    };
  },
  computed: {
    query() {
      return this.title || this.minRating || this.genre;
    },
  },
  watch: {
    '$route.query': {
      immediate: true,
      handler(newQuery) {
        this.title = newQuery.title || '';
        this.minRating = Number(newQuery.minRating) || 0;
        this.genre = newQuery.genre || '';
        this.fetchMovies({ title: this.title, minRating: this.minRating, genre: this.genre });
      },
    },
  },
  methods: {
    async fetchMovies(searchQuery) {
      console.log('search results got:', searchQuery);
      if (!searchQuery.title) {
        console.warn('Поисковой запрос пуст. Пропускаем запрос к API.');
        this.movies = [];
        return;
      }
      try {
        console.log('fetching');
        const results = await searchMovies(searchQuery.title, searchQuery.minRating, searchQuery.genre);
        console.log('results:', results);
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
  flex-wrap: wrap;
  gap: 20px;
}

.movie-item {
  text-align: center;
  width: 150px;
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
