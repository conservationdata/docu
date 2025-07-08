<template>
    <div class="form-field">
      <!-- Special Form Types (from formTypes.json mapping) -->
      <div v-if="specialFormType">
        <!-- Date Picker -->
        <q-input 
          v-if="specialFormType === 'date'"
          v-model="localValue"
          :label="term.prefLabel"
          :rules="validationRules"
          :error="hasValidationError"
          :error-message="validationErrorMessage"
          @blur="handleBlur"
          @update:model-value="updateValue"
          filled
          readonly
        >
          <template v-slot:append>
            <q-icon name="event" class="cursor-pointer">
              <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                <q-date 
                  v-model="localValue" 
                  @update:model-value="updateValue"
                  mask="YYYY-MM-DD"
                >
                  <div class="row items-center justify-end">
                    <q-btn v-close-popup label="Close" color="primary" flat />
                  </div>
                </q-date>
              </q-popup-proxy>
            </q-icon>
          </template>
        </q-input>
        
        <!-- Dropdown/Select -->
        <q-select
          v-else-if="specialFormType === 'dropdown' && specialFormOptions"
          v-model="localValue"
          :options="specialFormOptions"
          :label="term.prefLabel"
          :rules="validationRules"
          :error="hasValidationError"
          :error-message="validationErrorMessage"
          @blur="handleBlur"
          @update:model-value="updateValue"
          filled
          clearable
        />
        
        <!-- Measurement with Unit -->
        <div v-else-if="specialFormType === 'measurement'" class="measurement-field">
          <div class="row q-gutter-sm">
            <div class="col-8">
              <q-input
                v-model="measurementValue"
                :label="`${term.prefLabel} (Value)`"
                type="number"
                :rules="validationRules"
                :error="hasValidationError"
                :error-message="validationErrorMessage"
                @blur="handleBlur"
                @update:model-value="updateMeasurementValue"
                filled
              />
            </div>
            <div class="col-4">
              <q-select
                v-model="measurementUnit"
                :options="measurementUnits"
                label="Unit"
                @update:model-value="updateMeasurementUnit"
                filled
              />
            </div>
          </div>
        </div>
      </div>
      
      <!-- Standard Feldwert Types -->
      <div v-else>
        <!-- Text Input -->
        <q-input
          v-if="isTextInput"
          v-model="localValue"
          :label="term.prefLabel"
          :rules="validationRules"
          :error="hasValidationError"
          :error-message="validationErrorMessage"
          @blur="handleBlur"
          @update:model-value="updateValue"
          filled
        />
        
        <!-- Date Input (Text (Datum)) -->
        <q-input 
          v-else-if="isDateInput"
          v-model="localValue"
          :label="term.prefLabel"
          :rules="validationRules"
          :error="hasValidationError"
          :error-message="validationErrorMessage"
          @blur="handleBlur"
          @update:model-value="updateValue"
          filled
          readonly
        >
          <template v-slot:append>
            <q-icon name="event" class="cursor-pointer">
              <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                <q-date 
                  v-model="localValue" 
                  @update:model-value="updateValue"
                  mask="YYYY-MM-DD"
                >
                  <div class="row items-center justify-end">
                    <q-btn v-close-popup label="Close" color="primary" flat />
                  </div>
                </q-date>
              </q-popup-proxy>
            </q-icon>
          </template>
        </q-input>
        
        <!-- Text/URI Toggle -->
        <div v-else-if="isTextUriInput" class="text-uri-field">
          <div class="row q-gutter-sm q-mb-sm">
            <q-btn-toggle
              v-model="inputMode"
              :options="[
                { label: 'Text', value: 'text' },
                { label: 'URI', value: 'uri' }
              ]"
              @update:model-value="handleInputModeChange"
              color="primary"
              toggle-color="primary"
            />
          </div>
          
          <!-- Text Mode -->
          <q-input
            v-if="inputMode === 'text'"
            v-model="localValue"
            :label="term.prefLabel"
            :rules="validationRules"
            :error="hasValidationError"
            :error-message="validationErrorMessage"
            @blur="handleBlur"
            @update:model-value="updateValue"
            filled
          />
          
          <!-- URI Mode -->
          <div v-else class="uri-selection">
            <q-input
              v-model="uriDisplayValue"
              :label="term.prefLabel"
              :rules="validationRules"
              :error="hasValidationError"
              :error-message="validationErrorMessage"
              @blur="handleBlur"
              filled
              readonly
            >
              <template v-slot:append>
                <q-btn 
                  icon="search" 
                  flat 
                  @click="openUriSelector"
                  :disable="!hasNormData"
                >
                  <q-tooltip>Select from controlled vocabulary</q-tooltip>
                </q-btn>
              </template>
            </q-input>
          </div>
        </div>
        
        <!-- Pure URI Input -->
        <div v-else-if="isUriInput" class="uri-field">
          <q-input
            v-model="uriDisplayValue"
            :label="term.prefLabel"
            :rules="validationRules"
            :error="hasValidationError"
            :error-message="validationErrorMessage"
            @blur="handleBlur"
            filled
            readonly
          >
            <template v-slot:append>
              <q-btn 
                icon="search" 
                flat 
                @click="openUriSelector"
                :disable="!hasNormData"
              >
                <q-tooltip>Select from controlled vocabulary</q-tooltip>
              </q-btn>
            </template>
          </q-input>
        </div>
      </div>
      
      <!-- URI Selector Dialog -->
      <q-dialog v-model="showUriSelector" maximized>
        <q-card class="uri-selector-dialog">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">Select {{ term.prefLabel }}</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>
          
          <q-card-section class="q-pt-none">
            <TreeSelector
              v-if="hasNormData"
              :tree-data="normData[term.notation]"
              :selected-value="selectedUri"
              @select="handleUriSelection"
            />
            <div v-else class="text-center q-py-xl text-grey-6">
              No controlled vocabulary available for this field
            </div>
          </q-card-section>
        </q-card>
      </q-dialog>
    </div>
  </template>
  
  <script>
  import { ref, computed, watch } from 'vue'
  import TreeSelector from './TreeSelector.vue'
  
  export default {
    name: 'FormField',
    components: {
      TreeSelector
    },
    props: {
      term: {
        type: Object,
        required: true
      },
      value: {
        default: null
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
    emits: ['update:value', 'validation-error'],
    setup(props, { emit }) {
      // Local state
      const localValue = ref(props.value || '')
      const inputMode = ref('text')
      const showUriSelector = ref(false)
      const selectedUri = ref(null)
      const uriDisplayValue = ref('')
      const hasBlurred = ref(false)
      
      // Measurement field states
      const measurementValue = ref('')
      const measurementUnit = ref('')
      const measurementUnits = ref(['mm', 'cm', 'm', 'km', 'g', 'kg', 'mg'])
      
      // Computed properties
      const specialFormType = computed(() => {
        return props.formTypes[props.term.notation]?.type || null
      })
      
      const specialFormOptions = computed(() => {
        return props.formTypes[props.term.notation]?.options || []
      })
      
      const feldwert = computed(() => {
        return props.term.Feldwert || ''
      })
      
      const isTextInput = computed(() => {
        return feldwert.value.toLowerCase().includes('text') && 
               !feldwert.value.toLowerCase().includes('datum') &&
               !feldwert.value.toLowerCase().includes('uri')
      })
      
      const isDateInput = computed(() => {
        return feldwert.value.toLowerCase().includes('text') && 
               feldwert.value.toLowerCase().includes('datum')
      })
      
      const isTextUriInput = computed(() => {
        return feldwert.value.toLowerCase().includes('text/uri')
      })
      
      const isUriInput = computed(() => {
        return feldwert.value.toLowerCase().includes('uri') && 
               !feldwert.value.toLowerCase().includes('text/')
      })
      
      const hasNormData = computed(() => {
        return props.normData[props.term.notation] !== undefined
      })
      
      const isRequired = computed(() => {
        return props.term.Verpflichtungsgrad === 'Pflicht'
      })
      
      const hasValidationError = computed(() => {
        return hasBlurred.value && isRequired.value && !localValue.value
      })
      
      const validationErrorMessage = computed(() => {
        if (hasValidationError.value) {
          return `${props.term.prefLabel} is required`
        }
        return ''
      })
      
      const validationRules = computed(() => {
        if (isRequired.value) {
          return [
            val => (val && val.length > 0) || `${props.term.prefLabel} is required`
          ]
        }
        return []
      })
      
      // Methods
      const updateValue = (newValue) => {
        localValue.value = newValue
        emit('update:value', newValue)
      }
      
      const handleBlur = () => {
        hasBlurred.value = true
        if (hasValidationError.value) {
          emit('validation-error', {
            notation: props.term.notation,
            message: validationErrorMessage.value
          })
        }
      }
      
      const handleInputModeChange = (mode) => {
        inputMode.value = mode
        if (mode === 'text') {
          uriDisplayValue.value = ''
          selectedUri.value = null
          updateValue('')
        } else {
          localValue.value = ''
          updateValue('')
        }
      }
      
      const openUriSelector = () => {
        showUriSelector.value = true
      }
      
      const handleUriSelection = (selection) => {
        selectedUri.value = selection.uri
        uriDisplayValue.value = `${selection.label} (${selection.uri})`
        updateValue(selection.uri)
        showUriSelector.value = false
      }
      
      // Measurement field methods
      const updateMeasurementValue = (newValue) => {
        measurementValue.value = newValue
        updateMeasurementData()
      }
      
      const updateMeasurementUnit = (newUnit) => {
        measurementUnit.value = newUnit
        updateMeasurementData()
      }
      
      const updateMeasurementData = () => {
        if (measurementValue.value && measurementUnit.value) {
          const measurementData = {
            value: measurementValue.value,
            unit: measurementUnit.value
          }
          updateValue(measurementData)
        } else {
          updateValue(null)
        }
      }
      
      // Initialize measurement data if needed
      const initializeMeasurementData = () => {
        if (specialFormType.value === 'measurement' && props.value) {
          if (typeof props.value === 'object' && props.value.value && props.value.unit) {
            measurementValue.value = props.value.value
            measurementUnit.value = props.value.unit
          }
        }
      }
      
      // Initialize URI display if needed
      const initializeUriDisplay = () => {
        if ((isTextUriInput.value || isUriInput.value) && props.value) {
          if (typeof props.value === 'string' && props.value.startsWith('http')) {
            inputMode.value = 'uri'
            selectedUri.value = props.value
            uriDisplayValue.value = props.value // Will be enhanced by TreeSelector if available
          } else {
            inputMode.value = 'text'
            localValue.value = props.value
          }
        }
      }
      
      // Watch for prop changes
      watch(() => props.value, (newValue) => {
        if (newValue !== localValue.value) {
          localValue.value = newValue || ''
          initializeMeasurementData()
          initializeUriDisplay()
        }
      }, { immediate: true })
      
      // Initialize on mount
      initializeMeasurementData()
      initializeUriDisplay()
      
      return {
        localValue,
        inputMode,
        showUriSelector,
        selectedUri,
        uriDisplayValue,
        hasBlurred,
        measurementValue,
        measurementUnit,
        measurementUnits,
        specialFormType,
        specialFormOptions,
        isTextInput,
        isDateInput,
        isTextUriInput,
        isUriInput,
        hasNormData,
        hasValidationError,
        validationErrorMessage,
        validationRules,
        updateValue,
        handleBlur,
        handleInputModeChange,
        openUriSelector,
        handleUriSelection,
        updateMeasurementValue,
        updateMeasurementUnit
      }
    }
  }
  </script>
  
  <style scoped>
  .form-field {
    width: 100%;
  }
  
  .text-uri-field {
    width: 100%;
  }
  
  .uri-selection {
    width: 100%;
  }
  
  .uri-field {
    width: 100%;
  }
  
  .measurement-field {
    width: 100%;
  }
  
  .uri-selector-dialog {
    width: 90vw;
    max-width: 800px;
  }
  </style>