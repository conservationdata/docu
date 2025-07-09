<template>
  <q-page>
    <q-form
    @submit="onSubmit"
    @reset="onReset"
    >
      <div v-for="term in terms" :key="term.notation">
        <TermComponent :term="term" />
      </div>
      <div>
        <q-btn label="Submit" type="submit" color="primary"/>
        <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
      </div>
    </q-form>
  </q-page>
</template>

<script setup>
import { ref, provide } from 'vue';
import docuData from 'src/data/docu.json';
import TermComponent from 'src/components/termComponent.vue';

const formData = ref({});
const terms = ref(docuData);


</script>