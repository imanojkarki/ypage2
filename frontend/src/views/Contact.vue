<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <div class="card-header bg-warning d-flex justify-content-between p-1">
        <span class="fw-bold ms-1"><i :class="config.Icon_Contact"></i> {{ config.Form_Contact_Title }} </span>
        <span class="close px-1" @click="$emit('close')"> <i :class="config.Icon_Close"></i></span>
      </div>
      <div class="modal-body p-1">
        <Alertbox2 :msg_el="msg2.el" :msg_text="msg2.text"></Alertbox2>
        <div class="row row-cols-2 g-1">
          <!-- <input type="hidden" name="slug" :value="props.recordset.contact.slug" /> -->

          <div class="col">
            <div class="card mb-1">
              <div class="card-header fw-bold p-1"><i :class="config.Icon_Badge"></i> Name & Address</div>
              <div class="card-body p-1">
                <div class="input-group input-group-sm mb-1">
                  <input type="text" class="form-control" name="name" v-model="model.contact.name" maxlength="50"
                    minlength="2" placeholder="Name" />
                </div>
                <div class="input-group input-group-sm mb-1">
                  <input type="text" class="form-control" name="address" v-model="model.contact.address" maxlength="50"
                    minlength="2" placeholder="address" />
                </div>
              </div>
            </div>
            <div class="card">
              <div class="card-header fw-bold p-1"><i :class="config.Icon_Groups"></i> Group </div>
              <div class="card-body p-1">
                <select class="form-select form-select-sm" name="group2ms" v-model="model.groupm2ms" size="14" multiple>
                  <option v-for="r in props.groups" :key="r.slug" :value="r.id"
                    :selected="model.groupm2ms.includes(r.id)"> {{ r.group }} </option>
                </select>
              </div>
              <small class="card-footer p-1">Ctrl+Click for multi select group</small>
            </div>
          </div>
          <div class="col">
            <div class="card">
              <div class="card-header fw-bold p-1"><i :class="config.Icon_Mobile"></i> Phone No </div>
              <div class="card-body p-1">
                <div class="input-group input-group-sm mb-1" v-for="(r, i) in model.phones" :key="i">
                  <input type="text" class="form-control" v-model="model.phones[i]" maxlength="10" minlength="2"
                    placeholder="landline/mobile" />
                  <span class="input-group-text text-danger btn2" v-show="i > 0" @click.prevent="handleDelete(i)"><i
                      :class="config.Icon_Delete"></i></span>
                  <span class="input-group-text btn2" v-show="i === 0" @click.prevent="handleAdd()"><i
                      :class="config.Icon_Plus"></i></span>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
      <div class="d-flex bd-highligh mt-1">
        <button type="button" class="btn btn-sm mx-1" @click.prevent="handleSubmit(true, false)"
          :class="model.contact.name.length > 2 && model.phones[0].length > 3 ? 'btn-primary' : 'btn-danger disabled'"
          v-show="!model.editmode"><i :class="config.Icon_Save"></i> Save & Add New </button>
        <button type="button" class="btn btn-sm btn-info mx-1" @click.prevent="handleSubmit(false, false)"
          :class="model.contact.name.length > 2 && model.phones[0].length > 3 ? '' : 'disabled'">
          <i :class="config.Icon_Save"></i> Save & {{ model.editmode ? 'Update' : 'Exit' }} </button>
        <button type="button" class="btn btn-sm btn-danger mx-1" v-show="model.editmode"
          @click.prevent="handleSubmit(false, true)"> <i :class="config.Icon_Delete"></i> Delete
        </button>
      </div>
    </div>
  </div>

</template>

<script setup>

import { reactive, watchEffect } from "vue";
import Alertbox2 from "../components/Alertbox2.vue";
import config from "../composables/config.js"

const props = defineProps({ slug: { type: String, default: config.Slug_Defualt }, groups: { type: Array, default() { return [] } } })
const emit = defineEmits(['getContact', 'onSaveData', 'close'])

const model = reactive({
  editmode: false,
  contact: { slug: config.Slug_Defualt, name: '', address: '', is_deleted: false },
  phones: [''],
  groupm2ms: [0]
})
const msg2 = reactive({ el: config.MSG_Default, text: config.MSG_Default_Msg })
const msg2setter = (text, el) => { msg2.el = el, msg2.text = text }

watchEffect(() => emit('getContact', props.slug, model))

const handleDelete = (i) => model.phones.splice(i, 1)
const handleAdd = () => model.phones.push('')

const handleSubmit = (is_continue, is_deleted) => { // icrud, row, callback
  let ishttp_post = true
  if (is_deleted) ishttp_post = confirm(`${config.MSG_Delete} ${model.contact.name}`)
  if (!is_deleted && model.phones.length > 1) model.phones = [...new Set(model.phones)]
  if (ishttp_post) emit('onSaveData', is_continue, is_deleted ? config.ICRUD_Delete : model.editmode ? config.ICRUD_Update : config.ICRUD_Create, model, msg2setter)

  model.editmode = false
  model.contact = { slug: config.Slug_Defualt, name: '', address: '', is_deleted: false }
  model.phones = ['']
  model.groupm2ms = [0]

  if (!is_continue) setTimeout(() => emit('close'), 2222)

}

</script>

<style scoped>
.modal-content {
  width: 575px;
  height: 600px;
  min-height: 350px;
  min-width: 375px;
}
</style>