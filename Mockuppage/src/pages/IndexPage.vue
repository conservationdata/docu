<template>
  <q-page class="q-pa-md">
    <!-- Header -->
    <div class="text-h4 q-mb-md">Metadata Entry Form</div>
    
    <!-- Loading State -->
    <div v-if="loading" class="text-center q-py-xl">
      <q-spinner size="2em" />
      <div class="q-mt-md">Loading form data...</div>
    </div>

    <!-- Error State -->
    <q-banner v-if="error" class="bg-negative text-white q-mb-md" dense>
      <template v-slot:avatar>
        <q-icon name="error" />
      </template>
      {{ error }}
    </q-banner>

    <!-- Main Content -->
    <div v-if="!loading && !error">
      <!-- Action Buttons -->
      <div class="q-mb-lg">
        <q-btn 
          color="primary" 
          icon="save" 
          label="Save" 
          @click="saveForm"
          :disable="!canSave"
          class="q-mr-sm"
        />
        <q-btn 
          color="secondary" 
          icon="refresh" 
          label="Reset" 
          @click="resetForm"
          outline
          class="q-mr-sm"
        />
        <q-btn 
          color="accent" 
          icon="auto_fix_high" 
          label="Fill All Fields" 
          @click="fillAllFields"
          outline
        />
      </div>

      <!-- Validation Error Banner -->
      <q-banner v-if="validationError" class="bg-warning text-black q-mb-md" dense>
        <template v-slot:avatar>
          <q-icon name="warning" />
        </template>
        <div>{{ validationError }}</div>
        <template v-slot:action>
          <q-btn 
            flat 
            color="black" 
            label="Go to first error" 
            @click="scrollToFirstError"
          />
        </template>
      </q-banner>

      <!-- Dynamic Form -->
      <q-form @submit="saveForm" class="q-gutter-md">
        <DynamicForm 
          v-if="docuData"
          :terms="docuData"
          :form-data="formData"
          :norm-data="normData"
          :form-types="formTypes"
          @update:form-data="updateFormData"
          @validation-error="handleValidationError"
        />
      </q-form>
    </div>
  </q-page>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import DynamicForm from '../components/DynamicForm.vue'

export default {
  name: 'IndexPage',
  components: {
    DynamicForm
  },
  setup() {
    const $q = useQuasar()
    
    // State
    const loading = ref(true)
    const error = ref('')
    const validationError = ref('')
    const docuData = ref(null)
    const exemplaryData = ref(null)
    const normData = ref(null)
    const formTypes = ref(null)
    const formData = ref({})
    
    // Auto-prefill notations on startup
    const PREFILL_NOTATIONS = ['A13CD1', 'ADD53A', 'CCCC7G', 'F2244D', 'G814D2', 'K343FVC', 'F58F6D']
    
    // Computed
    const canSave = computed(() => {
      return validateRequiredFields().isValid
    })
    
    // Methods
    const loadDataFiles = async () => {
      try {
        loading.value = true
        error.value = ''
        
        // Load all JSON files
        const [docuResponse, exemplaryResponse, normResponse, formTypesResponse] = await Promise.all([
          fetch('/data/docu.json'),
          fetch('/data/exemplary.json'),
          fetch('/data/normdata.json'),
          fetch('/data/formTypes.json')
        ])
        
        if (!docuResponse.ok) throw new Error('Failed to load docu.json')
        if (!exemplaryResponse.ok) throw new Error('Failed to load exemplary.json')
        if (!normResponse.ok) throw new Error('Failed to load normdata.json')
        if (!formTypesResponse.ok) throw new Error('Failed to load formTypes.json')
        
        docuData.value = await docuResponse.json()
        exemplaryData.value = await exemplaryResponse.json()
        normData.value = await normResponse.json()
        formTypes.value = await formTypesResponse.json()
        
        // Auto-prefill specific notations
        prefillFromExemplary(PREFILL_NOTATIONS)
        
      } catch (err) {
        error.value = `Error loading data: ${err.message}`
        console.error('Load error:', err)
      } finally {
        loading.value = false
      }
    }
    
    const prefillFromExemplary = (notations) => {
      if (!exemplaryData.value) return
      
      notations.forEach(notation => {
        if (exemplaryData.value[notation] !== undefined) {
          formData.value[notation] = exemplaryData.value[notation]
        }
      })
    }
    
    const fillAllFields = () => {
      if (!exemplaryData.value) return
      
      // Fill all available exemplary data
      Object.keys(exemplaryData.value).forEach(notation => {
        if (isNotationInDocu(notation)) {
          formData.value[notation] = exemplaryData.value[notation]
        }
      })
      
      $q.notify({
        type: 'positive',
        message: 'All fields filled with exemplary data'
      })
    }
    
    const isNotationInDocu = (notation) => {
      // Recursively check if notation exists in docu structure
      const checkInTerms = (terms) => {
        if (!Array.isArray(terms)) return false
        
        for (const term of terms) {
          if (term.notation === notation) return true
          if (term.narrower && checkInTerms(term.narrower)) return true
        }
        return false
      }
      
      return docuData.value ? checkInTerms(docuData.value) : false
    }
    
    const validateRequiredFields = () => {
      const errors = []
      
      // Recursively validate all required fields
      const validateTerms = (terms) => {
        if (!Array.isArray(terms)) return
        
        terms.forEach(term => {
          if (term.Verpflichtungsgrad === 'Pflicht' && term.Feldwert) {
            const value = formData.value[term.notation]
            if (!value || (Array.isArray(value) && value.length === 0)) {
              errors.push(term.prefLabel || term.notation)
            }
          }
          
          if (term.narrower) {
            validateTerms(term.narrower)
          }
        })
      }
      
      if (docuData.value) {
        validateTerms(docuData.value)
      }
      
      return {
        isValid: errors.length === 0,
        errors
      }
    }
    
    const saveForm = () => {
      validationError.value = ''
      
      const validation = validateRequiredFields()
      if (!validation.isValid) {
        validationError.value = `Missing required fields: ${validation.errors.join(', ')}`
        return
      }
      
      // Create clean output data (remove empty values)
      const cleanData = {}
      Object.keys(formData.value).forEach(key => {
        const value = formData.value[key]
        if (value !== null && value !== undefined && value !== '') {
          if (Array.isArray(value) && value.length > 0) {
            cleanData[key] = value
          } else if (!Array.isArray(value)) {
            cleanData[key] = value
          }
        }
      })
      
      // Save as JSON file
      const dataStr = JSON.stringify(cleanData, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      const url = URL.createObjectURL(dataBlob)
      const link = document.createElement('a')
      link.href = url
      link.download = 'form-data.json'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
      
      $q.notify({
        type: 'positive',
        message: 'Form data saved successfully'
      })
    }
    
    const resetForm = () => {
      formData.value = {}
      validationError.value = ''
      
      $q.notify({
        type: 'info',
        message: 'Form reset to initial state'
      })
    }
    
    const updateFormData = (data) => {
      formData.value = { ...formData.value, ...data }
    }
    
    const handleValidationError = (errorData) => {
      validationError.value = errorData.message
    }
    
    const scrollToFirstError = () => {
      // Find first element with validation error
      const errorElement = document.querySelector('.q-field--error')
      if (errorElement) {
        errorElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
    }
    
    // Lifecycle
    onMounted(() => {
      loadDataFiles()
    })
    
    return {
      loading,
      error,
      validationError,
      docuData,
      normData,
      formTypes,
      formData,
      canSave,
      saveForm,
      resetForm,
      fillAllFields,
      updateFormData,
      handleValidationError,
      scrollToFirstError
    }
  }
}
</script>

<style scoped>
.q-page {
  max-width: 1200px;
  margin: 0 auto;
}
</style>