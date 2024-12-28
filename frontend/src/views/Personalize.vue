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
                <option value="">正式文体：语言规范、严谨，用词准确、专业，句式较为复杂，多使用长句、复合句，较少使用口语化表达和缩写形式。</option>
                <option value="">商务文体：简洁明了、专业精准，注重表达的准确性和客观性，常使用专业术语和固定搭配，语气较为正式、礼貌。</option>
                <option value="">科技文体：逻辑性强，大量使用专业词汇和技术术语，语言表达精确，常包含复杂的概念和数据，句式结构较为严谨。</option>
                <option value="">文学文体：语言优美、富有感染力，注重形象性和艺术性，常使用各种修辞手法，如比喻、拟人、夸张等，用词丰富多样，句式灵活多变。</option>
                <option value="">口语化文体：语言通俗易懂、自然流畅，多使用简单句和常用词汇，语气随意、亲切，常包含口语化的表达和习惯用语。</option>
                <option value="">幽默文体：语言诙谐风趣，善于运用夸张、双关、反语等修辞手法，以达到幽默的效果，使读者在轻松愉快的氛围中接受信息。</option>
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
                <option value="">医学</option>
                <option value="">法律</option>
                <option value="">信息技术</option>
                <option value="">金融</option>
                <option value="">机械工程</option>
                <option value="">化工</option>
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
                <label
                  ><input
                    type="radio"
                    value="LM"
                    v-model="languagePreference"
                  />
                  拉丁美洲西班牙语</label
                >
                <label
                  ><input
                    type="radio"
                    value="Brazil"
                    v-model="languagePreference"
                  />
                  巴西葡萄牙语</label
                >
                <label
                  ><input
                    type="radio"
                    value="Canada"
                    v-model="languagePreference"
                  />
                  加拿大法语</label
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
import { message } from 'ant-design-vue';
import axios from 'axios';

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
      axios
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
        // 无论是否成功，都弹出提示框
        message.info('已上传个性化');
    },
    resetSettings() {
      // 重置设置的逻辑
      
      this.$data = this.$data.constructor();
    },
    importGlossary() {
      // 假设这里通过某种方式获取用户粘贴的术语库内容并设置到customGlossary
      const inputElement = document.getElementById("glossaryInput");
      if (inputElement) {
        this.customGlossary = inputElement.value;
        console.log("Glossary imported:", this.customGlossary);
      } else {
        console.log("未找到术语库输入框");
      }
      message.info('已导入术语库');
    },
    getUserID() {
      try {
        return localStorage.getItem("user_id");
      } catch (error) {
        this.getUserIDError = error.message;
        console.error("获取用户ID时发生错误", error);
        return null;
      }
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
  display: flex;
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
