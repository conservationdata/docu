<template>
  <div>
    <div class="row items-center">
      <h6 :title="term.definition" class="q-ma-none">
        <a :href="link" target="_blank">{{ term.prefLabel }}</a>
      </h6>

      <q-btn
        v-if="term.narrower"
        flat
        round
        dense
        :icon="isExpanded ? 'expand_more' : 'chevron_right'"
        @click="toggleExpansion"
        class="q-ml-sm"
        aria-label="Toggle expansion"
      />
    </div>

    <div v-if="term.Wiederholbar === 'Ja' && term.Feldwert">
      <div v-for="(value, index) in formManager.formData.value[term.notation]" :key="index" class="row items-center q-mb-sm">
        <InputComponent
          v-model="formManager.formData.value[term.notation][index]"
          :term="term"
          class="col"
        />
        <q-btn
          flat
          round
          dense
          icon="delete"
          color="negative"
          class="q-ml-sm"
          @click="formManager.removeField(term.notation, index)"
          :disable="formManager.formData.value[term.notation].length <= 1"
        />
      </div>
      <q-btn
        label="Add"
        icon="add"
        size="sm"
        color="positive"
        @click="formManager.addField(term.notation)"
      />
    </div>

    <div v-else-if="term.Feldwert">
      <InputComponent
        v-model="formManager.formData.value[term.notation]"
        :term="term"
      />
    </div>

    <div v-if="term.narrower && isExpanded" class="q-ml-md">
      <TermComponent
        v-for="child in term.narrower"
        :key="child.notation"
        :term="child"
      />
    </div>
  </div>
</template>

<script setup>
import { inject, ref } from 'vue'; // Import ref
import InputComponent from './inputComponent.vue';

const props = defineProps(['term']);
const link = `https://www.w3id.org/conservation/terms/metadata/${props.term.notation}`;

// Inject the central form manager for state management
const formManager = inject('formManager');

// 1. Add a local reactive state to track the expansion state. Default to true (expanded).
const isExpanded = ref(false);

// 2. Create a function to toggle the state.
function toggleExpansion() {
  isExpanded.value = !isExpanded.value;
}
</script>

<style scoped>
/* Optional: Add a cursor pointer to the title to indicate it's clickable */
h6 {
  margin-bottom: 0;
  margin-top: 0.5rem;
}
</style>