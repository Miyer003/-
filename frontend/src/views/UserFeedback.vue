<template>
  <div>
    <!-- 侧边栏容器 -->
    <Sidebar @navigate="handleSidebarNavigation" />
    <div class="content">
      <div class="fd">
          <!-- 左侧区域：质量反馈、功能反馈 -->
        <div class="left-wall">
          <!-- 质量反馈容器 -->
          <div class="quality-feedback">
            <h2 class="container-title">质量反馈</h2>
            <div class="feedback-options">
              <label v-for="option in qualityOptions" :key="option">
                <input type="checkbox" :value="option" v-model="selectedOptions" />
                <span>{{ option }}</span>
              </label>
            </div>

            <div class="other-feedback">
              <input type="text" placeholder="其他问题" v-model="otherFeedback" />
            </div>

            <button @click="submitFeedback" class="submit-button">提交反馈</button>
            <FeedbackPopup ref="feedbackPopup" />
          </div>

          <!-- 功能建议反馈容器 -->
          <div class="function-suggestion">
            <h2 class="container-title">功能建议反馈</h2>
            <textarea placeholder="请输入您的功能建议" v-model="functionSuggestion" class="fucsuggest"></textarea>
            <button @click="submitSuggestion" class="submit-button">提交建议</button>
          </div>
        </div>

        
        <!-- 右侧区域：在线客服 -->
        <div class="right-wall">
          <!-- 在线客服容器 -->
          <div class="live-chat">
            <h2 class="container-title">在线客服</h2>
            <hr class="separator"> <!-- 添加分隔线 -->
            <div class="chat-history">
              <div v-for="message in chatHistory" :key="message.id">
                <div class="message-container" :class="{ mine: message.type === 'user' }">
                  <img v-if="message.type !== 'user'" src="../assets/云译网.png" alt="Agent Avatar" class="avatar">
                  <div class="message-content">{{ message.text }}</div>
                </div>
              </div>
            </div>
            <div class="message-input">
              <!-- 文件选择图标 -->
              <label class="file-icon">
                <input type="file" style="display:none;" @change="handleFileChange">
                <img src="../assets/add.png" alt="File Icon" class="icon">
              </label>
              <!-- 输入框 -->
              <input type="text" placeholder="请输入文字" v-model="userMessage">
              <!-- 发送按钮 -->
              <button @click="sendMessage" class="send-button">发送</button>
            </div>
          </div>
        </div>
        
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue'; // 导入 Sidebar 组件
import FeedbackPopup from '../components/FeedbackPopup.vue';

export default {
  name: 'UserFeedback',
  components: {
    Sidebar,FeedbackPopup
  },
  data() {
    return {
      selectedOptions: [],
      otherFeedback: '',
      functionSuggestion: '',
      chatHistory: [
        { id: 0, type: 'system', text: '欢迎您使用我们的服务！' }
      ],
      userMessage: ''
    };
  },
  methods: {
    submitFeedback() {
      console.log('提交反馈：', this.selectedOptions, this.otherFeedback);
      // 在这里调用后端 API 发送反馈
      this.$refs.feedbackPopup.show();
    },
    submitSuggestion() {
      console.log('提交功能建议：', this.functionSuggestion);
      // 在这里调用后端 API 发送功能建议
      this.$refs.feedbackPopup.show();
    },
    sendMessage() {
      const newMessage = {
        id: this.chatHistory.length,
        type: 'user',
        text: this.userMessage
      };
      this.chatHistory.push(newMessage);
      this.userMessage = '';
      // 在这里调用后端 API 发送在线客服消息
    },
    handleSidebarNavigation(page) {
      // 根据页面导航的不同需要改变代码逻辑
      console.log('Navigating to', page);
    },
    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        // 处理文件选择后的逻辑
      }
    }
  },
  computed: {
    qualityOptions() {
      return ['翻译结果存在错误', '页面设计不够清晰', '页面加载速度较慢', '其他'];
    }
  }
};

</script>

<style scoped>

.content {
      margin-top: 70px;
      margin-left: 220px; 
      padding: 15px;
      
}

.fd{
      display: flex;
      justify-content: space-between;
      height: max-content;
      position: relative; /* 确保子元素可以相对定位 */
}

.left-wall {
  /* 修改了宽度，这里需要根据内容调整 */
  width: 55%;  /* 调整宽度以适配你的布局 */
  
}

.right-wall {
  /* 修改了宽度，这里需要根据内容调整 */
  width: 40%; /* 调整宽度以适配你的布局 */
}

/*这是左侧反馈区 */
.quality-feedback {
  width: 100%;
  border: 1px solid #ccc; /* 边框 */
  border-radius: 16px; /* 圆角 */
  box-shadow: 0 4px 8px rgba(102, 51, 153, 0.3); /* 添加阴影 */
  padding: 16px; /* 内边距 */
}

.function-suggestion{
  width: 100%;
  height: 45%;
  border: 1px solid #ccc; /* 边框 */
  border-radius: 16px; /* 圆角 */
  box-shadow: 0 4px 8px rgba(102, 51, 153, 0.3); /* 添加阴影 */
  padding: 16px; /* 内边距 */
  margin: 20px 0; /* 添加间距 */
}

.feedback-options {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.fucsuggest{
      border: 1px solid #dfe1e5;
      outline: none;
      width: 90%; /* 宽度占父容器的100% */
      height: 130px; /* 固定高度 */
      border-radius: 20px;
      margin: 5px 0; /* 添加间距 */
      box-shadow: 0 4px 8px rgba(102, 51, 153, 0.3); /* 添加阴影 */
      resize: vertical; /* 允许用户调整高度 */
      padding: 20px; /* 内边距 */
     
}

.submit-button {
  background-color: #007bff; /* 调整颜色为蓝色 */
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 24px;
  font-size: 14px;
  margin-top: 24px;
  cursor: pointer;
}



/*这是在线客服的部分 */

.live-chat {
  border: 1px solid #ccc; /* 边框 */
  border-radius: 16px; /* 圆角 */
  box-shadow: 0 4px 8px rgba(102, 51, 153, 0.3); /* 添加阴影 */
  padding: 10px;
  height: 95%; /* 调整高度为100% */
  display: flex; /* 使用 Flexbox 布局 */
  flex-direction: column; /* 垂直排列 */
}

.separator {
  border: none; /* 去掉默认边框 */
  border-top: 1px solid #ccc; /* 添加分隔线 */
  margin: 10px 10px; /* 增加分隔线与内容之间的间距 */
}

.chat-history {
  flex: 1; /* 让聊天历史区域占据除了输入框之外的所有剩余空间 */
  overflow-y: auto; /* 添加滚动条 */
  padding-right: 10px; /* 留出头像的空间 */
}

.message-container {
  display: flex; /* 使用 Flexbox 布局 */
  align-items: flex-start; /* 内容顶部对齐 */
  margin-bottom: 10px; /* 消息之间的间距 */
}

.message-container.mine {
  flex-direction: row-reverse; /* 用户消息反转布局方向 */
}

.message-content {
  border-radius: 16px; /* 消息圆角 */
  padding: 8px;
  max-width: calc(100% - 40px); /* 消息框的最大宽度，留出头像空间 */
  word-wrap: break-word; /* 自动换行 */
  margin-left: 10px; /* 留出头像的空间 */
}

.message-container:not(.mine) .message-content {
  background-color: #f1f1f1; /* 客服消息背景色 */
  color: #333; /* 客服消息颜色 */
}

.message-container.mine .message-content {
  background-color: #8e44ad; /* 用户消息背景色 */
  color: #fff; /* 用户消息颜色 */
}

.avatar {
  width: 32px; /* 头像宽度 */
  height: 32px; /* 头像高度 */
  border-radius: 50%; /* 头像圆形 */
}

.message-input {
  display: flex; /* 使用 Flexbox 布局 */
  margin-top: 10px; /* 输入框与聊天历史之间的间距 */
  background-image: linear-gradient(to bottom, rgba(113, 47, 199, 0), rgb(83, 62, 205));
  padding: 4px;
  border-radius: 20px;
  margin-left: 20px;
  margin-right: 20px;
  margin-bottom: 20px;
}

.message-input input {
  flex: 1; /* 让输入框占据剩余空间 */
  outline: none;
  border: none;
  padding: 6px;
  border-radius: 6px;
  margin-right: 6px; /* 输入框与按钮之间的间距 */
}

.message-input button {
  background-image: linear-gradient(to bottom, rgba(113, 47, 199, 0), rgb(83, 62, 205));
  color: #fff; /* 按钮文字颜色 */
  border: none;
  padding: 6px 12px;
  border-radius: 10px;
}

.file-icon {
  margin-right: 10px; /* 图标与输入框之间的间距 */
  cursor: pointer; /* 鼠标悬停时变成手型 */
}

.file-icon .icon {
  width: 24px; /* 图标宽度 */
  height: 24px; /* 图标高度 */
}
</style>