# Data Structure

This document defines the JSON data model used to describe terms in an extended SKOS-like scheme for generating hierarchical metadata entry forms.

Each term in the JSON file is represented as an object with the following properties:

---

## Properties

### notation
- **Type:** String
- The unique identifier of the term.
- Used to generate its URI based on a namespace + notation.
- Also serves as the key for filled data output and for lookups in exemplary data or norm data.

---

### prefLabel
- **Type:** String
- The preferred label or name of the term.
- Displayed as the form title.

---

### altLabel
- **Type:** String (delimited)
- Alternative labels for the term.
- Multiple labels are separated with the `|` character.

---

### definition
- **Type:** String
- A definition of the term.
- Shown as a tooltip on the form title.

---

### Verwendungshinweis
- **Type:** String
- Guidance on how to use or interpret the term.
- Displayed as a tooltip on the form body.

---

### source
- **Type:** String
- References to literature or other sources for the definition or usage of the term.

---

### Verpflichtungsgrad
- **Type:** String
- Defines how mandatory the field is in the form.
  - `"Pflicht"` → required.
  - `"bedingte Pflicht"`, `"empfohlen"`, `"optional"` → optional, or conditionally required depending on context (the app treats them as optional for validation).

---

### Feldwert
- **Type:** String
- Defines the allowed data type(s) for the form field:
  - `"Text"` → free text input.
  - `"Text (Datum)"` → date input (app uses date picker).
  - `"Text/URI"` → input that can switch between text and a URI selected from a tree.
  - `"URI"` → selection from controlled norm data (no free text).
- Any additional annotation in brackets (e.g. `"Text (max. 250 Zeichen)"`) is to be ignored for form logic, but may be used to improve UX (e.g. hint text or counters).

---

### Wiederholbar
- **Type:** String
- Specifies if the field is repeatable:
  - `"Ja"` → user can add or remove multiple instances.
  - `"Nein"` → only one instance allowed.

---

### Vokabulare
- **Type:** String (optional)
- Lists recommended controlled vocabularies for this field.
- Can guide UI (e.g. offering dropdowns for predefined values if the vocabulary is known).

---

### narrower
- **Type:** Array
- Contains all child elements of this term.
- Each child is a term object with the same set of properties, allowing recursive hierarchy.

---

## Hierarchical Structure

- The overall JSON is a tree of terms connected via the `narrower` property.
- Terms without a `Feldwert` value are **pure containers**:
  - Used only to organize and group their `narrower` children.
  - They do not collect data themselves but appear in the form as labeled sections.
- Terms with a `Feldwert` can also have `narrower` children:
  - They contain their own form fields **and** embed nested child forms below them.

---

## Notes

- The form generation system relies entirely on this schema:
  - All UI hierarchy and form types are auto-generated from these properties.
- Terms must have a unique `notation` to avoid conflicts in output data.
- This structure supports dynamic use across different projects by simply swapping the JSON definition.
