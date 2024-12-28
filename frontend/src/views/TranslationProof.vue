<template>
  <div>
    <!-- 侧边栏容器 -->
    <Sidebar @navigate="handleSidebarNavigation" />
    <div class="content">
      <div class="su-input-container">
        <div class="su-input">
          <p>翻译校对</p>
          <div class="su-input-1">
            <textarea v-model="sourceText" @input="detectSourceLanguage" placeholder="请输入原文" class="source-text"></textarea>
            <div class="language-indicator">检测为: {{ sourceDetectedLanguage }}</div>
            <div class="speak-button" @click="speakSourceText">🔊</div>
          </div>

          <div class="su-input-1">
            <textarea v-model="userText" @input="detectUserLanguage" placeholder="请输入译文" class="user-text"></textarea>
            <div class="language-indicator">检测为: {{ userDetectedLanguage }}</div>
            <div class="speak-button" @click="speakUserText">🔊</div>
          </div>

        <div style="display: flex;">
          <button @click="checkTranslation">点击校验</button>
          <button style="margin-left: 20px;" @click="seeHistory">查看历史记录</button>
        </div>
          
        </div>

        <div class="total-output">
          <div class="translation-score">
            <span class="score-label">翻译打分：</span>
            <span class="score-value">{{ score }}</span>
            <div class="rating-stars">
              <i v-for="(star, index) in stars" :key="index" :class="['fas', 'fa-star', { 'filled': index < filledStars }]"></i>
            </div>
          </div>

          <div class="output-container">
            <div class="output-header">
              <button class="output-toggle" @click="toggleContent('grammar')">语法检查</button>
              <button class="output-toggle" @click="toggleContent('terminology')">术语校验</button>
              <button class="output-toggle" @click="toggleContent('consistency')">内容一致性</button>
              <button class="output-toggle" @click="toggleContent('style')">语言风格一致性</button>
              <button class="output-toggle" @click="toggleContent('optimization')">句式优化</button>
            </div>
            <hr style="border-top: 1px solid #ccc; margin: 10px 10;">
            <div class="output-content" v-if="contentToShow">
              <div v-if="contentToShow === 'grammar'">{{ grammarResult }}</div>
              <div v-if="contentToShow === 'terminology'">{{ terminologyResult }}</div>
              <div v-if="contentToShow === 'consistency'">{{ consistencyResult }}</div>
              <div v-if="contentToShow === 'style'">{{ styleResult }}</div>
              <div v-if="contentToShow === 'optimization'">{{ optimizationResult }}</div>
            </div>
          </div>
        </div>

        <!-- 历史记录面板 -->
      <div class="history-panel" v-if="isHistoryPanelVisible">
            <div class="history-header">
              <button @click="isHistoryPanelVisible = false">关闭</button>
              历史记录
            </div>
            <ul class="history-list">
              <li v-for="record in historyRecords" :key="record.id" @click="handleHistoryItemClick(record)">
                {{ record.originalText }}
              </li>
            </ul>
          </div>

      </div>
  </div>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue';
import { franc } from 'franc';

export default {
  name: 'tproof',
  components: {
    Sidebar,
  },
  data() {
    return {
      userId: this.$store.state.user_id, // 从 Vuex 中获取 user_id,
      sourceText: '',
      userText: '',
      sourceDetectedLanguage: '',
      userDetectedLanguage: '',
      grammarResult: '请点击检测',
      terminologyResult: '请点击检测',
      consistencyResult: '请点击检测',
      styleResult: '请点击检测',
      optimizationResult: '请点击检测',
      contentToShow: 'grammar',
      score: 0,
      stars: 5,
      filledStars: 0,
      historyRecords: [],
      isHistoryPanelVisible: false,
    };
  },
  methods: {
    detectSourceLanguage() {
      this.sourceDetectedLanguage = this.detectLanguage(this.sourceText);
    },
    detectUserLanguage() {
      this.userDetectedLanguage = this.detectLanguage(this.userText);
    },
    detectLanguage(text) {
      const langCode = franc(text);
      switch (langCode) {
        case 'zh':
          return '中文';
        case 'en':
          return '英语';
        case 'fr':
          return '法语';
        case 'de':
          return '德语';
        default:
          return '未知';
      }
    },
    speakSourceText() {
      if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(this.sourceText);
        window.speechSynthesis.speak(utterance);
      } else {
        console.error('Text-to-Speech API 不被该浏览器支持');
      }
      console.log('朗读原文:', this.sourceText);
    },
    speakUserText() {
      if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(this.userText);
        window.speechSynthesis.speak(utterance);
      } else {
        console.error('Text-to-Speech API 不被该浏览器支持');
      }
      console.log('朗读译文:', this.userText);
    },
    async checkTranslation() {
      const url = 'http://8.138.30.178/translate/proofread';
      const data = {
        user_id: this.userId,
        originalText: this.sourceText,
        translatedText: this.userText,
      };

      console.log('发送的请求数据:', data);

      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }

        const result = await response.json();
        console.log('接收到的响应数据:', result);

        this.score = result.score || 10;
        this.filledStars = Math.floor(this.score / 20);

        this.grammarResult = result.grammarCheck || '语法检查结果';
        this.terminologyResult = result.terminologyValidation || '术语校验结果';
        this.consistencyResult = result.contentConsistency || '内容一致性结果';
        this.styleResult = result.languageStyle || '语言风格一致性结果';
        this.optimizationResult = result.sentenceStructure || '句式优化建议';

        this.saveProofreadResult({
          user_id: this.userId,
          originalText: this.sourceText,
          translatedText: this.userText,
          score: this.score,
          grammarCheck: this.grammarResult,
          terminologyValidation: this.terminologyResult,
          contentConsistency: this.consistencyResult,
          languageStyle: this.styleResult,
          sentenceStructure: this.optimizationResult,
        });
      } catch (error) {
        console.error('错误:', error);
        this.grammarResult = '请求失败，请检查后端服务。';
        this.terminologyResult = '请求失败，请检查后端服务。';
        this.consistencyResult = '请求失败，请检查后端服务。';
        this.styleResult = '请求失败，请检查后端服务。';
        this.optimizationResult = '请求失败，请检查后端服务。';
      }
    },

    async saveProofreadResult(data) {
      const saveUrl = 'http://localhost:8080/translate/upproofread';
      //const saveUrl = 'http://8.138.30.178/translate/upproofread';
      try {
        const response = await fetch(saveUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }

        const result = await response.json();
        console.log('保存翻译校对结果到数据库:', result);
      } catch (error) {
        console.error('保存翻译校对结果到数据库时发生错误:', error);
      }
    },

    toggleContent(content) {
      this.contentToShow = content;
    },
    handleSidebarNavigation(page) {
      console.log('Navigating to', page);
    },
    seeHistory() {
      this.isHistoryPanelVisible = true;
      this.fetchHistoryRecords();
    },
    async fetchHistoryRecords() {
      const url = 'http://localhost:8080/translate/history';
      //const url = 'http://8.138.30.178/translate/history';
      try {
        const response = await fetch(`${url}?user_id=${this.userId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        this.historyRecords = data.data.map(record => ({
          id: record[0],
          originalText: record[1],
          translatedText: record[2],
          score: record[3],
          grammarCheck: record[4],
          terminologyValidation: record[5],
          contentConsistency: record[6],
          languageStyle: record[7],
          sentenceStructure: record[8],
        }));
      } catch (error) {
        console.error('Error fetching history:', error);
      }
    },

    handleHistoryItemClick(record) {
      this.sourceText = record.originalText;
      this.userText = record.translatedText;

      this.score = record.score || 10;
      this.filledStars = Math.floor(this.score / 20);

      this.grammarResult = record.grammarCheck || '语法检查结果';
      this.terminologyResult = record.terminologyValidation || '术语校验结果';
      this.consistencyResult = record.contentConsistency || '内容一致性结果';
      this.styleResult = record.languageStyle || '语言风格一致性结果';
      this.optimizationResult = record.sentenceStructure || '句式优化建议';

      this.isHistoryPanelVisible = false;
    },
  },
};
</script>

<style scoped>
.content {
  margin-top: 70px;
  margin-left: 220px; 
  padding: 15px;
}

.su-input-container {
  display: flex;
  justify-content: space-between;
}

.su-input {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 30%;
}

.su-input-1 {
  width: 100%; /* 宽度占父容器的100% */
  position: relative; /* 确保子元素可以相对定位 */
}

.su-input button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #0b47c7;
  color: white;
  border: none;
  border-radius: 15px;
  padding: 10px;
}

.source-text,
.user-text {
  border: 1px solid #dfe1e5;
  outline: none;
  width: 100%; /* 宽度占父容器的100% */
  height: 200px; /* 固定高度 */
  border-radius: 20px;
  margin: 5px 0; /* 添加间距 */
  box-shadow: 0 4px 8px rgba(102, 51, 153, 0.3); /* 添加阴影 */
  resize: vertical; /* 允许用户调整高度 */
  padding: 20px; /* 内边距 */
  margin-left: 20px;
}

.language-indicator {
  position: absolute;
  left: 45px; /* 根据输入框的内边距调整 */
  bottom: 15px; /* 调整到底部 */
  font-size: 12px;
  color: #666;
}

.speak-button {
  position: absolute;
  right: 10px; /* 根据输入框的内边距调整 */
  bottom: 15px; /* 调整到底部 */
  cursor: pointer;
  font-size: 20px;
  color: #007bff;
}

.total-output {
  width: 60%;
  border: 1px solid #dfe1e5;
  background-image: linear-gradient(to left, rgba(113, 47, 199, 0), rgb(83, 62, 205));
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(102, 51, 153, 0.3);
  padding: 10px;
  display: flex;
  flex-direction: column;
}

.output-container {
  width: 90%; /* 设置宽度为90% */
  height: 80%; /* 设置高度为80% */
  border: 1px solid #dfe1e5;
  border-radius: 20px;
  background-color: #FFFF;
  box-shadow: 0 4px 8px rgba(102, 51, 153, 0.3);
  padding: 20px;
  display: flex;
  flex-direction: column;
  margin: auto; /* 居中对齐 */
}

.output-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.output-toggle {
  padding: 10px 20px;
  border: none;
  background-color: #f1f1f1;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.output-toggle:hover {
  background-color: #dfe1e5;
}

.output-text {
  padding: 10px;
}

.translation-score {
  display: flex;
  align-items: center;
  padding: 10px;
  font-size: 20px;
  color: #f4f4f7;
}

.score-label {
  font-weight: bold;
}

.score-value {
  font-size: 32px;
  padding-right: 10px;
}

.rating-stars {
  display: flex;
  color: #ffd700;
  font-size: 24px;
}

.rating-stars .fas {
  font-style: normal;
}

.rating-stars .fas.filled {
  color: #ffd700;
}

.rating-stars .fas:not(.filled) {
  color: #e0e0ff;
}

.history-panel {
  width: 300px;
  border: 1px solid #dfe1e5;
  background-color: #f4f4f7;
  border-radius: 20px;
  padding: 10px;
  margin-left: 15px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.history-list {
  list-style: none;
  padding: 0;
}

.history-list li {
  padding: 5px 10px;
  cursor: pointer;
  border-bottom: 1px solid #dfe1e5;
}

.history-list li:hover {
  background-color: #e0e0ff;
}
</style>
