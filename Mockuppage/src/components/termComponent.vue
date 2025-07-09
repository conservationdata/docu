<template>
  <div>
    <h6 :title="term.definition">
      <a :href="link" target="_blank">{{ term.prefLabel }}</a>
    </h6>
    <div v-if="term.Wiederholbar === 'Ja' && term.Feldwert">
      <div v-for="(value, index) in formManager.formData.value[term.notation]" :key="index" class="row items-center q-mb-sm">
        <q-input
          v-model="formManager.formData.value[term.notation][index]"
          filled
          dense
          class="col"
          :hint="term.Verwendungshinweis || ''"
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
      <UriSelector
        v-if="term.Feldwert.includes('URI')"
        :notation="term.notation"
        @uri-selected="(uri) => (formManager.formData.value[term.notation] = uri)"
      />
      <q-input
        v-if="term.Feldwert.includes('Text') || term.Feldwert.includes('URI')"
        v-model="formManager.formData.value[term.notation]"
        filled
        dense
        :readonly="!term.Feldwert.includes('Text')"
        :hint="term.Verwendungshinweis || ''"
        @click="handleInputClick"
      />
    </div>

    <div v-if="term.narrower" class="q-ml-md">
      <TermComponent
        v-for="child in term.narrower"
        :key="child.notation"
        :term="child"
      />
    </div>
  </div>
</template>

<script setup>
import { inject } from 'vue';
import UriSelector from 'src/components/uriSelector.vue';

// No local state needed for the input value anymore!
const props = defineProps(['term']);
const link = "https://www.w3id.org/conservation/terms/metadata/" + props.term.notation;

// Inject the central form manager
const formManager = inject('formManager');

function handleInputClick() {
  if (!props.term.Feldwert.includes('Text')) {
    alert('Please select a value from the normdata URI tree below');
  }
}
</script>