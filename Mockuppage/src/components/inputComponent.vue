<template>
  <div class="input-wrapper q-pa-sm">
    <div v-if="inputConfig.type === 'date'">
      <q-date
        filled
        dense
        :model-value="modelValue"
        @update:model-value="(value) => emit('update:modelValue', value)"
        :hint="term.Verwendungshinweis || 'Bitte Datum eintragen'"
      />
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
        :hint="term.Verwendungshinweis || 'Bitte Wert eintragen'"
      />
    </div>

    <div v-else-if="inputConfig.type === 'checkbox'" class="checkbox-group">
      <q-checkbox
        :model-value="modelValue"
        @update:model-value="(value) => emit('update:modelValue', value)"
        :label="inputConfig.label"
        :true-value="inputConfig['true-value']"
        :false-value="inputConfig['false-value']"
        :hint="term.Verwendungshinweis || 'Bitte Wert eintragen'"
      />
      <div class="text-caption checkbox-hint" v-if="term.Verwendungshinweis">{{ term.Verwendungshinweis }}</div>
    </div>

    <div v-else>
      <UriSelector
        v-if="term.Feldwert.includes('URI')"
        :term="term"
        @uri-selected="(uri) => emit('update:modelValue', uri)"
        class="uri-selector"
      />
      <div class="text-caption text-grey-7 q-mt-sm" v-if="!term.Feldwert.includes('Text')">
      {{ props.term.Verwendungshinweis || 'Bitte Wert eintragen' }}
    </div>
      <q-input
        v-show="term.Feldwert.includes('Text')"
        :model-value="modelValue"
        @update:model-value="(value) => emit('update:modelValue', value)"
        filled
        dense
        class="col text-input"
        :hint="props.term.Verwendungshinweis || 'Bitte Wert eintragen'" 
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import UriSelector from 'src/components/uriSelector.vue';

const props = defineProps(['modelValue', 'term']);
const emit = defineEmits(['update:modelValue']);

const inputConfig = computed(() => {
  const defaultConfig = { type: 'default' };

  if (!props.term || !props.term.Typ) {
    return defaultConfig;
  }

  try {
    const config = JSON.parse(props.term.Typ);
    if (config && typeof config === 'object' && config.type) {
      return config;
    }
    console.log('Error: Parsed term.Typ is invalid or missing a "type" property.');
    return defaultConfig;
  } catch (error) {
    console.log('Error parsing term.Typ JSON string:');
    const errorArray =[error]
    errorArray.pop();
    return defaultConfig;
  }
});
</script>

<style scoped>
.input-wrapper {
  width: 100%;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  margin-bottom: 8px;
  padding: 12px;
  background-color: #ffffff;
}

.q-input, .q-radio, .q-checkbox {
  margin-bottom: 8px;
}

.radio-group, .checkbox-group {
  padding-top: 8px;
}

.radio-hint, .checkbox-hint {
  color: #757575;
  margin-bottom: 8px;
}

.uri-selector, .text-input {
  margin-top: 8px;
}
</style>