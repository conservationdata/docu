<template>
  <div class="input-wrapper q-pa-sm">
    <div v-if="inputConfig.type === 'date'">
      <q-input
        filled
        dense
        :model-value="modelValue"
        @update:model-value="(value) => emit('update:modelValue', value)"
        mask="date"
        :rules="['date']"
        :hint="term.Verwendungshinweis || 'Please select a date'"
      >
        <template v-slot:append>
          <q-icon name="event" class="cursor-pointer">
            <q-popup-proxy cover transition-show="scale" transition-hide="scale">
              <q-date :model-value="modelValue" @update:model-value="(value) => emit('update:modelValue', value)">
                <div class="row items-center justify-end">
                  <q-btn v-close-popup label="Close" color="primary" flat />
                </div>
              </q-date>
            </q-popup-proxy>
          </q-icon>
        </template>
      </q-input>
    </div>

    <div v-else-if="inputConfig.type === 'radio'" class="q-gutter-y-sm radio-group">
      <div class="text-caption radio-hint" v-if="term.Verwendungshinweis">{{ term.Verwendungshinweis }}</div>
      <q-radio
        v-for="option in inputConfig.options"
        :key="option"
        :model-value="modelValue"
        @update:model-value="(value) => emit('update:modelValue', value)"
        :val="option"
        :label="option"
      />
    </div>

    <div v-else-if="inputConfig.type === 'checkbox'" class="checkbox-group">
      <q-checkbox
        :model-value="modelValue"
        @update:model-value="(value) => emit('update:modelValue', value)"
        :label="inputConfig.label"
        :true-value="inputConfig['true-value']"
        :false-value="inputConfig['false-value']"
      />
      <div class="text-caption checkbox-hint" v-if="term.Verwendungshinweis">{{ term.Verwendungshinweis }}</div>
    </div>

    <div v-else>
      <UriSelector
        v-if="term.Feldwert.includes('URI')"
        :notation="term.notation"
        @uri-selected="(uri) => emit('update:modelValue', uri)"
        class="uri-selector"
      />
      <q-input
        v-if="term.Feldwert.includes('Text')"
        :model-value="modelValue"
        @update:model-value="(value) => emit('update:modelValue', value)"
        filled
        dense
        class="col text-input"
        :hint="term.Verwendungshinweis || ''"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import UriSelector from 'src/components/uriSelector.vue';
import inputTypes from 'src/data/inputType.json';

const props = defineProps(['modelValue', 'term']);
const emit = defineEmits(['update:modelValue']);

const inputConfig = computed(() => {
  const config = inputTypes[props.term.notation];
  return config ? config : { type: 'default' };
});
</script>

<style scoped>
.input-wrapper {
  width: 100%;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  margin-bottom: 8px;
  padding: 12px; /* Increased padding */
  background-color: #ffffff;
}

.q-input, .q-radio, .q-checkbox {
  margin-bottom: 8px; /* Spacing between input elements */
}

.radio-group, .checkbox-group {
  padding-top: 8px;
}

.radio-hint, .checkbox-hint {
  color: #757575; /* Softer color for hints */
  margin-bottom: 8px;
}

.uri-selector, .text-input {
  margin-top: 8px;
}
</style>