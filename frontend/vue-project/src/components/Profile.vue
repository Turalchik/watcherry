<!-- frontend/src/components/Profile.vue -->
<template>
  <div class="profile-container">
    <h2>Личный кабинет</h2>
    <p>Никнейм: {{ userName }}</p>
    <p>Другие данные профиля...</p>
  </div>
</template>

<script>
import { fetchUserProfile } from '../api';

export default {
  data() {
    return {
      userName: '',
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem('token'); // Получаем токен из localStorage
      const profile = await fetchUserProfile(token); // Получаем профиль пользователя
      this.userName = profile.username; // Отображаем никнейм
    } catch (error) {
      console.error('Ошибка получения профиля:', error);
    }
  }
};
</script>

<style scoped>
.profile-container {
  padding: 20px;
  background-color: #f4f4f4;
}
</style>
