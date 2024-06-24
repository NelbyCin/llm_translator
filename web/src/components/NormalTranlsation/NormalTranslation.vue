<script setup lang="ts">
import ChooseLang from '@/components/ChooseLang.vue'
import InputComponent from '@/components/NormalTranlsation/InputComponent.vue'
import OutputComponent from '@/components/NormalTranlsation/OutputComponent.vue'
import ChangeButton from '@/components/ChangeButton.vue'
import {LangStore} from '@/stores/language'
import {ContentStore} from '@/stores/translation'
import {computed} from 'vue'
import {storeToRefs} from 'pinia'

const langStore = LangStore()
const contentStore = ContentStore()

const {getSourceLang, getTargetLang, isInput} = storeToRefs(langStore)
const {isLoading} = storeToRefs(contentStore)

// 获取所有语言列表和目标语言列表
const sourceLang = computed(() => langStore.getSourceLangKeys())
const targetLangList = computed(() => langStore.getTargetLangKeys())

// 交换按钮调用事件
function handleSwap() {
  langStore.swapLang()
  contentStore.swapContent()
}
</script>

<template>
  <div class="translation">
    <div class="lang-choose">
      <div class="source-lang">
        <ChooseLang :LangList="sourceLang" :activeLang="getSourceLang" :chooseKind="'source'">
        </ChooseLang>
      </div>
      <ChangeButton class="change-btn" @click="handleSwap"></ChangeButton>
      <div class="target-lang">
        <ChooseLang
            :LangList="targetLangList"
            :activeLang="getTargetLang"
            :chooseKind="'target'"
        ></ChooseLang>
      </div>
    </div>
    <div class="input-box" :class="{inputFocus:isInput}">
      <InputComponent></InputComponent>
    </div>
    <div class="output-box">
      <OutputComponent v-show="!isLoading"></OutputComponent>
      <div v-show="isLoading" class="loading">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.translation {
  width: 90%;
  height: 100%;
  background-color: white;
  border-radius: 10px;
  border: rgba(0, 0, 0, 0.1) 1px solid;
  box-shadow: 0 0 5px 0 rgba(218, 225, 232, 0.8);
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 7fr;
  grid-template-areas:
    'lang-choose lang-choose'
    'input-box output-box';

  & > * {
    padding: 20px;
  }

  .lang-choose {
    min-height: 50px;
    grid-area: lang-choose;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    border-bottom: rgba(218, 225, 232, 0.5) 2px solid;

    .source-lang {
      width: 45%;
      flex-grow: 1;
      display: flex;
      justify-content: flex-start;
    }

    .change-btn {
      margin: 0 20px;
    }

    .target-lang {
      width: 45%;
      flex-grow: 1;
      display: flex;
      justify-content: flex-start;
      z-index: 100;
    }
  }

  .input-box {
    height: 100%;
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

.inputFocus{
  border: 1px solid rgba(1, 119, 169, 0.8) !important;
  border-radius: 0 0 0 10px;
}
</style>
