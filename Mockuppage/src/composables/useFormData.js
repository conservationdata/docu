import { ref, computed } from 'vue'

// Global reactive form data store
const formData = ref({})

// Validation errors store
const validationErrors = ref(new Set())

export function useFormData() {
  
  // Set a field value
  const setFieldValue = (notation, value) => {
    if (!notation) return
    
    // Handle array values for repeatable fields
    if (Array.isArray(value)) {
      formData.value[notation] = [...value]
    } else {
      formData.value[notation] = value
    }
    
    // Remove from validation errors if value is provided
    if (value !== '' && value !== null && value !== undefined) {
      validationErrors.value.delete(notation)
    }
  }

  // Get a field value
  const getFieldValue = (notation) => {
    if (!notation) return undefined
    return formData.value[notation]
  }

  // Add a validation error
  const addValidationError = (notation) => {
    if (notation) {
      validationErrors.value.add(notation)
    }
  }

  // Remove a validation error
  const removeValidationError = (notation) => {
    if (notation) {
      validationErrors.value.delete(notation)
    }
  }

  // Check if field has validation error
  const hasValidationError = (notation) => {
    return validationErrors.value.has(notation)
  }

  // Validate all required fields recursively
  const validateRequired = (docuData, path = '') => {
    const errors = []
    
    const validateTerm = (term, currentPath) => {
      const notation = term.notation
      const fullPath = currentPath ? `${currentPath}.${notation}` : notation
      
      // Check if this term is required and has a field value
      if (term.Verpflichtungsgrad === 'Pflicht' && term.Feldwert) {
        const value = getFieldValue(notation)
        
        // Check if value is empty
        if (!value || value === '' || (Array.isArray(value) && value.length === 0)) {
          errors.push({
            notation,
            prefLabel: term.prefLabel,
            path: fullPath
          })
          addValidationError(notation)
        } else {
          removeValidationError(notation)
        }
      }
      
      // Recursively validate children
      if (term.narrower && Array.isArray(term.narrower)) {
        term.narrower.forEach(child => {
          validateTerm(child, fullPath)
        })
      }
    }
    
    // Validate all terms
    if (Array.isArray(docuData)) {
      docuData.forEach(term => validateTerm(term, path))
    } else {
      validateTerm(docuData, path)
    }
    
    return errors
  }

  // Reset all form data
  const resetForm = () => {
    formData.value = {}
    validationErrors.value.clear()
  }

  // Prefill form with exemplary data
  const prefillFromExemplary = (exemplaryData, notations = []) => {
    if (!exemplaryData) return
    
    // If specific notations are provided, only fill those
    if (notations.length > 0) {
      notations.forEach(notation => {
        if (exemplaryData[notation] !== undefined) {
          setFieldValue(notation, exemplaryData[notation])
        }
      })
    } else {
      // Fill all available data
      Object.entries(exemplaryData).forEach(([notation, value]) => {
        setFieldValue(notation, value)
      })
    }
  }

  // Get all form data as JSON
  const getFormDataAsJson = () => {
    return JSON.stringify(formData.value, null, 2)
  }

  // Load form data from JSON
  const loadFormDataFromJson = (jsonData) => {
    try {
      const data = typeof jsonData === 'string' ? JSON.parse(jsonData) : jsonData
      formData.value = { ...data }
      validationErrors.value.clear()
      return true
    } catch (error) {
      console.error('Error loading form data:', error)
      return false
    }
  }

  // Add item to repeatable field
  const addRepeatableItem = (notation, defaultValue = '') => {
    const currentValue = getFieldValue(notation)
    
    if (Array.isArray(currentValue)) {
      setFieldValue(notation, [...currentValue, defaultValue])
    } else {
      setFieldValue(notation, [currentValue || defaultValue, defaultValue])
    }
  }

  // Remove item from repeatable field
  const removeRepeatableItem = (notation, index) => {
    const currentValue = getFieldValue(notation)
    
    if (Array.isArray(currentValue) && index >= 0 && index < currentValue.length) {
      const newValue = [...currentValue]
      newValue.splice(index, 1)
      
      // If only one item left, convert back to single value
      if (newValue.length === 1) {
        setFieldValue(notation, newValue[0])
      } else if (newValue.length === 0) {
        setFieldValue(notation, '')
      } else {
        setFieldValue(notation, newValue)
      }
    }
  }

  // Update item in repeatable field
  const updateRepeatableItem = (notation, index, value) => {
    const currentValue = getFieldValue(notation)
    
    if (Array.isArray(currentValue) && index >= 0 && index < currentValue.length) {
      const newValue = [...currentValue]
      newValue[index] = value
      setFieldValue(notation, newValue)
    }
  }

  // Get flattened list of all terms for easier processing
  const flattenTerms = (terms) => {
    const flattened = []
    
    const processTerm = (term) => {
      flattened.push(term)
      if (term.narrower && Array.isArray(term.narrower)) {
        term.narrower.forEach(child => processTerm(child))
      }
    }
    
    if (Array.isArray(terms)) {
      terms.forEach(term => processTerm(term))
    }
    
    return flattened
  }

  // Find term by notation
  const findTermByNotation = (terms, notation) => {
    const flattened = flattenTerms(terms)
    return flattened.find(term => term.notation === notation)
  }

  // Computed properties
  const hasValidationErrors = computed(() => {
    return validationErrors.value.size > 0
  })

  const validationErrorCount = computed(() => {
    return validationErrors.value.size
  })

  const formDataCount = computed(() => {
    return Object.keys(formData.value).length
  })

  // Debug helpers
  const debugFormData = () => {
    console.log('Current form data:', formData.value)
    console.log('Validation errors:', Array.from(validationErrors.value))
  }

  return {
    // Reactive data
    formData,
    validationErrors,
    
    // Basic field operations
    setFieldValue,
    getFieldValue,
    
    // Validation
    addValidationError,
    removeValidationError,
    hasValidationError,
    validateRequired,
    
    // Form operations
    resetForm,
    prefillFromExemplary,
    getFormDataAsJson,
    loadFormDataFromJson,
    
    // Repeatable field operations
    addRepeatableItem,
    removeRepeatableItem,
    updateRepeatableItem,
    
    // Utility functions
    flattenTerms,
    findTermByNotation,
    
    // Computed properties
    hasValidationErrors,
    validationErrorCount,
    formDataCount,
    
    // Debug
    debugFormData
  }
}