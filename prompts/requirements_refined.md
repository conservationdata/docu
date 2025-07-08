# quasar app

The app takes a JSON file with the structure defined in `datastructure.md` to produce a dynamic metadata entry interface for hierarchical forms in cultural heritage documentation.

It is designed to handle different `docu.json` files in a generic, schema-driven way, rendering the entire form hierarchy automatically without manual configuration.

---

## Requirements

### Forms

- **Dynamic generation**:
  - Forms are fully auto-generated from the uploaded `docu.json`.
  - Hierarchy is represented in the forms. Parent elements without `Feldwert` values are treated as containers of their children. Parents with `Feldwert` are forms that also contain children forms.
  - Hierarchy can have multiple nested levels and is rendered recursively.

- **Titles & tooltips**:
  - Each form has the `prefLabel` of the term as its title.
  - Mouseover on the title shows the `definition` of the term.
  - Mouseover on the entire form area shows the `Verwendungshinweis` of the term.

- **Wiederholbar**:
  - If `Wiederholbar` is "Ja", users can add or remove instances of the form (including their full nested children).
  - Multiple instances are stored as arrays under the term's `notation`.

- **Containers**:
  - Terms without `Feldwert` values serve purely as hierarchical containers.
  - They are rendered with a visible label/title and styled as containers to group their child forms clearly.

- **Input types based on `Feldwert`**:
  - containing only `"Text"` → single-line text input.
  - containing `"URI"` → input with a toggle to switch between free text and URI selection.

  - **Special form types via mapping**:
  - A `formTypes.json` file maps specific notations to specialized form components.
  - Supported special types include date pickers, measurement inputs with units and enumeration dropdowns.
  - The mapping overrides default `Feldwert` behavior for specified notations.
  - If no mapping exists, the app falls back to standard `Feldwert` parsing.

- **URI fields**:
  - For terms allowing URI Feldwerte, selection is via a treeview fueled by `normdata.json`.
  - Only leaf nodes of the normdata tree can be selected.
  - Selected entries are displayed as **Label (URI)** in the form.
  - No free-form URI entry is offered (all URIs are chosen from normdata).

- **Inline validation**:
  - Required fields (`Verpflichtungsgrad = "Pflicht"`) are validated immediately.
  - If left empty, the field shows a red border and a warning as soon as the user leaves the input.
  - This ensures better UX by guiding users early.

---

### Buttons

- **Save button**:
  - Saves the filled form data as JSON.
  - Disabled while any required ("Pflicht") field is empty. If saving is attempted with missing required fields, the app:
    - Displays an error listing the missing term.
    - Automatically scrolls to the first offending form.

- **Reset button**:
  - Clears all form inputs and resets to initial state.

- **Fill All Fields button**:
  - Loads data from `exemplary.json` and pre-fills the entire form hierarchy using its values.
  - Only fills terms whose `notation` exists in both `docu.json` and `exemplary.json`.

---

### Data Sources

- **docu.json**:
  - The main term definition file with the structure and hierarchy for the forms.

- **exemplary.json**:
  - Contains example data for pre-filling forms.
  - Keys = `notation` of the term to be filled, values = data to be filled.

- **normdata.json**:
  - Provides hierarchical norm data for filling URI-type fields.
  - Keys = `notation` of the term, values = hierarchical JSON structures used to power the treeview.

---

### Features

- **Prefill on App Start**:
  - At startup, the app automatically pre-fills specific main hierarchy branches of notations using data from `exemplary.json`:
    - `[A13CD1, ADD53A, CCCC7G, F2244D, G814D2, K343FVC, F58F6D]`
  - Only notations present in both `docu.json` and `exemplary.json` are prefilled.
  - Missing branches in `docu.json` are simply ignored.

- **Validation on Save**:
  - Data cannot be saved if any required ("Pflicht") field has no value.
  - Error feedback lists the missing terms and moves the user to the first one.

- **Generic handling**:
  - The app supports different `docu.json` structures, as long as they follow the data model.
  - No hard-coded knowledge about specific notations is assumed beyond the prefill list.

---

### Components

- **Recursive form generation**:
  - A single form component can render itself and all its children by calling itself recursively.
  - The hierarchy depth is not limited.

- **Component types**:
  - Containers without `Feldwert` → pure layout/grouping components with visible labels.
  - Containers with `Feldwert` → input forms that can contain nested forms.
  - Repetitive forms → dynamic add/remove buttons.
  - Specialized inputs → date pickers, text/URI toggle, dropdowns for controlled vocabularies, and treeviews for normdata.

- **Accessibility & UX**:
  - Tooltips for `definition` and `Verwendungshinweis`.
  - Inline validation for Pflicht fields with immediate visual feedback.
  - Clean, accessible navigation with automatic scrolling to errors.

---

### Notes

- The system assumes URIs are always selected from the normdata tree, so free-form URI validation is not required.
- The UI must remain clear, intuitive, and flexible enough to support changes in the `docu.json` structure between projects.
