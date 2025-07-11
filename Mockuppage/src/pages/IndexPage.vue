<template>
  <q-page>
    <q-form @submit="onSubmit" @reset="onReset">
      <TermComponent v-for="term in dataDefinition" :key="term.notation" :term="term" />
      <q-btn label="Submit" type="submit" color="primary" />
      <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
       
      <pre>{{ formData }}</pre>
      
    </q-form>
  </q-page>
</template>

<script setup>
import { ref, provide } from 'vue';
import TermComponent from 'src/components/termComponent.vue';
import docuData from 'src/data/docu.json';

const dataDefinition = ref(docuData);
const formData = ref({});

function createInitialFormData(terms) {
  const state = {};
  for (const term of terms) {
    if (term.Feldwert) {
      if (term.Wiederholbar === 'Ja') { 
        state[term.notation] = ['']; 
      } else {
        state[term.notation] = '';
      }
    }
    
    if (term.narrower) { 
      Object.assign(state, createInitialFormData(term.narrower));
    }
  }
  return state;
}

formData.value = createInitialFormData(dataDefinition.value);

const onReset = () => {
  formData.value = createInitialFormData(dataDefinition.value);
  console.log('Form has been reset!');
};

const onSubmit = () => {
  console.log('Final Form Data:', formData.value);
  alert('Form submitted! Check the console for the data.');
};

provide('formManager', {
  formData,
  addField: (notation) => {
    if (Array.isArray(formData.value[notation])) {
      formData.value[notation].push('');
    }
  },
  removeField: (notation, index) => {
    if (Array.isArray(formData.value[notation]) && formData.value[notation].length > 1) {
      formData.value[notation].splice(index, 1);
    }
  }
});
</script>