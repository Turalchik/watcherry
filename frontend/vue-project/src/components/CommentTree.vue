<template>
  <div class="comment">
    <p>
      <strong>{{ comment.user.username }}:</strong> {{ comment.text }}
    </p>

    <!-- Отображаем вложенные ответы рекурсивно -->
    <div v-if="comment.replies.length" class="replies" style="margin-left: 20px;">
      <CommentTree
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
        @reply="handleReply"
      />
    </div>

    <!-- Форма для добавления ответа -->
    <div v-if="isAuthenticated" style="margin-top: 5px;">
      <form @submit.prevent="submitReply">
        <textarea v-model="replyText" placeholder="Ваш ответ" rows="2"></textarea>
        <button type="submit">Ответить</button>
      </form>
    </div>
    <p v-else>Чтобы ответить, необходимо <router-link to="/login">войти</router-link>.</p>
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
      if (!this.replyText.trim()) return;

      // Отправляем ответ родительскому компоненту
      this.$emit('reply', {
        parentId: this.comment.id,
        text: this.replyText,
      });

      // Очищаем поле ответа
      this.replyText = '';
    },
    handleReply(replyData) {
      // Пробрасываем событие ответа дальше наверх
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
textarea {
  width: 100%;
  margin-bottom: 5px;
}
</style>
