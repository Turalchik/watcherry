<template>
    <div class="login">
        <h1>Вход</h1>
        <form @submit.prevent="login">
            <input v-model="username" placeholder="Логин" />
            <input v-model="password" type="password" placeholder="Пароль" />
            <button type="submit">Войти</button>
        </form>
        <p v-if="errorMessage">{{ errorMessage }}</p>
        <p class="register-link">
            Нет аккаунта? 
            <router-link to="/register">Зарегистрироваться</router-link>
        </p>
    </div>
</template>

<script>
import { loginUser } from '../api';
import { authState } from '../auth'; // Импорт глобального состояния

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

                // Отправляем запрос на сервер
                const response = await loginUser(credentials);

                // Сохраняем токен в localStorage
                localStorage.setItem('token', response.token); // Теперь response.token должен содержать токен
                authState.setAuth(true);
                // Перенаправляем на главную страницу
                this.$router.push('/');
            } catch (error) {
                this.errorMessage = 'Неверный логин или пароль';
            }
        }
    }
};
</script>

<style>
.register-link {
    margin-top: 10px;
    font-size: 14px;
}
</style>
