<template>
  <div class="input-box">
    <div class="input-content">
      <div class="language-selector-wrapper">
        <!-- 源语言选择器 -->
        <select v-model="sourceLanguage" class="source-language-selector">
          <option value="自动语言检查">自动检测语言</option>
          <option value="英语">英语</option>
          <option value="中文">中文</option>
          <option value="德语">德语</option>
          <option value="日语">日语</option>
          <option value="韩语">韩语</option>
          <option value="法语">法语</option>
        </select>

        <i class="fas fa-arrow-right arrow-icon"></i>

        <!-- 目标语言选择器 -->
        <select v-model="targetLanguage" class="target-language-selector">
          <option value="英文">英文</option>
          <option value="中文">中文</option>
          <option value="德语">德语</option>
          <option value="日语">日语</option>
          <option value="韩语">韩语</option>
          <option value="法语">法语</option>
        </select>
      </div>

      <!-- 翻译文本区域 -->
      <textarea
        v-model="text"
        placeholder="请输入要翻译的内容"
        class="input-field"
        :rows="textRows"
      ></textarea>

      <!-- 动作按钮 -->
      <div class="actions">
        <!-- 上传文件图标 -->
        <i class="fas fa-upload icon-upload" @click="triggerFileInput"></i>
        <!-- 上传选项 -->
        <div class="upload-options" :class="{ show: showUploadMenu }">
          <div class="upload-option" @click="openFileInput('image')">图片</div>
          <div class="upload-option" @click="openFileInput('document')">文档</div>
        </div>

        <!-- 翻译按钮 -->
        <i v-if="isLoading" class="fas fa-spinner icon-loading"></i>
        <i v-else class="fas fa-language icon-translate" @click="translate"></i>
      </div>
    </div>

    <!-- 上传成功弹窗 -->
    <div v-if="uploadedFiles.length" class="upload-popup">
      <div class="popup-header">
        文件已上传
        <i class="fas fa-times close-popup" @click="closePopup"></i>
      </div>
      <div class="popup-body">
        <div class="file-list">
          <div
            v-for="(file, index) in uploadedFiles"
            :key="index"
            class="file-item"
          >
            <!-- 如果是图片，显示图片 -->
            <img
              v-if="file.type.startsWith('image/')"
              :src="file.preview"
              alt="Uploaded image"
              class="uploaded-image"
            />
            <!-- 如果是 Word 文件，显示文件名 -->
            <p v-else-if="file.type === 'application/msword' || file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'" class="uploaded-file-name">
              <i class="fas fa-file-word"></i> {{ file.name }}
            </p>
            <!-- 其他文件类型 -->
            <p v-else class="uploaded-file-name">{{ file.name }}</p>
          </div>
          <!-- 上传图标，点击后继续上传 -->
          <div class="upload-more" @click="triggerFileInput"></div>
        </div>
      </div>
      <div class="popup-footer">
        <i class="fas fa-paper-plane icon-send" @click="sendFiles"></i>
      </div>
    </div>

    <!-- 隐藏的文件输入框 -->
    <input
      ref="fileInput"
      type="file"
      :accept="fileAccept"
      style="display: none;"
      @change="handleFileUpload"
      multiple
    />
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
      text: '', // 原文
      sourceLanguage: '自动语言检查',
      targetLanguage: '英文',
      textRows: 3,
      userId: Math.floor(Math.random() * 100000).toString(), // 随机生成 user_id
      uploadedFiles: [], // 保存上传文件信息的列表
      showUploadMenu: false, // 控制上传菜单的显示
      fileAccept: '', // 控制文件类型选择
      selectedType: '' // 记录用户选择的类型（图片或文档）
    };
  },
  methods: {
    translate() {
      if (!this.isLoading) {
        this.$emit('translate', {
          text: this.text,
          sourceLanguage: this.sourceLanguage,
          targetLanguage: this.targetLanguage
        });
      }
    },
    triggerFileInput() {
      this.showUploadMenu = !this.showUploadMenu;
    },
    openFileInput(type) {
      // 清空之前选择的文件，避免浏览器缓存影响
      this.$refs.fileInput.value = '';

      this.selectedType = type; // 记录用户选择的类型（图片或文档）

      // 设置文件类型过滤
      if (type === 'image') {
        this.fileAccept = 'image/jpeg,image/png'; // 只允许选择 .jpg 和 .png 图片
      } else if (type === 'document') {
        this.fileAccept = '.pdf,.docx,.xls,.xlsx'; // 只允许选择 pdf, docx, xls, xlsx 文档
      }

      this.showUploadMenu = false; // 隐藏上传选项菜单
      this.$nextTick(() => { // 确保 DOM 更新后再点击文件选择框
        this.$refs.fileInput.click(); // 打开文件选择框
      });
    },
    handleFileUpload(event) {
      const files = event.target.files;
      
      if (files.length > 0) {
        const file = files[0]; // 获取第一个文件
        const filePreview = file.type.startsWith('image/')
          ? URL.createObjectURL(file) // 图片预览
          : null;

        // 将文件作为 File 对象添加到上传列表
        this.uploadedFiles.push({
          file: file,
          name: file.name,
          type: file.type,
          preview: filePreview
        });
      }
    },
    sendFiles() {
  const file = this.uploadedFiles[0].file; // 获取上传的第一个文件
  const formData = new FormData();

  // 根据文件类型，选择相应的字段名和 API URL
  formData.append(this.selectedType === 'image' ? 'image' : 'document', file);
  formData.append('user_id', this.userId);
  formData.append('target_language', this.targetLanguage);

  // 选择正确的请求 URL
  const url = this.selectedType === 'image' 
    ? 'http://localhost:5001/translate/image'  
    : 'http://localhost:5001/translate/document'; 

  fetch(url, {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    // 根据新的响应格式来提取数据
    if (data && data.base && data.base.code === 200) {  // 修改为 200
      // 更新原文和翻译结果
      this.text = data.source_text;
      this.$emit('fileTranslated', {
        translation: data.translation
      });
    } else {
      console.error('Response does not contain the expected data structure or error occurred');
    }
  })
  .catch(error => {
    console.error('Error uploading file:', error);
  });
}
,

    // 添加一个方法来关闭上传弹窗
    closePopup() {
      this.uploadedFiles = []; // 清空上传的文件列表
    }
  }
};
</script>




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

.source-language-selector,
.target-language-selector {
  padding: 4px;
  border-radius: 8px;
  border: none;
  width: 25%;
  height: 30px;
}

.arrow-icon {
  font-size: 25px;
  color: rgb(179, 113, 202);
}

.input-box {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 90%;
  padding: 16px;
  background-color: #fff;
  border: 1px solid rgb(179, 113, 202);
  border-radius: 16px;
  box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.1);
  margin-top: 18px;
}

.input-field {
  min-height: 255px;
  padding: 25px;
  border: 1px solid rgb(179, 113, 202);
  border-radius: 8px;
  resize: none;
  font-size: 14px;
  color: rgb(25, 24, 25);
}

.actions {
  position: absolute;
  bottom: 10px;
  right: 15px;
  display: flex;
  gap: 10px;
}

.icon-upload,
.icon-translate {
  cursor: pointer;
  font-size: 28px;
  color: rgb(179, 113, 202);
  border-radius: 8px;
  padding: 4px;
  background-color: #f9f9f9;
}

.icon-upload:hover,
.icon-translate:hover {
  background-color: #e9e9e9;
}

/* 上传选项菜单样式 */
.upload-options {
  display: flex;
  gap: 5px;
  padding: 4px;
  background-color: #f9f9f9;
  border-radius: 8px;
  position: absolute;
  bottom: 50px;
  right: 15px;
  width: 100px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 100;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s, visibility 0.3s;
}

.upload-options {
  display: flex;
  flex-direction: column; /* 修改为垂直排列 */
  gap: 5px; /* 保持间距 */
  padding: 4px;
  background-color: #f9f9f9;
  border-radius: 8px;
  position: absolute;
  bottom: 50px;
  right: 15px;
  width: 100px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 100;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s, visibility 0.3s;
}

.upload-options.show {
  opacity: 1;
  visibility: visible;
}

.upload-option {
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 8px;
  background-color: #fff; /* 设置白色底色 */
  border: 2px solid #800080; /* 设置紫色边框 */
  width: 100%;
  text-align: center; /* 使文本居中 */
  transition: background-color 0.3s; /* 过渡效果 */
}

.upload-option:hover {
  background-color: #f1f1f1; /* 鼠标悬浮时的背景色 */
}
.file-list {
  display: flex;
  flex-wrap: nowrap;
  justify-content: flex-start;
  gap: 10px;
}

.file-item {
  width: 80px;
  height: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 12px;
  color: #333;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 5px;
}

.uploaded-image {
  max-width: 60px;
  max-height: 60px;
  margin-bottom: 5px;
}

.uploaded-file-name {
  word-break: break-all;
}

.upload-more {
  margin-top: 10px;
  font-size: 14px;
  color: rgb(179, 113, 202);
  cursor: pointer;
}

.upload-more:hover {
  color: rgb(140, 90, 180);
}

.popup-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 15px;
}

.icon-upload,
.icon-send {
  cursor: pointer;
  font-size: 24px;
  color: rgb(179, 113, 202);
}

.icon-upload:hover,
.icon-send:hover {
  color: rgb(140, 90, 180);
}
</style>
