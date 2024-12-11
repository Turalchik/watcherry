import Vue from 'vue';               // Импортируем Vue
import App from './App.vue';           // Главный Vue компонент
import VueRouter from 'vue-router';    // Импортируем Vue Router для маршрутизации
import Home from './components/Home.vue';   // Компонент главной страницы
import MovieDetail from './components/MovieDetail.vue';   // Компонент страницы фильма
import SearchResults from './components/SearchResults.vue';   // Компонент результатов поиска

// Используем Vue Router
Vue.use(VueRouter);

// Определяем маршруты
const routes = [
  { path: '/', component: Home },                        // Главная страница
  { path: '/movie/:id', component: MovieDetail },        // Страница фильма по ID
  { path: '/search', component: SearchResults },         // Страница с результатами поиска
];

// Создаем экземпляр маршрутизатора
const router = new VueRouter({
  routes,  // Роуты для маршрутизатора
});

// Инициализируем Vue приложение
new Vue({
  el: '#app',  // Привязываем приложение к элементу с id "app"
  router,      // Подключаем маршрутизатор
  render: h => h(App),  // Отображаем главный компонент
});
