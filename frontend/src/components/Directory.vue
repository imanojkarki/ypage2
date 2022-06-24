<template>
  <div class="table-responsive">
    <table class="table table-bordered table-condensed table-hover table-sm" id="xlTable">
      <thead @click="$emit('rowContactClicked', config.Slug_Defualt, -1)">
        <tr>
          <th width="35px;" class="btn2"><i :class="config.Icon_AddNew"></i></th>
          <th><i :class="config.Icon_Contact"></i> Contact</th>
          <th><i :class="config.Icon_Mobile"></i> Number</th>
        </tr>
      </thead>
      <tbody class="border-top-0" v-if="props.recordset && props.recordset.length > 0">
        <tr v-for="(r, i) in props.recordset" :key="r.slug">
          <td scope="row" @click="$emit('rowContactClicked', r.slug, i)" class="btn2">{{ i + 1 }}</td>
          <td :class="r.is_highlight ? 'bg-warning text-dark' : '' ">{{ r.contact }}</td>
          <td :class="r.is_highlight ? 'bg-warning text-dark' : '' ">{{ r.phones }}</td>
        </tr>
      </tbody>
      <tr v-else>
        <th scope="row"><i :class="config.Icon_EOF"></i></th>
        <td colspan="2">There is no record</td>
      </tr>
    </table>
  </div> <!-- eof table-responsive -->
</template>
<script setup>
import config from "../composables/config.js"
const props = defineProps({ recordset: { type: Array, default() { return [] } } })
</script>
<style scoped>
.table-responsive table thead tr th,
.table-responsive table tr td[scope=row] {
  background-color: #EFEDDE !important;
  text-align: center !important;
  vertical-align: middle !important;
}

.table-responsive table tr td[scope=row] {
  font-weight: normal !important;
}

.table-responsive table tr td {
  text-align: left !important;
}
</style>