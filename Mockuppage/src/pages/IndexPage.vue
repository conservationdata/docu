<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-page class="q-pa-md form-page" :style-fn="pageStyle">
        <q-form class="q-gutter-md">
          <TermComponent
            v-for="term in terms"
            :key="term.path.join('-')"
            :term="term"
          />
        </q-form>

        <div v-if="exportTerms.length > 0" class="q-mt-xl">
          <p class="text-h6">Submission Successful</p>
          <pre>{{ exportTerms }}</pre>
        </div>
      </q-page>
    </q-page-container>

    <q-footer bordered class="bg-white text-primary q-pa-sm">
      <q-toolbar class="row justify-center">
        <q-btn-group
        push
        >
          <q-btn
            label="Submit"
            type="submit"
            color="primary"
            icon="mdi-check-circle"
            @click="onSubmit"
            flat
          />
          <q-separator vertical class="q-mx-md" />
          <q-btn
            label="Reset"
            type="reset"
            color="grey"
            class="q-ml-sm"
            icon="mdi-reload"
            @click="onReset"
            flat
          />
          <q-separator vertical class="q-mx-md" />
          <q-btn
            label="Fill all fields"
            color="accent"
            icon="mdi-auto-fix"
            @click="fillAllFields"
            flat
          />
          <q-separator vertical class="q-mx-md" />
          <q-btn
            label="Expand All"
            color="secondary"
            icon="mdi-unfold-more-vertical"
            @click="toggleAll(true)"
            flat
          />
          <q-separator vertical class="q-mx-md" />
          <q-btn
            label="Collapse All"
            color="secondary"
            class="q-ml-sm"
            icon="mdi-unfold-less-vertical"
            @click="toggleAll(false)"
            flat
          />
        </q-btn-group>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<script setup>
import { ref, provide, toRaw, nextTick } from 'vue';
import { useQuasar } from 'quasar';
import TermComponent from 'src/components/termComponent.vue';
import docuData from 'src/data/docu.json';
import exampleData from 'src/data/example.json';

const $q = useQuasar();
const dataDefinition = ref(docuData);
const terms = ref([]);
const exportTerms = ref([]);
const validationError = ref(null);

const pageStyle = (offset) => {
  return { paddingBottom: `${offset + 16}px` };
};

function createInitialTerms(terms, path = []) {
  return terms.map((term, index) => {
    const currentPath = [...path, index];
    const formTerm = {
      path: currentPath,
      prefLabel: term.prefLabel,
      notation: term.notation,
      definition: term.definition,
      Wiederholbar: term.Wiederholbar,
      Verpflichtungsgrad: term.Verpflichtungsgrad,
      Verwendungshinweis: term.Verwendungshinweis,
      Feldwert: term.Feldwert,
      Typ: term.Typ,
      Baum: term.Baum,
      Einheit: term.Einheit,
      Unsicher: term.Unsicher,
      isExpanded: false,
      UnsicherValue: '',
    };
    if (term.Feldwert) {
      formTerm.value = '';
    }
    if (term.narrower) {
      formTerm.narrower = createInitialTerms(term.narrower, currentPath);
    }
    return formTerm;
  });
}

terms.value = createInitialTerms(dataDefinition.value);

const onReset = () => {
  terms.value = createInitialTerms(dataDefinition.value);
  exportTerms.value = [];
  validationError.value = null;
  $q.notify({
    message: 'Form has been reset.',
    color: 'info',
    icon: 'mdi-reload',
  });
};

const fillAllFields = () => {
  try {
    let fieldsFilledCount = 0;
    
    const fillTermsRecursively = (currentTerms) => {
      currentTerms.forEach(term => {
        if (term.Feldwert && term.notation && exampleData[term.notation]) {
          const exampleValue = exampleData[term.notation];
          if (exampleValue && exampleValue.trim() !== '') {
            term.value = exampleValue;
            fieldsFilledCount++;
          }
        }
        if (term.narrower && term.narrower.length > 0) {
          fillTermsRecursively(term.narrower);
        }
      });
    };
    
    fillTermsRecursively(terms.value);
    
    $q.notify({
      type: 'positive',
      message: `Successfully filled ${fieldsFilledCount} fields with example data.`,
      icon: 'mdi-auto-fix',
    });
  } catch (error) {
    console.error('Error filling fields:', error);
    $q.notify({
      type: 'negative',
      message: 'Error loading example data. Please check if example.json exists.',
      icon: 'mdi-alert-circle-outline',
    });
  }
};

const onSubmit = async () => {
  exportTerms.value = [];
  validationError.value = null;
  
  const errorInfo = validateForm(terms.value);

  if (errorInfo) {
    validationError.value = errorInfo.error;
    $q.notify({
      type: 'negative',
      message: errorInfo.error,
      icon: 'mdi-alert-circle-outline',
    });
    
    expandToPath(errorInfo.path);
    await nextTick();
    
    const errorElementId = `term-${errorInfo.path.join('-')}`;
    const element = document.getElementById(errorElementId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  } else {
    exportTerms.value = transformFormData(terms.value);
    $q.notify({
      type: 'positive',
      message: 'Form submitted successfully!',
      icon: 'mdi-check-circle-outline',
    });
  }
};

function validateForm(currentTerms) {
  for (const term of currentTerms) {
    if (term.Verpflichtungsgrad === 'Pflicht' && term.Feldwert && !term.value) {
      return { 
        error: `Error: '${term.prefLabel}' is a required field.`,
        path: term.path 
      };
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

function transformFormData(currentTerms) {
  const transformedTerms = [];
  for (const term of currentTerms) {
    if (term.value || (term.narrower && term.narrower.length > 0)) {
      const exportTerm = {
        Name: term.prefLabel,
        Identifikator: `https://www.w3id.org/conservation/terms/metadata/ ${term.notation}`,
      };
      if (term.Feldwert) {
        exportTerm.value = term.value;
      }

      // ✅ Only export Unsicher if it's set to 'Ja'
      if (term.Unsicher === 'Ja' && term.UnsicherValue === 'Ja') {
        exportTerm.Unsicher = 'Ja';
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


function toggleAll(expand) {
  const recursiveToggle = (nodes) => {
    nodes.forEach(node => {
      if (node.narrower && node.narrower.length > 0) {
        node.isExpanded = expand;
        recursiveToggle(node.narrower);
      }
    });
  };
  recursiveToggle(terms.value);
}

function expandToPath(path) {
  let currentLevel = terms.value;
  for (let i = 0; i < path.length - 1; i++) {
    const index = path[i];
    if (currentLevel[index]) {
      currentLevel[index].isExpanded = true;
      currentLevel = currentLevel[index].narrower;
    }
  }
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
updateValueAtPath(path, value, field = 'value') {
  let target = terms.value;
  path.forEach((index, i) => {
    target = (i < path.length - 1) ? target[index].narrower : target[index];
  });
  target[field] = value;
},

  toggleExpansionAtPath(path) {
    let target = terms.value;
    path.forEach((index, i) => {
      target = (i < path.length - 1) ? target[index].narrower : target[index];
    });
    target.isExpanded = !target.isExpanded;
  }
});

function resetValues(node) {
  if ('value' in node) node.value = '';
  if ('UnsicherValue' in node) node.UnsicherValue = '';
  if ('isExpanded' in node) node.isExpanded = false;
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
  margin: 0 auto;
  background-color: #ffffff;
}

pre {
  background-color: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 16px;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>