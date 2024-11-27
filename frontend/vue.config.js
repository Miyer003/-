const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  publicPath: "./", // 文件加载设置为相对路径
  transpileDependencies: true
})
