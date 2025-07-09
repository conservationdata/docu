<template>
  <q-page>
    <q-form @submit="onSubmit" @reset="onReset">
      <div v-for="term in dataDefinition" :key="term.notation">
        <TermComponent :term="term" />
      </div>
      <div>
        <q-btn label="Submit" type="submit" color="primary" />
        <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
      </div>
      <pre>{{ formData }}</pre>
    </q-form>
  </q-page>
</template>

<script setup>
import { ref, provide } from 'vue';
import TermComponent from 'src/components/termComponent.vue';
import docuData from 'src/data/docu.json'; // The static definition

// 1. DATA DEFINITION
const dataDefinition = ref(docuData);

// 2. FORM STATE
const formData = ref({});

// 3. HELPER FUNCTION TO CREATE THE INITIAL FORM STATE
function createInitialFormData(terms) {
  const state = {};
  for (const term of terms) {
    if (term.Feldwert) { // Only create entries for fields that can have a value
      if (term.Wiederholbar === 'Ja') { // If repeatable, initialize with an array
        state[term.notation] = ['']; // Start with one empty input
      } else {
        state[term.notation] = '';
      }
    }
    // Recurse for nested terms
    if (term.narrower) { //
      Object.assign(state, createInitialFormData(term.narrower));
    }
  }
  return state;
}

// 4. INITIALIZE AND MANAGE STATE
formData.value = createInitialFormData(dataDefinition.value);

const onReset = () => {
  formData.value = createInitialFormData(dataDefinition.value);
  console.log('Form has been reset!');
};

const onSubmit = () => {
  console.log('Final Form Data:', formData.value);
  // Here you would send formData.value to your backend
  alert('Form submitted! Check the console for the data.');
};

// 5. PROVIDE THE FORM MANAGER TO ALL CHILDREN
provide('formManager', {
  formData,
  // Function to add a new instance for a repeatable field
  addField: (notation) => {
    if (Array.isArray(formData.value[notation])) {
      formData.value[notation].push(''); // Add a new empty string to the array
    }
  },
  // Function to remove an instance from a repeatable field
  removeField: (notation, index) => {
    if (Array.isArray(formData.value[notation]) && formData.value[notation].length > 1) {
      formData.value[notation].splice(index, 1); // Remove the item at the given index
    }
  }
});
</script>