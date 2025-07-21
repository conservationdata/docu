<template>
  <div class="q-pa-sm term-container" :id="termId">
    <div class="row items-center term-header">
      <h6 class="q-ma-none term-label">
        <a 
          :href="link" 
          :title="term.definition"
          target="_blank"
          class="text-primary text-bold"
        >
          {{ term.prefLabel }}
        </a>
        <span 
          v-if="term.Verpflichtungsgrad === 'Pflicht'" 
          :title="'Verpflichtend'"
          class="text-red q-ml-sm required-indicator"
        >*</span>
      </h6>
      <q-btn
        v-if="term.narrower && term.narrower.length"
        flat
        round
        dense
        :icon="term.isExpanded ? 'expand_less' : 'expand_more'" 
        @click="toggleExpansion"
        class="q-ml-sm expand-btn"
        aria-label="Toggle expansion"
      />
      <q-space />
      <q-btn
        v-if="term.Wiederholbar === 'Ja'"
        icon="delete"
        color="negative"
        round
        dense
        flat
        aria-label="Delete"
        @click="formManager.removeFieldAtPath(term.path)"
        :disable="isOnlyInstance"
        class="delete-btn"
      />
    </div>

    <!-- Unsicher Checkbox -->
    <q-checkbox
      v-if="term.Unsicher === 'Ja'"
      v-model="unsicherValue"
      label="Unsicher"
      class="q-mt-sm"
    />

    <InputComponent 
      v-if="term.Feldwert"
      :modelValue="term.value" 
      @update:modelValue="updateValue" 
      :term="term" 
      class="q-mt-sm"
    />

    <q-btn
      v-if="term.Wiederholbar === 'Ja'"
      label="Add"
      icon="add"
      size="sm"
      color="positive"
      @click="formManager.addFieldAtPath(term.path)"
      class="q-mt-sm add-btn"
    />

    <div v-show="term.narrower && term.narrower.length && term.isExpanded" class="q-ml-md narrower-terms">
      <TermComponent
        v-for="child in term.narrower"
        :key="child.path.join('-')"
        :term="child"
      />
    </div>
  </div>
</template>

<script setup>
import { inject, computed } from 'vue';
import InputComponent from './inputComponent.vue';

const props = defineProps({
  term: {
    type: Object,
    required: true
  }
});

const formManager = inject('formManager');

const termId = computed(() => `term-${props.term.path.join('-')}`);
const link = computed(() => `https://www.w3id.org/conservation/terms/metadata/${props.term.notation}`);

function toggleExpansion() {
  formManager.toggleExpansionAtPath(props.term.path);
}

const isOnlyInstance = computed(() => {
  if (props.term.path.length === 1) {
    return formManager.terms.value.filter(t => t.notation === props.term.notation).length <= 1;
  }

  const parentPath = props.term.path.slice(0, -1);
  let parentArray = formManager.terms.value;
  for (let i = 0; i < parentPath.length; i++) {
    parentArray = parentArray[parentPath[i]].narrower;
  }

  const count = parentArray.filter(t => t.notation === props.term.notation).length;
  return count <= 1;
});

function updateValue(newVal) {
  formManager.updateValueAtPath(props.term.path, newVal);
}

// Handle Unsicher checkbox
const unsicherValue = computed({
  get: () => props.term.UnsicherValue === 'Ja',
  set: (isChecked) => {
    formManager.updateValueAtPath(props.term.path, isChecked ? 'Ja' : '', 'UnsicherValue');
  }
});
</script>

<style scoped>
.term-container {
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  margin-bottom: 1rem;
  background-color: #fcfcfc;
  padding: 1rem !important;
  scroll-margin-top: 20px; 
}

.term-header {
  margin-bottom: 0.5rem;
  align-items: center;
}

.term-label {
  font-size: 1.25rem;
  color: #333;
  display: flex;
  align-items: center;
}

.term-label a {
  text-decoration: none;
  color: #1976d2;
}

.term-label a:hover {
  text-decoration: underline;
}

.required-indicator {
  font-size: 1.5rem;
  font-weight: bold;
}

.expand-btn {
  color: #555;
}

.delete-btn {
  margin-left: 0.5rem;
}

.add-btn {
  margin-top: 0.75rem;
  margin-left: 0.25rem;
}

.narrower-terms {
  border-left: 2px solid #e0e0e0;
  padding-left: 1rem;
  margin-top: 1rem;
}

h6 {
  margin-top: 0;
  margin-bottom: 0;
}
</style>