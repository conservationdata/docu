<template>
  <q-page class="q-pa-md form-page">
    <q-form class="q-gutter-md">
      <TermComponent
        v-for="term in terms"
        :key="term.path.join('-')"
        :term="term"
      />
    </q-form>

    <div class="q-mt-lg button-group">
      <q-btn
        label="Submit"
        type="submit"
        color="primary"
        class="q-mr-sm"
        @click="onSubmit"
      />
      <q-btn
        label="Reset"
        type="reset"
        color="grey"
        flat
        class="q-ml-sm"
        @click="onReset"
      />
    </div>

    <div v-if="exportTerms.length > 0">
      <pre>{{ exportTerms }}</pre>
    </div>
  </q-page>
</template>

<script setup>
import { ref, provide, toRaw } from 'vue';
import { useQuasar } from 'quasar';
import TermComponent from 'src/components/termComponent.vue';
import docuData from 'src/data/docu.json';

const $q = useQuasar();
const dataDefinition = ref(docuData);
const terms = ref([]);

const exportTerms = ref([]);
const validationError = ref(null);

function createInitialTerms(terms, path = []) {
  const formTerms = [];
  for (const [index, term] of terms.entries()) {
    const currentPath = [...path, index];
    const formTerm = {
      path: currentPath,
      prefLabel: term.prefLabel,
      notation: term.notation,
      definition: term.definition,
      Wiederholbar: term.Wiederholbar,
      Verpflichtungsgrad: term.Verpflichtungsgrad,
      Feldwert: term.Feldwert,
    };
    if (term.Feldwert) {
      formTerm.value = '';
    }
    if (term.narrower) {
      formTerm.narrower = createInitialTerms(term.narrower, currentPath);
    }
    formTerms.push(formTerm);
  }
  return formTerms;
}

terms.value = createInitialTerms(dataDefinition.value);

const onReset = () => {
  terms.value = createInitialTerms(dataDefinition.value);
  exportTerms.value = [];
  validationError.value = null;
  $q.notify({
    message: 'Form has been reset.',
    color: 'grey',
    icon: 'mdi-reload',
  });
};

const onSubmit = () => {
  exportTerms.value = [];
  validationError.value = null;
  const error = validateForm(terms.value);

  if (error) {
    validationError.value = error;
    $q.notify({
      type: 'negative',
      message: error,
      icon: 'mdi-alert-circle-outline',
    });
  } else {
    exportTerms.value = transformFormData(terms.value);
    $q.notify({
      type: 'positive',
      message: 'Form submitted successfully!',
      icon: 'mdi-check-circle-outline',
    });
    console.log('Exported Data:', toRaw(exportTerms.value));
  }
};

function validateForm(terms) {
  for (const term of terms) {
    if (term.Verpflichtungsgrad === 'Pflicht' && term.Feldwert && !term.value) {
      return `Error: '${term.prefLabel}' is a required field.`;
    }
    if (term.narrower) {
      const nestedError = validateForm(term.narrower);
      if (nestedError) {
        return nestedError;
      }
    }
  }
  return null;
}

function transformFormData(terms) {
  const transformedTerms = [];
  for (const term of terms) {
    if (term.value || (term.narrower && term.narrower.length > 0)) {
       const exportTerm = {
        Name: term.prefLabel,
        Identifikator: `https://www.w3id.org/conservation/terms/metadata/${term.notation}`,
      };
      if (term.Feldwert) {
        exportTerm.value = term.value;
      }
      if (term.narrower) {
        const narrowerExport = transformFormData(term.narrower);
        if (narrowerExport.length > 0) {
           exportTerm.Untereinträge = narrowerExport;
        }
      }
      transformedTerms.push(exportTerm);
    }
  }
  return transformedTerms;
}

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
      target = i < path.length - 1 ? target[path[i]].narrower : target[path[i]];
    }
    target.value = value;
  },
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

<style scoped>
.form-page {
  max-width: 900px;
  margin: 2rem auto;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.button-group {
  display: flex;
  justify-content: flex-start;
  padding: 1rem 0;
  border-top: 1px solid #eee;
  margin-top: 2rem;
}
</style>