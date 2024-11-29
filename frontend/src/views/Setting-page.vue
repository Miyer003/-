<template>
  <div>
    <h1>修改资料</h1>
    <!-- 这里添加AI对话组件内容 -->
  </div>

  <div class="settings-page">
    <h1>设置页面</h1>
    <form @submit.prevent="updateSettings">
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
      <button type="submit">更新信息</button>
    </form>
    <div class="preview">
      <p>用户名: {{ userProfile.userName }}</p>
      <p>性别: {{ userProfile.gender }}</p>
      <p>出生日期: {{ userProfile.birthDate }}</p>
      <p>所在地: {{ userProfile.location }}</p>
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
        userName: '',
        gender: 'male', // 默认值为'male'
        birthDate: '',
        location: ''
      }
    };
  },
  
  components: {
    UserProfile
  },

  methods: {
    updateSettings() {
      console.log('user profile updated:', this.userProfile);
      localStorage.setItem('userProfile', JSON.stringify(this.userProfile));
    },

    backbutton (){
            //  路径/home对应我在router目录下index.js中定义的path属性值
               //this.$router.push('/home');
            //  对应router目录下index.js中定义的name
                this.$router.push({name:'UserProfile'});
            },
  },

  /*props: {
    userName: '',
    gender: '', // 默认值为'male'
    birthDate: '',
    location: '' 
  }*/
};
</script>




