import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import SearchPage from '../components/SearchResults.vue';
import ProfilePage from '../components/Profile.vue';
import MovieDetail from '../components/MovieDetailPage.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/search', component: SearchPage },
  { path: '/profile', component: ProfilePage },
  { path: '/movie/:id', component: MovieDetail, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
