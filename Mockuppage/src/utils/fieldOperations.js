// src/utils/fieldOperations.js

import exampleData from 'src/data/example.json';

export function fillAllFields(currentTerms, exclude) {
  const fillTermsRecursively = (terms, exclude) => {
    terms.forEach(term => {
      if (!exclude.includes(term.notation)) {
        if (term.Feldwert && term.notation && exampleData[term.notation]) {
          const exampleValue = exampleData[term.notation];
          if (exampleValue && exampleValue.trim() !== '') {
            term.value = exampleValue;
          }
        }
        if (term.narrower && term.narrower.length > 0) {
          fillTermsRecursively(term.narrower, exclude);
        }
      }
    });
  };
  fillTermsRecursively(currentTerms, exclude);
}

export function resetValues(node) {
  if ('value' in node) node.value = '';
  if ('UnsicherValue' in node) node.UnsicherValue = '';
  if ('isExpanded' in node) node.isExpanded = false;
  if (Array.isArray(node.narrower)) {
    node.narrower.forEach(child => resetValues(child));
  }
}