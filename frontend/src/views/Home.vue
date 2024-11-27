<template>
  <div class="home">
    <!-- 在线翻译字样 -->
    <div class="online-translate">
      <span>在线翻译</span>
    </div>
    <!-- 侧边栏容器 -->
    <Sidebar @navigate="handleSidebarNavigation" />

    <!-- 主内容部分 -->
    <div class="main-content">
      <div class="input-output-row">
        <!-- 输入框组件 -->
        <div class="input-wrapper">
          <!-- 艺术字和小图标 -->
          <div class="input-label">
            <img id="input" src="@/assets/1.png" alt="icon" class="icon-right" />
            <span id="input">输入</span>
          </div>

          <!-- InputBox 组件 -->
          <InputBox 
            @translate="handleTranslate" 
            :isLoading="isLoading"
            class="input-box" 
          />
        </div>

        <!-- OutputBox 显示翻译结果 -->
        <OutputBox 
          :translation="translation" 
          :synonyms="synonyms" 
          :examples="outputExamples" 
          class="output-box" 
        />
      </div>

      <!-- 翻译历史 -->
      <TranslateHistory :history="history" class="history-data" />

      <!-- 本周数据详情 -->
      <div class="week-data">
        <h2>本周数据详情</h2>
        <div>
          
         
        </div>
        <!-- 柱状图 -->
        <div class="chart1">
          <canvas id="barChart"></canvas>
        </div>
        <!-- 饼状图 -->
        <div class="chart2">
          <canvas id="pieChart"></canvas>
        </div>
      </div>

      <!-- 历史翻译记录 -->
<div class="history-data">

     <!-- 扩大图标 -->
  <i class="fas fa-expand-arrows-alt expand-icon1" aria-hidden="true" @click="goToHistoryPage"></i>
<h2 aria-hidden="true" @click="goToHistoryPage">历史翻译记录</h2>
<div>
  <!-- 雷达图 -->
  <div class="chart3">
    <canvas id="radarChart"></canvas>
  </div>

  <!-- 折线图 -->
  <div class="chart4">
    <canvas id="lineChart"></canvas>
  </div>
</div>
<div class="language-and-words">
  <div class="week-data1">
    <p><strong>本周最常用语言</strong></p>
    <ul>
<li v-for="(language, index) in topLanguages" :key="`language-${index}`">
  {{ language }}
</li>
</ul>

  </div>
  <div class="translation-data">
    <p><strong>本周最常翻译的词</strong></p>
    <ul>
      <li v-for="(word, index) in topWords" :key="`word-${index}`">
        {{ word }}
      </li>
    </ul>
  </div>
</div>
</div>
</div>
</div>
</template>

<script>
import InputBox from '@/components/InputBox.vue';
import OutputBox from '@/components/OutputBox.vue';
import TranslateHistory from '@/components/TranslateHistory.vue';
import Sidebar from '@/components/Sidebar.vue';
import axios from 'axios';
import { Chart } from 'chart.js/auto';

export default {
components: { InputBox, OutputBox, TranslateHistory, Sidebar },
data() {
  return {
    topLanguages: ["English", "Spanish", "French"], // 存储 top_3_languages
    topWords: ["example", "word", "translation"], // 存储 top_words
    translation: '',
    synonyms: [],
    examples: [],
    history: [],
    weeklyTranslationCount: 0,
    weeklyAiDialogCount: 5,
    weeklyTranslations: [],
    userId: Math.floor(Math.random() * 100000).toString(), // 随机生成 user_id
    isLoading: false, // 初始化 isLoading 状态
    translationStats: [
      { languagePair: '汉译英', count: 8 },
      { languagePair: '英译汉', count: 5 },
      { languagePair: '汉译法', count: 2 },
    ],
    totalSentenceQueries: 0, // 本周查询例句总次数
    totalSynonymQueries: 0, // 本周查询同义词总次数
  };
},
async mounted() {
  // 调用一个方法来获取所有的数据，并确保数据加载完成
  await this.loadData();
  this.renderBarChart();  // 在数据获取完成后渲染图表
  this.renderPieChart();
  this.renderRadarChart();
  this.renderLineChart();
},

methods: {
  goToHistoryPage() {
    // 跳转到历史记录页面
    this.$router.push({ name: 'History1' });
  },
  // 方法用于加载数据
  async loadData() {
    await this.fetchWeeklyData();  // 获取本周数据
    await this.fetchWeeklyTranslationHistory();  // 获取翻译历史
  },

  async fetchWeeklyData() {
    const { startDate, endDate } = this.getWeekDateRange();
    console.log("Fetching weekly data for:", { startDate, endDate });

    try {
      const response = await axios.get('http://127.0.0.1:31/v1/weekly-data', {
        params: {
          user_id: this.userId,
          start_date: startDate,
          end_date: endDate,
        },
      });

      if (response.data && response.data.code === 200) {
        const { total_translations, translation_ranking, total_sentence_queries, total_ai_conversations, total_synonym_queries } = response.data;
        this.weeklyTranslationCount = total_translations;
        this.weeklyAiDialogCount = total_ai_conversations;
        this.translationStats = translation_ranking.map(item => ({
          languagePair: item.language_pair,
          count: item.count,
        }));
        this.totalSentenceQueries = total_sentence_queries;
        this.totalSynonymQueries = total_synonym_queries;
      } else {
        console.error('Failed to fetch weekly data:', response.data);
        this.setDefaultWeeklyData(); // 设置默认数据
      }
    } catch (error) {
      console.error('Error fetching weekly data:', error);
      this.setDefaultWeeklyData(); // 设置默认数据
    }
  },

  async fetchWeeklyTranslationHistory() {
    const { startDate, endDate } = this.getWeekDateRange();
    console.log("Fetching translation history for:", { startDate, endDate });

    try {
      const response = await axios.get('http://127.0.0.1:31/v1/user/weekly-translation-history', {
        params: { user_id: this.userId, start_date: startDate, end_date: endDate },
      });

      if (response.data && response.data.weekly_translation_history) {
        this.topLanguages = response.data.weekly_translation_history.top_3_languages;
        this.topWords = response.data.weekly_translation_history.top_words;
      } else {
        console.error('Failed to fetch translation history:', response.data);
        this.setDefaultTranslationHistory(); // 设置默认数据
      }
    } catch (error) {
      console.error('Error fetching translation history:', error);
      this.setDefaultTranslationHistory(); // 设置默认数据
    }
  },

  setDefaultWeeklyData() {
    this.weeklyTranslationCount = 10; // 默认翻译次数
    this.weeklyAiDialogCount = 5;    // 默认 AI 对话次数
    this.translationStats = [
      { languagePair: '汉译英', count: 6 },
      { languagePair: '英译汉', count: 3 },
      { languagePair: '汉译法', count: 1 },
    ];
    this.totalSentenceQueries = 20;  // 默认例句查询次数
    this.totalSynonymQueries = 10;  // 默认同义词查询次数
  },

  setDefaultTranslationHistory() {
    this.topLanguages = ['English', 'Spanish', 'French']; // 默认语言
    this.topWords = ['example', 'translation', 'language']; // 默认常翻译词
  },


  // 获取本周日期范围
  getWeekDateRange() {
    const today = new Date();
    const dayOfWeek = today.getDay();
    const startOfWeek = new Date(today);
    startOfWeek.setDate(today.getDate() - dayOfWeek);  // 将日期调整到周一

    const endOfWeek = new Date(startOfWeek);
    endOfWeek.setDate(startOfWeek.getDate() + 6);  // 将日期调整到周日

    const startDate = startOfWeek.toISOString().split('T')[0];  // 格式化日期为 YYYY-MM-DD
    const endDate = endOfWeek.toISOString().split('T')[0]; // 格式化日期为 YYYY-MM-DD

    return { startDate, endDate };
  },

  // 渲染柱状图
  renderBarChart() {
    const ctx = document.getElementById('barChart').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['翻译次数', 'AI 对话次数'],
        datasets: [
          {
            label: '次数',
            data: [this.weeklyTranslationCount, this.weeklyAiDialogCount],
            backgroundColor: ['#4a90e2', '#ae6ac9'],
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true },
        },
      },
    });
  },

  // 渲染饼图
  renderPieChart() {
    const ctx = document.getElementById('pieChart').getContext('2d');
    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: this.translationStats.map(stat => stat.languagePair),
        datasets: [
          {
            data: this.translationStats.map(stat => stat.count),
            backgroundColor: ['#4a90e2', '#ae6ac9', '#f5a623'],
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'left',
            labels: {
              font: { size: 14 },
              color: '#333',
            },
          },
        },
      },
    });
  },

  // 渲染雷达图
  renderRadarChart() {
    // 雷达图的渲染逻辑
  },

  // 渲染折线图
  renderLineChart() {
    // 折线图的渲染逻辑
  },












async handleTranslate({ text, sourceLanguage, targetLanguage }) {
this.isLoading = true;  // 开始请求时将 isLoading 设为 true
console.log('handleTranslate called'); // 调试输出



try {
  const response = await this.translateAPI(text, sourceLanguage, targetLanguage);
  console.log('API response:', response); // 调试输出

  // 确保后端返回了成功的响应
  if (response.data.base.code === 200) {
    // 将翻译结果存入 translation
    this.translation = response.data.translation;

    console.log('Translation result:', this.translation);  // 确保翻译结果已经更新

    // 保存历史记录
    this.history.push({ text, translation: this.translation });

    // 更新本周翻译数据
    this.updateWeeklyData(text);
  } else {
    console.error('Translation error:', response.data.base.message);
  }
} catch (error) {
  console.error('Translation failed', error);
} finally {
  this.isLoading = false;  // 请求完成后将 isLoading 设为 false
}
},


    async translateAPI(text, sourceLanguage, targetLanguage) {
const url = 'http://8.138.30.178/translate/instant';
/*const url = 'http://127.0.0.1:5000/translate/instant'*/;
return axios.post(url, {
  user_id: this.userId,
  source_text: text,
  source_language: sourceLanguage,
  target_language: targetLanguage,
}, {
  headers: {
    'Content-Type': 'application/json',  // 设置请求头，确保请求为 JSON 格式
  },
});
},

    
    renderRadarChart() {
const ctx = document.getElementById('radarChart').getContext('2d');
new Chart(ctx, {
  type: 'radar',
  data: {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    datasets: [{
      label: 'My Dataset',
      data: [12, 19, 3, 5, 2],
      fill: true,
      backgroundColor: 'rgba(238, 130, 238, 0.2)',  // 浅紫色背景
      borderColor: 'rgba(238, 130, 238, 1)',        // 浅紫色边框
      pointBackgroundColor: 'rgba(238, 130, 238, 1)', // 浅紫色数据点
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(238, 130, 238, 1)'
    }]
  },
  options: {
    responsive: true,
    scale: {
      ticks: {
        beginAtZero: true
      }
    }
  }
});
},

renderLineChart() {
const ctx = document.getElementById('lineChart').getContext('2d');
new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [{
      label: 'Line Dataset',
      data: [65, 59, 80, 81, 56, 55],
      fill: false,
      borderColor: '#f9a8d4',  // 浅红色折线
      tension: 0.1
    }]
  },
  options: {
    responsive: true,
    scales: {
      x: {
        beginAtZero: true
      },
      y: {
        beginAtZero: true
      }
    }
  }
});
},
    
  },
};




</script>





<style scoped>


.home {
  display: flex;
  flex-direction: row;
  width: 100%;
  margin-top: 30px;
  position: relative;
}

.online-translate {
  position: absolute;
  top: 30px;
  left: 23%;
  transform: translateX(-50%);
  font-size: 28px;
  color: #b1b3b4;
  font-weight: bold;
}

.main-content {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  margin-left: 200px;
  padding: 10px;
  justify-content: flex-start;
  width: calc(100% - 200px);
}

.input-output-row {
  display: flex;
  width: 100%;
  justify-content: space-between; /* 确保子元素平均分配空间 */
  margin-top: 50px;
}

.input-wrapper {
  flex: 1 1 50%;
  position: relative; /* 使得子元素图标相对定位 */
}

.input-label {
  position: relative;
  display: flex;
  align-items: center;
  margin-bottom: 0px;
  font-family: 'Dancing Script', cursive;
  font-size: 24px;
  color: #ae6ac9;
  padding-bottom: -10px;
}

.input-label span {
  margin-right: 8px;
}

.icon-right {
  width: 32px;
  height: 32px;
  margin-top: 2px;
}

.output-box {
  flex: 1 1 50%;
  overflow: hidden; /* 移除滚动功能 */
  /* 可以根据需求添加其他样式，例如边距、背景等 */
}



.content-area,
.week-data,
.history-data {
flex: 1 1 calc(33% - 20px);
box-sizing: border-box;
min-width: 31%;
height: 500px; /* 固定高度，调整为你需要的高度 */
overflow-y: auto; /* 允许内容内部的垂直滚动 */
border: 1px solid rgb(179, 113, 202); /* 设置紫色边框 */
box-shadow: 0px 6px 12px rgba(179, 113, 202, 0.1); /* 保持紫色阴影，透明度调整为0.1 */
background-color: #fff;
border-radius: 10px;
}


.chart1{
  width: 80%;
  height: 200px;
  margin-top: -10px; /* 向上移动 */
  margin-left: 10%; /* 向右移动 */
}
.chart2{
  width: 80%;
  height: 290px;
  margin-top: -60px; /* 向上移动 */
  margin-left: 10%; /* 向右移动 */
}

.history-data h2 {
color:rgb(5, 5, 5);  /* 浅紫色 */
font-size: 24px;
font-weight: bold;
margin-bottom: 20px;
}



.language-and-words {
display: flex;
justify-content: space-between;
width: 100%;
}

.week-data1, .translation-data {
flex: 1;
margin: 0 10px;
}

.week-data1 p strong, .translation-data p strong {
color:rgb(210, 213, 209);  /* 浅紫色 */
font-size: 20px;
font-weight: bold;
margin-bottom: 10px;
display: block;  /* 使标题独占一行 */
width: 100%;  /* 设置标题宽度为100% */
text-align: left;  /* 左对齐 */
}

.week-data1 ul, .translation-data ul {
list-style: none;
padding: 0;
margin: 0;
}

.week-data1 ul li, .translation-data ul li {
background-color: #fafdf5;  /* 粉色背景 */
padding: 12px 20px;
border-radius: 8px;
box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
margin-bottom: 10px; /* 列表项之间的间距 */
font-size: 16px;
color: #333;
text-align: center;
transition: all 0.3s ease;
}

.week-data1 ul li:hover, .translation-data ul li:hover {
background-color: #cdfbc9;  /* 悬浮时变成稍微深一点的粉色 */
transform: translateY(-5px);
}

/* 响应式设计：在屏幕宽度小于600px时将列表项调整为单列显示 */
@media (max-width: 600px) {
.language-and-words {
  flex-direction: column;
}

.week-data1, .translation-data {
  width: 100%;  /* 列表项宽度设置为100%，单列显示 */
  margin: 10px 0;
}
}

/* 设置图表容器的样式 */
.chart3, .chart4 {
width: 70%;
margin: 0 auto; /* 自动水平居中 */
padding: 2px;
background-color: #ffffff;
border-radius: 10px;
}

/* 设置图表的高度 */
.chart3 {
height: 280px;
}

.chart4 {
height: 130px;
}




/* 扩大图标样式 */
.expand-icon1 {
position: absolute;
color: rgb(232, 231, 232); /* 图标颜色 */
font-size: 28px; /* 图标大小 */
cursor: pointer; /* 鼠标悬停时显示点击效果 */
margin-top: 22px;
right: 30px; /* 向右移动30px */
}

.card {
  width: 280px;
  height: 150px;
  background-color: #fff;
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
overflow: hidden;
}

h2 {
color: #333;
}

#input {
margin-top: 14px;
}

.icon-upload {
width: 40px;
height: 40px;
cursor: pointer;
position: absolute;
bottom: 10px; 
right: 60px;
}

.translate-icon {
width: 40px;
height: 40px;
cursor: pointer;
position: absolute;
bottom: 10px; /* 调整底部距离 */
right: 10px;
border-radius: 8px;
}


</style>