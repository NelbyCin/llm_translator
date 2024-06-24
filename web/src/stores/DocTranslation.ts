import { ref } from 'vue'
import { defineStore } from 'pinia'

export const FileStore = defineStore('DocTranslateContent', () => {
  const isDocLoading = ref(false)
  const showResult = ref(false)
  const showError = ref(false)
  const tgtLang = ref()
  const tgtFile = ref()
  const tgtFileName = ref()
  const srcFile = ref({ file: '' })
  function setLoading() {
    isDocLoading.value = true
    showResult.value = false
    showError.value = false
  }
  function setResult() {
    isDocLoading.value = false
    showResult.value = true
    showError.value = false
  }
  function setError() {
    isDocLoading.value = false
    showResult.value = false
    showError.value = true
  }
  function setNone() {
    isDocLoading.value = false
    showResult.value = false
    showError.value = false
  }
  function setSourceFile(file) {
    srcFile.value.file = file
  }
  function setTargetFile(file, tgtStyle) {
    tgtFile.value = file
    tgtFileName.value = "("  +tgtStyle + ")" +tgtFile.value.substring('static/output_file/'.length)
  }
  function settgtLang(tgtlang) {
    tgtLang.value = tgtlang
  }
  return {
    isDocLoading,
    showResult,
    showError,
    tgtFile,
    srcFile,
    tgtLang,
    tgtFileName,
    setLoading,
    setResult,
    setError,
    setNone,
    setSourceFile,
    setTargetFile,
    settgtLang
  }
})
