<!-- frontend/src/components/Navbar.vue -->
<template>
  <nav class="navbar">
    <div class="navbar-left">
      <!-- Кнопка для перехода на главную страницу -->
      <router-link to="/" class="navbar-button">Главная</router-link>
      <!-- Поле для ввода поискового запроса -->
      <input
        v-model="searchQuery"
        @keydown.enter="performSearch"
        class="navbar-input"
        type="text"
        placeholder="Введите запрос для поиска"
      />
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
import { fetchUserProfile } from '../api'; // Импортируем функцию для получения профиля пользователя

export default {
  data() {
    return {
      isLoggedIn: false,  // Статус авторизации
      userName: '',       // Никнейм пользователя
      searchQuery: '',    // Хранение текста поискового запроса
    };
  },
  methods: {
    async getUserProfile() {
      const token = localStorage.getItem('token'); // Получаем токен
      if (!token || token == 'undefined') {
          console.warn('Токен отсутствует. Пользователь не авторизован.');
          this.isLoggedIn = false; // Убедитесь, что статус корректно обновляется
          return;
      }
      try {
          const profile = await fetchUserProfile(token);
          this.isLoggedIn = true;
          this.userName = profile.username;
      } catch (error) {
          console.error('Ошибка получения профиля:', error);
          this.isLoggedIn = false;
      }
    },
    goToProfile() {
      this.$router.push('/profile'); // Переход на страницу профиля
    },
    performSearch() {
      this.$router.push({ path: '/search', query: { q: this.searchQuery } }); // Обработка поискового запроса
    },
  },
  mounted() {
    this.getUserProfile(); // Получаем данные пользователя при загрузке компонента
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
