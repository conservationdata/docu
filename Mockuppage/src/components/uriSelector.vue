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
  import uriData from 'src/data/uri.json';

  const props = defineProps(['notation']);
  const selected = ref(null);
  const emit = defineEmits(['uri-selected']);

  // Your provided dummy tree
  const dummyTree = {
    "label": "Verwendetes Material",
    "uri": "https://www.conservation-science.org/ontology/conservation-material/CGC619",
    "selectable": false,
    "children": [
      {
        "label": "Paraloid B-72",
        "uri": "https://www.conservation-wiki.com/wiki/Paraloid_B-72"
      },
      {
        "label": "Primal AC-33",
        "uri": "https://www.conservation-wiki.com/wiki/Primal_AC-33"
      }
    ]
  };

  const tree = computed(() => {
    const data = uriData[props.notation];
    return data ? [data] : [dummyTree];
  });

  function handleSelection(targetKey) {
    console.log('Selection changed:', targetKey);
    selected.value = targetKey;
    if (targetKey) {
      emit('uri-selected', targetKey);
    }
  }
</script>