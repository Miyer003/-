import axios from "axios";

// 创建 axios 实例
export const api = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 添加请求拦截器
api.interceptors.request.use(
  config => {
    // 添加时间戳防止缓存
    if (config.method === 'get') {
      config.params = { ...config.params, _t: Date.now() };
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 添加响应拦截器
api.interceptors.response.use(
  response => response,
  error => {
    return Promise.reject(error);
  }
);

export const sendQuestionToAI = async (question) => {
  try {
    const response = await api.post("/ai/dialogue", {
      user_id: 123,
      input_text: question,
    });
    return response;
  } catch (error) {
    console.error('发送问题失败:', error);
    throw error;
  }
};

export const getChatHistory = () => api.get("/ai/dialogue/history");
export const getAutoPolishChatHistory = () => api.get("/api/autoPolish/chatHistory");
export const sendTextToWenxinForAutoPolish = (text) => api.post("/api/translate/polish", { text });
