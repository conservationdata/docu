<template>
  <div class="input-wrapper q-pa-sm">
    <div v-if="inputConfig.type === 'date'">
      <q-date
        filled
        dense
        :model-value="localValue"
        @update:model-value="(value) => emit('update:modelValue', value)"
        :hint="term.Verwendungshinweis || 'Bitte Datum eintragen'"
        color="accent"
      />
    </div>

    <div v-else-if="inputConfig.type === 'radio'" class="q-gutter-y-sm radio-group">
      <div class="text-caption radio-hint" v-if="term.Verwendungshinweis">
        {{ term.Verwendungshinweis }}
      </div>
      <q-radio
        v-for="option in inputConfig.options"
        :key="option"
        :model-value="localValue"
        @update:model-value="(value) => emit('update:modelValue', value)"
        :val="option"
        :label="option"
        :hint="term.Verwendungshinweis || 'Bitte Wert eintragen'"
        color="accent"
      />
    </div>

    <div v-else-if="inputConfig.type === 'checkbox'" class="checkbox-group">
      <q-checkbox
        :model-value="localValue"
        @update:model-value="(value) => emit('update:modelValue', value)"
        :label="inputConfig.label"
        :true-value="inputConfig['true-value']"
        :false-value="inputConfig['false-value']"
        :hint="term.Verwendungshinweis || 'Bitte Wert eintragen'"
        color="accent"
      />
      <div class="text-caption checkbox-hint" v-if="term.Verwendungshinweis">
        {{ term.Verwendungshinweis }}
      </div>
    </div>

    <div v-else>
      <UriSelector
        v-if="term.Feldwert.includes('URI')"
        :term="term"
        :model-value="localValue"
        @update:model-value="(uri) => emit('update:modelValue', uri)"
        class="uri-selector"
      />

      <div v-show="term.Feldwert.includes('Text')">
        <div class="row items-center">
          <q-input
            v-model="inputValue"
            filled
            dense
            class="col text-input"
            :hint="props.term.Verwendungshinweis || 'Bitte Wert eintragen'"
          />

          <!-- Single Unit -->
          <span v-if="unitOptions.length === 1" class="unit-label q-ml-sm">
            {{ unitOptions[0] }}
          </span>

          <!-- Multiple Units -->
          <q-select
            v-else-if="unitOptions.length > 1"
            v-model="selectedUnit"
            :options="unitOptions"
            dense
            borderless
            class="unit-select q-ml-sm"
          />
        </div>
      </div>

      <div class="text-caption text-grey-7 q-mt-sm" v-if="!term.Feldwert.includes('Text')">
        {{ props.term.Verwendungshinweis || 'Bitte Wert eintragen' }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import UriSelector from 'src/components/uriSelector.vue';

const props = defineProps(['modelValue', 'term', 'path']);
const emit = defineEmits(['update:modelValue']);

const localValue = ref(props.modelValue);

// Sync localValue with modelValue
watch(() => props.modelValue, (newVal) => {
  localValue.value = newVal;
});

// Parse input config
const inputConfig = computed(() => {
  if (!props.term || !props.term.Typ) return { type: 'default' };

  try {
    const config = JSON.parse(props.term.Typ);
    return config && typeof config === 'object' && config.type ? config : { type: 'default' };
  } catch (error) {
    console.error('Error parsing term.Typ:', error);
    return { type: 'default' };
  }
});

// Parse units
const unitOptions = computed(() => {
  if (!props.term.Einheit) return [];

  return props.term.Einheit
    .split(',')
    .map(u => u.trim())
    .filter(Boolean);
});

// Extract unit from modelValue if it matches one of the known units
const extractUnit = (value) => {
  if (!value || !unitOptions.value.length) return { valueOnly: value, unit: null };

  const escapedUnits = unitOptions.value.map(u => u.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');
  const regex = new RegExp(`\\s*(${escapedUnits})$`);
  const match = value.match(regex);

  if (match) {
    return {
      valueOnly: value.slice(0, match.index).trim(),
      unit: match[1],
    };
  }

  return { valueOnly: value.trim(), unit: null };
};

// Reactive input value
const { valueOnly, unit } = extractUnit(props.modelValue || '');
const inputValue = ref(valueOnly);
const selectedUnit = ref(unit || unitOptions.value[0] || '');

// Watch modelValue to update inputValue
watch(() => props.modelValue, (newVal) => {
  const { valueOnly: newValue, unit: newUnit } = extractUnit(newVal || '');
  inputValue.value = newValue;
  selectedUnit.value = newUnit || unitOptions.value[0] || '';
});

// Watch inputValue and selectedUnit to emit updated value
watch([inputValue, selectedUnit], ([newInput, newUnit]) => {
  const trimmedInput = newInput?.trim() || '';
  if (trimmedInput && unitOptions.value.includes(newUnit)) {
    emit('update:modelValue', `${trimmedInput} ${newUnit}`);
  } else if (trimmedInput) {
    emit('update:modelValue', trimmedInput);
  } else {
    emit('update:modelValue', '');
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

.unit-label {
  font-size: 14px;
  color: #424242;
}

.unit-select {
  min-width: 80px;
}
</style>