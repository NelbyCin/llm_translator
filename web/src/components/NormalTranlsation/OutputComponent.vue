<script setup lang="ts">
import { watch } from 'vue'
import { ContentStore } from '@/stores/translation'
import { storeToRefs } from 'pinia'
import { LangStore } from '@/stores/language'
import axios from 'axios'

const URL = 'http://10.244.4.85:5000/translate'

const contentStore = ContentStore()
const langStore = LangStore()
const { targetContent, sourceContent } = storeToRefs(contentStore)
const { getTargetLang, modelName } = storeToRefs(langStore)

async function pushTranslate(text: string) {
  contentStore.setLoading()
  let lang_code = langStore.getLangCode()
  console.log(modelName.value)
  await axios
    .post(URL, {
      text: text,
      source_lang: lang_code['src'],
      target_lang: lang_code['tgt'],
      model_name: modelName.value
    })
    .then((res) => {
      console.log(res)
      contentStore.setLoading()
      contentStore.setTargetContent(res.data.trans_result.dst)
    })
    .catch((err) => {
      contentStore.setLoading()
      console.log(err)
    })
}

function handleCopy() {
  navigator.clipboard
    .writeText(targetContent.value)
    .then(() => {
      console.log('Copy success')
    })
    .catch(() => {
      console.log('Copy failed')
    })
}

watch(getTargetLang, () => {
  if (sourceContent.value === '') return
  pushTranslate(sourceContent.value)
})
</script>

<template>
  <div class="main">
    <textarea class="content-area" v-model="targetContent" disabled> </textarea>
    <div class="tool-area">
      <svg
        :style="{ opacity: targetContent != '' ? 1 : 0 }"
        :class="{ disabled: targetContent == '' }"
        @click="handleCopy"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
      >
        <path
          d="M8.75 16.25H6.875C5.83947 16.25 5 15.1867 5 13.875V4.375C5 3.06332 5.83947 2 6.875 2H14.375C15.4105 2 16.25 3.06332 16.25 4.375V6.75M10.625 21H18.125C19.1605 21 20 19.9367 20 18.625V9.125C20 7.81332 19.1605 6.75 18.125 6.75H10.625C9.58947 6.75 8.75 7.81332 8.75 9.125V18.625C8.75 19.9367 9.58947 21 10.625 21Z"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        ></path>
      </svg>
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

  .content-area {
    width: 100%;
    height: 300px;
    padding: 10px;
    font-size: 18px;
    line-height: 1.5;
    overflow-y: auto;
    border: none;
    outline: none;
    resize: none;
    background-color: transparent;
    color: #333;
    font-family: 'Arial', sans-serif;
  }

  .content-area::-webkit-scrollbar {
    visibility: hidden;
  }

  .tool-area {
    width: 100%;
    height: 50px;
    display: flex;
    justify-content: flex-end;
    align-items: center;

    svg {
      transition: 0.3s ease-in-out;
      width: 50px;
      height: 50px;
      padding: 6px;
      border-radius: 6px;
      margin: 10px 20px;

      &:hover {
        cursor: pointer;
        background-color: rgba(242, 244, 247, 0.8);
      }
    }
  }
}

.disabled {
  pointer-events: none;
  opacity: 0.5;
}
</style>
