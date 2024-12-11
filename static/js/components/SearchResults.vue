<!-- SearchResults.vue -->
<template>
  <div>
    <h1>Результаты поиска</h1>
    <div class="movie-list" v-if="movies.length">
      <div v-for="movie in movies" :key="movie.id" class="movie-item">
        <a :href="`/movie/${movie.title_id}`">
          <img :src="movie.poster_url" :alt="`${movie.title} poster`" />
        </a>
        <a :href="`/movie/${movie.title_id}`">{{ movie.title }}</a>
      </div>
    </div>
    <p v-else>Фильмы не найдены.</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      movies: [],
    };
  },
  mounted() {
    const query = new URLSearchParams(window.location.search).get('q');
    fetch(`/api/movies/search?q=${query}`)
      .then(res => res.json())
      .then(data => {
        this.movies = data;
      });
  }
};
</script>
