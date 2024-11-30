<template>
  <div class="login-container">
    <div class="header">
      <img src="@/assets/云译网.png" alt="logo" class="logo" />
      <span class="site-name">云译网</span>
    </div>
    <div class="login-box">
      <div class="login-header">
        <h2>重置密码</h2>
      </div>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="phone" class="inline-label">输入密码</label>
          <input type="text" id="phone" v-model="phone" placeholder="请输入密码" required />
        </div>
        <div class="underline"></div>
        <div class="form-group">
          <label for="birthday" class="inline-label">确认密码</label>
          <input type="birthday" id="birthday" v-model="birthday" placeholder="请再次输入密码" required />
        </div>
        <div class="underline"></div>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <div class="button-group">
          <button type="submit" class="login-button" @click="resetPassword">确认</button>
          <button type="button" class="register-button" @click="navigateBack">返回</button>
        </div>
      </form>
    </div>
  </div>
</template>


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
  margin-right: 10px; /* 调整标签与输入框的间距 */
  font-size: 14px;
  color: #888;
}

input[type="text"],
input[type="birthday"] {
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

<style scoped>
.error-message {
  color: red;
  font-size: 14px;
  margin-bottom: 20px;
}
</style>


<script>
import axios from "axios"; // 引入axios进行API请求
export default {
  created() {
  this.phone = this.$route.query.phone;
  },
  data() {
    return {
      phone: '', // 接收的手机号
      newPassword: '',
      confirmPassword: '',
      errorMessage: '',
    };
  },
  methods: {
    resetPassword() {
      if (this.newPassword !== this.confirmPassword) {
    this.errorMessage = '两次输入的密码不一致！';
    return;
  }

  const requestData = {
    phone: this.phone, // 使用从 query 参数获取的手机号
    newPassword: this.newPassword,
  };

  axios
    .post('http://8.138.30.178/reset-password', requestData)
    .then((response) => {
      alert('密码重置成功，请重新登录！');
      this.$router.push({ name: 'Login' });
    })
    .catch((error) => {
      if (error.response && error.response.data) {
        this.errorMessage = error.response.data.message;
      } else {
        this.errorMessage = '无法连接到服务器，请稍后重试！';
      }
    });
    },
    navigateBack() {
      this.$router.push({ name: 'ForgotPassword' });
    },
  },
};
</script>

