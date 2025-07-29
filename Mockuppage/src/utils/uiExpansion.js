// src/utils/uiExpansion.js

export function toggleAll(terms, expand) {
  const recursiveToggle = (nodes) => {
    nodes.forEach(node => {
      if (node.narrower && node.narrower.length > 0) {
        node.isExpanded = expand;
        recursiveToggle(node.narrower);
      }
    });
  };
  recursiveToggle(terms);
}

export function expandToPath(path, terms) {
  let currentLevel = terms;
  for (let i = 0; i < path.length - 1; i++) {
    const index = path[i];
    if (currentLevel[index]) {
      currentLevel[index].isExpanded = true;
      currentLevel = currentLevel[index].narrower;
    }
  }
}