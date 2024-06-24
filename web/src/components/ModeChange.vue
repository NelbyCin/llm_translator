<script setup lang="ts">
import {ref, computed, onMounted} from 'vue'
import {useRouter, useRoute} from 'vue-router'

const isTranslation = ref(true)
const isOpacity = computed(() => (isTranslation.value ? 1 : 0))
const router = useRouter()

onMounted(() => {
  if (router.currentRoute.value.name === 'DocTranslation') {
    isTranslation.value = true
  }
})

function ChangeMode() {
  isTranslation.value = !isTranslation.value
  if (isTranslation.value) {
    router.push({name: 'Translation'})
  } else {
    router.push({name: 'DocTranslation'})
  }
}
</script>

<template>
  <div class="mode-change">
    <TransitionGroup name="ChangeMode">
      <img
          alt="Translation"
          :style="{ opacity: isOpacity }"
          @click="ChangeMode"
          v-if="isTranslation"
          src="@/assets/icon/Translation.png"
      />
      <img
          alt="DocTranslation"
          :style="{ opacity: Math.abs(isOpacity - 1) }"
          @click="ChangeMode"
          v-if="!isTranslation"
          src="@/assets/icon/DocTranslate.png"
      />
    </TransitionGroup>
  </div>
</template>

<style scoped lang="scss">
.mode-change {
  display: flex;
  justify-content: center;
  align-items: center;

  img {
    position: absolute;
    top: 20px;
    cursor: pointer;
    width: 35px;
    height: 35px;
    transform-origin: center center -100px;
  }

  .ChangeMode-enter-active,
  .ChangeMode-leave-active {
    animation: ModeOn 1s;
  }

  .ChangeMode-enter-from,
  .ChangeMode-leave-to {
    animation: ModeOff 1s;
  }
}

@keyframes ModeOff {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  20% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(0) rotateY(90deg);
    opacity: 0;
  }
}

@keyframes ModeOn {
  0% {
    transform: scale(0) rotateY(-90deg);
  }
  80% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
