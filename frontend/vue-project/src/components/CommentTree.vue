<template>
  <div class="comment">
    <p v-if="comment && comment.user && comment.text">
      <strong>{{ comment.user.username }}:</strong> {{ comment.text }}
    </p>
    <p v-else>Комментарий недоступен.</p>

    <!-- Отображаем вложенные ответы рекурсивно -->
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

    <!-- Форма для добавления ответа -->
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
    // Отправка ответа на комментарий
    async submitReply() {
      if (!this.replyText.trim()) {
        alert('Ответ не может быть пустым.');
        return;
      }

      // Пробрасываем событие родительскому компоненту
      this.$emit('reply', {
        parentId: this.comment?.id || null,
        text: this.replyText.trim(),
      });

      // Очищаем поле ответа
      this.replyText = '';
    },
    handleReply(replyData) {
      // Пробрасываем событие вверх по дереву
      this.$emit('reply', replyData);
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
