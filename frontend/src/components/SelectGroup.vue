<template>
  <div class="input-group input-group-sm p-0 m-0" style="width: 219px">
    <label class="input-group-text btn2" for="selGroup" @click="$emit('formGroupClicked')"><i
        :class="config.Icon_AddNew"></i></label>
    <select class="form-select" id="selGroup" @change="$emit('selectOnChange', parseInt($event.target.value))"
      :value="props.groupid">
      <option selected value="0" disabled>Choose group...</option>
      <option v-for="r in props.groups" :key="r.slug" :value="r.id">
        {{ r.group }}
      </option>
    </select>
    <label class="input-group-text" for="selGroup"><i :class="config.Icon_Groups"></i></label>
  </div>
</template>
<script setup>
import config from "../composables/config.js"
const props = defineProps({ groups: { type: Object, default() { return [] } }, groupid: { type: Number, default: 0 } })
</script>
