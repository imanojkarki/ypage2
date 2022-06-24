<template>
  <div class="alert d-flex align-items-center fade show mb-1 p-1" :class="config.MSG_Class[msgbox.el]">
    <i class="me-1" :class="config.MSG_Icon[msgbox.el]"></i> {{ msgbox.text }}
  </div>
</template>

<script setup>
import { reactive, watchEffect } from "vue";
import config from "../composables/config.js"

const props = defineProps({
  msg_el: { type: Number, default: config.MSG_Default },
  msg_text: { type: String, default: config.MSG_Default_Msg }
})

const msgbox = reactive({
  el: { type: Number, default: config.MSG_Default },
  text: { type: String, default: config.MSG_Default_Msg }
})

watchEffect(() => {
  if (props.msg_text !== config.MSG_Default) {
    msgbox.el = props.msg_el
    msgbox.text = props.msg_text
    setTimeout(() => {
      msgbox.el = config.MSG_Default
      msgbox.text = config.MSG_Default_Msg
    }, 6666)
  }
})

</script>

