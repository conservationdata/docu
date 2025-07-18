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
import { ref, computed, watch } from 'vue';

const props = defineProps(['term', 'modelValue']);
const emit = defineEmits(['update:modelValue']);

// Build the tree
const tree = computed(() => {
  if (!props.term || !props.term.Baum) {
    console.error('Error: "term.Baum" property is missing. Cannot render tree.');
    return [];
  }

  try {
    const treeData = JSON.parse(props.term.Baum);
    return [treeData];
  } catch (error) {
    console.error('Error parsing "term.Baum" JSON:', error);
    return [];
  }
});

// Flatten the tree to check if a value is a valid URI
const allUrisInTree = computed(() => {
  const uris = [];

  function traverse(node) {
    if (node.uri) uris.push(node.uri);
    if (node.children) node.children.forEach(child => traverse(child));
  }

  if (tree.value.length > 0) {
    tree.value.forEach(rootNode => traverse(rootNode));
  }

  return uris;
});

// Ref to store current valid selection
const selected = ref(null);

// Update selection only if the value is a valid URI in the tree
watch(() => props.modelValue, (newVal) => {
  if (newVal && allUrisInTree.value.includes(newVal)) {
    selected.value = newVal;
  } else {
    selected.value = null;
  }
}, { immediate: true });

function handleSelection(targetKey) {
  selected.value = targetKey;
  emit('update:modelValue', targetKey);
}
</script>