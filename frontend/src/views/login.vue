<template>
    <div class="login-container">
      <div class="header">
        <img src="@/assets/云译网.png" alt="logo" class="logo" />
        <span class="site-name">云译网</span>
      </div>
      <div class="login-box">
        <div class="login-header">
          <h2>账号登录</h2>
          <!-- 点击游客登录时，调用 guestLogin 方法 -->
          <a href="#" class="guest-login" @click.prevent="guestLogin">游客登录</a>
        </div>
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="phone" class="inline-label">手机号</label>
            <input type="text" id="phone" v-model="phone" placeholder="请输入手机号" required />
          </div>
          <div class="underline"></div>
          <div class="form-group">
            <label for="password" class="inline-label">密码</label>
            <input type="password" id="password" v-model="password" placeholder="请输入密码" required />
          </div>
          <div class="underline"></div>
          <div class="options">
            <div class="remember-me">
              <input type="checkbox" id="remember" v-model="remember" />
              <label for="remember" class="gray-text">自动登录</label>
            </div>
            <a href="#" class="forgot-password gray-text" @click.prevent="navigateToForgotPassword">忘记密码？</a>
          </div>
          <div class="button-group">
            <button type="submit" class="login-button" @click="handleLogin">登录</button>
            <button type="button" class="register-button" @click="navigateToRegister">注册</button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        phone: '',
        password: '',
        remember: false,
      };
    },
    methods: {
      handleLogin() {
        if (!this.phone || !this.password) {
          alert("手机号和密码不能为空！");
          return;  // 如果为空，阻止后续的表单提交
        }
  
        const loginData = {
          phone: this.phone,
          password: this.password,
        };
  
        axios.post('http://127.0.0.1:5001/login', loginData)
          .then((response) => {
            const { message, user_id } = response.data;
  
            // 检查是否返回了 user_id
            if (!user_id) {
              alert("登录成功，但未能获取用户ID！");
              return;
            }
  
            // 将 user_id 存储到 Vuex 的 store 中
            this.$store.commit('setUserId', user_id);
  
            alert(message);
            this.navigateToHome(); // 跳转到首页
          })
          .catch((error) => {
            if (error.response) {
              alert(error.response.data.message);
            } else {
              alert('登录失败，请检查网络或稍后重试');
            }
          });
      },
  
      // 游客登录，直接设置默认 user_id
      guestLogin() {
        const defaultUserId = 888888; // 游客默认的 user_id
  
        // 将默认的 user_id 存储到 Vuex 的 store 中
        this.$store.commit('setUserId', defaultUserId);
  
        // 跳转到首页
        this.navigateToHome();
      },
  
      navigateToRegister() {
        this.$router.push({ name: 'Register' });
      },
      navigateToHome() {
        this.$router.push({ name: 'Home' });
      },
      navigateToForgotPassword() {
        this.$router.push({ name: 'ForgotPassword' });
      },
    },
  };
  </script>
  
  
  <style scoped>
  .login-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-image: url('@/assets/back.png'); /* 使用绝对路径 */
    background-size: cover;
  }
  
  .header {
    display: flex;
    align-items: center;
    margin-bottom: 20px; /* 减小间距 */
  }
  
  .logo {
    width: 60px;
    height: 40px;
    margin-right: 10px;
  }
  
  .site-name {
    font-size: 36px; /* 增大字体 */
    font-weight: bold; /* 加粗字体 */
    color: #333;
    font-family: 'Courier New', Courier, monospace; /* 更改字体 */
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); /* 添加阴影 */
    letter-spacing: 2px; /* 增加字间距 */
  }
  
  .login-box {
    background-color: rgba(255, 255, 255, 0.9); /* 半透明背景 */
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
    width: 350px;
    text-align: center;
  }
  
  .login-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 60px; /* 增大与下一行的距离 */
  }
  
  h2 {
    text-align: left;
  }
  
  .guest-login {
    color: #6200ea;
    text-decoration: none;
    cursor: pointer;
  }
  
  .form-group {
    display: flex;
    align-items: center;
    margin-bottom: 20px; /* 调整行间距 */
  }
  
  .inline-label {
    width: 70px; /* 标签宽度 */
    text-align: right;
    margin-right: 15px; /* 调整标签与输入框的间距 */
    font-size: 14px;
    color: #888;
  }
  
  input[type="text"],
  input[type="password"] {
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 0;
    text-align: left; /* 确保文字左对齐 */
    box-sizing: border-box; /* 确保内边距和边框计算在内 */
  }
  
  .underline {
    height: 1px;
    background-color: #ccc;
    margin-bottom: 30px; /* 增加与下方的间距 */
  }
  
  .options {
    display: flex;
    justify-content: center; /* 向中间靠拢 */
    align-items: center;
    margin-bottom: 40px; /* 增大间距 */
  }
  
  .remember-me {
    display: flex;
    align-items: center;
    margin-right: 80px; /* 调整间距 */
  }
  
  .gray-text {
    color: #888;
  }
  
  .forgot-password {
    margin-left: 80px; /* 调整间距 */
    text-decoration: none;
  }
  
  .button-group {
    display: flex;
    justify-content: space-between;
  }
  
  .login-button,
  .register-button {
    width: 48%;
    padding: 12px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
  }
  
  .login-button {
    background-color: #6200ea;
    color: white;
  }
  
  .register-button {
    background-color: #ff9800;
    color: white;
  }
  </style>
  