# "Nur Pflichtfelder" Feature Documentation

## Overview

This feature adds a toggle button to the footer button group that allows users to switch between two view modes:

1. **Nur Pflichtfelder**: When active, the form only displays terms with `Verpflichtungsgrad` equal to "Pflicht" or "bedingte Pflicht"
2. **Erweiterter Datensatz**: When active, the form displays all terms

By default, the application starts in "Nur Pflichtfelder" mode.

## Implementation Details

### IndexPage.vue Changes

1. Added a `showOnlyRequired` reactive boolean, initialized to `true`
2. Added a toggle button to the footer that switches between the two view modes
3. Modified the `TermComponent` usage to pass the `showOnlyRequired` prop

### termComponent.vue Changes

1. Added `showOnlyRequired` prop
2. Implemented `shouldShowTerm` computed property that:
   - Returns `true` if `showOnlyRequired` is `false` (show all terms)
   - Returns `true` if the term's `Verpflichtungsgrad` is "Pflicht" or "bedingte Pflicht"
   - Returns `true` if the term has any descendants with "Pflicht" or "bedingte Pflicht" `Verpflichtungsgrad`
   - Returns `false` otherwise
3. Added `v-if="shouldShowTerm"` to the root template element to conditionally render the component
4. Pass `showOnlyRequired` prop to child `TermComponent` elements

### Filtering Logic

The filtering logic ensures that parent terms are still rendered if they have required children, even if the parent itself is not required. This maintains the hierarchical structure while hiding non-essential fields.

The recursive checking function traverses all descendants of a term to determine if any match the required criteria, ensuring that the entire path to required fields remains visible.

## User Experience

- The application starts with "Nur Pflichtfelder" mode active by default
- Users can click the button in the footer to toggle between the two modes:
  - When showing "Nur Pflichtfelder", only required fields and their parent containers are displayed
  - When showing "Erweiterter Datensatz", all form fields are displayed
- The filtering is applied in real-time as the user interacts with the toggle button
