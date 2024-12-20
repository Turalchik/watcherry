<template>
  <div class="comment">
    <p v-if="comment && comment.user && comment.text">
      <strong>{{ comment.user }}:</strong> {{ comment.text }}
    </p>
    <p v-else>Комментарий недоступен.</p>

    <div
      v-if="Array.isArray(comment.replies) && comment.replies.length"
      class="replies"
    >
      <CommentTree
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
        :isAuthenticated="isAuthenticated"
        @reply="handleReply"
      />
    </div>

    <div v-if="isAuthenticated" class="reply-form">
      <form @submit.prevent="submitReply">
        <textarea
          v-model="replyText"
          placeholder="Ваш ответ"
          rows="2"
        ></textarea>
        <button type="submit">Ответить</button>
      </form>
    </div>
    <p v-else>
      Чтобы ответить, необходимо <router-link to="/login">войти</router-link>.
    </p>
  </div>
</template>

<script>
export default {
  name: 'CommentTree',
  props: {
    comment: {
      type: Object,
      required: true,
    },
    isAuthenticated: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      replyText: '',
    };
  },
  methods: {
    async submitReply() {
      if (!this.replyText.trim()) {
        alert('Ответ не может быть пустым.');
        return;
      }

      const replyData = {
        parent: this.comment.id,
        text: this.replyText.trim(),
      };

      console.log('Отправка ответа: ', replyData);

      this.$emit('comment-reply', replyData);
      
      console.log('Событие отправлено');

      this.replyText = '';
    },
  },
};
</script>

<style scoped>
.comment {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
}
.replies {
  margin-left: 20px;
}
.reply-form textarea {
  width: 100%;
  margin-bottom: 5px;
}
.reply-form button {
  display: block;
}
</style>
