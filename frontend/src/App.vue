<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<style scoped>
#app {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

/* 移动端优化 */
@media (max-width: 768px) {
  #app {
    overflow-x: hidden;
    overflow-y: auto;
  }
}
</style>