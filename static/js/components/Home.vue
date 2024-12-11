<template>
  <div>
    <div class="navbar">
      <div class="navbar-left">
        <a href="/" class="site-title">Watcherry</a>
      </div>
      <div class="navbar-center">
        <form @submit.prevent="searchMovies">
          <input type="text" v-model="query" placeholder="Искать фильмы..." class="search-bar">
          <button type="submit" class="search-button">🔍</button>
        </form>
      </div>
      <div class="navbar-right">
        <a v-if="user" :href="'/profile/'" class="user-link">{{ user.username }}</a>
        <a v-else href="/login" class="login-link">Вход</a>
      </div>
    </div>

    <div class="movies-section">
      <h2>Популярные фильмы</h2>
      <div class="movie-list">
        <div v-for="movie in popularMovies" :key="movie.title_id" class="movie-item">
          <a :href="`/movie/${movie.title_id}`">
            <img :src="movie.poster_url || placeholder" :alt="`${movie.title} poster`" class="movie-poster" />
          </a>
          <a :href="`/movie/${movie.title_id}`" class="movie-title">{{ movie.title }}</a>
          <p class="movie-info">Рейтинг: {{ movie.rating || 'N/A' }} | Голосов: {{ movie.votes || 0 }}</p>
        </div>
      </div>
    </div>

    <div class="movies-section">
      <h2>Новые фильмы</h2>
      <div class="movie-list">
        <div v-for="movie in newMovies" :key="movie.title_id" class="movie-item">
          <a :href="`/movie/${movie.title_id}`">
            <img :src="movie.poster_url || placeholder" :alt="`${movie.title} poster`" class="movie-poster" />
          </a>
          <a :href="`/movie/${movie.title_id}`" class="movie-title">{{ movie.title }}</a>
          <p class="movie-info">Рейтинг: {{ movie.rating || 'N/A' }} | Голосов: {{ movie.votes || 0 }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      popularMovies: [],
      newMovies: [],
      query: '',
      user: null,
      placeholder: '/static/images/placeholder.png', // Добавьте изображение-заглушку в static/images
    };
  },
  mounted() {
    fetch('/?format=api')
      .then(res => res.json())
      .then(data => {
        this.popularMovies = data.popular_movies || [];
        this.newMovies = data.new_movies || [];
      });

    fetch('/api/user')
      .then(res => res.json())
      .then(data => {
        this.user = data;
      });
  },
  methods: {
    searchMovies() {
      fetch(`/api/movies/search?q=${this.query}`)
        .then(res => res.json())
        .then(data => {
          // Допустим, вы хотите отобразить результаты поиска
          this.popularMovies = data.results || [];
        });
    },
  },
};
</script>

<style>
.navbar {
  display: flex;
  justify-content: space-between;
  padding: 10px 20px;
  background-color: #333;
  color: white;
}

.navbar .site-title {
  font-size: 1.5em;
  color: #fff;
  text-decoration: none;
}

.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 20px 0;
}

.movie-item {
  flex: 0 0 calc(25% - 20px);
  text-align: center;
}

.movie-poster {
  max-width: 100%;
  border-radius: 8px;
}

.movie-title {
  font-weight: bold;
  margin: 10px 0;
  display: block;
  color: #333;
}

.movie-info {
  font-size: 0.9em;
  color: #666;
}
</style>
