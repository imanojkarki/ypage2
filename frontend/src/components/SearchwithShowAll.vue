<template>
  <div class="input-group input-group-sm p-0 m-0" style="width: 130px">
    <label class="input-group-text btn2" for="txtsearch"><i :class="config.Icon_Search"></i></label>
    <input type="text" @keyup.prevent="handleOnChangeText($event.target.value)" class="form-control"
      placeholder="search name" />
    <label class="input-group-text btn2" v-if="props.isfilter" @click="$emit('filterClicked')">
      <i :class="config.Icon_Filter"></i></label>
  </div>
</template>

<script setup>
import config from "../composables/config.js"
const props = defineProps({ isfilter: { type: Boolean, default: false } })
const emit = defineEmits(['filterClicked', 'filterText'])
const handleOnChangeText = (v) => emit('filterText', v)
</script>