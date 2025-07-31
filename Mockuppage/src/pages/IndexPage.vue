<template>
  <q-page class="q-pa-md form-page">
    <q-form class="q-gutter-md">
      <TermComponent
        v-for="term in terms"
        :key="term.path.join('-')"
        :term="term"
      />
    </q-form>

    <div v-if="exportTerms.length > 0" class="q-mt-xl q-mb-xl">
      <div class="row justify-around">
        <p class="text-h6 q-mb-none text-secondary">{{ outputFormat === 'json' ? 'Proto-JSON' : 'Proto-XML' }}</p>
        <q-btn-toggle
          v-model="outputFormat"
          toggle-color="accent"
          text-color="secondary"
          :options="[
            { label: 'JSON', value: 'json' },
            { label: 'XML', value: 'xml' }
          ]"
          @update:model-value="updateOutput"
          dense
        />
        <q-btn-group push>
          <q-btn
            label="Download"
            color="accent"
            text-color="secondary"
            @click="downloadOutputBound"
            dense
          />
          <q-btn
            label="Kopieren"
            color="accent"
            text-color="secondary"
            @click="copyToClipboardBound"
            dense
          />
        </q-btn-group>
      </div>
      <pre>{{ displayOutput }}</pre>
    </div>

    <q-page-sticky position="bottom" expand>
      <div class="row bg-white q-pa-sm justify-evenly full-width" style="max-width: 900px;">
      <q-btn
        label="Abschicken"
        color="accent"
        text-color="secondary"
        @click="onSubmit"
        dense
      />
      <q-btn
        label="Zurücksetzen"
        color="accent"
        text-color="secondary"
        @click="onReset"
        dense
      />
      <q-btn
        label="Felder ausfüllen"
        color="accent"
        text-color="secondary"
        @click="() => { 
          fillAllFields(terms, []); 
          $q.notify({ type: 'positive', message: 'Alle Felder befüllt' }); 
        }"
        dense
      />
      <q-btn
        label="Ausklappen"
        color="accent"
        text-color="secondary"
        @click="() => toggleAll(terms, true)"
        dense
      />
      <q-btn
        label="Einklappen"
        color="accent"
        text-color="secondary"
        @click="() => toggleAll(terms, false)"
        dense
      />
      </div>
    </q-page-sticky>
  </q-page>
</template>

<script setup>
import { ref, provide, toRaw, nextTick } from 'vue';
import { useQuasar } from 'quasar';
import TermComponent from 'src/components/termComponent.vue';
import docuData from 'src/data/docu.json';

import {
  createInitialTerms,
  recalculatePaths
} from 'src/utils/formStructure';

import {
  fillAllFields,
  resetValues
} from 'src/utils/fieldOperations';

import {
  jsonToSimplifiedXml,
  copyToClipboard,
  downloadOutput
} from 'src/utils/outputExport';

import {
  validateForm,
  transformFormData
} from 'src/utils/formValidation';

import {
  toggleAll,
  expandToPath
} from 'src/utils/uiExpansion';

const $q = useQuasar();
const dataDefinition = ref(docuData);
const terms = ref([]);
const exportTerms = ref([]);
const displayOutput = ref('');
const outputFormat = ref('json');
const validationError = ref(null);

const expandNotationsOnStartup = ["F52262", "BAA258"]; // F52262 Zustandserfassung BAA258 Konservierungskonzept
const excludeNotations = ["F52262", "BAA258"];
console.log(excludeNotations.value)

terms.value = createInitialTerms(dataDefinition.value, [], expandNotationsOnStartup);

const copyToClipboardBound = copyToClipboard(displayOutput, outputFormat, $q);
const downloadOutputBound = downloadOutput(displayOutput, outputFormat, $q);

const updateOutput = () => {
  if (exportTerms.value.length > 0) {
    displayOutput.value =
      outputFormat.value === 'json'
        ? JSON.stringify(exportTerms.value, null, 2)
        : jsonToSimplifiedXml(exportTerms.value);
  }
};

const onSubmit = async () => {
  exportTerms.value = [];
  displayOutput.value = '';
  validationError.value = null;

  const errorInfo = validateForm(terms.value);
  if (errorInfo) {
    validationError.value = errorInfo.error;
    $q.notify({ type: 'negative', message: errorInfo.error });
    expandToPath(errorInfo.path, terms.value);
    await nextTick();
    const el = document.getElementById(`term-${errorInfo.path.join('-')}`);
    el?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  } else {
    exportTerms.value = transformFormData(terms.value);
    updateOutput();
    $q.notify({ type: 'positive', message: 'Datensatz erstellt!' });
    await nextTick();
    document.querySelector('.q-mt-xl')?.scrollIntoView({ behavior: 'smooth' });
  }
};

const onReset = () => {
  terms.value = createInitialTerms(dataDefinition.value, [], expandNotationsOnStartup);
  exportTerms.value = [];
  displayOutput.value = '';
  $q.notify({ type: 'positive', message: 'Formular zurückgesetzt' });
};

// Provide form manager
provide('formManager', {
  terms,
  addFieldAtPath(path) {
    let parent = terms.value;
    for (let i = 0; i < path.length - 1; i++) parent = parent[path[i]].narrower;
    const index = path[path.length - 1];
    if (parent[index]['Wiederholbar'] === 'Ja') {
      const clone = structuredClone(toRaw(parent[index]));
      resetValues(clone);
      parent.splice(index + 1, 0, clone);
      recalculatePaths(terms.value);
    }
  },
  removeFieldAtPath(path) {
    let parent = terms.value;
    for (let i = 0; i < path.length - 1; i++) parent = parent[path[i]].narrower;
    const index = path[path.length - 1];
    const notation = parent[index].notation;
    if (parent.filter(n => n.notation === notation).length > 1) {
      parent.splice(index, 1);
      recalculatePaths(terms.value);
    }
  },
  updateValueAtPath(path, value, field = 'value') {
    let target = terms.value;
    path.forEach((idx, i) => {
      target = i < path.length - 1 ? target[idx].narrower : target[idx];
    });
    target[field] = value;
  },
  toggleExpansionAtPath(path) {
    let target = terms.value;
    path.forEach((idx, i) => {
      target = i < path.length - 1 ? target[idx].narrower : target[idx];
    });
    target.isExpanded = !target.isExpanded;
  }
});

fillAllFields(terms.value, excludeNotations);
$q.notify({ type: 'positive', message: 'Kuratorische Beispieldaten eingetragen.' });
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