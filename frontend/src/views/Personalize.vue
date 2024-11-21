<template>
  <div>
    <!-- 侧边栏容器 -->
    <Sidebar @navigate="handleSidebarNavigation" />
    <!-- 这里添加AI对话组件内容 -->
    <div class="main-content">
      <div class="person">
        <div class="header">
          <h4>个性化定制</h4>
        </div>
        <div class="personalization">
          <form @submit.prevent="saveSettings">
            <div class="form-group">
              <label for="textStyle" style="color: rgba(108, 66, 225, 0.7)"
                >文本风格:</label
              >
              <select v-model="textStyle" id="textStyle" class="form-control">
                <option value="">请选择</option>
                <!-- 这里可以添加更多选项 -->
              </select>
            </div>

            <div class="form-group">
              <label
                for="professionalField"
                style="color: rgba(108, 66, 225, 0.7)"
                >专业领域:</label
              >
              <select
                v-model="professionalField"
                id="professionalField"
                class="form-control"
              >
                <option value="">请选择</option>
                <!-- 这里可以添加更多选项 -->
              </select>
            </div>

            <div class="form-group">
              <label style="color: rgba(108, 66, 225, 0.7)">术语库:</label>
              <select
                v-model="publicGlossary"
                id="publicGlossary"
                class="form-control"
              >
                <option value="">公共术语库</option>
                <!-- 这里可以添加更多选项 -->
              </select>
              <button
                type="button"
                @click="importGlossary"
                class="btn btn-secondary"
              >
                导入记忆库
              </button>
            </div>

            <div class="form-group">
              <label style="color: rgba(108, 66, 225, 0.7)">语言偏好:</label>
              <div>
                <label
                  ><input
                    type="radio"
                    value="English"
                    v-model="languagePreference"
                  />
                  英式英语</label
                >
                <label
                  ><input
                    type="radio"
                    value="American"
                    v-model="languagePreference"
                  />
                  美式英语</label
                >
                <!-- 这里可以添加更多语言选项 -->
              </div>
            </div>

            <div class="form-group">
              <label for="feedback" style="color: rgba(108, 66, 225, 0.7)"
                >个性化定制反馈:</label
              >
              <textarea
                v-model="feedback"
                id="feedback"
                class="form-control"
              ></textarea>
            </div>

            <button type="submit" class="btn btn-primary">确定保存</button>
            <button
              type="button"
              @click="resetSettings"
              class="btn btn-secondary"
            >
              取消
            </button>
          </form>
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
      textStyle: "",
      professionalField: "",
      publicGlossary: "",
      customGlossary: null,
      languagePreference: "English",
      documentFormat: "txt",
      feedback: "",
    };
  },
  methods: {
    saveSettings() {
      // 构建上传个性化设置的参数对象
      const settingsData = {
        user_id: this.getUserID(), // 需要获取当前用户的ID，假设存在一个方法来获取
        style: this.textStyle,
        field: this.professionalField,
        public_term: this.publicGlossary,
        custom_term: this.customGlossary,
        target_language: this.languagePreference,
        additional_notes: this.feedback,
      };

      // 调用上传个性化设置接口
      this.$http
        .post("/settings/upload", settingsData)
        .then((response) => {
          if (response.status === 200) {
            console.log("个性化设置已成功保存");
            // 可以根据需要进行其他操作，比如提示用户保存成功
          } else {
            console.log("保存个性化设置失败", response.message);
          }
        })
        .catch((error) => {
          console.error("保存个性化设置时发生错误", error);
        });
    },    
    resetSettings() {
      // 重置设置的逻辑
      this.$data = this.$data.constructor();
    },
    importGlossary() {
      // 假设这里通过某种方式获取用户粘贴的术语库内容并设置到customGlossary
      const customGlossaryContent = this.getPastedGlossaryContent(); // 需要实现获取粘贴内容的方法
      this.customGlossary = customGlossaryContent;
      console.log("Glossary imported:", this.customGlossary);
    },
    getUserID() {
      // 这里需要根据实际情况获取当前用户的ID，例如从本地存储、Vuex状态管理等获取
      // 假设从本地存储获取用户ID
      return localStorage.getItem("user_id");
    },
    getPastedGlossaryContent() {
      // 这里需要实现获取用户粘贴术语库内容的逻辑，例如监听粘贴事件等
      // 假设通过一个输入框获取粘贴内容
      const inputElement = document.getElementById("glossaryInput"); // 假设存在一个id为glossaryInput的输入框
      return inputElement.value;
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
.person {
  display: flex;
  flex-direction: column; /* 改为列方向排列 */
  gap: 15px;
  flex: 1;
  height: 90%;
  width: 100%;
  margin-bottom: 20px;
  margin-top: 60px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  border: 1px solid #ccc;
  min-height: 100%;
}
.header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 0px;
  margin-left: 15px;
}
.input-group {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.personalization {
  width: 95%;
  margin: 0 auto;

  border: 1px solid #ffffff;
  border-radius: 5px;
}

.form-group {
  margin-bottom: 50px;
  display: flex;
  align-items: center; /* 垂直居中对齐 */
}

label {
  display: block;
  margin-bottom: 5px;
  margin-left: 5px;
}

select,
input[type="file"],
textarea {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  margin-left: 10px;
  border-radius: 5px;
}

button {
  padding: 10px 20px;
  margin-right: 10px;
  cursor: pointer;
  margin-left: 10px;
  box-shadow: 0 0 5px rgba(108, 66, 225, 0.7);
  border-radius: 10px;
}

button[type="submit"] {
  background-color: #6c42e1;
  color: white;
  border: none;
  border-radius: 5px;
}

button[type="button"] {
  background-color: #ccc;
  color: black;
}
.form-control {
  flex: 1;
}

.btn {
  padding: 10px 20px;
  margin-right: 10px;
  cursor: pointer;
}

.btn-primary {
  background-color: #6c42e1;
  color: white;
  border: none;
  border-radius: 5px;
}

.btn-secondary {
  background-color: #ccc;
  color: black;
}
</style>
