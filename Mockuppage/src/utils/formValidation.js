// src/utils/formValidation.js

export function validateForm(currentTerms) {
  for (const term of currentTerms) {
    if (term.Verpflichtungsgrad === 'Pflicht' && term.Feldwert && !term.value) {
      return {
        error: `Fehler: '${term.prefLabel}' ist ein verpflichtendes Feld.`,
        path: term.path,
      };
    }
    if (term.narrower) {
      const nestedError = validateForm(term.narrower);
      if (nestedError) return nestedError;
    }
  }
  return null;
}

export function transformFormData(currentTerms) {
  const transformedTerms = [];
  for (const term of currentTerms) {
    const hasValue = term.value || (term.Feldwert && term.value === '');
    const hasChildren = term.narrower && term.narrower.length > 0;
    let narrowerExport = [];
    if (hasChildren) {
      narrowerExport = transformFormData(term.narrower);
    }

    if (hasValue || narrowerExport.length > 0) {
      const exportTerm = {
        Name: term.prefLabel,
        Identifikator: `https://conservationdata.github.io/terms/metadata/${term.notation}`,
      };

      if (term.Feldwert) {
        exportTerm.value = term.value;
      }

      if (term.Unsicher === 'Ja' && term.UnsicherValue === 'Ja') {
        exportTerm.Unsicher = 'Ja';
      }

      if (narrowerExport.length > 0) {
        exportTerm.Untereinträge = narrowerExport;
      }

      transformedTerms.push(exportTerm);
    }
  }
  return transformedTerms;
}