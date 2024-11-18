<template>
  <div class="input-box">
    <div class="input-content">
      <div class="language-selector-wrapper">
        <!-- 源语言选择器 -->
        <select v-model="sourceLanguage" class="source-language-selector">
          <option value="自动语言检查">自动检测语言</option>
          <option value="中文">中文</option>
          <option value="英文">英文</option>
          <!-- 添加其他语言选项 -->
        </select>
        
        <i class="fas fa-arrow-right arrow-icon"></i> 
        
        <!-- 目标语言选择器 -->
        <select v-model="targetLanguage" class="target-language-selector">
          <option value="英文">英文</option>
          <option value="中文">中文</option>
          <!-- 添加其他语言选项 -->
        </select>
      </div>

      <!-- 翻译文本区域 -->
      <textarea
        v-model="text"
        placeholder="请输入要翻译的内容"
        class="input-field"
        :rows="textRows"
      ></textarea>
      
      <!-- 翻译按钮 -->
      <div class="actions">
        <i v-if="isLoading" class="fas fa-spinner icon-loading"></i>
        <i v-else class="fas fa-language icon-translate" @click="translate"></i>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InputBox',
  props: {
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      text: '',
      sourceLanguage: '自动语言检查',  // 默认设置为自动检测语言
      targetLanguage: '英文',  // 默认目标语言设置为英文
      textRows: 3,
    };
  },
  methods: {
    translate() {
      if (!this.isLoading) {  // 确保没有其他请求正在进行
        console.log('Translate button clicked'); // 调试输出
        this.$emit('translate', {
          text: this.text,
          sourceLanguage: this.sourceLanguage,
          targetLanguage: this.targetLanguage
        });
      }
    }
  }
}
</script>

<style scoped>
/* 样式定义保持不变 */
</style>





<style scoped>
.input-content {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
}

.language-selector-wrapper {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 15px;
}

.language-selector-inner {
  display: flex;
  align-items: center;
  gap: 80px; /* 两个选择器之间的间距 */
}

.source-language-selector {
  padding: 4px; /* 内边距 */
  border-radius: 8px; /* 边框圆角 */
  border: none; /* 取消边框 */
  width: 25%; /* 宽度设置为40% */
  height: 30px; /* 高度设置为30px */
}

.target-language-selector {
  padding: 4px; /* 内边距 */
  border-radius: 8px; /* 边框圆角 */
  border: none; /* 取消边框 */
  width: 25%; /* 宽度设置为40% */
  height: 30px; /* 高度设置为30px */
}

.arrow-icon {
  font-size: 25px; /* 调整箭头图标大小 */
  color: rgb(179, 113, 202);
}

.input-box {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 90%; /* 宽度为父元素宽度的88% */
  
  height: auto; /* 高度自适应 */
  padding: 16px;
  background-color: #fff;
  border: 1px solid  rgb(179, 113, 202);
  border-radius: 16px;
  box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.1);
  margin-top: 18px;
  align-items: flex-start;
}

.input-field {
  width: 88%; /* 宽度占满父容器 */
  min-height: 255px; /* 最小高度 */
  padding: 25px;
  border: 1px solid  rgb(179, 113, 202);
  border-radius: 8px;
  resize: none;
  font-size: 14px;
  color:  rgb(25, 24, 25);
}

.actions {
  position: absolute; /* 图标放置于绝对定位 */
  bottom: 10px; /* 离底部10px */
  right: 15px; /* 离右侧15px */
  display: flex;
  gap: 10px; /* 图标间距 */
}

.icon-upload, .icon-translate {
  cursor: pointer;
  font-size: 28px; /* 调整图标大小 */
  color: rgb(179, 113, 202);
  border-radius: 8px; /* 可选，图标圆角 */
  padding: 4px; /* 增加点击区域 */
  background-color: #f9f9f9; /* 可选，图标背景色 */
}

.icon-upload:hover, .icon-translate:hover {
  background-color: #e9e9e9; /* 鼠标悬停时的背景色 */
}
</style>