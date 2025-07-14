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

    <div v-else-if="inputConfig.type === 'radio'" class="q-gutter-y-sm">
      <div class="text-caption" v-if="term.Verwendungshinweis">{{ term.Verwendungshinweis }}</div>
      <q-radio
        v-for="option in inputConfig.options"
        :key="option"
        :model-value="modelValue"
        @update:model-value="(value) => emit('update:modelValue', value)"
        :val="option"
        :label="option"
      />
    </div>

    <div v-else-if="inputConfig.type === 'checkbox'">
      <q-checkbox
        :model-value="modelValue"
        @update:model-value="(value) => emit('update:modelValue', value)"
        :label="inputConfig.label"
        :true-value="inputConfig['true-value']"
        :false-value="inputConfig['false-value']"
      />
      <div class="text-caption" v-if="term.Verwendungshinweis">{{ term.Verwendungshinweis }}</div>
    </div>

    <div v-else>
      <UriSelector
        v-if="term.Feldwert.includes('URI')"
        :notation="term.notation"
        @uri-selected="(uri) => emit('update:modelValue', uri)"
      />
      <q-input
        v-if="term.Feldwert.includes('Text')"
        :model-value="modelValue"
        @update:model-value="(value) => emit('update:modelValue', value)"
        filled
        dense
        class="col"
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
  border: 1px solid #eee;
  border-radius: 4px;
  margin-bottom: 8px;
}
</style>