<!-- FeedbackPopup.vue -->
<template>
    <div v-if="visible" class="popup">
      <div class="popup-content">
        <p>感谢您的反馈与建议</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        visible: false
      };
    },
    methods: {
      show() {
        this.visible = true;
        setTimeout(() => {
          this.visible = false;
        }, 2000); // 2秒后自动消失
      }
    }
  };
  </script>
  
  <style scoped>
  .popup {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 200px;
    padding: 20px;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    text-align: center;
    z-index: 1000;
  }
  </style>