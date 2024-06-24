<script setup lang="ts">
import { FileStore } from '@/stores/DocTranslation'
import { storeToRefs } from 'pinia'

const URL = 'http://10.244.4.85:5000/'

const fileStore = FileStore()
const { isDocLoading, showResult, showError, srcFile, tgtFile, tgtLang, tgtFileName } = storeToRefs(fileStore)

const loading = isDocLoading
const showresult = showResult
const showerror = showError
const tgtFilename = tgtFileName

const downloadFile = () => {
  const fileData = tgtFile.value

  const link = document.createElement('a')
  link.href = URL + fileData
  link.download = tgtFilename.value

  // 使用 fetch API 下载文件
  fetch(link.href)
    .then((response) => {
      if (!response.ok) {
        throw new Error('Failed to download file.')
      }
      return response.blob()
    })
    .then((blob) => {
      const url = window.URL.createObjectURL(blob)
      link.href = url
      link.click()
      // 等待下载完成后再删除链接
      setTimeout(() => {
        window.URL.revokeObjectURL(url) // 清理URL引用
      }, 0)
    })
    .catch((error) => {
      console.error('Error downloading file:', error)
    })
}
</script>

<template>
  <div class="main">
    <div class="tran_loading" v-if="loading">
      <svg
        width="80"
        height="84"
        viewBox="0 0 80 84"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style="margin-top: 30px"
      >
        <path
          d="M12.8574 21.4141V54.6504C12.8574 56.3769 13.7628 57.9596 15.2399 58.8229L43.8297 75.417C45.3068 76.2803 47.1175 76.2803 48.5947 75.417L77.1844 58.8229C78.6616 57.9596 79.5669 56.3769 79.5669 54.6504V21.4141C79.5669 19.6876 78.6616 18.1049 77.1844 17.2416L48.5947 0.647459C47.1175 -0.21582 45.3068 -0.21582 43.8297 0.647459L15.2399 17.2896C13.7628 18.1528 12.8574 19.7355 12.8574 21.4141Z"
          fill="#DDE3E9"
        />
        <path d="M58.1246 83.7148L58.077 76.5208L58.1246 69.9023L41.4473 74.0269" fill="#DDE3E9" />
        <path
          d="M45.5255 69.6319H1V16.291H37.3514L41.5381 20.9583L45.5255 25.6257V69.6319Z"
          stroke="#0F2B46"
          stroke-width="2"
          stroke-miterlimit="10"
        />
        <path
          d="M36.8867 16.291V25.6257H45.3931"
          stroke="#0F2B46"
          stroke-width="2"
          stroke-miterlimit="10"
        />
        <path d="M12.791 33.5928H34.8349" stroke="#0F2B46" stroke-width="2" />
        <path d="M12.791 43.5127H34.8349" stroke="#0F2B46" stroke-width="2" />
        <path d="M12.791 53.4326H34.8349" stroke="#0F2B46" stroke-width="2" />
      </svg>
      <div class="word">极速翻译中...</div>
      <div class="demo-progress">
        <el-progress :percentage="50" :stroke-width="15" :indeterminate="true" :show-text="false" />
      </div>
    </div>
    <div class="result" v-if="showresult">
      <svg
        width="110"
        height="110"
        viewBox="0 0 143 148"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <g clip-path="url(#clip0_493_6638)">
          <path
            d="M39.7297 37.4753C42.4575 35.1682 46.209 34.4915 49.5709 35.7003L93.8186 51.6097C97.1805 52.8184 99.6422 55.729 100.276 59.2449L108.622 105.519C109.256 109.035 107.967 112.622 105.239 114.929L69.3371 145.294C66.6093 147.601 62.8579 148.278 59.4959 147.069L15.2483 131.16C11.8863 129.951 9.42463 127.041 8.7905 123.525L0.444533 77.2505C-0.189595 73.7345 1.10017 70.1474 3.82799 67.8402L39.7297 37.4753Z"
            fill="#BDD9BF"
          />
          <rect
            opacity="0.7"
            x="29.8125"
            y="35.3877"
            width="95.9425"
            height="109.008"
            rx="5"
            transform="rotate(-2.636 29.8125 35.3877)"
            fill="#FFC857"
          />
          <rect
            x="40.5"
            y="26"
            width="94"
            height="112"
            rx="4"
            fill="white"
            stroke="black"
            stroke-width="2"
          />
          <rect
            x="57.8418"
            y="47.8807"
            width="60.6816"
            height="4.10011"
            rx="2.05005"
            fill="#0F2B46"
          />
          <rect x="57.5" y="57" width="53" height="4" rx="2" fill="#0F2B46" />
          <rect
            x="57.8418"
            y="65.9212"
            width="60.6816"
            height="4.10011"
            rx="2.05005"
            fill="#0F2B46"
          />
          <rect
            x="57.8418"
            y="76.5815"
            width="37.721"
            height="4.10011"
            rx="2.05005"
            fill="#0F2B46"
          />
          <rect
            x="57.8418"
            y="85.6017"
            width="37.721"
            height="4.10011"
            rx="2.05005"
            fill="#0F2B46"
          />
          <rect
            x="57.8418"
            y="94.6219"
            width="37.721"
            height="4.10011"
            rx="2.05005"
            fill="#0F2B46"
          />
          <g style="mix-blend-mode: multiply">
            <circle cx="25" cy="75.5" r="9.5" fill="#BDD9BF" />
          </g>
          <ellipse cx="133" cy="35" rx="10.5" ry="10" fill="#BDD9BF" />
          <path
            d="M133.226 32.4852C135.36 32.4852 137.09 30.7551 137.09 28.6208C137.09 26.4865 135.36 24.7563 133.226 24.7563C131.092 24.7563 129.361 26.4865 129.361 28.6208C129.361 30.7551 131.092 32.4852 133.226 32.4852Z"
            stroke="black"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
          <path
            d="M133.226 37.2414C128.465 37.2414 124.605 33.3818 124.605 28.6207C124.605 23.8596 128.465 20 133.226 20C141.327 20 141.847 25.2021 141.847 28.6207V30.107C141.847 31.4205 140.782 32.4851 139.469 32.4851C138.155 32.4851 137.091 31.4205 137.091 30.107V24.7562"
            stroke="black"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
          <path
            d="M29.8636 61.2273V73.25C29.8636 75.5605 27.9109 77.4318 25.5 77.4318C23.0891 77.4318 21.1364 75.5605 21.1364 73.25V60.1818C21.1364 58.7391 22.3582 57.5682 23.8636 57.5682C25.3691 57.5682 26.5909 58.7391 26.5909 60.1818V71.1591C26.5909 71.7341 26.1 72.2045 25.5 72.2045C24.9 72.2045 24.4091 71.7341 24.4091 71.1591V61.2273H22.7727V71.1591C22.7727 72.6018 23.9945 73.7727 25.5 73.7727C27.0055 73.7727 28.2273 72.6018 28.2273 71.1591V60.1818C28.2273 57.8714 26.2745 56 23.8636 56C21.4527 56 19.5 57.8714 19.5 60.1818V73.25C19.5 76.4282 22.1836 79 25.5 79C28.8164 79 31.5 76.4282 31.5 73.25V61.2273H29.8636Z"
            fill="black"
          />
          <path
            d="M17.5 15.3677L25.0931 21.9506"
            stroke="#FFC857"
            stroke-width="3"
            stroke-linecap="round"
          />
          <path
            d="M54.3848 2L48.568 10.1948"
            stroke="#FFC857"
            stroke-width="3"
            stroke-linecap="round"
          />
          <circle cx="39" cy="40.5" r="3.5" stroke="#F46F52" stroke-width="2" />
          <g opacity="0.2">
            <rect x="55.5" y="45" width="67" height="9" fill="#006494" />
            <rect x="55.5" y="55" width="60" height="9" fill="#006494" />
            <rect x="55.5" y="65" width="46" height="9" fill="#006494" />
          </g>
        </g>
        <defs>
          <clipPath id="clip0_493_6638">
            <rect width="143" height="148" fill="white" />
          </clipPath>
        </defs>
      </svg>
      <div class="sucesstip">{{ tgtLang }}翻译已完成</div>
      <div class="file">
        <svg id="svg4697" version="1.1" width="35px" height="35px" viewBox="0 0 185 205">
          <defs id="defs4701" />
          <path
            id="path4689"
            d="m131,10H43v164h124V46zv36h36"
            stroke-width="2"
            fill="#FFF"
            stroke="#999"
          />
          <path
            id="path4691"
            d="m94,25v135m23-1V56"
            stroke-dasharray="6,10"
            stroke-width="72"
            stroke="#999"
          />
        </svg>
        <div class="filename">{{ tgtFilename }}</div>
      </div>
      <el-button type="primary" class="download" @click="downloadFile">下载文件</el-button>
    </div>
    <div class="error" v-if="showerror">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="110" height="110">
        <path
          fill="#D33500"
          d="M805.504 320 640 154.496V320zM832 384H576V128H192v768h640zM160 64h480l256 256v608a32 32 0 0 1-32 32H160a32 32 0 0 1-32-32V96a32 32 0 0 1 32-32m308.992 546.304-90.496-90.624 45.248-45.248 90.56 90.496 90.496-90.432 45.248 45.248-90.496 90.56 90.496 90.496-45.248 45.248-90.496-90.496-90.56 90.496-45.248-45.248 90.496-90.496z"
        ></path>
      </svg>
      <div class="file">
        <svg
          id="svg4697"
          version="1.1"
          width="35px"
          height="35px"
          viewBox="0 0 185 215"
          style="margin-top: 10px"
        >
          <defs id="defs4701" />
          <path
            id="path4689"
            d="m131,10H43v164h124V46zv36h36"
            stroke-width="2"
            fill="#FFF"
            stroke="#999"
          />
          <path
            id="path4691"
            d="m94,25v135m23-1V56"
            stroke-dasharray="6,10"
            stroke-width="72"
            stroke="#999"
          />
        </svg>
        <div class="eFilename">{{ srcFile.file.name }}</div>
      </div>
      <div class="errorTip">翻译失败</div>
      <!-- <div class="errorResult">文件数量太大</div> -->
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

  .tran_loading {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .result {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .error {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .demo-progress {
    width: 100%;
    margin-left: 20px;
    margin-top: 10px;
    max-width: 300px;
  }
}

.word {
  font-size: 30px;
  margin-top: 30px;
  margin-bottom: 5px;
}
.filename {
  display: -webkit-box; /* For older browsers that don't support flexbox */
  display: -ms-flexbox; /* For IE 10 */
  display: flex;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1; /* 显示1行,如果超过则省略 */
  overflow: hidden; /* 隐藏超出的内容 */
  text-overflow: ellipsis;
  max-width: 550px;
  font-size: 30px;
  margin-bottom: 5px;
  margin-left: 10px;
}
.sucesstip {
  font-size: 30px;
  margin-top: 20px;
  margin-bottom: 5px;
}
.download {
  height: 50px;
  font-size: 25px;
  color: #fff;
  margin-top: 10px;
  margin-bottom: 10px;
  background-color: #0b4164;
  border-color: #0b4164;
}

.download:focus {
  font-size: 25px;
  color: #fff;
  margin-top: 10px;
  margin-bottom: 10px;
  background-color: #0b4164;
  border-color: #0b4164;
}

.download:hover {
  background: #0177a9;
  border-color: #0177a9;
  color: #fff;
}
.errorTip {
  margin-top: 10px;
  font-size: 28px;
  color: #e5053a;
}

.errorResult {
  margin-top: 5px;
  font-size: 18px;
  color: #485468;
}
.file {
  margin-top: 10px;
  display: flex;
  flex-direction: row;
  align-items: center;
}
.eFilename {
  display: -webkit-box; /* For older browsers that don't support flexbox */
  display: -ms-flexbox; /* For IE 10 */
  display: flex;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1; /* 显示1行,如果超过则省略 */
  overflow: hidden; /* 隐藏超出的内容 */
  text-overflow: ellipsis;
  max-width: 550px;
  font-size: 30px;
  margin-left: 10px;
}
</style>
