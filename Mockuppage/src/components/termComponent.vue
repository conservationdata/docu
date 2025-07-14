<template>
  <div class="q-pa-sm">
    <!-- Header with label, definition tooltip and expand button -->
    <div class="row items-center">
      <h6 class="q-ma-none">
        <a 
        :href="link" 
        :title="term.definition"
        target="_blank">
        {{ term.prefLabel }}
        </a>
        <span 
        v-if="term.Verpflichtungsgrad === 'Pflicht'" 
        :title="'Verpflichtend'"
        class="text-red q-ml-sm"
        >*</span>
      </h6>
      <q-btn
        v-if="term.narrower && term.narrower.length"
        flat
        round
        dense
        :icon="isExpanded ? 'expand_more' : 'expand_less'" 
        @click="toggleExpansion"
        class="q-ml-sm"
        aria-label="Toggle expansion"
      />
      <!--- '' --->
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
      />
    </div>

    <InputComponent 
    v-if="term.Feldwert"
    :modelValue="term.value" 
    @update:modelValue="updateValue" 
    :term="term" 
    />

    <q-btn
      v-if="term.Wiederholbar === 'Ja'"
      label="Add"
      icon="add"
      size="sm"
      color="positive"
      @click="formManager.addFieldAtPath(term.path)"
      class="q-mr-sm"
    />

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
