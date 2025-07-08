<template>
    <div class="tree-selector">
      <q-btn
        flat
        dense
        icon="keyboard_arrow_down"
        :label="displayValue || 'Select from tree...'"
        class="full-width tree-trigger"
        @click="showDialog = true"
        :class="{ 'has-selection': !!selectedValue }"
      />
  
      <q-dialog 
        v-model="showDialog" 
        persistent 
        maximized
        transition-show="slide-up"
        transition-hide="slide-down"
      >
        <q-card class="tree-dialog">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">Select {{ term.prefLabel }}</div>
            <q-space />
            <q-btn 
              icon="close" 
              flat 
              round 
              dense 
              @click="showDialog = false" 
            />
          </q-card-section>
  
          <q-separator />
  
          <q-card-section class="q-pt-none tree-content">
            <div v-if="!treeData || treeData.length === 0" class="text-center q-pa-md">
              <q-icon name="warning" size="md" class="q-mb-sm" />
              <div>No tree data available for this field</div>
            </div>
  
            <q-scroll-area 
              v-else
              style="height: 70vh;"
              class="tree-scroll"
            >
              <q-tree
                :nodes="treeData"
                :selected="selectedNode"
                @update:selected="onNodeSelect"
                node-key="id"
                label-key="label"
                children-key="children"
                :filter="filterText"
                :filter-method="filterTree"
                default-expand-all
                accordion
              >
                <template v-slot:default-header="prop">
                  <div class="row items-center full-width">
                    <div class="text-weight-medium">
                      {{ prop.node.label }}
                    </div>
                    <q-space />
                    <div v-if="prop.node.uri" class="text-caption text-grey-6">
                      {{ prop.node.uri }}
                    </div>
                  </div>
                </template>
              </q-tree>
            </q-scroll-area>
          </q-card-section>
  
          <q-separator />
  
          <q-card-section class="tree-search">
            <q-input
              v-model="filterText"
              placeholder="Filter tree..."
              dense
              outlined
              clearable
              class="q-mb-md"
            >
              <template v-slot:prepend>
                <q-icon name="search" />
              </template>
            </q-input>
          </q-card-section>
  
          <q-card-actions align="right">
            <q-btn 
              flat 
              label="Clear Selection" 
              @click="clearSelection"
              v-if="selectedValue"
            />
            <q-btn 
              flat 
              label="Cancel" 
              @click="showDialog = false" 
            />
            <q-btn 
              color="primary" 
              label="Select" 
              @click="confirmSelection"
              :disable="!selectedNode || !isLeafNode(selectedNode)"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, watch } from 'vue'
  
  const props = defineProps({
    term: {
      type: Object,
      required: true
    },
    modelValue: {
      type: String,
      default: ''
    },
    treeData: {
      type: Array,
      default: () => []
    }
  })
  
  const emit = defineEmits(['update:modelValue'])
  
  const showDialog = ref(false)
  const selectedNode = ref(null)
  const filterText = ref('')
  
  // Computed properties
  const selectedValue = computed(() => props.modelValue)
  
  const displayValue = computed(() => {
    if (!selectedValue.value) return ''
    
    // Try to find the node in the tree to get its label
    const node = findNodeByUri(props.treeData, selectedValue.value)
    if (node) {
      return `${node.label} (${node.uri})`
    }
    
    // Fallback to just the URI if we can't find the node
    return selectedValue.value
  })
  
  // Methods
  const findNodeByUri = (nodes, uri) => {
    for (const node of nodes) {
      if (node.uri === uri) {
        return node
      }
      if (node.children) {
        const found = findNodeByUri(node.children, uri)
        if (found) return found
      }
    }
    return null
  }
  
  const isLeafNode = (nodeId) => {
    const node = findNodeById(props.treeData, nodeId)
    return node && (!node.children || node.children.length === 0)
  }
  
  const findNodeById = (nodes, id) => {
    for (const node of nodes) {
      if (node.id === id) {
        return node
      }
      if (node.children) {
        const found = findNodeById(node.children, id)
        if (found) return found
      }
    }
    return null
  }
  
  const onNodeSelect = (nodeId) => {
    selectedNode.value = nodeId
  }
  
  const confirmSelection = () => {
    if (selectedNode.value && isLeafNode(selectedNode.value)) {
      const node = findNodeById(props.treeData, selectedNode.value)
      if (node && node.uri) {
        emit('update:modelValue', node.uri)
        showDialog.value = false
      }
    }
  }
  
  const clearSelection = () => {
    selectedNode.value = null
    emit('update:modelValue', '')
    showDialog.value = false
  }
  
  const filterTree = (node, filter) => {
    if (!filter) return true
    
    const searchText = filter.toLowerCase()
    const nodeMatches = node.label.toLowerCase().includes(searchText) ||
                       (node.uri && node.uri.toLowerCase().includes(searchText))
    
    // If this node matches, return true
    if (nodeMatches) return true
    
    // If any child matches, return true
    if (node.children) {
      return node.children.some(child => filterTree(child, filter))
    }
    
    return false
  }
  
  // Watch for changes to update selected node when modelValue changes
  watch(() => props.modelValue, (newValue) => {
    if (newValue) {
      const node = findNodeByUri(props.treeData, newValue)
      if (node) {
        selectedNode.value = node.id
      }
    } else {
      selectedNode.value = null
    }
  }, { immediate: true })
  </script>
  
  <style scoped>
  .tree-selector {
    width: 100%;
  }
  
  .tree-trigger {
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    text-align: left;
    justify-content: flex-start;
    padding: 8px 12px;
    min-height: 40px;
  }
  
  .tree-trigger:not(.has-selection) {
    color: #757575;
  }
  
  .tree-trigger.has-selection {
    color: #1976d2;
    border-color: #1976d2;
  }
  
  .tree-dialog {
    width: 100%;
    max-width: 800px;
  }
  
  .tree-content {
    flex: 1;
  }
  
  .tree-scroll {
    border: 1px solid #e0e0e0;
    border-radius: 4px;
  }
  
  .tree-search {
    padding-top: 0;
  }
  
  :deep(.q-tree__node-header) {
    padding: 8px 12px;
  }
  
  :deep(.q-tree__node-header:hover) {
    background-color: #f5f5f5;
  }
  
  :deep(.q-tree__node--selected > .q-tree__node-header) {
    background-color: #e3f2fd;
    color: #1976d2;
  }
  </style>