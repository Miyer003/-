<template>
  <div>
    <!-- 顶部栏 -->
    <div class="top">
      <div style="display: flex; align-items: center;">
        <img src="@/assets/logo.png" alt="Big Boat" class="img1">
        <div class="text">云译网</div>
        <div class="find_input">
          <i class="search-icon fas fa-search"></i> <!-- 搜索图标 -->
          <input type="text" placeholder="请输入功能名称" v-model="searchQuery" @input="handleSearch" style="border: none; outline: none;">
        </div>
      </div>

      <!-- 使用户头像区域可点击跳转到个人主页 -->
      <router-link :to="{ name: 'UserProfile' }" class="user-info">
        <img src="@/assets/profile.png" alt="头像" id="userAvatar" class="img2">
        <p id="userName" class="name">{{ userName }}</p>
        <i class="logout-icon fas fa-sign-out-alt" @click="handleLogout"></i> <!-- 退出图标 -->
      </router-link>
    </div>
  
    <!-- 侧边栏菜单 -->
    <div class="sidebar">
      <router-link 
        v-for="item in menuItems" 
        :key="item.text" 
        :to="{ name: item.route }" 
        class="menu-item">
        <i :class="item.icon" class="icon"></i>
        <div class="text">{{ item.text }}</div>
      </router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useStore } from 'vuex';  // 确保引入了 useStore

export default {
  data() {
    return {
      userName: '用户名', // 可以从用户认证系统获取用户名
      searchQuery: '',
      menuItems: [
        { text: '首页', icon: 'fas fa-home', route: 'Home' },
        { text: 'AI对话', icon: 'fas fa-robot', route: 'ai-chat' },
        { text: '个性化定制', icon: 'fas fa-cogs', route: 'personalize' },
        { text: '翻译校对', icon: 'fas fa-check', route: 'translation-proof' },
        { text: '用户反馈', icon: 'fas fa-comment', route: 'user-feedback' }
      ]
    };
  },
  methods: {
    
    handleLogout(event) {
      // 阻止 router-link 的默认行为，避免跳转到个人主页
      event.preventDefault();
  
      // 退出登录的逻辑
      console.log('Logging out...');
      // 这里可以调用实际的退出登录 API
      // 然后跳转到登录页或其他页面
      this.$router.push({ name: 'Login' }); // 假设您的登录页面路由名称为 'Login'
    },
    handleSearch() {
      console.log('搜索内容:', this.searchQuery);
      // 可以加入搜索逻辑
    },
    fetchUserInfo() {
      const store = useStore(); // 获取Vuex store实例
      axios.get('http://localhost:8080/users/info', {
        params: {
          user_id:store.state.user_id || 1, // 假设用户ID是1，或者从其他地方获取
          fields: 'username' // 假设我们只想获取用户名
        }
      })
      .then(response => {
        if (response.data.base.code === 200) {
          this.userName = response.data.username; // 更新用户名
        } else {
          console.error('获取用户信息失败:', response.data.base.message);
        }
      })
      .catch(error => {
        console.error('获取用户信息请求失败:', error);
      });
    }
  },

  mounted() {
    this.fetchUserInfo(); // 当组件挂载时获取用户信息
  }
};
</script>

<style scoped>
/* 顶部栏样式：固定在页面顶部 */
.top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 50px;
  padding: 4px;
  box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 20px;
  position: fixed; /* 固定顶部栏 */
  top: 0;
  left: 0;
  width: 100%; /* 占满整行 */
  background-color: white; /* 背景色 */
  z-index: 10; /* 使顶部栏位于其他内容之上 */
}

.top .img1 {
  margin-left: 10px;
  height: 35px;
}

.top .text {
  margin-left: 15px;
  margin-right: 15px;
  font-size: 20px;
  font-weight: bold;
}

.top .find_input {
  border: 1px solid #dfe1e5;
  outline: none;
  width: auto;
  height: 30px;
  border-radius: 20px;
  padding: 6px;
  display: flex;
  align-items: center;
  color: rgb(179, 113, 202);
}

.top .find_input .search-icon {
  margin-left: 5px;
  margin-right: 10px;
  cursor: pointer;
}

/* 用户信息区域样式 */
.user-info {
  display: flex;
  align-items: center;
  cursor: pointer; /* 增加点击手势 */
}

.user-info img {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-left: 10px;
}

.user-info p {
  font-size: 14px;
  margin-left: 20px;
  margin-right: 20px;
}

.user-info .logout-icon {
  color: rgb(179, 113, 202);
  margin-right: 20px;
}

/* 侧边栏样式 */
.sidebar {
  width: 200px;
  background-color: #FFFF;
  color: rgb(239, 236, 236);
  position: fixed;
  height: 100%;
  overflow: auto;
  top: 50px; /* 使侧边栏不被顶部栏覆盖 */
  box-shadow: 4px 0px 8px rgba(0, 0, 0, 0.1); /* 添加右侧阴影 */
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 16px;
  text-decoration: none;
  color: rgb(179, 113, 202);
  transition: background-color 0.3s;
}

.menu-item:hover {
  background-color: #e4c5e6;
}

.menu-item .icon {
  margin-right: 10px;
  font-size: 15px;
}

.menu-item .text {
  font-size: 14px;
}

.content {
  margin-top: 70px; /* 给内容区域增加顶部间距，避免被固定顶部栏遮挡 */
  margin-left: 200px;
  padding: 15px;
}

h2 {
  color: #333;
}
</style>
