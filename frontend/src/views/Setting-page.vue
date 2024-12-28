<template>
  <div>
    <h1>修改资料</h1>
    <!-- 这里添加AI对话组件内容 -->
  </div>

  <div class="settings-page">
    <h1>设置页面</h1>
    <form @submit.prevent="updateSettings">
      <!---<div>
        <label for="avatar">头像:</label>
        <input type="file" id="avatar" @change="handleAvatarChange" accept="image/*" />
      </div>
      <div v-if="userProfile.avatar">
        <p>头像预览:</p>
        <img :src="userProfile.avatar" alt="头像预览" />
      </div>--->
      <div>
        <label for="userName">用户名:</label>
        <input type="text" id="userName" v-model="userProfile.userName" required />
      </div>
      <div>
        <label for="gender">性别:</label>
        <select id="gender" v-model="userProfile.gender">
          <option value="male">男</option>
          <option value="female">女</option>
        </select>
      </div>
      <div>
        <label for="birthDateOfBirth">出生日期:</label>
        <input type="date" id="birthDateOfBirth" v-model="userProfile.birthDate" />
      </div>
      <div>
        <label for="location">所在地:</label>
        <input type="text" id="location" v-model="userProfile.location" />
      </div>
      <div>
        <label for="email">绑定邮箱:</label>
        <input type="text" id="birthDateOfBirth" v-model="userProfile.email" />
      </div>
      <div>
        <label for="mobile">绑定手机:</label>
        <input type="text" id="mobile" v-model="userProfile.mobile" />
      </div>

      <button type="submit">更新信息</button>
    </form>
    <div class="preview">
      <p>用户名: {{ userProfile.userName }}</p>
      <p>性别: {{ userProfile.gender }}</p>
      <p>出生日期: {{ userProfile.birthDate }}</p>
      <p>所在地: {{ userProfile.location }}</p>
      <p>绑定邮箱: {{ userProfile.email }}</p>
      <p>绑定手机: {{ userProfile.mobile }}</p>
      <!---<p>头像：{{ userProfile.avatar }}</p>--->
    </div>
    
    <div class="back">
        <button class="backbutton" @click="backbutton">返回</button>
      </div>

  </div>
</template>

<script>
import UserProfile from '@/views/UserProfile.vue'; // 用户个人主页
import axios from 'axios';
import { useRouter } from 'vue-router'; // 引入useRouter

export default {
  data() {
    return {
      userProfile: {
        user_id: this.$store.state.user_id || 1, 
        userName: '',
        gender: 'male', // 默认值为'male'
        birthDate: '',
        location: '',
        email: '',
        mobile: ''
        //avatar: '' // 用于存储头像URL//

      },
      //avatarFile: null // 用于存储上传的文件//
    };
  },
  
  components: {
    UserProfile
  },

  /*methods: {
    handleAvatarChange(event) {
      this.avatarFile = event.target.files[0];
      if (this.avatarFile) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.userProfile.avatar = e.target.result;
        };
        reader.readAsDataURL(this.avatarFile);
      }
    },

    updateSettings() {
      console.log('user profile updated:', this.userProfile);
      if (this.avatarFile) {
        this.uploadAvatar();
      } else {
        localStorage.setItem('userProfile', JSON.stringify(this.userProfile));
        this.$router.push({ name: 'UserProfile' });
      }
    },

    uploadAvatar() {
      const formData = new FormData();
      formData.append('avatar', this.avatarFile);
      axios.post('/api/upload-avatar', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        this.userProfile.avatar = response.data.url; // 假设后端返回新上传文件的URL
        localStorage.setItem('userProfile', JSON.stringify(this.userProfile));
        this.$router.push({ name: 'UserProfile' });
      })
      .catch(error => {
        console.error('上传头像失败:', error);
      });
    },
    

    backbutton (){
            //  路径/home对应我在router目录下index.js中定义的path属性值
               //this.$router.push('/home');
            //  对应router目录下index.js中定义的name
                this.$router.push({name:'UserProfile'});
            },
  },*/
  methods: {
     updateSettings() {
      // 发送POST请求到后端API以更新用户信息
      axios.post('http://localhost:8080/users/update', this.userProfile)
        .then(response => {
          if (response.data.base.code === 200) {
            console.log('用户信息更新成功');
            this.$router.push({ name: 'UserProfile' }); // 更新成功后跳转到用户个人主页
          } else {
            console.error('用户信息更新失败:', response.data.base.message);
          }
        })
        .catch(error => {
          console.error('更新用户信息请求失败:', error);
        });
    },

    fetchUserProfile() {
      // 发送GET请求到后端API以获取用户信息
      axios.get('http://localhost:8080/users/info', {
        params: {
          user_id: this.userProfile.user_id // 假设你有一个user_id来标识用户
        }
      })
      .then(response => {
        if (response.data.base.code === 200) {
          this.userProfile = { ...this.userProfile, ...response.data };
        } else {
          console.error('获取用户信息失败:', response.data.base.message);
        }
      })
      .catch(error => {
        console.error('获取用户信息请求失败:', error);
      });
    },

    backbutton (){
            //  路径/home对应我在router目录下index.js中定义的path属性值
               //this.$router.push('/home');
            //  对应router目录下index.js中定义的name
                this.$router.push({name:'UserProfile'});
            },

    mounted() {
      this.fetchUserProfile(); // 当组件挂载时获取用户信息
    }
  },

  /*props: {
    userName: '',
    gender: '', // 默认值为'male'
    birthDate: '',
    location: '' 
  }*/
};
</script>

<style scoped>
.preview{
  font-size: 25px;
  color:#27194d;
};
.backbutton{
  color: rgba(53, 63, 95, 0.695); /* 设置按钮文本的颜色为白色 */
  padding: 5px 10px; /* 设置按钮内部的填充，上下为10像素，左右为20像素 */
  border: none; /* 设置按钮没有边框 */
  border-radius: 5px; /* 设置按钮的边框圆角半径为5像素，使其边缘圆滑 */
  font-size: 15px;
}
</style>


