const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://localhost:8888/',
        ws: true,
        changeOrigin: true,
        pathRewrite: { '^/api': '/' },
      }
    }
  },  
})
