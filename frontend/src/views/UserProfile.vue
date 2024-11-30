<template>
  <div class="UserProfile">
    <div class="sidebar">
      <Sidebar @navigate="handleSidebarNavigation" />
    </div>
    <div class="main-content">
      <div class="background">
        <img src="@/assets/background.png" alt="背景图片" class="backgroundphoto">
        <img src="@/assets/avatar.jpg" alt="头像" class="avatar">
        <div class="ground">
          <p class="text-muted">咩咩</p>
          <p class="information">          
            电话号码：188****4125<br>出生日期：1997-05-06<br>地址：陕西省-咸阳市-杨陵区邰城路3号
          </p>
        </div>
      </div>

      <div class="my-Profile">
        <img id="input" src="@/assets/1.png" alt="icon" class="icon-right" />
        <span id="input">我的</span>
      </div>

      <div class="Personalized-Dressup">
        <img id="input" src="@/assets/1.png" alt="icon" class="icon-right" />
        <span id="input">个性装扮</span>
      </div>

      <div class="-Setting">
        <img id="input" src="@/assets/1.png" alt="icon" class="icon-right" />
        <span id="input">相关设置</span>
      </div>

      <div class="myProfile">
        <div class="BindPhone">
          <label>绑定手机</label>
          <div>
            <form @submit.prevent="bindPhone" class="phone-form">
              <input type="tel" v-model="phoneNumber" placeholder="请输入手机号码" required  class="phone-input"/>
              <button type="submit" class="phone-button">绑定</button>
            </form>
           </div>
        </div>
        <div class="BindEmail">
          <div class="p-BindEmail">绑定邮箱</div>
          <div>  
            <form @submit.prevent="bindEmail" class="email-form">
              <input type="email" v-model="email" placeholder="请输入邮箱地址" required  class="email-input"/>
              <button type="submit" class="email-button">绑定</button>
            </form>
          </div>
        </div>
        <div class="PasswordSettings">
          <div class="p-PasswordSettings">密码设置</div>
          <div>  
            <form @submit.prevent="passwordSettings" class="password-form">
              <input type="password" v-model="password" placeholder="请输入密码" required  class="password-input"/>
              <button type="submit" class="password-button">设置</button>
            </form>
          </div>
        </div>
        <div class="LoginRecords">
          <label>登录记录</label>
          <a href="#">查看></a>
        </div>
        <div class="AccountAppeal">
          <label>账号申诉</label>
          <a href="#">查看></a>
        </div>
        <div class="AccountFreezeandCancellation">
          <label>账号冻结与注销</label>
          <a href="#">查看></a>
        </div>
      </div>

      <div class="PersonalizedDressup">
        <div class="Dressup1"></div>
        <div class="Dressup2"></div>
        <div class="Dressup3"></div>
        <div class="Dressup4"></div>
      <div class="look">
        <a href="#">更多></a>
      </div>
      </div>

      <div class="Setting">
        <div class="Speechspeed">
          <label class="speed-label">语音语速</label>
          <select class="speed-select" v-model="speechRate">
            <option value="normal">适中</option>
            <option value="slow">慢</option>
            <option value="fast">快</option>
          </select>
        </div>
        <div class="EnglishPronunciation">
          <label class="english-label">英语发音</label>
          <select class="english-select" v-model="pronunciation">
            <option value="american">美式发音</option>
            <option value="british">英式发音</option>
          </select>
        </div>
        <div class="ChinesePronunciation">
          <label class="chinese-label">中文发音</label>
          <select class="chinese-select" v-model="gender">
            <option value="male">男声</option>
            <option value="female">女声</option>
          </select>
        </div>
        <div class="pronunciationMethod">
          <label class="method-label">发音方式</label>
          <select class="method-select" v-model="pronunciationMode">
            <option value="word">单词发音</option>
            <option value="sentence">重复发音</option>
          </select>
        </div>
        <div class="AutomaticPronunciation">
          <label class="automa-label">自动发音</label>
          <input type="checkbox" class="automa-input" v-model="autoPronunciation" />
        </div>
        <div class="PrivacyManagement">
          <label>隐私管理</label>
          <a href="#">查看></a>
        </div>
      </div>

      <div class="Settingbutton">
        <button class="settingbutton" @click="settingbutton">修改个人资料</button>
      </div>

    </div>
  </div>



  

</template>

<script>
import Sidebar from '@/components/Sidebar.vue';
import axios from 'axios';
import { useRouter } from 'vue-router'; // 引入useRouter
import page from '@/views/Setting-page.vue'; // 确保路径和文件名正确

export default {
  components: {
    Sidebar,
    page
  },
 


  methods: {
    handleSidebarNavigation() {
      // 处理侧边栏导航的逻辑
    },

    updateSettings() {
      console.log('User profile updated:', this.userProfile);
      localStorage.setItem('userProfile', JSON.stringify(this.userProfile));
    },
    
    bindEmail() {
      // 调用后端API进行邮箱绑定
      axios.post('/api/bind-email', { email: this.email })
        .then(response => {
          // 处理成功逻辑
        })
        .catch(error => {
          // 处理错误逻辑
        });
    },

    bindPhone() {
      // 调用后端API进行手机绑定
      axios.post('/api/bind-phone', { phoneNumber: this.phoneNumber })
        .then(response => {
          // 处理成功逻辑
        })
        .catch(error => {
          // 处理错误逻辑
        });
    },

    settingbutton (){
            //  路径/home对应我在router目录下index.js中定义的path属性值
               //this.$router.push('/home');
            //  对应router目录下index.js中定义的name
                this.$router.push({name:'page'});
            },

    fetchUserProfile(userId) {
    // 这里编写获取用户信息的逻辑，例如 API 调用
      axios.get(`/api/user/${userId}`)
        .then(response => {
          this.userProfile = response.data; // 假设响应中包含用户信息
        });
        
  }

  },


  //props: {
  //  userName: string,
  //  gender: string, // 默认值为'male'
  //  birthDate: string,
  //  location: string 
  // },


  data() {
  return {
    userProfile: {
        userName: '咩咩',
        gender: 'male',  
        birthDate: '1997-05-06',
        location: '陕西省-咸阳市-杨陵区邰城路3号',
      },
    email: '',
    phoneNumber: '',
    speechRate: 'normal',
    pronunciation: 'american',
    gender: 'male',
    pronunciationMode: 'word',
    autoPronunciation: false
    };
  },


  setup() {
  const router = useRouter(); // 获取路由实例

  function goToHome() {
    router.push('/page/:Transmissions'); // 导航到 '/home' 路由
  }
  
  return { goToHome };
}
};


</script>

<style scoped>
.sidebar {
  z-index: 1000 ; /* 确保这个值高于其他可能遮挡它的元素 */
}

.main-content {
  margin-top: -46px;
  margin-left: 36px; 
  padding: 15px;
  position: relative;
  overflow: auto;  /*或者使用 scroll */
  transform: scale(0.8);/*transform 属性用于对元素应用变换。scale(0.8) 表示元素的尺寸将缩小到原始尺寸的 80%。*/
  width: 1600px; /* 定义容器宽度 */
  height: 930px; /* 定义容器高度 */
  z-index: 20; /* 确保这个值高于其他可能遮挡它的元素 */
  background: linear-gradient(to bottom right, #ab7bfe18, #5fb7ff1f);/* 对角线渐变，从左上到右下 */
}

.background {
  height: 349px;
  width: 1573px;
  position: absolute; /* 绝对定位 */
  top: 10px; /* 距离包含块顶部0像素 */
  left: -35px; /* 距离包含块左侧245像素 */
  z-index: 1; /* 堆叠顺序 */
}

.avatar {
  height: 269px;
  width: 269px;
  position: absolute;
  top: 50px; 
  left: 120px; 
  z-index: 3;
  border-radius: 135px;
  box-shadow: 3px 3px 5px 8px rgba(132, 110, 213, 0.15);
  /*h-offset（水平偏移）：阴影在水平方向上的偏移量，正值向右偏移，负值向左偏移。
v-offset（垂直偏移）：阴影在垂直方向上的偏移量，正值向下偏移，负值向上偏移。
blur（模糊半径）：阴影的模糊程度，值越大，阴影越模糊。
spread（扩展半径）：阴影的尺寸，正值使阴影变大，负值使阴影变小。
color（颜色）：阴影的颜色，可以使用颜色名称、十六进制值、RGB、RGBA等。
inset（可选）：如果需要内部阴影，可以添加这个关键字，如果不写则默认为外部阴影。*/
}

.ground {
  height: 119px;
  width: 1079px;
  position: absolute; /* 绝对定位 */
  top: 185px; /* 距离包含块顶部185像素 */
  left: 431px; /* 距离包含块左侧611像素 */
  z-index: 2; /* 堆叠顺序 */
  background-color: #DFDAED;
  box-shadow: 0px 3px 6px 0px rgba(0,0,0,0.15);
  border-radius: 50px; /* 设置圆角半径 */
}

.text-muted{
  font-size: 70px;
  color:#4F3499;
  text-shadow: 0px 3px 6px #6c42e1ba; /* 文本阴影 */
  font-weight: bold;/*粗体字*/
  position: absolute; /* 绝对定位 */
  top: -60px; /* 距离包含块顶部0像素 */
  left: 50px; /* 距离包含块左侧245像素 */
  z-index: 3; /* 堆叠顺序 */
}

.information{
  font-size: 20px;
  color:#4F3499;
  position: absolute; /* 绝对定位 */
  text-align: left;
  top: 0px; /* 距离包含块顶部0像素 */
  left: 300px; /* 距离包含块左侧245像素 */
  z-index: 3; /* 堆叠顺序 */
}

.backgroundphoto {
  height: 349px;
  width: 1573px;
  position: absolute; /* 绝对定位 */
  top: 0; /* 距离包含块顶部0像素 */
  left: 65px; /* 距离包含块左侧245像素 */
  z-index: 2; /* 堆叠顺序 */
}

.my-Profile{
  position: absolute; /* relative设置元素的定位为相对定位，这意味着元素的位置相对于其正常位置进行偏移 */
  top: 370px;
  left: 60px;
  display: flex; /* 设置元素的显示类型为弹性盒（flex），这允许子元素在容器内灵活排列 */
  align-items: center; /* 在弹性盒中，此属性用于垂直居中对齐所有子元素 */
  margin-bottom: 0px; /* 设置元素底部的外边距为0像素，即没有外边距 */
  font-family: '优设标题黑'; /* 设置元素的字体为'Dancing Script'，如果没有这个字体， ,cursive则使用通用的cursive字体族 */
  font-size: 24px; /* 设置元素文本的字体大小为24像素 */
  font-weight: 700; /* 等同于 bold */
  color: #ae6ac9; /* 设置元素文本的颜色为十六进制颜色#ae6ac9，这是一种紫色调 */
  padding-bottom: -10px; /* 设置元素底部的内边距为-10像素，即向内压缩元素的底部 */
}

.Personalized-Dressup{
  position: absolute; /* relative设置元素的定位为相对定位，这意味着元素的位置相对于其正常位置进行偏移 */
  top: 370px;
  left: 600px;
  display: flex; /* 设置元素的显示类型为弹性盒（flex），这允许子元素在容器内灵活排列 */
  align-items: center; /* 在弹性盒中，此属性用于垂直居中对齐所有子元素 */
  margin-bottom: 0px; /* 设置元素底部的外边距为0像素，即没有外边距 */
  font-family: '优设标题黑'; /* 设置元素的字体为'Dancing Script'，如果没有这个字体， ,cursive则使用通用的cursive字体族 */
  font-size: 24px; /* 设置元素文本的字体大小为24像素 */
  font-weight: 700; /* 等同于 bold */
  color: #ae6ac9; /* 设置元素文本的颜色为十六进制颜色#ae6ac9，这是一种紫色调 */
  padding-bottom: -10px; /* 设置元素底部的内边距为-10像素，即向内压缩元素的底部 */
}

.-Setting{
  position: absolute; /* relative设置元素的定位为相对定位，这意味着元素的位置相对于其正常位置进行偏移 */
  top: 370px;
  left: 1110px;
  display: flex; /* 设置元素的显示类型为弹性盒（flex），这允许子元素在容器内灵活排列 */
  align-items: center; /* 在弹性盒中，此属性用于垂直居中对齐所有子元素 */
  margin-bottom: 0px; /* 设置元素底部的外边距为0像素，即没有外边距 */
  font-family: '优设标题黑'; /* 设置元素的字体为'Dancing Script'，如果没有这个字体， ,cursive则使用通用的cursive字体族 */
  font-size: 24px; /* 设置元素文本的字体大小为24像素 */
  font-weight: 700; /* 等同于 bold */
  color: #ae6ac9; /* 设置元素文本的颜色为十六进制颜色#ae6ac9，这是一种紫色调 */
  padding-bottom: -10px; /* 设置元素底部的内边距为-10像素，即向内压缩元素的底部 */
}




.myProfile {
  height: 492px;
  width: 475px;
  position: absolute;
  top: 424px; 
  left: 55px; 
  z-index: 1;
  background-color: #8C7BFD3b; /* 移除了多余的空格 */
  opacity: 0.56; /* 设置透明度 */
  display: flex;
  flex-direction: column;
  align-items: center;
}

.BindPhone {
  height: 48px;
  width: 411px;
  text-align: left;
  position: absolute;
  top: 34px; 
  left: 22px; 
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  color: #0921d8;
  opacity: 1;
  z-index: 3;
  background-color: rgba(140, 123, 253, 0.256); 
  padding: 0px 10px 0px 10px;/* 分别设置上、右、下、左方向的内边距 *//* 10px 20px 15px 10px 15px;分别设置上、右、下、左方向的内边距，中间留空 */

  display: flex; /* 启用Flexbox布局 */
  flex-direction: row; /* 子元素将横向排列 */
  justify-content: space-between; /* 子元素之间的间距 */
  align-items: center; /* 垂直居中对齐 */
}

.p-BindPhone  {
  /*margin-top: 10px;  向上移动文字 */
  margin-left: 0px;

}

.phone-form {
  font-size: 17px; /* 设置元素文本的字体大小为24像素 */
  display: flex;
  /* font-size: 20px; 设置元素文本的字体大小为24像素 */
  position: absolute; /* 绝对定位 */
  top: 10px; /* 根据需要调整 */
  left: 360px;  /*根据需要调整 */
  width: 50px; /* 或者设置一个固定宽度，例如 200px */
  height: 20px; /* 设置一个固定高度 */
  border-radius: 3px;
  background-color: #0a07ae;
  /*display: flex;*/
  align-items: flex-end; /* 将align-items: right; */
  /*margin-top: 20px;*/
  border: 5px solid #0a07ae;
}

.phone-input[type="tel"] {
  /*flex: 1; /* 让输入框占据剩余空间 */
  font-size: 17px; /* 设置元素文本的字体大小为24像素 */
  position: absolute; /* 绝对定位 */
  /*padding: 10px; /* 增加内边距，使按钮看起来更大 */
  top: -5px; /* 根据需要调整 */
  left: -180px; /*根据需要调整 */
  padding: 5px; /* 根据需要调整 */
  width: 150px; /* 或者设置一个固定宽度，例如 200px */
  height: 15px; /* 设置一个固定高度 */
  border-radius: 5px;
  /*margin-right: 10px;*/
  /*flex: none; /* flex: 1; *//*禁止元素在 Flexbox 布局中伸缩。*/
}

.phone-button {
  font-size: 10px; /* 设置元素文本的字体大小为24像素 */
  padding: 0px 0px; /* 增加内边距，使按钮看起来更大 */
  width: 50px; /* 或者设置一个固定宽度，例如 200px */
  height: 20px; /* 设置一个固定高度 */
  top: -1.5px; /* 根据需要调整 */
  left: 0px; /*根据需要调整 */
  font-size: 17px; /* 改变字体大小 */
  font-weight: 550; /* bold粗体 */
  color: #f9f8fb;
  position: absolute; /* 绝对定位 */
  border: none;/*无边框。*/
  background-color: transparent; /* 背景透明 */
  border-color: transparent; /* 边框透明 */
  border-radius: 5px;/*设置边框圆角为 5 像素。*/
  cursor: pointer;/*鼠标悬停时显示为手型，表示可点击*/
}

.phone-button:hover {
  font-size: 17px; /* 改变字体大小 */
  font-weight: 800; /* bold粗体 */
  color: #c4cbf6;
  background-color: #9477e36f;
}




.BindEmail {
  height: 48px;
  width: 411px;
  text-align: left;
  position: absolute;
  top: 105px; 
  left: 22px; 
  
  color: #0921d8;
  opacity: 1;
  z-index: 3;
  background-color: rgba(140, 123, 253, 0.256); 
  padding: 0px 10px 0px 10px;/* 分别设置上、右、下、左方向的内边距 *//* 10px 20px 15px 10px 15px;分别设置上、右、下、左方向的内边距，中间留空 */
  
  display: flex; /* 启用Flexbox布局 */
  flex-direction: row; /* 子元素将横向排列 */
  justify-content: space-between; /* 子元素之间的间距 */
  align-items: right; /* center垂直居中对齐 */
}

.p-BindEmail  {
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  /* margin-top: 10px; 向上移动文字 */
  margin-top: 10px;
}

.email-form {
  font-size: 17px; /* 设置元素文本的字体大小为24像素 */
  display: flex;
  /* font-size: 20px; 设置元素文本的字体大小为24像素 */
  position: absolute; /* 绝对定位 */
  top: 10px; /* 根据需要调整 */
  left: 360px;  /*根据需要调整 */
  width: 50px; /* 或者设置一个固定宽度，例如 200px */
  height: 20px; /* 设置一个固定高度 */
  border-radius: 3px;
  background-color: #0a07ae;
  /*display: flex;*/
  align-items: flex-end; /* 将align-items: right; */
  /*margin-top: 20px;*/
  border: 5px solid #0a07ae;
}

.email-input[type="email"] {
  /*flex: 1; /* 让输入框占据剩余空间 */
  font-size: 17px; /* 设置元素文本的字体大小为24像素 */
  position: absolute; /* 绝对定位 */
  /*padding: 10px; /* 增加内边距，使按钮看起来更大 */
  top: -5px; /* 根据需要调整 */
  left: -180px; /*根据需要调整 */
  padding: 5px; /* 根据需要调整 */
  width: 150px; /* 或者设置一个固定宽度，例如 200px */
  height: 15px; /* 设置一个固定高度 */
  border-radius: 5px;
  /*margin-right: 10px;*/
  /*flex: none; /* flex: 1; *//*禁止元素在 Flexbox 布局中伸缩。*/
}

.email-button {
  font-size: 10px; /* 设置元素文本的字体大小为24像素 */
  padding: 0px 0px; /* 增加内边距，使按钮看起来更大 */
  width: 50px; /* 或者设置一个固定宽度，例如 200px */
  height: 20px; /* 设置一个固定高度 */
  top: -1.5px; /* 根据需要调整 */
  left: 0px; /*根据需要调整 */
  font-size: 17px; /* 改变字体大小 */
  font-weight: 550; /* bold粗体 */
  color: #f9f8fb;
  position: absolute; /* 绝对定位 */
  border: none;/*无边框。*/
  background-color: transparent; /* 背景透明 */
  border-color: transparent; /* 边框透明 */
  border-radius: 5px;/*设置边框圆角为 5 像素。*/
  cursor: pointer;/*鼠标悬停时显示为手型，表示可点击*/
}

.email-button:hover {
  font-size: 17px; /* 改变字体大小 */
  font-weight: 800; /* bold粗体 */
  color: #c4cbf6;
  background-color: #9477e36f;
}





.PasswordSettings {
  height: 48px;
  width: 411px;
  text-align: left;
  position: absolute;
  top: 177px; 
  left: 22px; 
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  color: #0921d8;
  opacity: 1;
  z-index: 3;
  background-color: rgba(140, 123, 253, 0.256); 
  padding: 0px 10px 0px 10px;/* 分别设置上、右、下、左方向的内边距 *//* 10px 20px 15px 10px 15px;分别设置上、右、下、左方向的内边距，中间留空 */

  display: flex; /* 启用Flexbox布局 */
  flex-direction: row; /* 子元素将横向排列 */
  justify-content: space-between; /* 子元素之间的间距 */
  align-items: center; /* 垂直居中对齐 */
}

.p-PasswordSettings  {
  /*margin-top: 10px;  向上移动文字 */
  margin-left: 0px;
}

.password-form {
  font-size: 17px; /* 设置元素文本的字体大小为24像素 */
  display: flex;
  /* font-size: 20px; 设置元素文本的字体大小为24像素 */
  position: absolute; /* 绝对定位 */
  top: 10px; /* 根据需要调整 */
  left: 360px;  /*根据需要调整 */
  width: 50px; /* 或者设置一个固定宽度，例如 200px */
  height: 20px; /* 设置一个固定高度 */
  border-radius: 3px;
  background-color: #0a07ae;
  /*display: flex;*/
  align-items: flex-end; /* 将align-items: right; */
  /*margin-top: 20px;*/
  border: 5px solid #0a07ae;
}

.password-input[type="password"] {
  /*flex: 1; /* 让输入框占据剩余空间 */
  font-size: 17px; /* 设置元素文本的字体大小为24像素 */
  position: absolute; /* 绝对定位 */
  /*padding: 10px; /* 增加内边距，使按钮看起来更大 */
  top: -5px; /* 根据需要调整 */
  left: -180px; /*根据需要调整 */
  padding: 5px; /* 根据需要调整 */
  width: 150px; /* 或者设置一个固定宽度，例如 200px */
  height: 15px; /* 设置一个固定高度 */
  border-radius: 5px;
  /*margin-right: 10px;*/
  /*flex: none; /* flex: 1; *//*禁止元素在 Flexbox 布局中伸缩。*/
}

.password-button {
  font-size: 10px; /* 设置元素文本的字体大小为24像素 */
  padding: 0px 0px; /* 增加内边距，使按钮看起来更大 */
  width: 50px; /* 或者设置一个固定宽度，例如 200px */
  height: 20px; /* 设置一个固定高度 */
  top: -1.5px; /* 根据需要调整 */
  left: 0px; /*根据需要调整 */
  font-size: 17px; /* 改变字体大小 */
  font-weight: 550; /* bold粗体 */
  color: #f9f8fb;
  position: absolute; /* 绝对定位 */
  border: none;/*无边框。*/
  background-color: transparent; /* 背景透明 */
  border-color: transparent; /* 边框透明 */
  border-radius: 5px;/*设置边框圆角为 5 像素。*/
  cursor: pointer;/*鼠标悬停时显示为手型，表示可点击*/
}

.password-button:hover {
  font-size: 17px; /* 改变字体大小 */
  font-weight: 800; /* bold粗体 */
  color: #c4cbf6;
  background-color: #9477e36f;
}




.LoginRecords {
  height: 48px;
  width: 411px;
  text-align: left;
  position: absolute;
  top: 249px; 
  left: 22px; 
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  color: #0921d8;
  opacity: 1;
  z-index: 3;
  background-color: rgba(140, 123, 253, 0.256); 
  padding: 0px 10px 0px 10px;/* 分别设置上、右、下、左方向的内边距 *//* 10px 20px 15px 10px 15px;分别设置上、右、下、左方向的内边距，中间留空 */

  display: flex; /* 启用Flexbox布局 */
  flex-direction: row; /* 子元素将横向排列 */
  justify-content: space-between; /* 子元素之间的间距 */
  align-items: center; /* 垂直居中对齐 */
}

/*.p-LoginRecords  {
  margin-top: 10px; 向上移动文字
  margin-left: 0px;
} */

.AccountAppeal {
  height: 48px;
  width: 411px;
  text-align: left;
  position: absolute;
  top: 321px; 
  left: 22px; 
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  color: #0921d8;
  opacity: 1;
  z-index: 3;
  background-color: rgba(140, 123, 253, 0.256); 
  padding: 0px 10px 0px 10px;/* 分别设置上、右、下、左方向的内边距 *//* 10px 20px 15px 10px 15px;分别设置上、右、下、左方向的内边距，中间留空 */

  display: flex; /* 启用Flexbox布局 */
  flex-direction: row; /* 子元素将横向排列 */
  justify-content: space-between; /* 子元素之间的间距 */
  align-items: center; /* 垂直居中对齐 */
}

/*.p-AccountAppeal  {
   margin-top: 10px; 向上移动文字 
  margin-left: 0px;
}*/

.AccountFreezeandCancellation {
  height: 48px;
  width: 411px;
  text-align: left;
  position: absolute;
  top: 393px; 
  left: 22px; 
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  color: #0921d8;
  opacity: 1;
  z-index: 3;
  background-color: rgba(140, 123, 253, 0.256); 
  padding: 0px 10px 0px 10px;/* 分别设置上、右、下、左方向的内边距 *//* 10px 20px 15px 10px 15px;分别设置上、右、下、左方向的内边距，中间留空 */

  display: flex; /* 启用Flexbox布局 */
  flex-direction: row; /* 子元素将横向排列 */
  justify-content: space-between; /* 子元素之间的间距 */
  align-items: center; /* 垂直居中对齐 */
}

/*.p-AccountFreezeandCancellation  {
   margin-top: 10px; 向上移动文字 
  margin-left: 0px;
}*/


.PersonalizedDressup{
  height: 442px;
  width: 425px;
  padding: 25px; /* 设置内边距 */
  position: absolute;
  top: 424px; 
  left: 580px; 
  z-index: 1;
  background-color: #8C7BFD3b;
  color: #3D629C;
  opacity: 0.56; /* 设置透明度*/

  display: grid;
  grid-template-columns: repeat(2, 2fr); /* 创建三列 */
  grid-template-rows: repeat(2, 2fr); /* 创建三行 */
  gap: 10px; /* 网格项之间的间隔 */
}

.Dressup1{
  width: 195px; /* 根据需要设置宽度 */
  height: 140px; /* 根据需要设置高度 */
  border: 2px solid #ccc; /* dashed设置虚线边框 */
  border-radius: 5px; /* 设置圆角 */
  background-color: #fff; /* 设置背景颜色 */
  padding: 16px; /* 设置内边距 */
  box-sizing: border-box; /* 确保内边距不会增加元素的总宽度和高度 */
  margin-top: 30px;  /*顶部外边距 */
  margin-right: 20px; /*右侧外边距 */
  margin-bottom: 0px; /*底部外边距 */
  margin-left: 6px;  /*左侧外边距 */
  position: absolute;
  grid-column-start: 1; /* 从第二列开始 */
  grid-row-start: 1; /* 从第二行开始 */
}

.Dressup2{
  width: 195px; /* 根据需要设置宽度 */
  height: 140px; /* 根据需要设置高度 */
  border: 2px solid #ccc; /* dashed设置虚线边框 */
  border-radius: 5px; /* 设置圆角 */
  background-color: #fff; /* 设置背景颜色 */
  padding: 16px; /* 设置内边距 */
  box-sizing: border-box; /* 确保内边距不会增加元素的总宽度和高度 */
  margin-top: 30px;  /*顶部外边距 */
  margin-right: 20px; /*右侧外边距 */
  margin-bottom: 0px; /*底部外边距 */
  margin-left: 6px;  /*左侧外边距 */
  position: absolute;
  grid-column-start: 2; /* 从第二列开始 */
  grid-row-start: 1; /* 从第二行开始 */
}

.Dressup3{
  width: 195px; /* 根据需要设置宽度 */
  height: 140px; /* 根据需要设置高度 */
  border: 2px solid #ccc; /* dashed设置虚线边框 */
  border-radius: 5px; /* 设置圆角 */
  background-color: #fff; /* 设置背景颜色 */
  padding: 16px; /* 设置内边距 */
  box-sizing: border-box; /* 确保内边距不会增加元素的总宽度和高度 */
  margin-top: 0px;  /*顶部外边距 */
  margin-right: 20px; /*右侧外边距 */
  margin-bottom: 0px; /*底部外边距 */
  margin-left: 6px;  /*左侧外边距 */
  position: absolute;
  grid-column-start: 1; /* 从第二列开始 */
  grid-row-start: 2; /* 从第二行开始 */
}

.Dressup4{
  width: 195px; /* 根据需要设置宽度 */
  height: 140px; /* 根据需要设置高度 */
  border: 2px solid #ccc; /* dashed设置虚线边框 */
  border-radius: 5px; /* 设置圆角 */
  background-color: #fff; /* 设置背景颜色 */
  padding: 16px; /* 设置内边距 */
  box-sizing: border-box; /* 确保内边距不会增加元素的总宽度和高度 */
  margin-top: 0px;  /*顶部外边距 */
  margin-right: 20px; /*右侧外边距 */
  margin-bottom: 0px; /*底部外边距 */
  margin-left: 6px;  /*左侧外边距 */
  position: absolute;
  grid-column-start: 2; /* 从第二列开始 */
  grid-row-start: 2; /* 从第二行开始 */
}

.look{
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  color: #000dff;
  position: absolute;
  top: 440px; 
  left: 400px; 
}

.Setting {
  height: 492px;
  width: 475px;
  position: absolute;
  top: 424px; 
  left: 1100px; 
  z-index: 1;
  background-color: #8C7BFD3b;
  opacity: 0.56; /* 设置透明度*/


  display: flex;
  flex-direction: column;
  align-items: center;
}



.Speechspeed {
  height: 48px;
  width: 411px;
  position: absolute;
  top: 34px; 
  left: 22px; 
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  color: #0921d8;
  opacity: 1;
  z-index: 3;
  background-color: rgba(140, 123, 253, 0.256); 
  
  padding: 0px 10px 0px 10px;/* 分别设置上、右、下、左方向的内边距 *//* 10px 20px 15px 10px 15px;分别设置上、右、下、左方向的内边距，中间留空 */
  
  display: flex; /* 启用Flexbox布局 */
  flex-direction: row; /* 子元素将横向排列 */
  justify-content: space-between; /* 子元素之间的间距 */
  align-items: center; /* 垂直居中对齐 */
}


.speed-label {
  /*font-weight: bold;*/
  /*color: #333;*/
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  color: #0921d8;
  margin-left: 10px;
  /*font-size: 15px; /* 设置元素文本的字体大小为24像素 */
}

.speed-select,
.speed-input[type="checkbox"] {
  margin-left: 10px;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 17px; /* 设置元素文本的字体大小为24像素 */
}

.speed-select option {
  color: #36363b;
  text-decoration: none;

  font-size: 10px;  /*设置元素文本的字体大小为24像素 */
}

.speed-select option:hover {
  text-decoration: underline;

  font-size: 10px;  /*设置元素文本的字体大小为24像素 */
}



.EnglishPronunciation {
  height: 48px;
  width: 411px;
  position: absolute;
  top: 105px; 
  left: 22px; 
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  color: #0921d8;
  opacity: 1;
  z-index: 3;
  background-color: rgba(140, 123, 253, 0.256); 
  padding: 0px 10px 0px 10px;/* 分别设置上、右、下、左方向的内边距 *//* 10px 20px 15px 10px 15px;分别设置上、右、下、左方向的内边距，中间留空 */
  
  display: flex; /* 启用Flexbox布局 */
  flex-direction: row; /* 子元素将横向排列 */
  justify-content: space-between; /* 子元素之间的间距 */
  align-items: center; /* 垂直居中对齐 */
}

.english-label {
  /*font-weight: bold;*/
  /*color: #333;*/
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  color: #0921d8;
  margin-left: 10px;
  /*font-size: 15px; /* 设置元素文本的字体大小为24像素 */
}

.english-select,
.english-input[type="checkbox"] {
  margin-left: 10px;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 17px; /* 设置元素文本的字体大小为24像素 */
}

.english-select option {
  color: #36363b;
  text-decoration: none;

  font-size: 10px;  /*设置元素文本的字体大小为24像素 */
}

.english-select option:hover {
  text-decoration: underline;

  font-size: 10px;  /*设置元素文本的字体大小为24像素 */
}



.ChinesePronunciation {
  height: 48px;
  width: 411px;
  position: absolute;
  top: 177px; 
  left: 22px; 
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  color: #0921d8;
  opacity: 1;
  z-index: 3;
  background-color: rgba(140, 123, 253, 0.256); 
  padding: 0px 10px 0px 10px;/* 分别设置上、右、下、左方向的内边距 *//* 10px 20px 15px 10px 15px;分别设置上、右、下、左方向的内边距，中间留空 */
  
  display: flex; /* 启用Flexbox布局 */
  flex-direction: row; /* 子元素将横向排列 */
  justify-content: space-between; /* 子元素之间的间距 */
  align-items: center; /* 垂直居中对齐 */
}

.chinese-label {
  /*font-weight: bold;*/
  /*color: #333;*/
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  color: #0921d8;
  margin-left: 10px;
  /*font-size: 15px; /* 设置元素文本的字体大小为24像素 */
}

.chinese-select,
.chinese-input[type="checkbox"] {
  margin-left: 10px;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 17px; /* 设置元素文本的字体大小为24像素 */
}

.chinese-select option {
  color: #36363b;
  text-decoration: none;

  font-size: 10px;  /*设置元素文本的字体大小为24像素 */
}

.chinese-select option:hover {
  text-decoration: underline;

  font-size: 10px;  /*设置元素文本的字体大小为24像素 */
}



.pronunciationMethod {
  height: 48px;
  width: 411px;
  position: absolute;
  top: 249px; 
  left: 22px; 
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  color: #0921d8;
  opacity: 1;
  z-index: 3;
  background-color: rgba(140, 123, 253, 0.256); 
  padding: 0px 10px 0px 10px;/* 分别设置上、右、下、左方向的内边距 *//* 10px 20px 15px 10px 15px;分别设置上、右、下、左方向的内边距，中间留空 */
  
  display: flex; /* 启用Flexbox布局 */
  flex-direction: row; /* 子元素将横向排列 */
  justify-content: space-between; /* 子元素之间的间距 */
  align-items: center; /* 垂直居中对齐 */
}

.method-label {
  /*font-weight: bold;*/
  /*color: #333;*/
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  color: #0921d8;
  margin-left: 10px;
  /*font-size: 15px; /* 设置元素文本的字体大小为24像素 */
}

.method-select,
.method-input[type="checkbox"] {
  margin-left: 10px;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 17px; /* 设置元素文本的字体大小为24像素 */
}

.method-select option {
  color: #36363b;
  text-decoration: none;

  font-size: 10px;  /*设置元素文本的字体大小为24像素 */
}

.method-select option:hover {
  text-decoration: underline;

  font-size: 10px;  /*设置元素文本的字体大小为24像素 */
}



.AutomaticPronunciation {
  height: 48px;
  width: 411px;
  position: absolute;
  top: 321px; 
  left: 22px; 
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  color: #0921d8;
  opacity: 1;
  z-index: 3;
  background-color: rgba(140, 123, 253, 0.256); 
  padding: 0px 10px 0px 10px;/* 分别设置上、右、下、左方向的内边距 *//* 10px 20px 15px 10px 15px;分别设置上、右、下、左方向的内边距，中间留空 */
  
  display: flex; /* 启用Flexbox布局 */
  flex-direction: row; /* 子元素将横向排列 */
  justify-content: space-between; /* 子元素之间的间距 */
  align-items: center; /* 垂直居中对齐 */
}

.automa-label {
  /* 设置标签的样式 */
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  color: #0921d8;
  margin-left: 10px; /* 与复选框之间的间距 */
}

.automa-input {
  width: 20px;
  height: 20px;
  /* 设置复选框的样式，可能需要额外的技巧来完全自定义样式 */
  margin: 0; /* 移除默认的外边距 */
}


.PrivacyManagement {
  height: 48px;
  width: 401px;
  position: absolute;
  top: 393px; 
  left: 22px; 
  font-size: 20px; /* 设置元素文本的字体大小为24像素 */
  color: #0921d8;
  opacity: 1;
  z-index: 3;
  background-color: rgba(140, 123, 253, 0.256); 
  padding: 0px 10px 0px 20px;/* 分别设置上、右、下、左方向的内边距 *//* 10px 20px 15px 10px 15px;分别设置上、右、下、左方向的内边距，中间留空 */
  
  display: flex; /* 启用Flexbox布局 */
  flex-direction: row; /* 子元素将横向排列 */
  justify-content: space-between; /* 子元素之间的间距 */
  align-items: center; /* 垂直居中对齐 */
}

.settingbutton{
  /*background-color: blue; /* 设置按钮的背景颜色为蓝色 */
  color: rgba(53, 63, 95, 0.695); /* 设置按钮文本的颜色为白色 */
  padding: 5px 10px; /* 设置按钮内部的填充，上下为10像素，左右为20像素 */
  border: none; /* 设置按钮没有边框 */
  border-radius: 5px; /* 设置按钮的边框圆角半径为5像素，使其边缘圆滑 */
  font-size: 15px;
  position: absolute; /* 绝对定位 */
  top: 65px; /* 距离包含块顶部0像素 */
  left: 1450px; /* 距离包含块左侧245像素 */
  z-index: 4; /* 堆叠顺序 */
}

.settings-page {
  position: relative;
  overflow: auto; /* 或者使用 scroll */
  transform: scale(0.8);
  width: 1920px; /* 定义容器宽度 */
  height: 1080px; /* 定义容器高度 */
  padding-top: 131px; /* 增加内边距以避免内容被覆盖 */
}


</style>
