<script setup lang="ts">
import ChooseLang from '@/components/ChooseLang.vue'
import UploadComponent from '@/components/DocTranslation/UploadComponent.vue'
import DownloadComponent from '@/components/DocTranslation/DownloadComponent.vue'
import { LangStore } from '@/stores/language'
import { ContentStore } from '@/stores/translation'

import { computed } from 'vue'
import { storeToRefs } from 'pinia'

const langStore = LangStore()
const contentStore = ContentStore()

const { getSourceLang, getTargetLang } = storeToRefs(langStore)
const { isLoading } = storeToRefs(contentStore)

// 获取所有语言列表和目标语言列表
const sourceLang = computed(() => langStore.getSourceLangKeys())
const targetLangList = computed(() => langStore.getTargetLangKeys())
</script>

<template>
  <div class="doc-translation">
    <div class="lang-choose">
      <div class="source-lang">
        <ChooseLang :LangList="sourceLang" :activeLang="getSourceLang" :chooseKind="'source'">
        </ChooseLang>
      </div>
      <div class="arrow" style="margin-right: 30px; margin-left: 25px">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 1024 1024">
          <path
            fill="currentColor"
            d="M754.752 480H160a32 32 0 1 0 0 64h594.752L521.344 777.344a32 32 0 0 0 45.312 45.312l288-288a32 32 0 0 0 0-45.312l-288-288a32 32 0 1 0-45.312 45.312z"
          ></path>
        </svg>
      </div>
      <div class="target-lang">
        <ChooseLang
          :LangList="targetLangList"
          :activeLang="getTargetLang"
          :chooseKind="'target'"
        ></ChooseLang>
      </div>
    </div>
    <div class="input-box">
      <UploadComponent></UploadComponent>
    </div>
    <div class="output-box">
      <DownloadComponent></DownloadComponent>
      <div v-show="isLoading" class="loading">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.doc-translation {
  width: 90%;
  margin-top: 20px;
  margin-left: 83px;
  background-color: white;
  border-radius: 10px;
  border: rgba(0, 0, 0, 0.1) 1px solid;
  box-shadow: 0 0 5px 0 rgba(218, 225, 232, 0.8);
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 8fr;
  grid-template-areas:
    'lang-choose lang-choose'
    'input-box output-box';

  & > * {
    padding: 20px;
  }

  .lang-choose {
    max-height: 50px;
    grid-area: lang-choose;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    border-bottom: rgba(218, 225, 232, 0.5) 2px solid;
    z-index: 1;

    .source-lang {
      width: 45%;
      flex-grow: 1;
      display: flex;
      justify-content: flex-start;
    }
    .change-btn {
      margin: 0 28px;
    }
    .target-lang {
      width: 45%;
      flex-grow: 1;
      display: flex;
      justify-content: flex-start;
    }
  }
  .input-box {
    grid-area: input-box;
    border-right: rgba(218, 225, 232, 0.5) 2px solid;
  }
  .output-box {
    grid-area: output-box;

    .loading {
      padding: 20px;
      justify-self: center;
      display: flex;
      justify-content: space-between;
      width: 100px; /* 根据需要调整宽度 */

      .dot {
        width: 10px;
        height: 10px;
        background-color: rgb(40, 40, 40);
        border-radius: 50%;
        animation: dot-jump 1.2s infinite;
      }
      .dot:nth-child(1) {
        animation-delay: -0.8s; /* 第一个点的延迟 */
      }

      .dot:nth-child(2) {
        animation-delay: -0.4s; /* 第二个点的延迟 */
      }

      .dot:nth-child(3) {
        animation-delay: 0s; /* 第三个点的延迟 */
      }
    }
  }
}

@keyframes dot-jump {
  0%,
  60% {
    transform: translateY(0);
  }
  80% {
    transform: translateY(-10px); /* 调整跳动的距离 */
  }
  100% {
    transform: translateY(0);
  }
}
</style>
