import { reactive } from 'vue';

export const authState = reactive({
  isAuthenticated: !!localStorage.getItem('token'),
  setAuth(status) {
    this.isAuthenticated = status;
  },
});
