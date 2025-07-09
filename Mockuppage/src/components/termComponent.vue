<template>
  <div>
    <h6 :title="term.definition">
      <a :href="link" target="_blank">{{ term.prefLabel }}</a>
    </h6>
    <div v-if="term.Feldwert">
    <UriSelector
    v-if="term.Feldwert.includes('URI')"
    :notation="term.notation"
    @uri-selected="updateFieldValue"
    />
    <q-input
    v-if="term.Feldwert.includes('Text') || term.Feldwert.includes('URI')"
    v-model="fieldValue"
    filled
    dense
    :readonly="!term.Feldwert.includes('Text')"
    :hint="term.Verwendungshinweis || ''"
    @click="handleInputClick"
    >
    </q-input>
    </div>
    <div v-if="term.narrower">
      <TermComponent
        v-for="child in term.narrower"
        :key="child.notation"
        :term="child"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import UriSelector from 'src/components/uriSelector.vue';

const { term } = defineProps(['term'])
const link = "https://www.w3id.org/conservation/terms/metadata/" + term.notation

// Create a reactive ref to hold the value for the q-input.
const fieldValue = ref('');

function updateFieldValue(uri) {
  console.log('Updating field value with URI:', uri);
  fieldValue.value = uri;
}

function handleInputClick() {
  if (!term.Feldwert.includes('Text')) {
    alert('Please select a value from the normdata URI tree below');
  }
}

</script>
