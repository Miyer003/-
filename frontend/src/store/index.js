import { createStore } from 'vuex';

export default createStore({
  state: {
    user_id: localStorage.getItem('user_id') || 888888, // 从 localStorage 获取用户 ID，如果没有则使用默认值
  },
  mutations: {
    setUserId(state, user_id) {
      state.user_id = user_id;
      localStorage.setItem('user_id', user_id);  // 更新 localStorage 中的 user_id
    },
  },
  actions: {},
  modules: {},
});
