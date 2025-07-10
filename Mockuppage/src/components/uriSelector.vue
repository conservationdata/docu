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

    import { ref } from 'vue';
    import uriData from 'src/data/uri.json';

    const { notation } = defineProps(['notation'])
    const tree = [uriData[notation]];
    const selected = ref(null);
    const emit = defineEmits(['uri-selected']);
    function handleSelection(targetKey) {
        console.log('Selection changed:', targetKey);
        selected.value = targetKey;
        if (targetKey) {
            emit('uri-selected', targetKey);
        }
    }

</script>