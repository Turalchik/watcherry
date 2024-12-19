<!-- frontend/src/components/Navbar.vue -->
<template>
  <nav class="navbar">
    <div class="navbar-left">
      <!-- Кнопка для перехода на главную страницу -->
      <router-link to="/" class="navbar-button">Главная</router-link>
      <!-- Поле для ввода поискового запроса -->
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="Введите название"
      />
      <select v-model="minRating">
        <option value="0">Оценка</option>
        <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
      </select>
      <select v-model="selectedGenre">
        <option value="">Все жанры</option>
        <option v-for="genre in genres" :key="genre.id" :value="genre.name">
          {{ genre.name }}
        </option>
      </select>
      <button @click="searchMovies">Поиск</button>
    </div>
    <div class="navbar-right">
      <!-- Кнопка для перехода в личный кабинет или кнопка "Вход" -->
      <button v-if="isLoggedIn" @click="goToProfile" class="navbar-button">
        {{ userName }}
      </button>
      <router-link v-else to="/login" class="navbar-button">Вход</router-link>
    </div>
  </nav>
</template>

<script>
import { fetchUserProfile, fetchGenres } from '../api';

export default {
  data() {
    return {
      isLoggedIn: false,
      userName: '',
      searchQuery: '',
      minRating: 0,
      selectedGenre: '',
      genres: []
    };
  },
  methods: {
    async getUserProfile() {
        const token = localStorage.getItem('token');
        if (!token || token === 'undefined') {
            this.isLoggedIn = false;
            return;
        }

        try {
            const profile = await fetchUserProfile(token);
            this.isLoggedIn = true;
            this.userName = profile.profile.username;
            console.log(profile);
        } catch (error) {
            this.isLoggedIn = false;
        }
    },
    async fetchMovieGenres() {
      console.log('navbar fetchGenres')
      try {
        const response = await fetchGenres();
        this.genres = response;
      } catch (error) {
        console.error('Ошибка загрузки жанров:', error);
      }
    },
    goToProfile() {
      this.$router.push('/profile');
    },
    async searchMovies() {
      const params = new URLSearchParams();
      params.append('title', this.searchQuery);

      if (this.minRating > 0) {
        params.append('minRating', this.minRating);
      }
      
      if (this.selectedGenre) {
        params.append('genre', this.selectedGenre);
      }
      console.log('navbar sending params:', params);
      this.$router.push({ path: '/search', query: Object.fromEntries(params) });
    }
  },
  mounted() {
    this.getUserProfile();
    this.fetchMovieGenres();
  }
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  padding: 10px 20px;
  background-color: #333;
  color: white;
}

.navbar-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
  margin-right: 15px;
}

.navbar-input {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
  width: 300px;
}

.navbar-button:hover {
  background-color: #45a049;
}

.navbar-left, .navbar-right {
  display: flex;
  align-items: center;
}
</style>
