<template>
  <q-tree
    :nodes="tree"
    node-key="uri"
    :selected="selected"
    selected-color="primary"
    @update:selected="handleSelection"
    default-expand-all
  />
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps(['term']);
const emit = defineEmits(['uri-selected']);

const selected = ref(null);

const tree = computed(() => {
  if (!props.term || !props.term.Baum) {
    console.error('Error: "term.Baum" property is missing. Cannot render tree.');
    return [];
  }

  try {
    const treeData = JSON.parse(props.term.Baum);
    return [treeData];
  } catch (error) {
    console.log(props.term.prefLabel,'Error parsing "term.Baum" JSON. Please ensure it is valid JSON.');
    const errorArray =[error]
    errorArray.pop();
    return [];
  }
});

function handleSelection(targetKey) {
  selected.value = targetKey;
  if (targetKey) {
    emit('uri-selected', targetKey);
  }
}
</script>