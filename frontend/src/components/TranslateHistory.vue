<template>
  <div class="chat-container" @click="navigateToAiChat">
    <!-- 顶部标题 -->
    <h2 class="chat-title">
      <i class="fas fa-hand-point-right click-icon" aria-hidden="true"></i>
      AI对话
      <!-- 点击图标 -->
    </h2>

    <!-- 聊天内容 -->
    <div class="chat-messages">
      <!-- 左侧消息气泡 -->
      <div class="message left">
        <i class="fas fa-robot avatar" aria-hidden="true"></i> <!-- AI头像图标 -->
        <div class="bubble">AI助手已检测到wilderness，请问您需要我提供哪些相关内容？</div>
      </div>

      <!-- 右侧消息气泡（用户消息） -->
      <div class="message right">
        <div class="bubble">描绘天空之境</div>
        <i class="fas fa-dog avatar" aria-hidden="true"></i> <!-- 用户头像图标 -->
      </div>

      <!-- 再次显示左侧消息 -->
      <div class="message left">
        <i class="fas fa-robot avatar" aria-hidden="true"></i> <!-- AI头像图标 -->
        <div class="bubble large">很高兴为您服务，我将针对...</div>
      </div>
    
    <!-- 右侧消息气泡（用户消息） -->
    <div class="message right">
        <div class="bubble large">...........................................</div>
        <i class="fas fa-dog avatar" aria-hidden="true"></i> <!-- 用户头像图标 -->
      </div>
    </div>
    <!-- 输入框和发送按钮 -->
    <div class="input-container">
      <input
        type="text"
        placeholder="请输入内容（按Shift+Enter发送）"
        class="message-input"
      />
      <button class="send-button">
        <i class="fas fa-paper-plane" aria-hidden="true"></i> <!-- 发送图标 -->
      </button>
    </div>

    <!-- 扩大图标 -->
    <i class="fas fa-expand-arrows-alt expand-icon" aria-hidden="true"></i>
  </div>
</template>
<script>
export default {
  name: "AiChatEntry",
  methods: {
    navigateToAiChat() {
      this.$router.push({ name: "ai-chat" }); // 跳转到AI对话页面
    }
  }
};
</script>
<style scoped>

/* 容器样式 */
.chat-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  border: 1px solid rgb(179, 113, 202); /* 设置紫色边框 */
  box-shadow: 0px 6px 12px rgba(179, 113, 202, 0.1); /* 保持紫色阴影，透明度调整为0.1 */
  cursor: pointer;
  transition: background-color 0.3s ease;
  position: relative; /* 为扩大图标添加定位 */
}
/* 标题样式 */
.chat-title {
  font-size: 16px;
  color: #333;
  display: flex;
  align-items: center;
  gap: 5px; /* 设置图标和文字之间的间隙为5px */
  margin-top: 0;
  margin-bottom: 5px;
}

/* 点击图标样式 */
.click-icon {
  color:rgb(179, 113, 202); /* 图标颜色 */
  font-size: 16px; /* 图标大小 */
}

/* 扩大图标样式 */
.expand-icon {
  position: absolute;
  top: 20px; /* 根据需要调整位置 */
  right: 20px; /* 根据需要调整位置 */
  color: rgb(232, 231, 232); /* 图标颜色 */
  font-size: 28px; /* 图标大小 */
  cursor: pointer; /* 鼠标悬停时显示点击效果 */
}

/* 聊天内容区域样式 */
.chat-messages {
  max-height: 500px;
  overflow-y: auto;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

/* 消息块样式 */
.message {
  display: flex;
  align-items: flex-start;
  width: 100%;
}

/* 左侧消息 */
.message.left {
  justify-content: flex-start;
}

/* 右侧消息 */
.message.right {
  justify-content: flex-end;
}

/* 头像样式 */
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin: 8px;
  color: rgb(179, 113, 202); /* 头像颜色 */
  text-align: center;
  line-height: 30px; /* 使图标垂直居中 */
  font-size: 26px; /* 调整图标大小 */
}

/* 气泡框样式 */
.bubble {
  max-width: 60%;
  padding: 18px 15px;
  border-radius: 20px;
  background-color: #c0aaff;
  color: #fff;
  font-size: 14px;
  line-height: 1.0;
  position: relative;
}

/* 气泡颜色和位置 */
.message.left .bubble {
  background-color: #c0aaff;
}

.message.right .bubble {
  background-color: #f9a8d4;
}

.bubble.large {
  max-width: 60%;
  padding: 18px 15px;
  border-radius: 20px;
  background-color: #c0aaff;
  color: #fff;
  font-size: 14px;
  line-height: 1.0;
  position: relative;
}

/* 输入区域样式 */
.input-container {
  display: flex;
  align-items: center;
  margin-top: 25px;
  background: linear-gradient(to right, #f9a8d4, #c0aaff);
  border-radius: 30px;
  padding: 6px;
  margin-bottom: 10px; /* 设置与组件下部边框的距离 */
}

/* 输入框样式 */
.message-input {
  flex: 1;
  border: none;
  outline: none;
  padding: 5px;
  font-size: 12px;
  color: #333;
  background-color: transparent;
  
}

/* 发送按钮样式 */
.send-button {
  border: none;
  background-color: transparent;
  cursor: pointer;
  padding: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px; /* 调整图标大小 */
  color: #4a90e2; /* 发送按钮颜色 */
}

/* 聊天容器hover效果 */
.chat-container:hover {
  background-color: #f9f9f9;
}
</style>