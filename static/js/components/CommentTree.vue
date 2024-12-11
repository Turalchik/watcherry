<!-- CommentTree.vue -->
<template>
  <div class="comment">
    <p><strong>{{ comment.user.username }}</strong>: {{ comment.text }}</p>
    <div class="replies" v-if="comment.replies && comment.replies.length">
      <CommentTree
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'CommentTree',
  props: {
    comment: Object
  }
};
</script>
