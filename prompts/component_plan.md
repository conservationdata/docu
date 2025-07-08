src/
├── components/
│   ├── DynamicForm.vue          # Main recursive form component
│   ├── FormField.vue            # Individual field component
│   ├── ContainerGroup.vue       # Pure container component
│   └── TreeSelector.vue         # URI selection tree
├── data/
│   ├── docu.json               # Main term definitions
│   ├── exemplary.json          # Example data
│   ├── normdata.json           # URI tree data
│   └── formTypes.json          # Special form type mappings
├── composables/
│   └── useFormData.js          # Form state management
└── pages/
    └── IndexPage.vue           # Main page

Key Components
1. IndexPage.vue (Main Container)

Load all JSON files
Render top-level DynamicForm
Handle Save/Reset/Fill All buttons
Manage global validation state
Auto-prefill on startup

2. DynamicForm.vue (Recursive Core)

Accepts a term object and renders appropriately
Determines if term is container-only or has input field
Handles Wiederholbar (add/remove instances)
Recursively renders narrower children
Manages tooltips for definition and Verwendungshinweis

3. FormField.vue (Input Handler)

Renders appropriate input based on Feldwert
Handles validation for Verpflichtungsgrad
Supports text, date, URI, and special form types
Shows inline validation errors

4. ContainerGroup.vue (Pure Containers)

For terms without Feldwert
Just displays prefLabel and groups children
Styled as a visual container/section

5. TreeSelector.vue (URI Selection)

Modal or dropdown tree for normdata selection
Only leaf nodes selectable
Displays as "Label (URI)" format

Data Flow
Form State Management (useFormData.js)

// Reactive form data object
const formData = ref({})

// Methods for:
// - setFieldValue(notation, value)
// - getFieldValue(notation)
// - validateRequired(docuData)
// - resetForm()
// - prefillFromExemplary(exemplaryData, notations)

Component Communication

Top-down: Pass term definitions and current values
Bottom-up: Emit value changes to update central state
Validation: Computed properties for real-time validation

Implementation Strategy
Phase 1: Basic Structure

Create DynamicForm component with basic recursion
Implement simple text inputs with validation
Add container-only term handling
Test with minimal docu.json

Phase 2: Enhanced Inputs

Add FormField component with Feldwert parsing
Implement URI toggle functionality
Add TreeSelector for normdata
Handle special form types mapping

Phase 3: Features

Add Wiederholbar (repeatable) functionality
Implement Save/Reset/Fill All buttons
Add tooltips and validation feedback
Auto-prefill on startup

Quasar Components to Use

q-form: For validation and submission
q-input: Text inputs with validation
q-date: Date picker for "Text (Datum)"
q-btn: All buttons
q-tooltip: For definition and usage hints
q-card: Container styling
q-separator: Visual hierarchy
q-tree: For normdata URI selection
q-dialog: Modal for tree selection
q-banner: Error messages
q-scroll-area: For long forms

Key Design Decisions

Single recursive component: DynamicForm handles all term types
Centralized state: One reactive object for all form data
Notation-based keys: Use term.notation for all data storage
Validation on blur: Immediate feedback for required fields
No external routing: Single page application
JSON in /data: Static files for easy swapping

This structure keeps it simple while meeting all requirements. The recursive nature handles unlimited nesting, and the component separation makes it maintainable without over-engineering.