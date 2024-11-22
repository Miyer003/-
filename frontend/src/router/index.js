import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import OnlineTranslation from '../views/OnlineTranslation.vue';
import HistoryData from '../views/HistoryData.vue';
import AiChat from '../views/AiChat.vue';
import AutoPolish from '../views/AutoPolish.vue';
import Personalize from '../views/Personalize.vue';
import TranslationProof from '../views/TranslationProof.vue';
import UserFeedback from '../views/UserFeedback.vue';
import WeekData from '../views/WeekData.vue';
import UserProfile from '@/views/UserProfile.vue'; // 用户个人主页
import page from '@/views/Setting-page.vue'; // 确保路径和文件名正确
const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/user-profile', name: 'UserProfile', component: UserProfile },
  { path: '/online-translation', name: 'online-translation', component: OnlineTranslation },
  { path: '/history-data', name: 'history-data', component: HistoryData },
  { path: '/ai-chat', name: 'ai-chat', component: AiChat },
  { path: '/auto-polish', name: 'auto-polish', component: AutoPolish },
  { path: '/personalize', name: 'personalize', component: Personalize },
  { path: '/translation-proof', name: 'translation-proof', component: TranslationProof },
  { path: '/user-feedback', name: 'user-feedback', component: UserFeedback },
  { path: '/week-data', name: 'week-data', component: WeekData },
  { path: '/user-profile', name: 'UserProfile', component: UserProfile }, // 用户个人主页路由
  { path: '/history1', name: 'History1',component: HistoryData},
  { path: '/page', name: 'page', component: page },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
