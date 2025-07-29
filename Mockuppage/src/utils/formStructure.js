// src/utils/formStructure.js

export function createInitialTerms(termsList, path = [], expandNotations = ["F52262", "BAA258"]) {
  return termsList.map((term, index) => {
    const currentPath = [...path, index];
    const shouldExpand = expandNotations.includes(term.notation);
    if (shouldExpand && term.narrower && term.narrower.length > 0) {
      expandNotations.push(...term.narrower.map(t => t.notation));
    }
    const formTerm = {
      path: currentPath,
      prefLabel: term.prefLabel,
      notation: term.notation,
      definition: term.definition,
      Wiederholbar: term.Wiederholbar,
      Verpflichtungsgrad: term.Verpflichtungsgrad,
      Verwendungshinweis: term.Verwendungshinweis,
      Feldwert: term.Feldwert,
      Typ: term.Typ,
      Baum: term.Baum,
      Einheit: term.Einheit,
      Unsicher: term.Unsicher,
      isExpanded: shouldExpand,
      UnsicherValue: '',
    };

    if (term.Feldwert) {
      formTerm.value = '';
    }

    if (term.narrower) {
      formTerm.narrower = createInitialTerms(term.narrower, currentPath, expandNotations);
    }

    return formTerm;
  });
}

export function recalculatePaths(nodes, path = []) {
  nodes.forEach((node, index) => {
    const currentPath = [...path, index];
    node.path = currentPath;
    if (Array.isArray(node.narrower)) {
      recalculatePaths(node.narrower, currentPath);
    }
  });
}