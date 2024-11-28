<template>
  <div>
    <!-- 侧边栏容器 -->
    <Sidebar @navigate="handleSidebarNavigation" />
    <!-- 这里添加AI Chat相关的内容 -->
    <div class="main-content">
      <div class="ai-sections-container">
        <div class="information-retrieval">
          <div class="info-retrieval-header">
            <h4>信息检索</h4>
          </div>
          <div class="ai-dialogue-section">
            <!-- AI头像 -->
            <img src="@/assets/ai-avatar.png" alt="AI头像" class="ai-avatar" />
            <!-- AI对话框 -->
            <div class="ai-dialogue-box">
              <div class="ai-dialogue">
                <div class="ai-messages-container">
                  <div
                    v-for="(message, index) in aiChatMessages"
                    :key="index"
                    class="ai-message"
                  >
                    <div class="message-content">{{ message.content }}</div>
                  </div>
                </div>
              </div>
              <div class="ai-dialogue-box-buttons">
                <button @click="refreshInfoRetrievalAnswer">刷新</button>
                <button
                  @click="copyInformationRetrievalAnswer"
                  id="copyInfoRetrievalAnswer"
                >
                  复制
                </button>
              </div>
            </div>
            <!-- 用户对话框 -->
            <div class="user-dialogue-box">
              <div class="user-dialogue">
                <div class="user-messages-container">
                  <div
                    v-for="(message, index) in userChatMessages"
                    :key="index"
                    class="user-message"
                  >
                    <div class="message-content">{{ message.content }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="history">
            <div class="button-section">
              <!-- 新建对话和查看历史对话按钮 -->
              <button @click="newInformationRetrievalDialog">新建对话</button>
              <button @click="viewHistory">查看历史对话</button>
            </div>
            <div class="user-input-section">
              <div class="chat-input">
                <textarea
                  v-model="userInput"
                  :disabled="isLoading"
                  placeholder="请输入问题"
                  @keyup.enter="sendQuestion"
                ></textarea>
                <button @click="sendQuestion" :disabled="isLoading">
                  {{ isLoading ? "发送中..." : "发送" }}
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="auto-polish">
          <div class="info-retrieval-header">
            <h4>自动润色</h4>
          </div>
          <div class="auto-polish-section">
            <!-- AI头像 -->
            <img src="@/assets/ai-avatar.png" alt="AI头像" class="ai-avatar" />
            <!-- AI翻译并润色后的回答框 -->
            <div class="ai-answer-box">
              <div class="ai-answer">
                <div
                  v-for="(message, index) in chatMessagesList"
                  :key="index"
                  :class="
                    message.type === 'user' ? 'user-message' : 'ai-message'
                  "
                >
                  <div class="message-content">{{ message.content }}</div>
                </div>
              </div>
              <div class="ai-answer-box-buttons">
                <button @click="refreshAutoPolishAns">刷新</button>
                <button @click="copyAutoPolishAnswer" id="copyAutoPolishAnswer">
                  复制
                </button>
              </div>
            </div>
            <!-- 用户的待润色文本输入框 -->
            <div
              class="user-input-section"
              style="
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
              "
            >
              <div class="chat-input">
                <textarea
                  v-model="userInputForAutoPolish"
                  placeholder="用户待润色文本"
                  @keyup.enter="sendAutoPolishText"
                ></textarea>
              </div>

              <div class="user-input-section-bottom">
                <!-- 用户输入框内部的底侧左部显示文本检测 -->
                <span style="font-size: 10px"
                  >文本检测为{{ sourceDetectedLanguage }}</span
                >
                <!-- 用户输入框内部的底侧右部显示发送文本框按钮 -->
                <button
                  @click="sendAutoPolishText"
                  :disabled="isPolishing"
                  style="border-color: #a58de7"
                >
                  {{ isPolishing ? "处理中..." : "发送文本" }}
                </button>
              </div>
            </div>
          </div>

          <div class="button-section">
            <!-- 新建对话和查看历史对话按钮 -->
            <button @click="newAutoPolishDialog">新建对话</button>
            <button @click="viewAutoPolishHistory">查看历史对话</button>
          </div>
        </div>
      </div>
    </div>
    <!-- 可以添加错误提示显示 -->
    <div v-if="autoPolishError" class="error-message">
      {{ autoPolishError }}
    </div>
    <!-- 在信息检索部分添加错误提示 -->
    <div v-if="retrievalError" class="error-message">
      {{ retrievalError }}
    </div>
  </div>
</template>

<script>
import Sidebar from "../components/Sidebar.vue";
import { api, sendQuestionToAI } from "../api/chatApi.js";
import { getChatHistory } from "../api/chatApi.js";
import { getAutoPolishChatHistory } from "../api/chatApi.js";
import { sendTextToWenxinForAutoPolish } from "../api/chatApi.js";
import axios from "axios";

export default {
  components: {
    Sidebar,
  },
  data() {
    return {
      // 用于存储信息检索部分用输入的问题
      informationRetrievalQuestion: "",
      // 用于存储信息检索部分AI的回答
      informationRetrievalAnswer: "",
      // 用于存储自动润色部分用户输入的待润色文本
      autoPolishText: "",
      // 用于存储自动润色部分AI的润色回答
      autoPolishAnswer: "",
      // 用于存储文本语种检测结果
      detectedLanguage: "",
      // 当前用户ID，假设已经获取并存储在这里
      currentUserId: 123,
      sourceDetectedLanguage: "",
      userInput: "",
      userInputForAutoPolish: "",
      userChatMessages: [],
      aiChatMessages: [],
      chatMessagesList: [],
      isLoading: false,
      isPolishing: false, // 添加自动润色的加载状态
      autoPolishError: null, // 添加错误状态
      retrievalError: null, // 添加信息检索的错误状态
    };
  },
  methods: {
    async sendQuestion() {
      if (this.isLoading) return;
      this.isLoading = true;

      try {
        if (this.userInput.trim() !== "") {
          // 添加用户消息到显示
          const userMessage = {
            type: "user",
            content: this.userInput,
          };
          this.userChatMessages.push(userMessage);

          // 保存当前输入
          const currentInput = this.userInput;
          // 清空输入框
          this.userInput = "";

          // 发送请求到后端
          const response = await api.post("/ai/dialogue", {
            user_id: this.currentUserId,
            input_text: currentInput,
          });

          // 检查响应
          if (response.data) {
            // 添加 AI 回复到显示
            const aiMessage = {
              type: "ai",
              content: response.data.answer || response.data.message,
            };
            this.aiChatMessages.push(aiMessage);
          } else {
            throw new Error("返回数据为空");
          }
        }
      } catch (error) {
        console.error("发送问题时发生错误:", error);

        // 显示错误消息
        const errorMessage = {
          type: "error",
          content: "发送问题失败，请稍后重试",
        };
        this.aiChatMessages.push(errorMessage);

        // 恢复输入内容
        if (!this.userInput) {
          this.userInput = currentInput;
        }
      } finally {
        this.isLoading = false;
      }
    },

    async checkConnection() {
      try {
        await api.get("/health-check", {
          timeout: 5000,
          retry: 1,
        });
        return true;
      } catch (error) {
        console.error("连接检查失败:", error);
        return false;
      }
    },

    // 修改自动润色发送方法
    async sendAutoPolishText() {
      if (this.isPolishing) return;
      this.isPolishing = true;
      this.autoPolishError = null;

      try {
        console.log("准备发送润色文本:", this.userInputForAutoPolish); // 调试日志

        if (!this.userInputForAutoPolish.trim()) {
          throw new Error("请输入需要润色的文本");
        }

        // 添加用户消息到显示
        const userMessage = {
          type: "user",
          content: this.userInputForAutoPolish,
        };
        this.chatMessagesList.push(userMessage);

        // 发送语言检测请求
        console.log("发送语言检测请求"); // 调试日志
        const detectResponse = await api.post("/api/detectLanguage", {
          text: this.userInputForAutoPolish,
        });

        console.log("语言检测响应:", detectResponse.data); // 调试日志

        if (detectResponse.data) {
          this.sourceDetectedLanguage =
            detectResponse.data.language === "zh" ? "中文" : "英文";

          // 发送润色请求
          console.log("发送润色请求"); // 调试日志
          const polishResponse = await api.post("/api/translate/polish", {
            text: this.userInputForAutoPolish,
            target: detectResponse.data.language === "en" ? "zh" : "en",
          });

          console.log("润色响应:", polishResponse.data); // 调试日志

          if (polishResponse.data && polishResponse.data.translation) {
            const aiMessage = {
              type: "ai",
              content: polishResponse.data.translation,
            };
            this.chatMessagesList.push(aiMessage);
            this.userInputForAutoPolish = ""; // 清空输入
          } else {
            throw new Error("润色服务返回数据格式错误");
          }
        }
      } catch (error) {
        console.error("自动润色过程发生错误:", error);
        console.error("错误详情:", {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status,
        });

        this.autoPolishError =
          error.response?.data?.message ||
          error.message ||
          "润色失败，请稍后重试";
        alert(this.autoPolishError);
      } finally {
        this.isPolishing = false;
        console.log("润色请求处理完成"); // 调试日志
      }
    },

    // 修改刷新润色答案的方法
    async refreshAutoPolishAns() {
      if (this.isPolishing) return;
      this.isPolishing = true;
      this.autoPolishError = null;

      try {
        if (!this.userInputForAutoPolish.trim()) {
          throw new Error("没有可以重新润色的文本");
        }

        // 清空当前消息列表
        this.chatMessagesList = [];

        // 重新添加用户消息
        const userMessage = {
          type: "user",
          content: this.userInputForAutoPolish,
        };
        this.chatMessagesList.push(userMessage);

        // 重新发送润色请求
        const response = await api.post("/api/translate/polish", {
          text: this.userInputForAutoPolish,
          target: this.sourceDetectedLanguage === "中文" ? "en" : "zh",
        });

        if (response.data && response.data.translation) {
          const aiMessage = {
            type: "ai",
            content: response.data.translation,
          };
          this.chatMessagesList.push(aiMessage);
        } else {
          throw new Error("刷新润色返回数据格式错误");
        }
      } catch (error) {
        console.error("刷新润色时发生错误:", error);
        this.autoPolishError = error.message || "刷新失败，请稍后重试";
        alert(this.autoPolishError);
      } finally {
        this.isPolishing = false;
      }
    },

    // 修改新建润色对话的方法
    newAutoPolishDialog() {
      try {
        if (this.isPolishing) {
          alert("请等待当前润色完成");
          return;
        }

        if (confirm("确定要新建自动润色对话吗？此操作将清空当前润色内容。")) {
          this.userInputForAutoPolish = "";
          this.chatMessagesList = [];
          this.sourceDetectedLanguage = "";
          this.autoPolishError = null;
        }
      } catch (error) {
        console.error("新建对话时发生错误:", error);
        alert("新建对话失败：" + error.message);
      }
    },
  },
};
</script>

<style scoped>
.ai-chat-component {
  width: 100%;
  display: flex;
  flex-direction: column;
  height: 100%;
}
.chat-header {
  margin-bottom: 10px;
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
  display: flex;
  flex-direction: column;
}
.message-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
}
.user-message {
  background-color: #e4dfed;
  border-radius: 5px;
  padding: 2px 2px;
  max-width: 70%;
  word-break: break-word;
  margin-bottom: 10px;
}
.ai-message {
  background-color: #d4edda;
  border-radius: 5px;
  padding: 2px 2px;
  max-width: 70%;
  word-break: break-word;
  margin-bottom: 10px;
}
.chat-input {
  display: flex;
  margin-top: 10px;
}
.chat-input textarea {
  flex: 1;
  border: none;
  border-radius: 5px;
  padding: 5px;
  height: 12px;
  width: 1;
}
.chat-input button {
  margin-left: 10px;
  padding: 5px 10px;
  border: none;
  background-color: #8352ae;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}
.chat-footer {
  margin-top: 10px;
}
.message-content {
  word-break: break-all;
}
.main-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-left: 220px;
  padding: 10px;
  justify-content: flex-start;
  width: calc(100%-220px);
  min-height: calc(100vh-60px);
  height: 700px;
}
.ai-sections-container {
  display: flex;
  gap: 15px;
  flex: 1;
  height: 90%;
}
.information-retrieval,
.auto-polish {
  width: 50%;
  margin-bottom: 20px;
  margin-top: 60px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  border: 1px solid #ccc;
  min-height: 100%;
}
.info-retrieval-header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 10px;
  margin-left: 15px;
}
.ai-dialogue,
.ai-answer {
  height: 88%;
}
.user-dialogue {
}
.ai-dialogue-section,
.auto-polish-section {
  display: flex;
  align-items: flex-start;
  height: 75%;
  margin-bottom: 20px;
}
.ai-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 10px;
  margin-left: 15px;
}
.ai-dialogue-box,
.ai-answer-box,
.user-dialogue-box {
  border: 1px solid #ccc;
  padding: 10px;
  width: 35%;
  height: 400px; /* 固定高度 */
  display: flex;
  flex-direction: column;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(108, 66, 225, 0.7);
}
.ai-dialogue,
.user-dialogue {
  flex: 1;
  overflow-y: auto; /* 启用垂直滚动 */
  margin-bottom: 10px;
}
.ai-messages-container,
.user-messages-container {
  padding: 10px;
}
.ai-message,
.user-message {
  margin-bottom: 10px;
  word-wrap: break-word; /* 确保长文本会换行 */
}
.message-content {
  background-color: #f5f5f5;
  padding: 8px 12px;
  border-radius: 8px;
  max-width: 100%; /* 确保内容不会超出容器 */
  word-break: break-word; /* 处理长单词换行 */
}
.ai-dialogue-box,
.ai-answer-box {
  background-color: #f9f9f9;
  margin-right: 50px;
  box-shadow: 0 0 5px rgba(108, 66, 225, 0.7);
  border-radius: 10px;
  display: flex;
  flex-direction: column;
}
.ai-dialogue-box-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 10px;
  border-top: 1px solid #eee;
}
.ai-dialogue-box-buttons button {
  padding: 5px 15px;
  border-radius: 5px;
  border: 1px solid #a58de7;
  background-color: white;
  cursor: pointer;
  transition: background-color 0.2s;
}
.ai-dialogue-box-buttons button:hover {
  background-color: #f0f0f0;
}
/* 自定义滚动条样式 */
.ai-dialogue::-webkit-scrollbar,
.user-dialogue::-webkit-scrollbar {
  width: 6px;
}
.ai-dialogue::-webkit-scrollbar-track,
.user-dialogue::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}
.ai-dialogue::-webkit-scrollbar-thumb,
.user-dialogue::-webkit-scrollbar-thumb {
  background: #a58de7;
  border-radius: 3px;
}
.ai-dialogue::-webkit-scrollbar-thumb:hover,
.user-dialogue::-webkit-scrollbar-thumb:hover {
  background: #8b6cd4;
}
.button-section button {
  margin-right: 10px;
  border-color: #a58de7;
  border-radius: 10px;
}
.button-section {
  margin-bottom: 10px;
}
.user-input-section {
  display: flex;
  align-items: center;
  margin-left: 20px;
  box-shadow: 0 0 5px rgba(108, 66, 225, 0.7);

  border-radius: 10px;
  margin-right: 20px;
}
.user-input-section button {
  margin-left: 10px;
  border-color: #a58de7;
  border-radius: 10px;
}
.user-input-section-bottom {
  margin-bottom: 10px;
}
.ai-dialogue-box-buttons,
.ai-answer-box-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 15px;
}
.ai-dialogue-box-buttons button,
.ai-answer-box-buttons button {
  margin-left: 10px;

  border-radius: 10px;
  border-color: #a58de7;
}
.error-message {
  color: #ff4444;
  font-size: 14px;
  margin-top: 8px;
  padding: 8px;
  background-color: #ffebee;
  border-radius: 4px;
}
</style>
