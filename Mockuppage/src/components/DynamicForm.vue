<template>
    <div class="dynamic-form">
      <!-- Render each term -->
      <div 
        v-for="term in terms" 
        :key="term.notation"
        class="term-container q-mb-md"
      >
        <!-- Container without Feldwert (Pure Container) -->
        <ContainerGroup 
          v-if="!term.Feldwert"
          :term="term"
          :form-data="formData"
          :norm-data="normData"
          :form-types="formTypes"
          @update:form-data="$emit('update:form-data', $event)"
          @validation-error="$emit('validation-error', $event)"
        />
        
        <!-- Term with Feldwert (Form Field + possible children) -->
        <div v-else class="field-term">
          <!-- Repeatable Field Container -->
          <div v-if="term.Wiederholbar === 'Ja'" class="repeatable-container">
            <div class="repeatable-header q-mb-sm">
              <div class="text-h6">{{ term.prefLabel }}</div>
              <q-btn 
                icon="add" 
                color="primary" 
                size="sm" 
                round 
                @click="addRepeatableInstance(term)"
                class="q-ml-sm"
              >
                <q-tooltip>Add {{ term.prefLabel }}</q-tooltip>
              </q-btn>
            </div>
            
            <!-- Repeatable Instances -->
            <div 
              v-for="(instance, index) in getRepeatableInstances(term)"
              :key="`${term.notation}-${index}`"
              class="repeatable-instance q-mb-sm"
            >
              <q-card class="q-pa-md" bordered>
                <div class="row items-center q-mb-sm">
                  <div class="col text-subtitle2">
                    {{ term.prefLabel }} #{{ index + 1 }}
                  </div>
                  <q-btn 
                    icon="delete" 
                    color="negative" 
                    size="sm" 
                    flat 
                    round 
                    @click="removeRepeatableInstance(term, index)"
                    class="q-ml-sm"
                  >
                    <q-tooltip>Remove this instance</q-tooltip>
                  </q-btn>
                </div>
                
                <!-- Form Field for this instance -->
                <FormField 
                  :term="term"
                  :value="instance.fieldValue"
                  :norm-data="normData"
                  :form-types="formTypes"
                  @update:value="updateRepeatableFieldValue(term, index, $event)"
                  @validation-error="$emit('validation-error', $event)"
                />
                
                <!-- Nested children for this instance -->
                <div v-if="term.narrower && term.narrower.length > 0" class="nested-children q-mt-md">
                  <DynamicForm 
                    :terms="term.narrower"
                    :form-data="instance.childrenData || {}"
                    :norm-data="normData"
                    :form-types="formTypes"
                    @update:form-data="updateRepeatableChildrenData(term, index, $event)"
                    @validation-error="$emit('validation-error', $event)"
                  />
                </div>
              </q-card>
            </div>
            
            <!-- Add first instance if none exist -->
            <div v-if="getRepeatableInstances(term).length === 0" class="text-center q-py-md">
              <q-btn 
                icon="add" 
                color="primary" 
                @click="addRepeatableInstance(term)"
                outline
              >
                Add {{ term.prefLabel }}
              </q-btn>
            </div>
          </div>
          
          <!-- Non-repeatable Field -->
          <div v-else class="single-field">
            <q-card class="q-pa-md" flat bordered>
              <!-- Field Title with Tooltip -->
              <div class="field-title q-mb-sm">
                <div class="text-h6">
                  {{ term.prefLabel }}
                  <q-icon 
                    v-if="term.definition" 
                    name="info" 
                    size="sm" 
                    class="q-ml-xs text-grey-6"
                  >
                    <q-tooltip class="text-body2" max-width="300px">
                      {{ term.definition }}
                    </q-tooltip>
                  </q-icon>
                  <span v-if="term.Verpflichtungsgrad === 'Pflicht'" class="text-red">*</span>
                </div>
              </div>
              
              <!-- Usage Hint Tooltip on entire form area -->
              <div 
                class="field-content"
                :class="{ 'field-with-hint': term.Verwendungshinweis }"
              >
                <q-tooltip 
                  v-if="term.Verwendungshinweis" 
                  class="text-body2" 
                  max-width="400px"
                >
                  {{ term.Verwendungshinweis }}
                </q-tooltip>
                
                <!-- Form Field -->
                <FormField 
                  :term="term"
                  :value="formData[term.notation]"
                  :norm-data="normData"
                  :form-types="formTypes"
                  @update:value="updateFieldValue(term, $event)"
                  @validation-error="$emit('validation-error', $event)"
                />
                
                <!-- Nested children -->
                <div v-if="term.narrower && term.narrower.length > 0" class="nested-children q-mt-md">
                  <q-separator class="q-mb-md" />
                  <DynamicForm 
                    :terms="term.narrower"
                    :form-data="formData"
                    :norm-data="normData"
                    :form-types="formTypes"
                    @update:form-data="$emit('update:form-data', $event)"
                    @validation-error="$emit('validation-error', $event)"
                  />
                </div>
              </div>
            </q-card>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed } from 'vue'
  import FormField from './FormField.vue'
  import ContainerGroup from './ContainerGroup.vue'
  
  export default {
    name: 'DynamicForm',
    components: {
      FormField,
      ContainerGroup
    },
    props: {
      terms: {
        type: Array,
        required: true
      },
      formData: {
        type: Object,
        default: () => ({})
      },
      normData: {
        type: Object,
        default: () => ({})
      },
      formTypes: {
        type: Object,
        default: () => ({})
      }
    },
    emits: ['update:form-data', 'validation-error'],
    setup(props, { emit }) {
      
      // Methods for repeatable fields
      const getRepeatableInstances = (term) => {
        const data = props.formData[term.notation]
        if (!data || !Array.isArray(data)) {
          return []
        }
        return data
      }
      
      const addRepeatableInstance = (term) => {
        const currentData = props.formData[term.notation] || []
        const newInstance = {
          fieldValue: null,
          childrenData: {}
        }
        
        const updatedData = [...currentData, newInstance]
        emit('update:form-data', {
          [term.notation]: updatedData
        })
      }
      
      const removeRepeatableInstance = (term, index) => {
        const currentData = props.formData[term.notation] || []
        const updatedData = currentData.filter((_, i) => i !== index)
        
        emit('update:form-data', {
          [term.notation]: updatedData.length > 0 ? updatedData : null
        })
      }
      
      const updateRepeatableFieldValue = (term, index, value) => {
        const currentData = [...(props.formData[term.notation] || [])]
        if (currentData[index]) {
          currentData[index].fieldValue = value
          emit('update:form-data', {
            [term.notation]: currentData
          })
        }
      }
      
      const updateRepeatableChildrenData = (term, index, childData) => {
        const currentData = [...(props.formData[term.notation] || [])]
        if (currentData[index]) {
          currentData[index].childrenData = {
            ...currentData[index].childrenData,
            ...childData
          }
          emit('update:form-data', {
            [term.notation]: currentData
          })
        }
      }
      
      const updateFieldValue = (term, value) => {
        emit('update:form-data', {
          [term.notation]: value
        })
      }
      
      return {
        getRepeatableInstances,
        addRepeatableInstance,
        removeRepeatableInstance,
        updateRepeatableFieldValue,
        updateRepeatableChildrenData,
        updateFieldValue
      }
    }
  }
  </script>
  
  <style scoped>
  .dynamic-form {
    width: 100%;
  }
  
  .term-container {
    margin-bottom: 1rem;
  }
  
  .repeatable-container {
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    padding: 1rem;
    background: #fafafa;
  }
  
  .repeatable-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 0.5rem;
  }
  
  .repeatable-instance {
    margin-left: 1rem;
  }
  
  .single-field {
    margin-bottom: 1rem;
  }
  
  .field-title {
    display: flex;
    align-items: center;
  }
  
  .field-content {
    position: relative;
  }
  
  .field-with-hint {
    cursor: help;
  }
  
  .nested-children {
    margin-left: 1rem;
    padding-left: 1rem;
    border-left: 2px solid #e0e0e0;
  }
  
  .text-red {
    color: #f44336;
  }
  </style>