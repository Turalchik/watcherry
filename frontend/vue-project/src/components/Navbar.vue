<!-- frontend/src/components/Navbar.vue -->
<template>
  <nav class="navbar">
    <div class="navbar-left">
      <!-- Кнопка для перехода на главную страницу -->
      <router-link to="/" class="navbar-button">Главная</router-link>
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
    };
  },
  methods: {
    async getUserProfile() {
      try {
        const token = localStorage.getItem('token'); // Получаем токен из localStorage
        if (token) {
          const profile = await fetchUserProfile(token); // Получаем профиль пользователя
          this.isLoggedIn = true;
          this.userName = profile.username; // Устанавливаем никнейм пользователя
        }
      } catch (error) {
        console.error('Ошибка получения профиля:', error);
        this.isLoggedIn = false;
      }
    },
    goToProfile() {
      this.$router.push('/profile'); // Переход на страницу профиля
    }
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
}

.navbar-button:hover {
  background-color: #45a049;
}

.navbar-left, .navbar-right {
  display: flex;
  align-items: center;
}
</style>
