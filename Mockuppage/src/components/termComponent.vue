<template>
  <div>
    <h6 :title="term.definition">
      <a :href="link" target="_blank">{{ term.prefLabel }}</a>
    </h6>

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
import InputComponent from './inputComponent.vue';

const props = defineProps(['term']);
const link = `https://www.w3id.org/conservation/terms/metadata/${props.term.notation}`;

// Inject the central form manager for state management
const formManager = inject('formManager');
</script>