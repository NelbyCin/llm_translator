<script setup lang="ts">
import { ref } from 'vue'

const isRotate = ref(false)
const changeSource = () => {
  isRotate.value = !isRotate.value
}
</script>

<template>
  <div class="change-btn" @click="changeSource">
    <div
      :class="{ rotate: isRotate }"
      style="
        height: 25px;
        width: 25px;
        transition: 0.3s ease-in-out;
        transform-origin: center center;
      "
    >
      <svg>
        <path
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M8 7L20 7M20 7L16 3M20 7L16 11M16 17L4 17M4 17L8 21M4 17L8 13"
        ></path>
      </svg>
    </div>
  </div>
</template>

<style scoped lang="scss">
.change-btn {
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 5px;
  transition: 0.3s ease;

  &:hover {
    cursor: pointer;
    background-color: rgba(218, 225, 232, 0.5);
  }

  svg {
    width: 25px;
    height: 25px;
  }
}

.rotate {
  transform: rotateZ(180deg);
}
</style>
