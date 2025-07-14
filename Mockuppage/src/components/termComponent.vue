<template>
  <div class="q-pa-sm">
    <!-- Header with label, definition tooltip and expand button -->
    <div class="row items-center">
      <h6 :title="term.definition" class="q-ma-none">
        <a :href="link" target="_blank">{{ term.prefLabel }}</a>
      </h6>
      <q-btn
        v-if="term.narrower && term.narrower.length"
        flat
        round
        dense
        :icon="isExpanded ? 'expand_more' : 'chevron_right'"
        @click="toggleExpansion"
        class="q-ml-sm"
        aria-label="Toggle expansion"
      />
    </div>

    <!-- Input for term with Feldwert -->
    <div v-if="term.Feldwert" class="q-mb-sm">
      <InputComponent 
      :modelValue="term.value" 
      @update:modelValue="updateValue" 
      :term="term" 
      />
    </div>

    <!-- Add/Remove buttons if Wiederholbar === 'Ja' -->
    <div v-if="term.Wiederholbar === 'Ja'" class="q-mb-sm">
      <q-btn
        label="Add"
        icon="add"
        size="sm"
        color="positive"
        @click="formManager.addFieldAtPath(term.path)"
        class="q-mr-sm"
      />
      <q-btn
        icon="delete"
        color="negative"
        round
        dense
        flat
        aria-label="Delete"
        @click="formManager.removeFieldAtPath(term.path)"
        :disable="isOnlyInstance"
      />
    </div>

    <!-- Children terms (narrower) -->
    <div v-if="term.narrower && term.narrower.length && isExpanded" class="q-ml-md">
      <TermComponent
        v-for="child in term.narrower"
        :key="child.path.join('-')"
        :term="child"
      />
    </div>
  </div>
</template>

<script setup>
import { inject, ref, computed } from 'vue';
import InputComponent from './inputComponent.vue';

const props = defineProps({
  term: {
    type: Object,
    required: true
  }
});

const link = `https://www.w3id.org/conservation/terms/metadata/${props.term.notation}`;

const formManager = inject('formManager');

const isExpanded = ref(false);
function toggleExpansion() {
  isExpanded.value = !isExpanded.value;
}

const isOnlyInstance = computed(() => {
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

</script>

<style scoped>
h6 {
  margin-bottom: 0;
  margin-top: 0.5rem;
}
</style>
