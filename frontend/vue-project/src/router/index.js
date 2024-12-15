import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import SearchPage from '../components/SearchResults.vue';
import ProfilePage from '../components/Profile.vue';
import Login from '../components/Login.vue';
import MovieDetail from '../components/MovieDetailPage.vue';
import Register from '../components/Register.vue'

const routes = [
  { path: '/', component: HomePage },
  { path: '/search', component: SearchPage },
  { path: '/profile', component: ProfilePage },
  { path: '/movie/:id', component: MovieDetail, props: true },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/profile', component: ProfilePage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
