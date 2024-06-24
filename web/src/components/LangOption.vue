<script setup lang="ts">
import { computed } from 'vue'
import { LangStore } from '@/stores/language'

const langStore = LangStore()

const props = defineProps(['currentLang', 'activeLang', 'chooseKind'])

const currentLang = computed(() => props.currentLang)
const activeLang = computed(() => props.activeLang)
const chooseKind = computed(() => props.chooseKind)

function chooseLang(lang_name: string) {
  chooseKind.value == 'source'
    ? langStore.changeSourceLang(lang_name)
    : langStore.changeTargetLang(lang_name)
}
</script>

<template>
  <div class="options" @click="chooseLang(currentLang)">
    <svg
      :style="{ opacity: currentLang == activeLang ? 1 : 0 }"
      xmlns="http://www.w3.org/2000/svg"
      color="rgba(1, 119, 169, 0.8)"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="3"
      stroke="currentColor"
      aria-hidden="true"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        vector-effect="non-scaling-stroke"
        d="M4.5 12.75l6 6 9-13.5"
      ></path>
    </svg>
    <p :class="{ activated: currentLang == activeLang }">
      <slot name="lang-name"></slot>
    </p>
  </div>
</template>

<style scoped lang="scss">
.options {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 10px 15px;
  gap: 30px;
  width: 230px;
  height: 40px;
  border-radius: 5px;
  transition: 0.3s ease;

  &:hover {
    cursor: pointer;
    background-color: rgba(218, 225, 232, 0.5);
  }

  svg {
    width: 20px;
    height: 20px;
  }

  p {
    font-family: Arial, sans-serif;
    font-weight: bold;
    font-size: 16px;
  }
}

.activated {
  color: rgba(1, 119, 169, 0.8);
}
</style>
