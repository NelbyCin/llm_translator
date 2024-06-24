<script setup lang="ts">
import ModeChange from '@/components/ModeChange.vue'
import {LangStore} from '@/stores/language'
import { ref, watch, onMounted } from 'vue'

const langStore = LangStore()

const value = ref('chatgpt3.5')

onMounted(() => {
      langStore.setModelName(value.value);
    });

watch(value, (newValue) => {
      langStore.setModelName(newValue)
    });

const options = [
  {
    value: 'chatgpt3.5',
    label: 'chatgpt3.5',
  },
  {
    value: 'chatglm3',
    label: 'chatglm3',
  },
  {
    value: 'chatglm4',
    label: 'chatglm4',
  }
]
</script>

<template>
  <div id="app">
    <div class="header">
      <div class="logo">
        <img alt="logo" src="@/assets/icon/LOGO.png" />
        <div class="title">
          <h1>智能翻译器</h1>
          <p>您的翻译好伴侣</p>
        </div>
      </div>
      <ModeChange></ModeChange>
      <div class="model-select">
        <el-select v-model="value" placeholder="Select" style="width: 240px">
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
      </div>
    </div>
    <RouterView />
  </div>
</template>

<style scoped lang="scss">
#app {
  background-color: whitesmoke;
  display: flex;
  flex-direction: column;

  .header {
    height: 80px;
    padding: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: white;

    .logo {
      position: absolute;
      width: auto;
      height: 80px;
      left: 30px;
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: center;
      gap: 15px;
      border-bottom: 5px solid rgba(1, 119, 169, 0.5);

      img {
        width: 50px;
        height: 50px;
      }

      h1 {
        font-family: 'Arial', sans-serif;
        font-weight: bold;
      }
      p {
        margin-left: 2px;
        font-family: 'Arial', sans-serif;
      }
    }

    .model-select {
      position: absolute;
      width: auto;
      height: 80px;
      right: 120px;
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: center;
      gap: 15px;
      border-bottom: 5px solid rgba(1, 119, 169, 0.5);
    }
  }
}
</style>
