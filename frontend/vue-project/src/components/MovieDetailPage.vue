<template>
  <div v-if="movie">
    <header>
      <h1>{{ movie.title }}</h1>
      
      <div v-if="movie.poster_url">
        <img :src="movie.poster_url" :alt="'Постер фильма ' + movie.title" style="max-width: 300px;">
      </div>
      <p v-else>Постер не доступен.</p>

      <p><strong>Жанр:</strong> {{ movie.genres.join(', ') }}</p>
      <p><strong>Год выпуска:</strong> {{ movie.release_year }}</p>
      <p><strong>Рейтинг:</strong> {{ movie.rating }}</p>
      <p><strong>Количество голосов:</strong> {{ movie.votes }}</p>
      <p><strong>Продолжительность:</strong> {{ movie.duration }} минут</p>
    </header>

    <main>
      <!-- Секция для актеров -->
      <section>
        <h2>Актеры</h2>
        <ul v-if="movie.actors.length > 0">
          <li v-for="actor in movie.actors" :key="actor.id">{{ actor.name }}</li>
        </ul>
        <p v-else>Нет информации о актерах.</p>
      </section>

      <!-- Секция для режиссеров -->
      <section>
        <h2>Режиссеры</h2>
        <ul v-if="movie.directors.length > 0">
          <li v-for="director in movie.directors" :key="director.id">{{ director.name }}</li>
        </ul>
        <p v-else>Нет информации о режиссерах.</p>
      </section>

      <!-- Секция для продюсеров -->
      <section>
        <h2>Продюсеры</h2>
        <ul v-if="movie.producers.length > 0">
          <li v-for="producer in movie.producers" :key="producer.id">{{ producer.name }}</li>
        </ul>
        <p v-else>Нет информации о продюсерах.</p>
      </section>

      <!-- Секция для отзывов -->
      <section>
        <h2>Отзывы</h2>
        <ul v-if="reviews.length > 0">
          <li v-for="review in reviews" :key="review.id">
            <p><strong>{{ review.user }}:</strong> {{ review.rating }} / 10</p>
            <p>{{ review.text }}</p>

            <!-- Комментарии к отзыву -->
            <div class="comments">
              <CommentTree
                v-for="comment in review.comments"
                :key="comment.id"
                :comment="comment"
                v-if="!comment.parent"
              />
            </div>

            <!-- Форма добавления комментария -->
            <div v-if="isAuthenticated">
              <form @submit.prevent="addComment(review.id)">
                <textarea v-model="newComment[review.id]" placeholder="Ваш комментарий"></textarea>
                <button type="submit">Добавить комментарий</button>
              </form>
            </div>
            <p v-else>Чтобы оставить комментарий, необходимо <router-link to="/login">войти</router-link>.</p>
          </li>
        </ul>
        <p v-else>Нет отзывов для этого фильма.</p>
      </section>

      <!-- Форма для добавления отзыва -->
      <section>
        <div v-if="isAuthenticated">
          <div v-if="userHasReviewed">
            <p>Вы уже оставили отзыв для этого фильма.</p>
          </div>
          <div v-else>
            <h3>Оставить отзыв:</h3>
            <form @submit.prevent="addReview">
              <textarea v-model="newReview.text" placeholder="Ваш отзыв"></textarea>
              <input type="number" v-model="newReview.rating" placeholder="Оценка (1-10)" min="1" max="10">
              <button type="submit">Отправить отзыв</button>
            </form>
          </div>
        </div>
        <p v-else>Чтобы оставить отзыв, необходимо <router-link to="/login">войти</router-link>.</p>
      </section>

      <!-- Ссылка на главную -->
      <router-link to="/">На главную</router-link>
    </main>
  </div>
  <div v-else>
    <p>Загрузка...</p>
  </div>
</template>

<script>
import CommentTree from './CommentTree.vue';
import { fetchMovieDetails } from '../api';

export default {
  components: { CommentTree },
  data() {
    return {
      movie: null,
      reviews: [],
      isAuthenticated: false, // Проверка авторизации пользователя
      userHasReviewed: false, // Проверка, оставлял ли пользователь отзыв
      newReview: { text: '', rating: null },
      newComment: {}, // Поле для хранения новых комментариев к отзывам
    };
  },
  async created() {
    try {
      const movieId = this.$route.params.id;
      const data = await fetchMovieDetails(movieId);
      this.movie = data.movie;
      this.reviews = data.reviews;
      this.isAuthenticated = data.isAuthenticated; // Используем данные из API
      this.userHasReviewed = data.userHasReviewed; // Используем данные из API
    } catch (error) {
      console.error('Ошибка при загрузке данных:', error);
    }
  },
  methods: {
    async addReview() {
      // Реализация добавления отзыва
      console.log('Submitting review:', this.newReview);
    },
    async addComment(reviewId) {
      // Реализация добавления комментария
      console.log('Adding comment for review:', reviewId, this.newComment[reviewId]);
    },
  },
};
</script>


<style scoped>
/* Add styles here as needed */
</style>
