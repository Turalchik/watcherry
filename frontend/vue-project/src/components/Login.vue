<template>
    <div class="login">
        <h1>Вход</h1>
        <form @submit.prevent="login">
            <input v-model="username" placeholder="Логин" />
            <input v-model="password" type="password" placeholder="Пароль" />
            <button type="submit">Войти</button>
        </form>
        <p v-if="errorMessage">{{ errorMessage }}</p>
    </div>
</template>

<script>
import { loginUser } from '../api';

export default {
    data() {
        return {
            username: '',
            password: '',
            errorMessage: ''
        };
    },
    methods: {
        async login() {
            try {
                const credentials = {
                    username: this.username,
                    password: this.password
                };
                const response = await loginUser(credentials);
                localStorage.setItem('token', response.token); // Сохраняем токен
                this.$router.push('/'); // Переходим на главную страницу
            } catch (error) {
                this.errorMessage = 'Неверный логин или пароль';
            }
        }
    }
};
</script>
