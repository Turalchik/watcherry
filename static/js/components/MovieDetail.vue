<!-- MovieDetail.vue -->
<template>
  <div>
    <h1>{{ movie.title }}</h1>
    <img v-if="movie.poster_url" :src="movie.poster_url" :alt="`Poster of ${movie.title}`" />
    <p><strong>Жанр:</strong> {{ movie.genres.join(', ') }}</p>
    <p><strong>Рейтинг:</strong> {{ movie.rating }}</p>
    <p><strong>Продолжительность:</strong> {{ movie.duration }} минут</p>

    <section>
      <h2>Актеры</h2>
      <ul>
        <li v-for="actor in movie.actors" :key="actor.id">{{ actor.name }}</li>
      </ul>
    </section>

    <section>
      <h2>Режиссеры</h2>
      <ul>
        <li v-for="director in movie.directors" :key="director.id">{{ director.name }}</li>
      </ul>
    </section>

    <section>
      <h2>Продюсеры</h2>
      <ul>
        <li v-for="producer in movie.producers" :key="producer.id">{{ producer.name }}</li>
      </ul>
    </section>

    <section>
      <h2>Отзывы</h2>
      <div v-if="movie.reviews">
        <div v-for="review in movie.reviews" :key="review.id">
          <p><strong>{{ review.user.username }}</strong>: {{ review.rating }} / 10</p>
          <p>{{ review.text }}</p>
          <CommentTree v-for="comment in review.comments" :key="comment.id" :comment="comment" />
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import CommentTree from './CommentTree.vue';

export default {
  components: {
    CommentTree
  },
  data() {
    return {
      movie: {}
    };
  },
  mounted() {
    const titleId = this.$route.params.id;
    fetch(`/api/movies/${titleId}`)
      .then(res => res.json())
      .then(data => {
        this.movie = data;
      });
  }
};
</script>
