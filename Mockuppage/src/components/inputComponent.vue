<template>
  <div class="input-wrapper q-pa-sm">
    <div v-if="inputConfig.type === 'date'">
      <q-date
        filled
        dense
        :model-value="modelValue"
        @update:model-value="(value) => emit('update:modelValue', value)"
        :hint="term.Verwendungshinweis || 'Please select a date'"
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
        :term="term"
        @uri-selected="(uri) => emit('update:modelValue', uri)"
        class="uri-selector"
      />
      <q-input
        :readonly="isInputReadonly"
        :model-value="modelValue"
        @update:model-value="(value) => emit('update:modelValue', value)"
        filled
        dense
        class="col text-input"
        :hint="inputHint"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import UriSelector from 'src/components/uriSelector.vue';

const props = defineProps(['modelValue', 'term']);
const emit = defineEmits(['update:modelValue']);

const isInputReadonly = computed(() => {
  return !props.term.Feldwert.includes('Text');
});

const inputHint = computed(() => {
  if (isInputReadonly.value) {
    return 'This field is read-only. Please use the URI tree to select a value.';
  }
  return props.term.Verwendungshinweis || 'Please enter a value';
});

const inputConfig = computed(() => {
  // Fallback configuration
  const defaultConfig = { type: 'default' };

  if (!props.term || !props.term.Typ) {
    console.log('Error: term.Typ is missing. Falling back to default input.');
    return defaultConfig;
  }

  try {
    const config = JSON.parse(props.term.Typ);
    // Validate that the parsed object has a 'type' property
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