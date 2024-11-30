<template>
  <div class="output-container">
    <div class="output-item">
      <div class="output-label">
        <img src="@/assets/1.png" alt="output-icon" class="icon" />
        <span>输出</span>
      </div>

      <div class="translation-box">
        <h3>翻译结果</h3>
        <!-- 绑定 translation 到 textarea 的 value -->
        <textarea :value="translation" readonly></textarea>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OutputBox',
  props: {
    translation: {
      type: String,
      default: '', // 默认翻译结果为空
    },
    
  },
};
</script>





<style scoped>
.output-container {
  display: flex;
  flex-direction: row;
  gap: 16px;
  padding: 16px;
  border: none;
  box-shadow: none;
  background-color: transparent;
}

.translation-box,
.synonyms-box,
.examples-box {
  padding: 16px;
  background-color: transparent;
  border-radius: 16px;
  border: 1px solid #ae6ac9;
  box-shadow: 0px 8px 8px rgba(251, 248, 248, 0.05);
  height: 350px;
  overflow: auto;
}

.output-item {
  flex: 1;
  min-width: 180px;
  border-bottom: px solid #ae6ac9; /* 增加底部边框的宽度和颜色 */
}
.output-item textarea {
  height: 279px;
}

.output-label {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  font-family: 'Dancing Script', cursive; /* 应用艺术字体 */
  font-size: 24px; /* 调整字体大小 */
  color: #ae6ac9;
}

.output-label .icon {
  margin-left: 8px;
  width: 32px;
  height: 32px;
}

h3 {
  margin-bottom: 12px;
  font-size: 16px;
  color: #4a4a4a;
  font-weight: 600;
}

/* 修改 textarea 样式 */
textarea {
  width:95%;
  height: 260px;
  padding: 8px;
  border: 1px solid #ae6ac9;
  border-radius: 8px;
  resize: none;
  font-family: 'Arial', sans-serif;
  font-size: 14px;
  color: #555;
  background-color: #f9f9f9;
}

textarea[readonly] {
  background-color: #ffffff; /* 禁用状态下的背景色 */
}

@media (max-width: 768px) {
  .output-container {
    padding: 12px;
  }

  .translation-box,
  .synonyms-box,
  .examples-box {
    padding: 12px;
  }
}
</style>
