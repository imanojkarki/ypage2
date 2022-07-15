<template>
  <div class="d-flex justify-content-between bg-light p-1">
    <a class="fw-bold mt-1 ms-2 text-decoration-none text-dark" href="/">
      <i :class="config.Apps_Logo"></i> {{ config.Apps_Title }}
    </a>
    <SearchwithShowAll v-show="yPage.dbset.contacts && yPage.dbset.contacts.length > 1" :isfilter="hasFilter"
      @filterClicked="showAll" @filterText="showText"></SearchwithShowAll>
    <SelectGroup @formGroupClicked="openModalGroup" @selectOnChange="viewByGroup" :groups="yPage.dbset.groups"
      :groupid="filterGroupID"></SelectGroup>
  </div>
  <AlphaNumericButton @alphanumClicked="viewByAlphaNum"></AlphaNumericButton>

  <Directory :recordset="yPage.directory" @rowContactClicked="openModalContact"></Directory>

  <Teleport to="#form">
    <Group v-show="showModalGroup" :recordset="yPage.dbset.groups" @onSaveData="onChangeGroup"
      @close="showModalGroup = false" ref="refGroup"></Group>
    <Contact v-show="showModalContact" :slug="yPage.slug" :groups="yPage.dbset.groups" @getContact="getContactBySlug"
      @onSaveData="onChangePhone" @close="handleCloseModalContact" ref="refContact"></Contact>
  </Teleport>


</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import SearchwithShowAll from "./components/SearchwithShowAll.vue";
import SelectGroup from "./components/SelectGroup.vue";
import AlphaNumericButton from "./components/AlphaNumericButton.vue";
import Directory from "./components/Directory.vue";
import config from "./composables/config.js"
import fetchapi from "./composables/fetchapi.js"

import Group from "./views/Group.vue";
import Contact from "./views/Contact.vue";


const yPage = reactive({
  dbset: { csrf: '', groups: [], contacts: [], phones: [], groupm2ms: [] }, directory: [], slug: '', el: -1, reload: false
})

const showModalGroup = ref(false)
const showModalContact = ref(false)
const refGroup = ref()
const refContact = ref()

const hasFilter = ref(false)
const filterText = ref('')
const filterGroupID = ref(0)
/*
Format Document (Shift+Alt+F) - Format the entire active file. Format Selection (Ctrl+K Ctrl+F) - Format the selected text.
On Windows Shift + Alt + F On Mac Shift + Option + F On Linux Ctrl + Shift + I
*/

const openModalGroup = () => {
  showModalContact.value = false
  showModalGroup.value = true
  refGroup.value.focusX()
}

const viewByAlphaNum = (v, isAlpha = true) => {
  hasFilter.value = true
  filterText.value = v
  populate_contact(yPage.dbset.contacts.filter(j => isAlpha ? j.name.toUpperCase().startsWith(v) : /^\d/.test(j.name)))
}

const viewByGroup = (v) => {
  hasFilter.value = true
  filterGroupID.value = v
  const groups = [... new Set(yPage.dbset.groupm2ms.filter(r => r.group_fk === v).map(j => j.contact_fk))]
  populate_contact(yPage.dbset.contacts.filter(r => groups.includes(r.id)))
}

const showAll = () => {
  hasFilter.value = false
  filterText.value = ''
  filterGroupID.value = 0
  apps_init().then(() => populate_contact(yPage.dbset.contacts))
}

const showText = (v) => {
  const table = document.getElementById("xlTable")
  const [tr, th] = [table.getElementsByTagName("tr"), table.getElementsByTagName("th")]

  for (let i = 1; i < tr.length; i++) {
    tr[i].style.display = "none"
    for (let j = 0; j < th.length; j++) {
      let td = tr[i].getElementsByTagName("td")[j];
      if (td) {
        if (td.innerHTML.toUpperCase().indexOf(v.toUpperCase()) > -1) {
          tr[i].style.display = ""
          break
        }
      }
    }
  }
}

const dbset_url = `${config.Apps_Url}/${config.API_Request_4Index}${config.ICRUD_Index}/${config.Slug_Defualt}/`
const apps_init = async () => yPage.dbset = await fetchapi.get_data(dbset_url).then((r) => r.json())

const populate_contact = async (contacts) => {
  yPage.directory = []
  contacts.forEach(r => {
    const contact = r.name + (r.address && r.address.length > 0 ? `, ${r.address}` : '')
    const phones = yPage.dbset.phones.filter(j => j.contact_fk === r.id).map(e => e.phone).join(",")
    yPage.directory.push({ slug: r.slug, contact, phones, is_highlight: false })
  })
}

onMounted(() => apps_init().then(() => populate_contact(yPage.dbset.contacts)))

const openModalContact = (slug, el) => {
  showModalContact.value = true
  yPage.el = el
  if (el > -1) yPage.directory[el].is_highlight = true
  yPage.slug = slug

  showModalGroup.value = false
  refContact.value.focusX()

}

const getContactBySlug = (slug, row) => {
  row.editmode = false
  row.contact = { slug, name: '', address: '', is_deleted: false }

  row.phones = ['']
  row.groupm2ms = [0]

  if (slug !== config.Slug_Defualt) {
    const contact = yPage.dbset.contacts.find(r => r.slug === slug)

    if (contact && typeof contact === "object") {
      row.editmode = true
      row.contact = { ...row.contact, name: contact.name, address: contact.address }

      const phones = yPage.dbset.phones.filter(r => r.contact_fk === contact.id).map(j => j.phone || '')
      row.phones = phones.length > 0 ? phones : ['']
      row.groupm2ms = yPage.dbset.groupm2ms.filter(r => r.contact_fk === contact.id).map(j => j.group_fk)

    }
  }
}

const onChangeGroup = async (icrud, row, index, callback) => {
  callback(config.MSG_Processing, config.MSG_Loading)
  let group, msg_text, msg_el, ishttp_post
  if (config.ICRUD_Delete === icrud) {
    group = yPage.dbset.groupm2ms.filter(r => r.group_fk === row.id)
    if (group.length > 0) {
      const names = group.map((j) => yPage.dbset.contacts.find(r => r.id === j.contact_fk)).map(e => e.name).join(",")
      msg_text = `Unable to delete as it is in used with ${names}`, msg_el = config.MSG_Failure
    } else {
      yPage.dbset.groups.splice(index, 1)
      msg_text = `Delete successfully`, msg_el = config.MSG_Success, ishttp_post = true
      row.is_deleted = true
    }
  } else {
    group = yPage.dbset.groups.findIndex(r => r.group.toUpperCase() == row.group.toUpperCase() && r.id !== row.id)
    if (group !== -1) {
      msg_text = `Unable to save as it is already in used`, msg_el = config.MSG_Failure
    } else {
      msg_text = `Saved successfully`, msg_el = config.MSG_Success, ishttp_post = true
    }
  }
  if (ishttp_post) { // url, body, csrf
    const ajax = await fetchapi.save_data(`${config.Apps_Url}/${config.API_Request_4Group}${icrud}/${row.slug}/`, row, yPage.dbset.csrf).then((r) => r.json())
    yPage.dbset.csrf = ajax.csrf
    if (icrud === config.ICRUD_Create) {
      yPage.dbset.groups.push(ajax.new_data)
      row.slug = config.Slug_Defualt
      row.group = ''
    }
  }
  callback(msg_text, msg_el)
}

const onChangePhone = async (is_staywithmodal, icrud, row, callback) => {
  yPage.reload = true
  callback(config.MSG_Processing, config.MSG_Loading)
  const ajax = await fetchapi.save_data(`${config.Apps_Url}/${config.API_Request_4Contact}${icrud}/${row.contact.slug}/`, row, yPage.dbset.csrf).then((r) => r.json())
  yPage.dbset.csrf = ajax.csrf

  if (is_staywithmodal && icrud === config.ICRUD_Create) {
    const { slug, name, address } = ajax.new_data
    const contact = name + (address && address.length > 0 ? `, ${address}` : '')
    const phones = ajax.phones.toString()
    yPage.directory = [{ slug, contact, phones, is_highlight: true }, ...yPage.directory]
  }
  if (!is_staywithmodal) apps_init().then(() => populate_contact(yPage.dbset.contacts))
  callback(is_staywithmodal ? config.MSG_FillAllNextField : icrud === config.ICRUD_Delete ? config.MSG_DeletedSuccessfully : config.MSG_SavedSuccessfully, config.MSG_Success)

}

const handleCloseModalContact = () => {
  if (yPage.reload) {
    apps_init().then(() => populate_contact(yPage.dbset.contacts))
    if (hasFilter.value) {
      if (filterGroupID.value > 0) {
        viewByGroup(filterGroupID.value)
      } else {
        viewByAlphaNum(filterText.value, filterText.value.length === 1)
      }
    }
    yPage.reload = false
  } else {
    if (yPage.el > -1) yPage.directory[yPage.el].is_highlight = false
  }
  showModalContact.value = false
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.close:hover {
  background: #f00 !important;
  color: #fff !important;
}

.btn2:hover,
.table-responsive table .btn2:hover,
.table-responsive table tr td[scope=row].btn2:hover {
  background: #ffc107 !important;
  color: #000 !important;
}

.modal-overlay {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  display: grid;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  border-radius: 2px;
  display: inline-block;
  margin: 1rem;
  position: relative;
  box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
  justify-self: center;
  background: #f9fafb !important;
  color: #000 !important;

}
</style>
