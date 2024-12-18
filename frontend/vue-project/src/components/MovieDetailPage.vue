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
      <p><strong>Рейтинг фильма на watcherry:</strong>{{ movie.rating_from_website.toFixed(1) }}</p>
      <p><strong>Количество голосов с базы данных:</strong> {{ movie.votes }}</p>
      <p><strong>Количество голосов на watcherry</strong>{{ movie.votes_from_website }}</p>
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

      <!-- Секция для отзывов -->
      <section>
        <h2>Отзывы</h2>
        <ul v-if="reviews.length > 0">
          <li v-for="review in reviews" :key="review.id">
            <p><strong>{{ review.user }}:</strong> {{ review.rating }} / 10</p>
            <p>{{ review.text }}</p>

            <!-- Комментарии к отзыву -->
            <div v-if="review.comments && review.comments.length > 0">
              <ul>
                <li v-for="comment in review.comments" :key="comment.id">
                  <p><strong>{{ comment.user }}:</strong> {{ comment.text }}</p>

                  <!-- Форма для добавления ответа на комментарий -->
                  <div v-if="isAuthenticated">
                    <form @submit.prevent="addComment(review.id, comment.id)">
                      <textarea
                        :value="getNestedComment(review.id, comment.id)"
                        @input="setNestedComment(review.id, comment.id, $event.target.value)"
                        placeholder="Ответ на комментарий">
                      </textarea>
                      <button type="submit">Ответить</button>
                    </form>
                  </div>

                  <!-- Отображение ответов на комментарий -->
                  <div v-if="comment.replies && comment.replies.length > 0">
                    <ul>
                      <li v-for="reply in comment.replies" :key="reply.id">
                        <p><strong>{{ reply.user }}:</strong> {{ reply.text }}</p>
                      </li>
                    </ul>
                  </div>

                </li>
              </ul>
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
import { fetchMovieDetails, toggleLike, postComment, postReview } from '../api';
import { authState } from '../auth';

export default {
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
      const token = localStorage.getItem('token');
      this.isAuthenticated = !!token; // если токен существует, то пользователь авторизован
      const movieId = this.$route.params.id;
      const data = await fetchMovieDetails(movieId);
      this.movie = data.movie;
      this.reviews = data.reviews || [];
      this.liked = data.liked;
      this.userHasReviewed = data.userHasReviewed; // Получаем информацию о том, оставил ли пользователь отзыв
    } catch (error) {
      console.error('Ошибка при загрузке данных:', error);
    }
  },
  computed: {
    isAuthenticated() {
      return this.authState?.isAuthenticated || false;
    },
  },
  methods: {

    getNestedComment(reviewId, commentId) {
    return this.newComment[reviewId]?.[commentId] || '';
    },



    setNestedComment(reviewId, commentId, value) {
      if (!this.newComment[reviewId]) {
        this.newComment[reviewId] = {}; // Создаем вложенный объект, если его еще нет
      }
      // Изменяем конкретный комментарий, не затрагивая остальные
      this.newComment[reviewId][commentId] = value;
  },




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
        const reviewData = { text: this.newReview.text, rating: this.newReview.rating };
        const newReview = await postReview(this.movie.title_id, reviewData, token);

        this.reviews.unshift(newReview);
        this.newReview = { text: '', rating: null };
        alert('Отзыв успешно добавлен!');
      } catch (error) {
        console.error('Ошибка при добавлении отзыва:', error);
        alert('Не удалось добавить отзыв. Попробуйте еще раз.');
      }
    },

    async addComment(reviewId, parentCommentId = null) {
      const commentContent = parentCommentId
          ? this.newComment[reviewId]?.[parentCommentId]
          : this.newComment[reviewId] || '';

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
        const commentData = { text: commentContent, parentId: parentCommentId };
        const newComment = await postComment(reviewId, commentData, token);

        // Обновление комментариев в объекте review
        const review = this.reviews.find(r => r.id === reviewId);
        if (review) {
          if (parentCommentId) {
            // Если это ответ на комментарий
            const parent = review.comments.find(c => c.id === parentCommentId);
            if (parent) {
              parent.replies = [...(parent.replies || []), newComment]; // Добавляем в поле replies
            }
          } else {
            // Просто добавляем комментарий
            review.comments.push(newComment);
          }
        }

        // Очищаем поле для нового комментария после добавления
        if (parentCommentId) {
          this.newComment[reviewId][parentCommentId] = ''; // Очистить для ответа
        } else {
          this.newComment[reviewId] = ''; // Очистить для основного комментария
        }

        alert('Комментарий успешно добавлен!');
      } catch (error) {
        console.error('Ошибка при добавлении комментария:', error);
      }

    },
  },
};
</script>