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

      <button 
        v-if="isAuthenticated" 
        @click="toggleLikeStatus"
        :class="{ liked: liked }">
        {{ liked ? 'Удалить из понравившихся' : 'Добавить в понравившиеся' }}
      </button>
      <p v-else>Войдите, чтобы добавить фильм в список понравившихся.</p>
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
            <div class="comments" v-if="review.comments && review.comments.length > 0">
              <CommentTree
                v-for="comment in review.comments || []"
                :key="comment.id"
                :comment="comment"
                :isAuthenticated="isAuthenticated"
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
import { inject, reactive } from 'vue';
import CommentTree from './CommentTree.vue';
import { fetchMovieDetails, toggleLike } from '../api';
import { postComment } from '../api';
import { postReview } from '../api';
import { authState } from '../auth';

export default {
  components: { CommentTree },
  setup() {
    const authState = inject('authState');
    return { authState };
  },
  data() {
    return {
      movie: null,
      reviews: [],
      newReview: { text: '', rating: null },
      newComment: reactive({}), // Поле для хранения новых комментариев к отзывам
      userHasReviewed: false,
    };
  },
  async created() {
    try {
      const movieId = this.$route.params.id;
      const data = await fetchMovieDetails(movieId);
      this.movie = data.movie;
      this.reviews = data.reviews || [];
      this.liked = data.liked;
      console.log(this.liked)
    } catch (error) {
      console.error('Ошибка при загрузке данных:', error);
    }
  },
  computed: {
    isAuthenticated() {
      return this.authState?.isAuthenticated || false;
    },
    userHasReviewed() {
      return this.user_has_reviewed;
    },
  },
  methods: {
    async toggleLikeStatus() {
      if (!this.isAuthenticated) {
        alert('Необходимо войти в аккаунт для выполнения этого действия.');
        return;
      }

      const token = localStorage.getItem('token');
      if (!token) {
        alert('Не удалось получить токен. Пожалуйста, войдите заново.');
        return;
      }

      try {
        const result = await toggleLike(this.movie.title_id, token);
        this.liked = result.liked; // Обновляем состояние
        alert(result.message || (this.liked ? 'Фильм добавлен в понравившиеся!' : 'Фильм удалён из понравившихся!'));
      } catch (error) {
        console.error('Ошибка при переключении состояния "понравился":', error);
        alert('Не удалось выполнить действие. Попробуйте ещё раз.');
      }
    },
    // Добавление отзыва
    async addReview() {
        if (!this.newReview.text || this.newReview.text.trim() === '') {
            alert('Отзыв не может быть пустым.');
            return;
        }

        const token = localStorage.getItem('token');
        if (!token) {
            alert('Необходимо войти в аккаунт для добавления отзыва.');
            return;
        }

        try {
            const reviewData = { 
                text: this.newReview.text, 
                rating: this.newReview.rating 
            };
            console.log('Отправляемые данные:', reviewData);
            const newReview = await postReview(this.movie.title_id, reviewData, token);

            // Добавляем новый отзыв в список
            this.reviews.unshift(newReview);
            // Очищаем поля ввода
            this.newReview = { text: '', rating: null };
            alert('Отзыв успешно добавлен!');
        } catch (error) {
            console.error('Ошибка при добавлении отзыва:', error);
            alert('Не удалось добавить отзыв. Попробуйте еще раз.');
        }
    },

    // Добавление комментария
    async addComment(reviewId) {
        const commentContent = this.newComment[reviewId];
        if (!commentContent || commentContent.trim() === '') {
            alert('Комментарий не может быть пустым.');
            return;
        }

        const token = localStorage.getItem('token');
        if (!token) {
            alert('Необходимо войти в аккаунт для добавления комментария.');
            return;
        }

        try {
            const commentData = { text: commentContent };
            const newComment = await postComment(reviewId, commentData, token);

            // Находим отзыв и добавляем комментарий в список
            const review = this.reviews.find(r => r.id === reviewId);
            if (review) {
              if (!Array.isArray(review.comments)) {
                review.comments = []; // Инициализация, если массив отсутствует
              }
              review.comments.push(newComment);
            }

            // Очищаем поле ввода
            this.newComment[reviewId] = '';
            alert('Комментарий успешно добавлен!');
        } catch (error) {
            console.error('Ошибка при добавлении комментария:', error);
            alert('Не удалось добавить комментарий. Попробуйте еще раз.');
        }
    },
  },
};
</script>


<style scoped>
/* Add styles here as needed */
</style>
