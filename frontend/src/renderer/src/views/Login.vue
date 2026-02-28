<script setup lang="ts">
import { ref } from 'vue'
import { useAppStore } from '../stores/useAppStore'
import http from '../api/request'
import { ElMessage } from 'element-plus'
import { Lock } from '@element-plus/icons-vue'

const password = ref('')
const loading = ref(false)
const appStore = useAppStore()

async function handleLogin() {
  if (!password.value) {
    ElMessage.warning('请输入密码')
    return
  }

  loading.value = true
  try {
    const res = await http.post('/auth/login', { password: password.value }, '/api', { showLoading: false }) as any
    if (res.token) {
      appStore.setToken(res.token)
      ElMessage.success('登录成功')
      window.location.hash = '#/'
      appStore.goToDashboard()
      // 强制加载 Schema
      window.location.reload()
    } else {
      ElMessage.error('登录失败：未收到 Token')
    }
  } catch (error) {
    // 错误处理已由拦截器负责
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="login-header">
          <h2>NovelForge</h2>
          <p>创作者的 AI 助手</p>
        </div>
      </template>

      <el-form @submit.prevent="handleLogin">
        <el-form-item>
          <el-input
            v-model="password"
            type="password"
            placeholder="请输入管理员密码"
            show-password
            @keyup.enter="handleLogin"
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            class="login-button"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-footer">
        <p>个人部署版 · 认证受限</p>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: var(--el-bg-color-page);
  background-image: radial-gradient(circle at 20% 30%, rgba(64, 158, 255, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 70%, rgba(103, 194, 58, 0.1) 0%, transparent 50%);
}

.login-card {
  width: 400px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  padding: 10px 0;
}

.login-header h2 {
  margin: 10px 0 5px;
  font-size: 24px;
  color: var(--el-text-color-primary);
}

.login-header p {
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.logo {
  width: 64px;
  height: 64px;
}

.login-button {
  width: 100%;
  height: 40px;
  font-size: 16px;
  margin-top: 10px;
}

.login-footer {
  text-align: center;
  margin-top: 20px;
  color: var(--el-text-color-placeholder);
  font-size: 12px;
}
</style>
