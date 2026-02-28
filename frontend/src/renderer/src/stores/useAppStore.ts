import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  // 当前视图
  const isWeb = import.meta.env.VITE_APP_PLATFORM === 'web'
  const hasToken = !!localStorage.getItem('novelforge_token')
  const initialView = (isWeb && !hasToken) ? 'login' : 'dashboard'
  const currentView = ref<'dashboard' | 'editor' | 'ideas' | 'workflows' | 'code-workflows' | 'triggers' | 'login'>(initialView)

  // 主题状态
  const isDarkMode = ref(false)

  // 认证状态 (Reactive)
  const token = ref(localStorage.getItem('novelforge_token') || '')
  const isAuthenticated = computed(() => !!token.value)

  function setToken(newToken: string) {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('novelforge_token', newToken)
    } else {
      localStorage.removeItem('novelforge_token')
    }
  }

  // 设置对话框状态
  const settingsDialogVisible = ref(false)
  const settingsInitialTab = ref<string>('llm')

  // 全局加载状态
  const globalLoading = ref(false)

  // 全局错误状态
  const globalError = ref<string | null>(null)

  // Computed
  const isDashboard = computed(() => currentView.value === 'dashboard')
  const isEditor = computed(() => currentView.value === 'editor')
  const isWorkflows = computed(() => currentView.value === 'workflows')

  // Actions
  function setCurrentView(view: 'dashboard' | 'editor' | 'ideas' | 'workflows' | 'code-workflows' | 'triggers') {
    currentView.value = view
  }

  function goToDashboard() {
    currentView.value = 'dashboard'
  }

  function goToEditor() {
    currentView.value = 'editor'
  }

  function goToIdeas() {
    currentView.value = 'ideas'
  }

  function goToWorkflows() {
    currentView.value = 'workflows'
  }

  function goToCodeWorkflows() {
    currentView.value = 'code-workflows'
  }

  function goToTriggers() {
    currentView.value = 'triggers'
  }

  function goToLogin() {
    currentView.value = 'login'
  }


  function toggleTheme() {
    isDarkMode.value = !isDarkMode.value
    localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
    applyTheme()
  }

  function setTheme(dark: boolean) {
    isDarkMode.value = dark
    localStorage.setItem('theme', dark ? 'dark' : 'light')
    applyTheme()
  }

  function applyTheme() {
    const html = document.documentElement
    if (isDarkMode.value) {
      html.classList.add('dark')
    } else {
      html.classList.remove('dark')
    }
  }

  function initTheme() {
    const savedTheme = localStorage.getItem('theme')
    isDarkMode.value = savedTheme === 'dark'
    applyTheme()
  }

  function openSettings(tab?: string) {
    if (tab) settingsInitialTab.value = tab
    settingsDialogVisible.value = true
  }

  function closeSettings() {
    settingsDialogVisible.value = false
  }

  function setGlobalLoading(loading: boolean) {
    globalLoading.value = loading
  }

  function setGlobalError(error: string | null) {
    globalError.value = error
  }

  function clearGlobalError() {
    globalError.value = null
  }

  function reset() {
    currentView.value = 'dashboard'
    settingsDialogVisible.value = false
    globalLoading.value = false
    globalError.value = null
  }

  return {
    // State
    currentView,
    isDarkMode,
    settingsDialogVisible,
    settingsInitialTab,
    globalLoading,
    globalError,

    // Computed
    isDashboard,
    isEditor,
    isWorkflows,

    // Actions
    setCurrentView,
    setToken,
    goToDashboard,
    goToEditor,
    goToIdeas,
    goToWorkflows,
    goToCodeWorkflows,
    goToTriggers,
    goToLogin,
    toggleTheme,
    setTheme,
    applyTheme,
    initTheme,
    openSettings,
    closeSettings,
    setGlobalLoading,
    setGlobalError,
    clearGlobalError,
    isAuthenticated,
    reset
  }
}) 
