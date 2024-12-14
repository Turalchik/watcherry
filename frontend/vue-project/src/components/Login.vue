<!-- frontend/src/components/Login.vue -->
<template>
  <div class="login-container">
    <h2>Вход</h2>
    <form @submit.prevent="login">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Пароль" required />
      <button type="submit">Войти</button>
    </form>
  </div>
</template>

<script>
import { loginUser } from '../api';

export default {
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    async login() {
      try {
        const credentials = { email: this.email, password: this.password };
        const user = await loginUser(credentials); // Пытаемся войти в систему
        localStorage.setItem('token', user.token); // Сохраняем токен в localStorage
        this.$router.push('/'); // Перенаправляем на главную страницу
      } catch (error) {
        console.error('Ошибка входа:', error);
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  width: 300px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f4f4f4;
  border-radius: 8px;
}

input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>
