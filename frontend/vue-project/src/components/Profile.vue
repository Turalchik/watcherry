<template>
  <div>
    <header>
      <h1>Добро пожаловать, {{ user.username }}!</h1>
      <p>Это ваш личный кабинет.</p>
    </header>

    <main>
      <!-- Отображение аватара -->
      <section>
        <h2>Ваш аватар</h2>
        <img :src="user.profile.avatarUrl" alt="Аватар" width="150" height="150" />
      </section>

      <!-- Форма для загрузки нового аватара -->
      <section>
        <form @submit.prevent="uploadAvatar" id="avatar-form">
          <input type="file" ref="avatarInput" @change="handleAvatarChange" style="display: none;" />
          <button type="button" @click="triggerAvatarUpload">Изменить аватар</button>
        </form>
      </section>

      <!-- Выход из системы -->
      <section>
        <button @click="logout">Выйти</button>
      </section>

      <!-- Вернуться на главную -->
      <section>
        <router-link to="/">Вернуться на главную страницу</router-link>
      </section>

      <!-- Форма обновления профиля -->
      <section>
        <form @submit.prevent="updateProfile">
          <div v-for="(value, key) in profileForm" :key="key">
            <label :for="key">{{ key }}</label>
            <input v-model="profileForm[key]" :id="key" />
          </div>
          <button type="submit">Обновить профиль</button>
        </form>
      </section>

      <!-- Отзывы пользователя -->
      <section>
        <h2>Понравившиеся фильмы</h2>
        <ul v-if="likedMovies.length">
          <li v-for="movie in likedMovies" :key="movie.title_id">
            <router-link :to="`/movie/${movie.title_id}`">{{ movie.title }}</router-link>
          </li>
        </ul>
        <p v-else>У вас пока нет понравившихся фильмов.</p>

        <h2>Рекомендованные фильмы</h2>
        <ul v-if="recommendations.length">
          <li v-for="movie in recommendations" :key="movie.title_id">
            <router-link :to="`/movie/${movie.title_id}`">{{ movie.title }}</router-link>
          </li>
        </ul>
        <p v-else>Рекомендаций пока нет.</p>

        <h2>Ваши отзывы</h2>
        <ul v-if="reviews.length">
          <li v-for="review in reviews" :key="review.id">
            <strong>{{ review.movie.title }}</strong>: {{ review.content }}
            <router-link :to="`/movie/${review.movie.title_id}`">Перейти к фильму</router-link>
          </li>
        </ul>
        <p v-else>У вас нет отзывов.</p>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: {
        username: "ИмяПользователя",
        profile: {
          avatarUrl: "https://via.placeholder.com/150",
        },
      },
      profileForm: {
        name: "",
        email: "",
      },
      likedMovies: [],
      recommendations: [],
      reviews: [],
    };
  },
  methods: {
    triggerAvatarUpload() {
      this.$refs.avatarInput.click();
    },
    handleAvatarChange(event) {
      const file = event.target.files[0];
      if (file) {
        const formData = new FormData();
        formData.append("avatar", file);
        // Отправка файла на сервер
        this.uploadAvatar(formData);
      }
    },
    uploadAvatar(formData) {
      // Логика для отправки аватара на сервер
      console.log("Аватар загружен", formData);
    },
    logout() {
      // Логика выхода из системы
      console.log("Выход из системы");
    },
    updateProfile() {
      // Логика для обновления профиля
      console.log("Профиль обновлен", this.profileForm);
    },
  },
};
</script>

<style scoped>
header {
  text-align: center;
  margin-bottom: 20px;
}

section {
  margin-bottom: 20px;
}
</style>
