import { ref } from 'vue'
import { defineStore } from 'pinia'

export const ContentStore = defineStore('TranslateContent', () => {
  const sourceContent = ref('')
  const targetContent = ref('')
  const isLoading = ref(false)

  function setSourceContent(content: string) {
    sourceContent.value = content
  }

  function setTargetContent(content: string) {
    targetContent.value = content
  }

  function setLoading() {
    isLoading.value = !isLoading.value
  }

  function swapContent() {
    const source = sourceContent.value
    const target = targetContent.value
    setSourceContent(target)
    setTargetContent(source)
  }

  return {
    sourceContent,
    targetContent,
    isLoading,
    setSourceContent,
    setTargetContent,
    setLoading,
    swapContent
  }
})
