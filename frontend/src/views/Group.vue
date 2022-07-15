<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header bg-warning d-flex justify-content-between p-1">
        <span class="fw-bold ms-1"><i :class="config.Icon_Groups"></i> {{ config.Form_Group_Title }} </span>
        <span class="close px-1" @click="$emit('close')"> <i :class="config.Icon_Close"></i></span>
      </div>
      <div class="modal-body p-1">
        <Alertbox2 :msg_el="msg2.el" :msg_text="msg2.text"></Alertbox2>
        <div class="row row-cols-2 g-1">
          <div class="col" v-for="(r, i) in props.recordset" :key="r.slug">
            <div class="input-group input-group-sm">
              <span class="input-group-text text-danger btn2" @click.prevent="handleDelete(r, i)">
                <i :class="config.Icon_Delete"></i></span>
              <input type="text" class="form-control form-control-sm" v-model="r.group" maxlength="15" minlength="2"
                placeholder="group name" autocomplete="off" />
              <span class="input-group-text btn2"
                :class="r.group.length > 2 ? 'text-success pointer' : 'text-secondary disabled'"
                @click.prevent="handleSave(r, i)"><i :class="config.Icon_Save"></i></span>
            </div>
          </div>
          <div class="col">
            <div class="input-group input-group-sm">
              <span class="input-group-text btn2"><i :class="config.Icon_Group"></i></span>
              <input type="text" class="form-control form-control-sm" v-model="model.group" maxlength="15" minlength="2"
                placeholder="group name" ref="focusRef" />
              <span class="input-group-text btn2"
                :class="model.group.length > 1 ? 'text-success pointer' : 'text-secondary disabled'"
                @click.prevent="handleSave(model, -1)"><i :class="config.Icon_Save"></i></span>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import Alertbox2 from "../components/Alertbox2.vue";
import config from "../composables/config.js"


const emit = defineEmits(['onSaveData'])
const props = defineProps({ recordset: { type: Array, default() { return [] } } })
const model = reactive({ slug: config.Slug_Defualt, group: '', is_deleted: false })
const msg2 = reactive({ el: config.MSG_Default, text: config.MSG_Default_Msg }) 
const msg2setter = (text, el) => { msg2.el = el, msg2.text = text }

const handleDelete = (form, i) => {
  if (confirm(`${config.MSG_Delete} ${form.group}`)) emit('onSaveData', config.ICRUD_Delete, form, i, msg2setter)
}
const handleSave = (form, i) => emit('onSaveData', i === -1 ? config.ICRUD_Create : config.ICRUD_Update, form, i, msg2setter)

const focusRef = ref(null)
const focusX = () => setTimeout(() => { focusRef.value.focus()}, 333)

defineExpose({focusX})
</script>

<style scoped>
.modal-content {
  width: 600px;
  height: 500px;
  min-height: 350px;
  min-width: 350px;
}
</style>