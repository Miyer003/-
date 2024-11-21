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
              <div class="ai-dialogue">AI对话内容</div>
              <div class="ai-dialogue-box-buttons">
                <button>刷新</button>
                <button>复制</button>
              </div>
            </div>
            <!-- 用户对话框 -->
            <div class="user-dialogue-box">
              <div class="user-dialogue">用户对话内容</div>
            </div>
          </div>
          <div class="history">
            <div class="button-section">
              <!-- 新建对话和查看历史对话按钮 -->
              <button>新建对话</button>
              <button>查看历史对话</button>
            </div>
            <div class="user-input-section">
              <!-- 用户输入框 -->
              <textarea placeholder="用户输入内容"></textarea>
              <!-- 发送按钮 -->
              <button>发送</button>
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
              <div class="ai-answer">AI润色后回答内容</div>
              <div class="ai-answer-box-buttons">
                <button>刷新</button>
                <button>复制</button>
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
              <textarea placeholder="用户待润色文本"></textarea>
              <div class="user-input-section-bottom">
                <!-- 用户输入框内部的底侧左部显示文本检测 -->
                <span style="font-size: 10px">文本检测为英语</span>
                <!-- 用户输入框内部的底侧右部显示发送文本框按钮 -->
                <button style="border-color: #a58de7">发送文本</button>
              </div>
            </div>
          </div>

          <div class="button-section">
            <!-- 新建对话和查看历史对话按钮 -->
            <button>新建对话</button>
            <button>查看历史对话</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from "../components/Sidebar.vue";

export default {
  components: {
    Sidebar,
  },
  data() {
    return {
      // 用于存储信息检索部分用户输入的问题
      informationRetrievalQuestion: "",
      // 用于存储信息检索部分AI的回答
      informationRetrievalAnswer: "",
      // 用于存储自动润色部分用户输入的待润色文本
      autoPolishText: "",
      // 用于存储自动润色部分AI的润色回答
      autoPolishAnswer: "",
      // 用于存储文本语种检测结果
      detectedLanguage: "",
    };
  },
  methods: {
    // 信息检索部分发送问题的方法
    sendInformationRetrievalQuestion() {
      // 这里需要调用接口文档中的接口来发送问题并获取AI回答
      // 假设接口为sendQuestionToAI，参数为问题内容
      // 例如：this.$http.post('/api/sendQuestionToAI', { question: this.informationRetrievalQuestion }).then(response => {
      //   this.informationRetrievalAnswer = response.data.answer;
      // });
      // 实际接口地址和参数需要根据接口文档确定
    },
    // 信息检索部分AI回答对话框下刷新按钮的方法
    refreshInformationRetrievalAnswer() {
      // 这里可以根据需求重新获取AI回答，可能需要再次调用接口
      // 具体实现取决于接口文档中的接口定义
    },
    // 信息检索部分AI回答对话框下复制按钮的方法
    copyInformationRetrievalAnswer() {
      // 实现复制AI回答到剪贴板的功能
      const textarea = document.createElement("textarea");
      textarea.value = this.informationRetrievalAnswer;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      document.body.removeChild(textarea);
    },
    // 自动润色部分发送待润色文本的方法
    sendAutoPolishText() {
      // 调用接口检测文本语种并显示
      // 假设接口为detectLanguage，参数为文本内容
      // 例如：this.$http.post('/api/detectLanguage', { text: this.autoPolishText }).then(response => {
      //   this.detectedLanguage = response.data.language;
      // });
      // 然后调用接口获取AI的润色回答
      // 假设接口为sendTextForAutoPolish，参数为待润色文本
      // 例如：this.$http.post('/api/sendTextForAutoPolish', { text: this.autoPolishText }).then(response => {
      //   this.autoPolishAnswer = response.data.answer;
      // });
      // 实际接口地址和参数需要根据接口文档确定
    },
    // 自动润色部分AI润色回答对话框下刷新按钮的方法
    refreshAutoPolishAnswer() {
      // 类似信息检索部分的刷新逻辑，根据接口文档重新获取润色回答
    },
    // 自动润色部分AI润色回答对话框下复制按钮的方法
    copyAutoPolishAnswer() {
      // 类似信息检索部分的复制逻辑，将润色回答复制到剪贴板
    },
    // 信息检索部分新建对话的方法（刷新页面）
    newInformationRetrievalDialog() {
      location.reload();
    },
    // 信息检索部分查看历史对话的方法（需根据实际情况实现）
    viewInformationRetrievalHistory() {
      // 这里需要根据接口文档获取历史对话数据并展示，可能涉及到与后端的交互
    },
    // 自动润色部分新建对话的方法（刷新页面）
    newAutoPolishDialog() {
      location.reload();
    },
    // 自动润色部分查看历史对话的方法（需根据实际情况实现）
    viewAutoPolishHistory() {
      // 这里需要根据接口文档获取历史润色文本数据并展示，可能涉及到与后端的交互
    },
  },
};
</script>

<style scoped>
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
.user-dialogue-box,
textarea {
  border: 1px solid #ccc;
  padding: 10px;
  width: 35%;
  height: 60%;
}
textarea {
  width: 80%;
  border-radius: 10px;
  border: none;
}

.ai-dialogue-box,
.ai-answer-box {
  background-color: #f9f9f9;
  margin-right: 50px;
  box-shadow: 0 0 5px rgba(108, 66, 225, 0.7);
  border-radius: 10px;
}
.user-dialogue-box {
  background-color: #f9f9f9;
  box-shadow: 0 0 5px rgba(108, 66, 225, 0.7);
  border-radius: 10px;
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
</style>
