<template>
  <div class="d-flex justify-content-between bg-warning p-2">
    <span class="text-dark btn-sm btn-outline-light"
      v-for="chr in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']"
      :key="chr" @click="handleAlphaClicked(chr)">{{ chr }}</span>
    <span class="text-dark btn-sm btn-outline-light" @click="handleNumberClicked('09')">09</span>
  </div>
</template>

<script setup>
const emit = defineEmits(['alphaClicked'])
const handleAlphaClicked = (v) => emit('alphanumClicked', v, true)
const handleNumberClicked = (v) => emit('alphanumClicked', v, false)
</script>

