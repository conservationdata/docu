<template>
    <div class="container-group">
      <q-card flat bordered class="q-mb-md">
        <q-card-section class="q-pb-none">
          <div class="container-header">
            <h6 class="text-h6 q-ma-none q-mb-sm">
              {{ term.prefLabel }}
              <q-tooltip v-if="term.definition" class="bg-primary">
                {{ term.definition }}
              </q-tooltip>
            </h6>
          </div>
        </q-card-section>
  
        <q-card-section 
          class="container-body"
          v-if="term.Verwendungshinweis"
        >
          <q-tooltip class="bg-secondary">
            {{ term.Verwendungshinweis }}
          </q-tooltip>
          
          <div class="container-children">
            <slot></slot>
          </div>
        </q-card-section>
  
        <q-card-section 
          v-else
          class="container-body"
        >
          <div class="container-children">
            <slot></slot>
          </div>
        </q-card-section>
      </q-card>
    </div>
  </template>
  
  <script setup>
  defineProps({
    term: {
      type: Object,
      required: true
    }
  })
  </script>
  
  <style scoped>
  .container-group {
    width: 100%;
  }
  
  .container-header {
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 8px;
  }
  
  .container-body {
    position: relative;
    min-height: 60px;
  }
  
  .container-children {
    padding-left: 16px;
  }
  
  .text-h6 {
    color: #1976d2;
    font-weight: 500;
    cursor: help;
  }
  
  .q-card {
    background: #fafafa;
    border-left: 4px solid #1976d2;
  }
  </style>