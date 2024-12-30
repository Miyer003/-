<template>
    <div class="login-container">
      <div class="header">
        <img src="@/assets/云译网.png" alt="logo" class="logo" />
        <span class="site-name">云译网</span>
      </div>
      <div class="login-box">
        <h2>账号注册</h2>
        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label for="phone" class="inline-label">手机号</label>
            <input
              type="text"
              id="phone"
              v-model="phone"
              placeholder="请输入手机号"
              required
            />
          </div>
          <div class="error" v-if="errors.phone">{{ errors.phone }}</div>
          <div class="underline"></div>
  
          <div class="form-group">
            <label for="password" class="inline-label">密码</label>
            <input
              type="password"
              id="password"
              v-model="password"
              placeholder="请输入密码"
              required
            />
          </div>
          <div class="error" v-if="errors.password">{{ errors.password }}</div>
          <div class="underline"></div>
  
          <div class="form-group">
            <label for="confirmPassword" class="inline-label">确认密码</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="confirmPassword"
              placeholder="请再次输入密码"
              required
            />
          </div>
          <div class="error" v-if="errors.confirmPassword">{{ errors.confirmPassword }}</div>
          <div class="underline"></div>
  
          <div class="form-group">
            <label for="birthday" class="inline-label">生日</label>
            <input
              type="text"
              id="birthday"
              v-model="birthday"
              placeholder="请输入生日 例：20001109"
              required
            />
          </div>
          <div class="error" v-if="errors.birthday">{{ errors.birthday }}</div>
          <div class="underline"></div>
  
          <div class="form-group">
            <label for="avatar" class="inline-label">上传头像</label>
            <input type="file" id="avatar" @change="handleAvatarUpload" />
          </div>
          <div class="underline"></div>
  
          <div class="button-group">
            <button type="submit" class="register-button">注册</button>
            <button type="button" class="register-button" @click="navigateToLogin">
              登录
            </button>
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
        confirmPassword: '',
        birthday: '',
        avatar: null,
        errors: {},
      };
    },
    methods: {
      async handleRegister() {
        this.errors = {}; // 清除旧的错误信息
  
        // 表单验证
        if (this.phone.length !=11) {
          this.errors.phone = '请输入有效的手机号';
        }
        if (this.password.length < 6) {
          this.errors.password = '密码至少为6位';
        }
        if (this.password !== this.confirmPassword) {
          this.errors.confirmPassword = '两次输入的密码不一致';
        }
        if (!this.birthday.match(/^\d{8}$/)) {
          this.errors.birthday = '请输入正确的生日格式，例如：20001109';
        }
        if (Object.keys(this.errors).length > 0) {
          return; // 如果有错误，停止注册
        }
  
        // 提交注册信息
        const formData = new FormData();
        formData.append('phone', this.phone);
        formData.append('password', this.password);
        formData.append('birthday', this.birthday);
        if (this.avatar) {
          formData.append('avatar', this.avatar);
        }
  
        try {
          const response = await axios.post('http://localhost:5001/register', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
          });
          alert(response.data.message);
          this.navigateToLogin();
        } catch (error) {
          if (error.response) {
            alert(error.response.data.message);
          } else {
            alert('注册失败，请稍后重试');
          }
        }
      },
      handleAvatarUpload(event) {
        const file = event.target.files[0];
        this.avatar = file;
      },
      navigateToLogin() {
        this.$router.push({ name: 'Login' });
      },
    },
  };
  </script>
  
  <style scoped>
  /* 样式保持不变，仅调整错误提示 */
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
  .error {
    color: red;
    font-size: 12px;
    text-align: left;
    margin-top: -10px;
    margin-bottom: 10px;
  }
  </style>
  
