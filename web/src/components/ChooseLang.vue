<script setup lang="ts">
import LangOption from '@/components/LangOption.vue'
import { computed, ref, watch } from 'vue'

const props = defineProps(['LangList', 'activeLang', 'chooseKind'])

const LangList = computed(() => props.LangList)
const activeLang = computed(() => props.activeLang)
const chooseKind = computed(() => props.chooseKind)
const searchLangList = ref([])

const isFlipped = ref(false)
const searchInput = ref('')

const chooseLang: () => void = () => {
  searchInput.value = ''
  searchLangList.value = []
  isFlipped.value = !isFlipped.value
  if(isFlipped.value) {
    setTimeout(() => {
      const langMenu = document.querySelector('.lang-menu') as HTMLDivElement | null
      langMenu?.focus()
    }, 0)
  }
}

function handleMenuBlur() {
  setTimeout(() => {
    const searchInput = document.querySelector('.search-input') as HTMLInputElement
    const isSearchInputFocused = document.activeElement === searchInput
    if (!isSearchInputFocused) {
      isFlipped.value = false
      setTimeout(() => {
        const langMenu = document.querySelector('.lang-menu') as HTMLDivElement | null
        langMenu?.focus()
      }, 0)
    }
  }, 0)
}

watch(searchInput, (newVal) => {
  if (newVal === '') searchLangList.value = []
  searchLangList.value = LangList.value.filter((lang: string) => lang.includes(newVal))
  if (searchLangList.value.length == 0) searchLangList.value = []
})
</script>

<template>
  <div class="change-lang">
    <div class="choose-btn" @click="chooseLang" :class="{ isActivated: isFlipped }">
      {{ activeLang }}
      <div
        style="width: 20px; height: 20px; transition: 0.3s ease"
        :class="{ isFlipped: isFlipped }"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            vector-effect="non-scaling-stroke"
            d="M19.5 8.25l-7.5 7.5-7.5-7.5"
          ></path>
        </svg>
      </div>
    </div>
    <Transition name="lang-menu-open">
      <div class="lang-menu" v-if="isFlipped" @blur="handleMenuBlur" tabindex="0" ref="langMenu">
        <div class="search-box">
          <svg
            class="h-6 flex-none"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z"
              stroke="#9BA3AC"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            ></path>
          </svg>
          <input
            @blur="handleMenuBlur"
            v-model="searchInput"
            type="text"
            placeholder="搜索语言"
            class="search-input"
          />
        </div>
        <div class="lang-options">
          <LangOption
            @click="
              () => {
                isFlipped = false
              }
            "
            v-show="searchLangList.length == 0 && searchInput == ''"
            v-for="(lang, index) in LangList"
            :key="index"
            :activeLang="activeLang"
            :currentLang="LangList[index]"
            :chooseKind="chooseKind"
          >
            <template #lang-name>
              {{ lang }}
            </template>
          </LangOption>
          <LangOption
            @click="
              () => {
                isFlipped = false
              }
            "
            v-show="searchLangList.length != 0"
            v-for="(lang, index) in searchLangList"
            :key="index"
            :activeLang="activeLang"
            :currentLang="searchLangList[index]"
            :chooseKind="chooseKind"
          >
            <template #lang-name>
              {{ lang }}
            </template>
          </LangOption>
          <span v-show="searchLangList.length == 0 && searchInput != ''"
            >没有找到相关语言，试试其它语言吧~</span
          >
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped lang="scss">
.lang-menu-open-enter-from,
.lang-menu-open-leave-to {
  transform: scaleY(0);
}

.lang-menu-open-active,
.lang-menu-open-leave-from {
  transform: scaleY(1);
}

.change-lang {
  .choose-btn {
    padding: 0 10px;
    max-width: 300px;
    height: 40px;
    border: none;
    border-radius: 5px;
    transition: 0.3s ease;
    display: flex;
    justify-content: space-around;
    align-items: center;
    gap: 10px;
    font-family: Arial, sans-serif;
    font-weight: bold;
    font-size: 16px;

    &:hover {
      cursor: pointer;
      background-color: rgba(218, 225, 232, 0.5);
    }
  }

  .lang-menu {
    padding: 10px;
    transition: 0.3s ease-in-out;
    transform-origin: top;
    position: absolute;
    margin-top: 8px;
    width: 550px;
    height: auto;
    max-height: 450px;
    overflow: auto;
    border: 1px solid rgba(218, 225, 232, 0.5);
    border-radius: 0 0 10px 10px;
    background-color: white;
    box-shadow: 0 0 5px 0 rgba(218, 225, 232, 0.8);
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 5fr;
    grid-template-areas:
      'search-box'
      'lang-options';
    justify-content: space-around;
    gap: 10px;

    &::-webkit-scrollbar {
      width: 2px; /* 设置滚动条宽度 */
    }

    /* 滚动条滑块样式 */
    &::-webkit-scrollbar-thumb {
      background-color: #888; /* 设置滑块背景颜色 */
      border-radius: 4px; /* 设置滑块圆角 */
    }

    /* 滚动条轨道hover状态样式 */
    &::-webkit-scrollbar-track:hover {
      background-color: #f1f1f1; /* 设置轨道hover状态时的背景颜色 */
    }

    /* 滚动条滑块hover状态样式 */
    &::-webkit-scrollbar-thumb:hover {
      background-color: #555; /* 设置滑块hover状态时的背景颜色 */
    }

    &:focus {
      outline: none;
    }

    .search-box {
      margin: 0 auto;
      width: 98%;
      height: 40px;
      display: flex;
      align-items: center;
      border: 1px solid rgba(1, 119, 169, 0.8);
      border-radius: 5px;

      svg {
        width: 20px;
        height: 20px;
        margin: 0 5px 0 10px;
      }

      .search-input {
        margin: 0 5px;
        width: 95%;
        height: 100%;
        border: none;
        outline: none;
        font-size: 16px;
      }
    }

    .lang-options {
      display: flex;
      justify-content: space-between;
      align-content: flex-start;
      flex-wrap: wrap;
      padding: 5px;

      LangOption{
        margin-right: auto;
      }
    }
  }

  svg {
    width: 20px;
    height: 20px;
  }
}

.isFlipped {
  transform: rotate(-180deg);
}

.isActivated {
  background-color: rgba(218, 225, 232, 0.5);
  color: rgba(1, 119, 169, 1);
}
</style>
