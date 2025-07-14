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
const formData = ref([]);

function createInitialFormData(terms, path = []) {
  const formTerms = [];
  for (const [index, term] of terms.entries()) {
    const currentPath = [...path, index];
    const formTerm = {
      path: currentPath,
      notation: term.notation,
      definition:term.definition,
      Wiederholbar:term.Wiederholbar,
      Verpflichtungsgrad:term.Verpflichtungsgrad,
      Feldwert:term.Feldwert,
    }
    if (term.Feldwert) {
      formTerm.value = "";
    }
    if (term.narrower) {
      formTerm.narrower = createInitialFormData(term.narrower, currentPath);
    }
    formTerms.push(formTerm);
  }
  return formTerms;
}

formData.value = createInitialFormData(dataDefinition.value);
console.log("Initial form data:", formData.value)

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
  
  addFieldAtPath(path) {
    let parentArray = formData.value;
    for (let i = 0; i < path.length - 1; i++) {
      parentArray = parentArray[path[i]].narrower;
    }
    const index = path[path.length - 1];
    const node = parentArray[index];

    if (node['Wiederholbar:'] === 'Ja') {
      const clone = structuredClone(node);
      resetValues(clone);
      parentArray.splice(index + 1, 0, clone);
      recalculatePaths(formData.value);
    }
  },

  removeFieldAtPath(path) {
    let parentArray = formData.value;
    for (let i = 0; i < path.length - 1; i++) {
      parentArray = parentArray[path[i]].narrower;
    }
    const index = path[path.length - 1];

    const notation = parentArray[index].notation;
    const sameNotationCount = parentArray.filter(n => n.notation === notation).length;
    if (sameNotationCount > 1) {
      parentArray.splice(index, 1);
      recalculatePaths(formData.value);
    }
  }
});

function resetValues(node) {
  if ('value' in node) {
    node.value = '';
  }
  if (Array.isArray(node.narrower)) {
    node.narrower.forEach(child => resetValues(child));
  }
}

function recalculatePaths(nodes, path = []) {
  nodes.forEach((node, index) => {
    const currentPath = [...path, index];
    node.path = currentPath;
    if (Array.isArray(node.narrower)) {
      recalculatePaths(node.narrower, currentPath);
    }
  });
}


</script>