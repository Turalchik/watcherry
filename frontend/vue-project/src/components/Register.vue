<template>
    <div class="register">
        <h1>Регистрация</h1>
        <form @submit.prevent="register">
            <input v-model="username" placeholder="Логин" />
            <input v-model="email" type="email" placeholder="Электронная почта" />
            <input v-model="password" type="password" placeholder="Пароль" />
            <input v-model="passwordConfirm" type="password" placeholder="Подтверждение пароля" />
            <button type="submit">Зарегистрироваться</button>
        </form>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>
        <p class="login-link">
            Уже есть аккаунт? 
            <router-link to="/login">Войти</router-link>
        </p>
    </div>
</template>

<script>
import { registerUser } from '../api';

export default {
    data() {
        return {
            username: '',
            email: '',
            password: '',
            passwordConfirm: '',
            errorMessage: '',
            successMessage: ''
        };
    },
    methods: {
        async register() {
            if (this.password !== this.passwordConfirm) {
                this.errorMessage = 'Пароли не совпадают';
                return;
            }
            try {
                const userData = {
                    username: this.username,
                    email: this.email,
                    password: this.password
                };
                const response = await registerUser(userData);
                this.successMessage = 'Регистрация прошла успешно! Теперь вы можете войти.';
                this.errorMessage = ''; // Clear any previous error messages
                this.resetForm(); // Reset the form fields
            } catch (error) {
                this.errorMessage = 'Ошибка при регистрации. Попробуйте еще раз.';
                this.successMessage = ''; // Clear any previous success messages
            }
        },
        resetForm() {
            this.username = '';
            this.email = '';
            this.password = '';
            this.passwordConfirm = '';
        }
    }
};
</script>

<style>
.error {
    color: red;
    margin-top: 10px;
}
.success {
    color: green;
    margin-top: 10px;
}
.login-link {
    margin-top: 20px;
    font-size: 14px;
}
</style>
