<script setup lang="ts">
import axios from 'axios'
import { storeToRefs } from 'pinia'
import { ElMessage } from 'element-plus'
import type { UploadProps } from 'element-plus'
import { reactive, ref } from 'vue'
import { FileStore } from '@/stores/DocTranslation'
import { LangStore } from '@/stores/language'

const URL = 'http://10.244.4.85:5000/doctranslate'

const fileStore = FileStore()
const langStore = LangStore()
const { defaultTargetLang, modelName } = storeToRefs(langStore)

const File = reactive({ file: '' })

const tgtLang = defaultTargetLang
const showUploadArea = ref(true)
const showDOC = ref(false)
const showPDF = ref(false)
const showTXT = ref(false)

// 超出文件数量，给出提示信息
const handleExceed = () => {
  ElMessage.warning('超出最大文件数！')
}
// 检查文件类型
const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
  const fileName = rawFile.name
  if (fileName.includes(' ')) {
    ElMessage.error('文件名不允许包含空格！')
    return false
  }
  if (
    rawFile.type !== 'application/pdf' &&
    rawFile.type !== 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' &&
    rawFile.type !== 'text/plain'
  ) {
    ElMessage.error('上传的文件必须是.docx、.pdf、.txt格式！')
    return false
  }
  return true
}

const uploadFile = (params) => {
  console.log(params.file.name)
  File.file = params.file

  if (File.file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
    showDOC.value = true
    showPDF.value = false
    showTXT.value = false
  }
  if (File.file.type == 'application/pdf') {
    showDOC.value = false
    showPDF.value = true
    showTXT.value = false
  }
  if (File.file.type == 'text/plain') {
    showDOC.value = false
    showPDF.value = false
    showTXT.value = true
  }
  showUploadArea.value = false
}

function cancel() {
  showUploadArea.value = true
  fileStore.setNone()
}

async function confirm() {
  fileStore.setLoading()
  fileStore.setSourceFile(File.file)
  fileStore.settgtLang(defaultTargetLang.value)

  const formData = new FormData()
  let lang_code = langStore.getLangCode()
  formData.append('file', File.file)
  formData.append('source_lang', lang_code['src'])
  formData.append('target_lang', lang_code['tgt'])
  formData.append('model_name',modelName.value)

  // Make an AJAX request using Axios
  await axios
    .post(URL, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    .then((res) => {
      console.log('Upload successful:', res.data)
      fileStore.setTargetFile(res.data.link, res.data.to)
      fileStore.setResult()
    })
    .catch((error) => {
      // Handle error
      console.log(formData)
      console.error('Error uploading file:', error)
      fileStore.setError()
    })
}
</script>

<template>
  <div class="main">
    <div v-if="showUploadArea" class="uploadarea">
      <el-upload
        class="upload-demo"
        drag
        action=""
        :before-upload="beforeAvatarUpload"
        :http-request="uploadFile"
        :limit="1"
        :on-exceed="handleExceed"
      >
        <svg
          width="100"
          height="100"
          viewBox="0 0 100 100"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M19 88V12C19 10.3431 20.3431 9 22 9H61.7574C62.553 9 63.3161 9.31607 63.8787 9.87868L80.1213 26.1213C80.6839 26.6839 81 27.447 81 28.2426V88C81 89.6569 79.6569 91 78 91H22C20.3431 91 19 89.6569 19 88Z"
            fill="white"
            stroke="#373737"
            stroke-width="1.75"
          />
          <path d="M62 9V25C62 26.6569 63.3431 28 65 28H81" stroke="#373737" stroke-width="1.75" />
          <path
            fill-rule="evenodd"
            clip-rule="evenodd"
            d="M69 42C69 42.5523 68.5523 43 68 43H30C29.4477 43 29 42.5523 29 42V42C29 41.4477 29.4477 41 30 41H68C68.5523 41 69 41.4477 69 42V42Z"
            fill="#292C32"
          />
          <path
            fill-rule="evenodd"
            clip-rule="evenodd"
            d="M69 54C69 54.5523 68.5523 55 68 55H30C29.4477 55 29 54.5523 29 54V54C29 53.4477 29.4477 53 30 53H68C68.5523 53 69 53.4477 69 54V54Z"
            fill="#292C32"
          />
          <path
            fill-rule="evenodd"
            clip-rule="evenodd"
            d="M69 66C69 66.5523 68.5523 67 68 67H30C29.4477 67 29 66.5523 29 66V66C29 65.4477 29.4477 65 30 65H68C68.5523 65 69 65.4477 69 66V66Z"
            fill="#292C32"
          />
          <rect x="10" y="34" width="40" height="40" rx="4" fill="#1F48A0" />
          <path
            d="M38.0405 64L45 44H42.542L36.9151 61.3429L31.229 44L28.8598 44.0286L23.233 61.3429L17.5469 44H15L21.9299 64H24.3583L30.0148 47.1429L35.612 64H38.0405Z"
            fill="white"
          />
        </svg>
        <svg
          width="100"
          height="100"
          viewBox="0 0 100 100"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M19 88V12C19 10.3431 20.3431 9 22 9H61.7574C62.553 9 63.3161 9.31607 63.8787 9.87868L80.1213 26.1213C80.6839 26.6839 81 27.447 81 28.2426V88C81 89.6569 79.6569 91 78 91H22C20.3431 91 19 89.6569 19 88Z"
            fill="white"
            stroke="#373737"
            stroke-width="1.75"
          />
          <path d="M62 9V25C62 26.6569 63.3431 28 65 28H81" stroke="#373737" stroke-width="1.75" />
          <path
            fill-rule="evenodd"
            clip-rule="evenodd"
            d="M48.5333 23C47.192 23 46.0889 24.1031 46.0889 25.4444C46.0889 27.1119 47.0154 29.182 47.991 31.1278C47.2284 33.515 46.363 36.0732 45.2562 38.2319C44.8554 38.3892 44.4622 38.5394 44.0798 38.6854C42.3012 39.3646 40.7559 39.9547 39.7563 40.7604C39.7373 40.7798 39.7195 40.8002 39.7028 40.8215C39.2589 41.2754 39 41.8934 39 42.5556C39 43.8969 40.1031 45 41.4444 45C42.0985 45 42.7299 44.7559 43.1861 44.2896C43.2019 44.2775 43.2172 44.2647 43.2319 44.2514C44.126 43.1838 45.1802 41.2472 46.1194 39.4771C48.2842 38.6255 50.553 37.759 52.7424 37.2389C54.3406 38.5269 56.6528 39.3778 58.5556 39.3778C59.8969 39.3778 61 38.2747 61 36.9333C61 35.592 59.8969 34.4889 58.5556 34.4889C57.0296 34.4889 54.8122 35.0336 53.1167 35.6042C51.7424 34.314 50.4797 32.7027 49.5722 30.9903C49.6703 30.6881 49.7709 30.3859 49.8709 30.0853L49.871 30.0852L49.871 30.0851L49.871 30.0851C50.4324 28.3983 50.9778 26.7597 50.9778 25.4444C50.9778 24.1031 49.8747 23 48.5333 23ZM48.5334 24.4665C49.0821 24.4665 49.5112 24.8956 49.5112 25.4443C49.5112 26.1779 49.1183 27.5288 48.6633 28.9811C48.0552 27.5683 47.5556 26.2128 47.5556 25.4443C47.5556 24.8956 47.9847 24.4665 48.5334 24.4665ZM51.4896 36.0549C50.5498 35.0889 49.6887 34.0007 48.9535 32.8313C48.4421 34.3875 47.9019 35.9679 47.2271 37.491C48.6242 36.9592 50.04 36.4513 51.4896 36.0549ZM58.5554 35.9556C59.1041 35.9556 59.5332 36.3847 59.5332 36.9334C59.5332 37.4821 59.1041 37.9112 58.5554 37.9112C57.4539 37.9112 55.8883 37.4139 54.6367 36.7195C56.0733 36.3133 57.6409 35.9556 58.5554 35.9556ZM42.1165 43.2813C42.5944 42.705 43.2777 41.5597 43.9651 40.3327C42.5472 40.9002 41.2996 41.432 40.7262 41.8758C40.5762 42.041 40.4665 42.2974 40.4665 42.5556C40.4665 43.1043 40.8956 43.5334 41.4443 43.5334C41.7361 43.5334 41.9532 43.4374 42.1165 43.2813Z"
            fill="#373737"
          />
          <rect x="10" y="52" width="48" height="22" rx="2" fill="#DA5E5C" />
          <path
            d="M26.2761 60.2326C26.2761 61.6945 25.797 62.8149 24.8387 63.5937C23.8804 64.3725 22.5165 64.762 20.7469 64.762H19.2903V70H17V56H21.0343C22.7848 56 24.0944 56.3575 24.9633 57.0725C25.8385 57.7875 26.2761 58.8409 26.2761 60.2326ZM19.2903 62.8372H20.5073C21.6828 62.8372 22.5452 62.6329 23.0946 62.2244C23.644 61.8158 23.9187 61.1774 23.9187 60.3092C23.9187 59.5048 23.6728 58.9047 23.1809 58.5089C22.689 58.1131 21.9223 57.9152 20.881 57.9152H19.2903V62.8372Z"
            fill="white"
          />
          <path
            d="M40.2719 62.8659C40.2719 65.1769 39.6299 66.9453 38.3458 68.171C37.0617 69.3903 35.2122 70 32.7974 70H28.878V56H33.2094C35.439 56 37.1735 56.6001 38.4129 57.8003C39.6522 59.0005 40.2719 60.689 40.2719 62.8659ZM37.8571 62.9425C37.8571 59.591 36.2887 57.9152 33.1519 57.9152H31.1683V68.0752H32.7974C36.1705 68.0752 37.8571 66.3643 37.8571 62.9425Z"
            fill="white"
          />
          <path
            d="M45.3653 70H43.0942V56H51V57.9343H45.3653V62.3105H50.6454V64.2544H45.3653V70Z"
            fill="white"
          />
        </svg>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          version="1.1"
          width="100"
          height="100"
          viewBox="0 0 37 34"
          xml:space="preserve"
        >
          <g display="none">
            <g display="inline">
              <g><polygon points="22.556,0 29.245,6.689 29.245,32 5.08,32 5.08,0    "></polygon></g>
              <g><polygon points="29.245,6.689 22.555,6.689 22.555,0    "></polygon></g>
              <g>
                <g><rect x="2.755" y="18.313" width="24.093" height="8.118"></rect></g>
                <g><polygon points="5.08,28.755 5.08,26.431 2.755,26.431     "></polygon></g>
              </g>
            </g>
            <g display="inline">
              <path d="M11.02,20.749v4.086h-0.934v-4.086H8.664v-0.836h3.826v0.836H11.02z"></path>
              <path
                d="M17.109,19.913l-1.479,2.383l1.576,2.539h-1.096l-0.707-1.183c-0.107-0.183-0.211-0.368-0.311-0.556    l-0.101-0.194l-0.104-0.191h-0.015l-0.104,0.194c-0.125,0.236-0.267,0.485-0.426,0.747l-0.71,1.183h-1.125l1.615-2.539l-1.5-2.383    h1.114l0.656,1.096c0.104,0.173,0.201,0.344,0.292,0.512l0.091,0.174l0.09,0.173h0.014c0.041-0.077,0.071-0.135,0.091-0.173    l0.09-0.17c0.077-0.148,0.173-0.319,0.288-0.512l0.656-1.1H17.109z"
              ></path>
              <path d="M19.576,20.749v4.086h-0.934v-4.086h-1.421v-0.836h3.827v0.836H19.576z"></path>
            </g>
          </g>
          <g>
            <g>
              <polygon
                points="8.664,20.21 10.086,20.21 10.086,24.296 11.02,24.296 11.02,20.21 12.49,20.21 12.49,19.374 8.664,19.374   "
              ></polygon>
              <path
                d="M17.109,19.374h-1.104l-0.656,1.1c-0.115,0.192-0.211,0.363-0.288,0.512l-0.09,0.17c-0.02,0.038-0.05,0.096-0.091,0.173    h-0.014l-0.09-0.173l-0.091-0.174c-0.091-0.168-0.188-0.339-0.292-0.512l-0.656-1.096h-1.114l1.5,2.383l-1.615,2.539h1.125    l0.71-1.183c0.159-0.262,0.301-0.511,0.426-0.747l0.104-0.194h0.015l0.104,0.191l0.101,0.194c0.1,0.188,0.203,0.373,0.311,0.556    l0.707,1.183h1.096l-1.576-2.539L17.109,19.374z"
              ></path>
              <polygon
                points="17.222,20.21 18.643,20.21 18.643,24.296 19.576,24.296 19.576,20.21 21.049,20.21 21.049,19.374 17.222,19.374       "
              ></polygon>
              <path
                d="M5.08,28.755v-2.324h0V32h24.165V6.689L22.556,0H5.08v17.313H2.755v9.118h0L5.08,28.755z M23.055,2.414l3.776,3.775    h-3.776V2.414z M6.08,1h15.974v6.189h6.19V31H6.08v-4.569h20.768v-9.118H6.08V1z M3.755,18.313h22.093v7.118H3.755V18.313z"
              ></path>
            </g>
          </g>
        </svg>
        <div class="el-upload__text" style="font-size: 28px">
          拖拽文件至此 或 <em>点击此处上传</em>
        </div>
        <div class="el-upload__tip">暂支持 .docx、.pdf、.txt 格式</div>
      </el-upload>
    </div>
    <div v-else class="confirmarea">
      <svg
        v-if="showDOC"
        width="100"
        height="100"
        viewBox="0 0 100 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style="margin-top: 10px"
      >
        <path
          d="M19 88V12C19 10.3431 20.3431 9 22 9H61.7574C62.553 9 63.3161 9.31607 63.8787 9.87868L80.1213 26.1213C80.6839 26.6839 81 27.447 81 28.2426V88C81 89.6569 79.6569 91 78 91H22C20.3431 91 19 89.6569 19 88Z"
          fill="white"
          stroke="#373737"
          stroke-width="1.75"
        />
        <path d="M62 9V25C62 26.6569 63.3431 28 65 28H81" stroke="#373737" stroke-width="1.75" />
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M69 42C69 42.5523 68.5523 43 68 43H30C29.4477 43 29 42.5523 29 42V42C29 41.4477 29.4477 41 30 41H68C68.5523 41 69 41.4477 69 42V42Z"
          fill="#292C32"
        />
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M69 54C69 54.5523 68.5523 55 68 55H30C29.4477 55 29 54.5523 29 54V54C29 53.4477 29.4477 53 30 53H68C68.5523 53 69 53.4477 69 54V54Z"
          fill="#292C32"
        />
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M69 66C69 66.5523 68.5523 67 68 67H30C29.4477 67 29 66.5523 29 66V66C29 65.4477 29.4477 65 30 65H68C68.5523 65 69 65.4477 69 66V66Z"
          fill="#292C32"
        />
        <rect x="10" y="34" width="40" height="40" rx="4" fill="#1F48A0" />
        <path
          d="M38.0405 64L45 44H42.542L36.9151 61.3429L31.229 44L28.8598 44.0286L23.233 61.3429L17.5469 44H15L21.9299 64H24.3583L30.0148 47.1429L35.612 64H38.0405Z"
          fill="white"
        />
      </svg>
      <svg
        v-if="showPDF"
        width="100"
        height="100"
        viewBox="0 0 100 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style="margin-top: 10px"
      >
        <path
          d="M19 88V12C19 10.3431 20.3431 9 22 9H61.7574C62.553 9 63.3161 9.31607 63.8787 9.87868L80.1213 26.1213C80.6839 26.6839 81 27.447 81 28.2426V88C81 89.6569 79.6569 91 78 91H22C20.3431 91 19 89.6569 19 88Z"
          fill="white"
          stroke="#373737"
          stroke-width="1.75"
        />
        <path d="M62 9V25C62 26.6569 63.3431 28 65 28H81" stroke="#373737" stroke-width="1.75" />
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M48.5333 23C47.192 23 46.0889 24.1031 46.0889 25.4444C46.0889 27.1119 47.0154 29.182 47.991 31.1278C47.2284 33.515 46.363 36.0732 45.2562 38.2319C44.8554 38.3892 44.4622 38.5394 44.0798 38.6854C42.3012 39.3646 40.7559 39.9547 39.7563 40.7604C39.7373 40.7798 39.7195 40.8002 39.7028 40.8215C39.2589 41.2754 39 41.8934 39 42.5556C39 43.8969 40.1031 45 41.4444 45C42.0985 45 42.7299 44.7559 43.1861 44.2896C43.2019 44.2775 43.2172 44.2647 43.2319 44.2514C44.126 43.1838 45.1802 41.2472 46.1194 39.4771C48.2842 38.6255 50.553 37.759 52.7424 37.2389C54.3406 38.5269 56.6528 39.3778 58.5556 39.3778C59.8969 39.3778 61 38.2747 61 36.9333C61 35.592 59.8969 34.4889 58.5556 34.4889C57.0296 34.4889 54.8122 35.0336 53.1167 35.6042C51.7424 34.314 50.4797 32.7027 49.5722 30.9903C49.6703 30.6881 49.7709 30.3859 49.8709 30.0853L49.871 30.0852L49.871 30.0851L49.871 30.0851C50.4324 28.3983 50.9778 26.7597 50.9778 25.4444C50.9778 24.1031 49.8747 23 48.5333 23ZM48.5334 24.4665C49.0821 24.4665 49.5112 24.8956 49.5112 25.4443C49.5112 26.1779 49.1183 27.5288 48.6633 28.9811C48.0552 27.5683 47.5556 26.2128 47.5556 25.4443C47.5556 24.8956 47.9847 24.4665 48.5334 24.4665ZM51.4896 36.0549C50.5498 35.0889 49.6887 34.0007 48.9535 32.8313C48.4421 34.3875 47.9019 35.9679 47.2271 37.491C48.6242 36.9592 50.04 36.4513 51.4896 36.0549ZM58.5554 35.9556C59.1041 35.9556 59.5332 36.3847 59.5332 36.9334C59.5332 37.4821 59.1041 37.9112 58.5554 37.9112C57.4539 37.9112 55.8883 37.4139 54.6367 36.7195C56.0733 36.3133 57.6409 35.9556 58.5554 35.9556ZM42.1165 43.2813C42.5944 42.705 43.2777 41.5597 43.9651 40.3327C42.5472 40.9002 41.2996 41.432 40.7262 41.8758C40.5762 42.041 40.4665 42.2974 40.4665 42.5556C40.4665 43.1043 40.8956 43.5334 41.4443 43.5334C41.7361 43.5334 41.9532 43.4374 42.1165 43.2813Z"
          fill="#373737"
        />
        <rect x="10" y="52" width="48" height="22" rx="2" fill="#DA5E5C" />
        <path
          d="M26.2761 60.2326C26.2761 61.6945 25.797 62.8149 24.8387 63.5937C23.8804 64.3725 22.5165 64.762 20.7469 64.762H19.2903V70H17V56H21.0343C22.7848 56 24.0944 56.3575 24.9633 57.0725C25.8385 57.7875 26.2761 58.8409 26.2761 60.2326ZM19.2903 62.8372H20.5073C21.6828 62.8372 22.5452 62.6329 23.0946 62.2244C23.644 61.8158 23.9187 61.1774 23.9187 60.3092C23.9187 59.5048 23.6728 58.9047 23.1809 58.5089C22.689 58.1131 21.9223 57.9152 20.881 57.9152H19.2903V62.8372Z"
          fill="white"
        />
        <path
          d="M40.2719 62.8659C40.2719 65.1769 39.6299 66.9453 38.3458 68.171C37.0617 69.3903 35.2122 70 32.7974 70H28.878V56H33.2094C35.439 56 37.1735 56.6001 38.4129 57.8003C39.6522 59.0005 40.2719 60.689 40.2719 62.8659ZM37.8571 62.9425C37.8571 59.591 36.2887 57.9152 33.1519 57.9152H31.1683V68.0752H32.7974C36.1705 68.0752 37.8571 66.3643 37.8571 62.9425Z"
          fill="white"
        />
        <path
          d="M45.3653 70H43.0942V56H51V57.9343H45.3653V62.3105H50.6454V64.2544H45.3653V70Z"
          fill="white"
        />
      </svg>
      <svg
        v-if="showTXT"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        version="1.1"
        width="100"
        height="100"
        viewBox="0 0 37 34"
        xml:space="preserve"
        style="margin-top: 10px"
      >
        <g display="none">
          <g display="inline">
            <g><polygon points="22.556,0 29.245,6.689 29.245,32 5.08,32 5.08,0    "></polygon></g>
            <g><polygon points="29.245,6.689 22.555,6.689 22.555,0    "></polygon></g>
            <g>
              <g><rect x="2.755" y="18.313" width="24.093" height="8.118"></rect></g>
              <g><polygon points="5.08,28.755 5.08,26.431 2.755,26.431     "></polygon></g>
            </g>
          </g>
          <g display="inline">
            <path d="M11.02,20.749v4.086h-0.934v-4.086H8.664v-0.836h3.826v0.836H11.02z"></path>
            <path
              d="M17.109,19.913l-1.479,2.383l1.576,2.539h-1.096l-0.707-1.183c-0.107-0.183-0.211-0.368-0.311-0.556    l-0.101-0.194l-0.104-0.191h-0.015l-0.104,0.194c-0.125,0.236-0.267,0.485-0.426,0.747l-0.71,1.183h-1.125l1.615-2.539l-1.5-2.383    h1.114l0.656,1.096c0.104,0.173,0.201,0.344,0.292,0.512l0.091,0.174l0.09,0.173h0.014c0.041-0.077,0.071-0.135,0.091-0.173    l0.09-0.17c0.077-0.148,0.173-0.319,0.288-0.512l0.656-1.1H17.109z"
            ></path>
            <path d="M19.576,20.749v4.086h-0.934v-4.086h-1.421v-0.836h3.827v0.836H19.576z"></path>
          </g>
        </g>
        <g>
          <g>
            <polygon
              points="8.664,20.21 10.086,20.21 10.086,24.296 11.02,24.296 11.02,20.21 12.49,20.21 12.49,19.374 8.664,19.374   "
            ></polygon>
            <path
              d="M17.109,19.374h-1.104l-0.656,1.1c-0.115,0.192-0.211,0.363-0.288,0.512l-0.09,0.17c-0.02,0.038-0.05,0.096-0.091,0.173    h-0.014l-0.09-0.173l-0.091-0.174c-0.091-0.168-0.188-0.339-0.292-0.512l-0.656-1.096h-1.114l1.5,2.383l-1.615,2.539h1.125    l0.71-1.183c0.159-0.262,0.301-0.511,0.426-0.747l0.104-0.194h0.015l0.104,0.191l0.101,0.194c0.1,0.188,0.203,0.373,0.311,0.556    l0.707,1.183h1.096l-1.576-2.539L17.109,19.374z"
            ></path>
            <polygon
              points="17.222,20.21 18.643,20.21 18.643,24.296 19.576,24.296 19.576,20.21 21.049,20.21 21.049,19.374 17.222,19.374       "
            ></polygon>
            <path
              d="M5.08,28.755v-2.324h0V32h24.165V6.689L22.556,0H5.08v17.313H2.755v9.118h0L5.08,28.755z M23.055,2.414l3.776,3.775    h-3.776V2.414z M6.08,1h15.974v6.189h6.19V31H6.08v-4.569h20.768v-9.118H6.08V1z M3.755,18.313h22.093v7.118H3.755V18.313z"
            ></path>
          </g>
        </g>
      </svg>
      <div class="filename">{{ File.file.name }}</div>
      <el-button type="info" class="confirm" @click="confirm">确认翻译为{{ tgtLang }}</el-button>
      <el-button type="info" text @click="cancel">取消</el-button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.main {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  justify-content: space-around;
  align-items: center;
  gap: 20px;

  .uploadarea {
    width: 100%;
    height: 100%;
  }
  .confirmarea {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
}
.confirm {
  height: 50px;
  max-width: 400px;
  font-size: 25px;
  color: #fff;
  margin-top: 10px;
  margin-bottom: 10px;
  background-color: #0177a9;
  border-color: #0177a9;
}
.confirm:focus {
  font-size: 25px;
  color: #fff;
  margin-top: 10px;
  margin-bottom: 10px;
  background-color: #0177a9;
  border-color: #0177a9;
}

.confirm:hover {
  background: #0b4164;
  border-color: #0b4164;
  color: #fff;
}

.filename {
  display: -webkit-box; /* For older browsers that don't support flexbox */
  display: -ms-flexbox; /* For IE 10 */
  display: flex;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1; /* 显示1行,如果超过则省略 */
  overflow: hidden; /* 隐藏超出的内容 */
  text-overflow: ellipsis;
  max-width: 600px;
  font-size: 30px;
  margin-top: 20px;
  margin-bottom: 5px;
}
</style>
