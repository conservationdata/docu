# Project Documentation

This document provides an overview of the Quasar Vue3 web application, detailing its scripts, functions, and their purposes.

## Boot Files

### `boot/axios.js`

**Purpose:** This file configures and integrates the `axios` HTTP client into the Vue application. It creates a pre-configured instance for API communication and makes it globally available within Vue components.

**Functions:**

- **`defineBoot(callback)`**
  - **Purpose:** A Quasar helper function to register a boot file. The provided callback is executed during the application's initialization process.
  - **Ingoing Parameter:** `({ app })` - An object containing the Vue application instance.
  - **Outgoing Returns:** None. It modifies the `app` instance by attaching global properties.
  - **Called Functions:** None.

**Exports:**

- **`api`**
  - **Purpose:** An `axios` instance created with a default `baseURL` of `'https://api.example.com'`. It is intended for all communications with the application's backend API. It can be imported and used directly in JavaScript modules like Pinia stores.

### `boot/i18n.js`

**Purpose:** This file initializes and configures the `vue-i18n` library, enabling internationalization (i18n) for the application. It sets up the i18n instance with the necessary translation messages and integrates it with Vue.

**Functions:**

- **`defineBoot(callback)`**
  - **Purpose:** A Quasar helper function that registers this file to be executed when the application starts.
  - **Ingoing Parameter:** `({ app })` - An object containing the Vue application instance.
  - **Outgoing Returns:** None. It configures the `app` instance to use the i18n plugin.
  - **Called Functions:**
    - `createI18n()`: Creates an instance of the i18n plugin.
    - `app.use()`: Installs the i18n plugin into the Vue application.

## Components

### `components/contactComponent.vue`

**Purpose:** This component displays a "Kontakt" button that, when clicked, reveals a list of contact email addresses. The emails are stored in an obfuscated format to deter scrapers and are decoded on the fly. The component is responsive, showing a vertical list on mobile and a horizontal list on desktop.

**State:**

- **`showEmails`**: A reactive boolean (`ref`) that toggles the visibility of the email list.
- **`obfuscatedEmails`**: A reactive `ref` holding an array of strings, where each string is an obfuscated email address.

**Computed Properties:**

- **`decodedEmails`**
  - **Purpose:** Decodes the `obfuscatedEmails` into a readable format.
  - **Logic:** It maps over the `obfuscatedEmails` array, removes all numeric characters from each string, and then splits the string by the character 'x' to reconstruct the email address in the format `firstName.lastName@domain.tld`.
  - **Returns:** An array of decoded email address strings.

### `components/dialogueComponent.vue`

**Purpose:** This component presents a persistent welcome dialog to the user upon visiting the application. The dialog provides an introduction to the tool, explains its key features, and gives instructions on how to proceed. It remains on screen until the user explicitly dismisses it.

**State:**

- **`showIntroDialog`**: A reactive boolean (`ref`) that controls the visibility of the dialog. It is initialized to `true`, making the dialog visible by default.

### `components/inputComponent.vue`

**Purpose:** A versatile and dynamic component that renders different types of form inputs based on the configuration provided in the `term` prop. It is designed to be highly reusable and is central to the application's data entry forms.

**Props:**

- **`modelValue`**: The value of the input, enabling `v-model` binding.
- **`term`**: An object containing metadata that defines the input's behavior, such as its type (`Typ`), usage instructions (`Verwendungshinweis`), expected value format (`Feldwert`), and associated units (`Einheit`).
- **`path`**: A string representing the location of the data within the overall form structure.

**Emits:**

- **`update:modelValue`**: Emitted whenever the input's value changes, allowing for two-way data binding with the parent component.

**Computed Properties:**

- **`inputConfig`**:
  - **Purpose:** Parses the `term.Typ` JSON string to determine the type of input to render (e.g., `date`, `radio`, `checkbox`).
  - **Returns:** A configuration object.
- **`unitOptions`**:
  - **Purpose:** Parses the `term.Einheit` string to extract a list of possible units for the input value.
  - **Returns:** An array of unit strings.

**Functions:**

- **`extractUnit(value)`**:
  - **Purpose:** Separates a string value into its numerical part and its unit.
  - **Ingoing Parameter:** `value` (String) - The input string to parse.
  - **Returns:** An object `{ valueOnly, unit }`.

**Watchers:**

- The component uses `watch` to synchronize its internal state with the `modelValue` prop and to emit `update:modelValue` events when the user changes the input.

### `components/termComponent.vue`

**Purpose:** This is a recursive component responsible for rendering an individual "term" or field within the data entry form. It dynamically displays the term's label, an appropriate input field (via `InputComponent`), and controls for repeating or nesting terms.

**Props:**

- **`term`**: An object representing the metadata and value of a single form field.

**Injected Services:**

- **`formManager`**: A global service that manages the state of the entire form, including adding, removing, and updating fields.

**Computed Properties:**

- **`termId`**: Generates a unique DOM ID for the term's container.
- **`link`**: Constructs a URL to the term's definition.
- **`isOnlyInstance`**: Determines if the term is the last of its kind, which is used to disable the delete button.
- **`unsicherValue`**: A computed property with a getter and setter to manage the "Unsicher" (Uncertain) checkbox.

**Functions:**

- **`toggleExpansion()`**: Toggles the visibility of a term's child terms.
- **`updateValue(newVal)`**: Updates the term's value in the central `formManager`.

### `components/uriSelector.vue`

**Purpose:** This component renders a hierarchical tree structure, allowing users to select a value from a controlled vocabulary. It is used within `InputComponent` when a field is configured to accept a URI.

**Props:**

- **`term`**: The term object, which contains the tree structure in a JSON string property named `Baum`.
- **`modelValue`**: The currently selected URI, enabling `v-model` binding.

**Emits:**

- **`update:modelValue`**: Emitted when the user selects a new URI from the tree.

**Computed Properties:**

- **`tree`**:
  - **Purpose:** Parses the `term.Baum` JSON string to build the data structure required by the Quasar `q-tree` component.
  - **Returns:** An array of nodes representing the tree.
- **`allUrisInTree`**:
  - **Purpose:** Flattens the tree structure into a simple array of all possible URI values. This is used to validate the `modelValue`.
  - **Returns:** An array of URI strings.

**Functions:**

- **`handleSelection(targetKey)`**:
  - **Purpose:** Updates the component's internal state and emits the `update:modelValue` event when a user selects a node in the tree.
  - **Ingoing Parameter:** `targetKey` (String) - The `node-key` of the selected item.

## i18n

### `i18n/index.js`

**Purpose:** This file acts as the central hub for the application's translation messages. It imports all the individual language packs and exports them as a single object, which is then used to configure the `vue-i1e-i18n` instance.

### `i18n/en-US/index.js`

**Purpose:** This file provides the English (US) language pack for the application. It exports an object containing key-value pairs, where each key is a unique identifier for a piece of text, and the value is its English translation.

## Layouts

### `layouts/MainLayout.vue`

**Purpose:** This component serves as the primary visual structure for the application. It defines a consistent layout with a header, a footer, and a main content area for displaying different pages. The layout is responsive, adapting its design for both mobile and desktop viewports.

**Components Used:**

- **`DialogueComponent`**: The welcome dialog is included here, so it is displayed as soon as the main layout is loaded.
- **`ContactComponent`**: This component is used in the footer to provide contact information.
- **`router-view`**: This is the placeholder where the content of the current page (as determined by the router) is rendered.

## Pages

### `pages/ErrorNotFound.vue`

**Purpose:** This page is displayed whenever the user tries to access a route that doesn't exist within the application. It serves as a user-friendly "404 Not Found" error page, providing a clear message and a button to navigate back to the homepage.

### `pages/IndexPage.vue`

**Purpose:** This is the core page of the application, responsible for rendering the main data entry form. It dynamically generates the form based on a JSON data definition and provides a suite of tools for the user to interact with the form, validate their input, and export the final data.

**State:**

- **`terms`**: A reactive `ref` that holds the entire form structure as a tree of term objects.
- **`exportTerms`**: A `ref` to store the transformed and validated form data, ready for export.
- **`displayOutput`**: A `ref` containing the string representation of the output data (either JSON or XML).
- **`outputFormat`**: A `ref` that tracks the user's selected format for the output data ('json' or 'xml').

**Functions:**

- **`onSubmit()`**: Validates the form, and if successful, transforms the data and prepares it for export.
- **`onReset()`**: Resets the form to its initial state.
- **`updateOutput()`**: Updates the `displayOutput` string based on the current `outputFormat`.

**Provided Services:**

- **`formManager`**: This page provides a `formManager` object to all its child components. This service is a central hub for all form-related actions, including:
  - **`addFieldAtPath(path)`**: Adds a new instance of a repeatable field.
  - **`removeFieldAtPath(path)`**: Removes an instance of a repeatable field.
  - **`updateValueAtPath(path, value, field)`**: Updates the value of a specific field.
  - **`toggleExpansionAtPath(path)`**: Toggles the expanded/collapsed state of a term.

## Router

### `router/index.js`

**Purpose:** This file is the main configuration entry point for the application's routing system. It uses the `defineRouter` helper from Quasar to create and configure the Vue Router instance.

**Functions:**

- **`defineRouter(callback)`**:
  - **Purpose:** A Quasar wrapper function that initializes the router. The callback function it receives is responsible for creating and returning the router instance.
  - **Logic:**
    - It determines the appropriate history mode (`createMemoryHistory` for SSR, `createWebHistory` or `createWebHashHistory` for client-side rendering) based on the environment variables.
    - It instantiates the router with the defined `routes` and a `scrollBehavior` that scrolls to the top of the page on every navigation.
  - **Returns:** The configured Vue Router instance.

### `router/routes.js`

**Purpose:** This file defines the application's routes. It exports an array of route objects, where each object maps a URL path to a specific component.

**Routes:**

- **`path: '/'`**: The main route of the application.
  - It uses `MainLayout.vue` as its layout.
  - Its main content is provided by the `IndexPage.vue` component.
- **`path: '/:catchAll(.*)*'`**: A catch-all route.
  - This route will match any URL that hasn't been matched by the other routes.
  - It displays the `ErrorNotFound.vue` page, effectively handling 404 errors.

## Stores

### `stores/example-store.js`

**Purpose:** This file serves as a boilerplate example of a Pinia store. It defines a simple store named `counter` to manage a piece of state and is intended to be a template for creating new stores.

**State:**

- **`counter`**: A number that holds the current count.

**Getters:**

- **`doubleCount`**: A computed property that returns the value of `counter` multiplied by 2.

**Actions:**

- **`increment()`**: A function that increases the value of `counter` by 1.

### `stores/index.js`

**Purpose:** This file is the initialization point for the Pinia state management library. It uses the `defineStore` helper from Quasar to create the main Pinia instance for the application.

**Functions:**

- **`defineStore(callback)`**:
  - **Purpose:** A Quasar wrapper function that sets up the Pinia store. The callback it receives is responsible for creating and returning the Pinia instance.
  - **Returns:** The root Pinia instance.

## Utils

### `utils/fieldOperations.js`

**Purpose:** This module contains utility functions for performing operations on the form's data fields, such as filling them with example data or clearing their values.

**Functions:**

- **`fillAllFields(currentTerms, exclude)`**:
  - **Purpose:** Recursively traverses the form's term structure and populates each field with a corresponding value from `src/data/example.json`.
  - **Ingoing Parameters:**
    - `currentTerms` (Array): The array of term objects to be filled.
    - `exclude` (Array): An array of `notation` strings for terms that should not be filled with example data.
- **`resetValues(node)`**:
  - **Purpose:** Recursively clears the `value` and `UnsicherValue` properties of a given term and all its descendants. It also collapses any expanded sections.
  - **Ingoing Parameter:** `node` (Object): The term object to reset.

### `utils/formStructure.js`

**Purpose:** This module provides functions for creating and managing the hierarchical structure of the form.

**Functions:**

- **`createInitialTerms(termsList, path, expandNotations)`**:
  - **Purpose:** Recursively transforms a list of term definitions into a reactive data structure that can be used to render the form. It initializes each term with default values and sets its initial expansion state.
  - **Ingoing Parameters:**
    - `termsList` (Array): The list of term definitions from the JSON data.
    - `path` (Array): The current path in the hierarchy.
    - `expandNotations` (Array): A list of `notation` strings for terms that should be expanded by default.
  - **Returns:** An array of initialized term objects.
- **`recalculatePaths(nodes, path)`**:
  - **Purpose:** Recursively traverses the form's data structure and updates the `path` property of each term. This is essential after adding or removing repeatable fields to ensure that each field can be uniquely identified.
  - **Ingoing Parameters:**
    - `nodes` (Array): The array of term objects to update.
    - `path` (Array): The current path in the hierarchy.

### `utils/formValidation.js`

**Purpose:** This module contains functions related to form validation and data transformation for export.

**Functions:**

- **`validateForm(currentTerms)`**:
  - **Purpose:** Recursively checks the form data to ensure that all mandatory fields have been filled.
  - **Ingoing Parameter:** `currentTerms` (Array): The array of term objects to validate.
  - **Returns:** An object containing an error message and the path to the invalid field if validation fails, otherwise `null`.
- **`transformFormData(currentTerms)`**:
  - **Purpose:** Recursively traverses the form data and transforms it into a simplified, clean format suitable for export. It only includes fields that have a value or have child fields with values.
  - **Ingoing Parameter:** `currentTerms` (Array): The array of term objects to transform.
  - **Returns:** A new array of transformed term objects.

### `utils/outputExport.js`

**Purpose:** This module contains utility functions for exporting the final form data.

**Functions:**

- **`jsonToSimplifiedXml(jsonData)`**:
  - **Purpose:** Converts the transformed JSON data into a well-structured XML string.
  - **Ingoing Parameter:** `jsonData` (Array): The array of transformed term objects.
  - **Returns:** A string containing the XML representation of the data.
- **`copyToClipboard(displayOutput, outputFormat, $q)`**:
  - **Purpose:** Returns a function that, when called, copies the generated output (either JSON or XML) to the user's clipboard.
  - **Ingoing Parameters:**
    - `displayOutput` (Ref): A Vue ref containing the string to be copied.
    - `outputFormat` (Ref): A Vue ref indicating the current format ('json' or 'xml').
    - `$q` (Object): The Quasar `useQuasar` composable, used for showing notifications.
  - **Returns:** An asynchronous function.
- **`downloadOutput(displayOutput, outputFormat, $q)`**:
  - **Purpose:** Returns a function that, when called, triggers a file download of the generated output.
  - **Ingoing Parameters:**
    - `displayOutput` (Ref): A Vue ref containing the string content for the file.
    - `outputFormat` (Ref): A Vue ref indicating the current format, which determines the file extension and MIME type.
    - `$q` (Object): The Quasar `useQuasar` composable, for notifications.
  - **Returns:** A function.

### `utils/uiExpansion.js`

**Purpose:** This module contains utility functions for controlling the expansion and collapse state of the UI components.

**Functions:**

- **`toggleAll(terms, expand)`**:
  - **Purpose:** Recursively traverses the entire form structure and sets the `isExpanded` property of each term to either `true` or `false`.
  - **Ingoing Parameters:**
    - `terms` (Array): The array of term objects to act upon.
    - `expand` (Boolean): `true` to expand all terms, `false` to collapse them.
- **`expandToPath(path, terms)`**:
  - **Purpose:** Expands all parent terms along a given path to ensure that a specific nested term becomes visible to the user. This is particularly useful for highlighting validation errors.
  - **Ingoing Parameters:**
    - `path` (Array): An array of indices representing the path to the target term.
    - `terms` (Array): The root array of term objects.
