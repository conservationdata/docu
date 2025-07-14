<template>
  <q-page>
    <q-form @submit="onSubmit" @reset="onReset">
      <TermComponent 
      v-for="term in terms" 
      :key="term.path.join('-')" 
      :term="term" 
      />
      <q-btn label="Submit" type="submit" color="primary" />
      <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
      <!-- 
      <pre>{{ exportTerms }}</pre>
      -->
    </q-form>
  </q-page>
</template>

<script setup>
import { ref, provide, toRaw, computed } from 'vue';
import TermComponent from 'src/components/termComponent.vue';
import docuData from 'src/data/docu.json';

const dataDefinition = ref(docuData);
const terms = ref([]);

function createInitialTerms(terms, path = []) {
  const formTerms = [];
  for (const [index, term] of terms.entries()) {
    const currentPath = [...path, index];
    const formTerm = {
      path: currentPath,
      prefLabel: term.prefLabel,
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
      formTerm.narrower = createInitialTerms(term.narrower, currentPath);
    }
    formTerms.push(formTerm);
  }
  return formTerms;
}

terms.value = createInitialTerms(dataDefinition.value);
console.log("Initial form data:", terms.value)

const onReset = () => {
  terms.value = createInitialTerms(dataDefinition.value);
  console.log('Form has been reset!');
};

const onSubmit = () => {
  console.log('Final Form Data:', exportTerms.value);
  alert('Form submitted! Check the console for the data.');
};

provide('formManager', {
  terms,
  addFieldAtPath(path) {
    let parentArray = terms.value;
    for (let i = 0; i < path.length - 1; i++) {
      parentArray = parentArray[path[i]].narrower;
    }
    const index = path[path.length - 1];
    const node = parentArray[index];

    if (node['Wiederholbar'] === 'Ja') {
      const clone = structuredClone(toRaw(node));
      resetValues(clone);
      parentArray.splice(index + 1, 0, clone);
      recalculatePaths(terms.value);
    }
  },

  removeFieldAtPath(path) {
    let parentArray = terms.value;
    for (let i = 0; i < path.length - 1; i++) {
      parentArray = parentArray[path[i]].narrower;
    }
    const index = path[path.length - 1];

    const notation = parentArray[index].notation;
    const sameNotationCount = parentArray.filter(n => n.notation === notation).length;
    if (sameNotationCount > 1) {
      parentArray.splice(index, 1);
      recalculatePaths(terms.value);
    }
  },

  updateValueAtPath(path, value) {
  let target = terms.value;
  for (let i = 0; i < path.length; i++) {
    target = target[path[i]];
    if (i < path.length - 1) {
      target = target.narrower;
    }
  }
  target.value = value;
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

function exportFormData (terms) {
  const exportTerms = [];
  for (const term of terms) {
    const exportTerm = {
      Name: term.prefLabel,
      Identifikator: term.notation,
    }
    if (term.Feldwert) {
      exportTerm.value = term.value;
    }
    if (term.narrower) {
      exportTerm.Untereinträge = exportFormData(term.narrower);
    }
    exportTerms.push(exportTerm);
  }
  return exportTerms;
}

const exportTerms = computed(() => exportFormData(terms.value));


</script>