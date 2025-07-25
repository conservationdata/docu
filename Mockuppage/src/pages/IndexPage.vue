<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-page class="q-pa-md form-page" :style-fn="pageStyle">
        <q-form class="q-gutter-md">
          <TermComponent
            v-for="term in terms"
            :key="term.path.join('-')"
            :term="term"
          />
        </q-form>
        <div v-if="exportTerms.length > 0" class="q-mt-xl">
          <div class="row">
            <p class="text-h6 q-mb-none text-secondary">{{ outputFormat === 'json' ? 'Proto-JSON' : 'Proto-XML' }}</p>
            <q-space />
            <div class="row">
              <q-btn-toggle
                v-model="outputFormat"
                toggle-color="accent"
                text-color="secondary"
                :options="[
                  {label: 'JSON', value: 'json'},
                  {label: 'XML', value: 'xml'}
                ]"
                @update:model-value="updateOutput"
              />
              <q-btn-group push>
                <q-btn
                  :label="`Download`"
                  color="accent"
                  text-color="secondary"
                  icon="mdi-download"
                  @click="downloadOutput"
                  flat
                />
                <q-separator vertical class="q-mx-sm" />
                <q-btn
                  label="Kopieren"
                  color="accent"
                  text-color="secondary"
                  icon="mdi-content-copy"
                  @click="copyToClipboard"
                  flat
                />
              </q-btn-group>
            </div>
          </div>
          <pre>{{ displayOutput }}</pre>
        </div>
        <div v-if="exportTerms.length > 0" class="q-pb-xl"></div>
      </q-page>
    </q-page-container>
    <q-footer bordered class="bg-primary text-secondary footer-container">
      <q-toolbar class="column q-py-sm">
        <div class="row justify-center q-mb-sm">
          <q-btn-group push>
            <q-btn
              label="Abschicken"
              type="submit"
              color="accent"
              text-color="secondary"
              icon="mdi-check-circle"
              @click="onSubmit"
              flat
            />
            <q-separator vertical class="q-mx-sm" />
            <q-btn
              label="Zurücksetzen"
              type="reset"
              color="accent"
              text-color="secondary"
              icon="mdi-reload"
              @click="onReset"
              flat
            />
            <q-separator vertical class="q-mx-sm" />
            <q-btn
              label="Felder ausfüllen"
              color="accent"
              text-color="secondary"
              icon="mdi-auto-fix"
              @click="() => fillAllFields(excludeNotations.value)"
              flat
            />
            <q-separator vertical class="q-mx-sm" />
            <q-btn
              label="Ausklappen"
              color="accent"
              text-color="secondary"
              icon="mdi-unfold-more-vertical"
              @click="toggleAll(true)"
              flat
            />
            <q-separator vertical class="q-mx-sm" />
            <q-btn
              label="Einklappen"
              color="accent"
              text-color="secondary"
              icon="mdi-unfold-less-vertical"
              @click="toggleAll(false)"
              flat
            />
          </q-btn-group>
        </div>
        <q-breadcrumbs  separator="|" separator-color="secondary" active-color="" >
          <q-breadcrumbs-el label="Leibniz-Zentrum für Archäologie (LEIZA) 2025" />
          <q-breadcrumbs-el label="Lasse Mempel-Länger & Kristina Fischer & Nathaly Witt" />
        </q-breadcrumbs>
        <q-breadcrumbs separator="" separator-color="secondary" active-color="">
          <a href="https://www.leiza.de/impressum" target="_blank" style="">
            <q-breadcrumbs-el label="Impressum"/>
          </a>
          <ContactComponent></ContactComponent>
          <a href="https://www.leiza.de/datenschutz" target="_blank" style="">
            <q-breadcrumbs-el label="Datenschutz" />
          </a>
        </q-breadcrumbs>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<script setup>
import { ref, provide, toRaw, nextTick } from 'vue';
import { useQuasar } from 'quasar';
import TermComponent from 'src/components/termComponent.vue';
import ContactComponent from 'src/components/contactComponent.vue';
import docuData from 'src/data/docu.json';
import exampleData from 'src/data/example.json';

const $q = useQuasar();
const dataDefinition = ref(docuData);
const terms = ref([]);
const exportTerms = ref([]);
const displayOutput = ref('');
const outputFormat = ref('json');
const validationError = ref(null);
const expandNotationsOnStartup = ref(["F52262", "BAA258"]);
const excludeNotations = ref(["F52262", "BAA258"]);

const pageStyle = (offset) => {
  return { paddingBottom: `${offset + 16}px` };
};

function jsonToSimplifiedXml(jsonData) {
    function escapeXml(text) {
        if (text === null || typeof text === 'undefined') return '';
        return String(text)
            .replace(/&/g, '&amp;')
            .replace(/</g, '<')
            .replace(/>/g, '>')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function processEntries(entries, level = 0) {
        let xml = '';
        const indent = '  '.repeat(level);

        for (const entry of entries) {
            const hasChildren = entry.Untereinträge && entry.Untereinträge.length > 0;
            const hasValue = entry.value !== null && entry.value !== undefined && entry.value !== '';
            const uncertainAttr = entry.Unsicher === 'Ja' ? ' Unsicher="true"' : '';

            // Open <Dokumentationseintrag>
            xml += `${indent}<Dokumentationseintrag${uncertainAttr}>\n`;
            xml += `${indent}  <Name>${escapeXml(entry.Name)}</Name>\n`;
            xml += `${indent}  <Identifikator>${escapeXml(entry.Identifikator)}</Identifikator>\n`;

            // Add <Value> first if present
            if (hasValue) {
                xml += `${indent}  <Value>${escapeXml(entry.value)}</Value>\n`;
            }

            // Add <Untereinträge> container if children exist
            if (hasChildren) {
                xml += `${indent}  <Untereinträge>\n`;
                xml += processEntries(entry.Untereinträge, level + 2);
                xml += `${indent}  </Untereinträge>\n`;
            }

            // Close </Dokumentationseintrag>
            xml += `${indent}</Dokumentationseintrag>\n`;
        }

        return xml;
    }

    // Build final XML
    let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
    xml += '<ConservationData>\n';
    xml += processEntries(jsonData, 1);
    xml += '</ConservationData>\n';

    return xml.trimEnd();
}

function createInitialTerms(termsList, path = [], expandNotations = expandNotationsOnStartup.value) {
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

terms.value = createInitialTerms(dataDefinition.value);

const onReset = () => {
  terms.value = createInitialTerms(dataDefinition.value);
  exportTerms.value = [];
  displayOutput.value = '';
  validationError.value = null;
  $q.notify({
    message: 'Formular zurückgesetzt',
    color: 'info',
    icon: 'mdi-reload',
  });
};

const fillAllFields = (exclude = []) => {
  try {
    const fillTermsRecursively = (currentTerms, exclude = []) => {
      currentTerms.forEach(term => {
        if (!(exclude.includes(term.notation))) {
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

    fillTermsRecursively(terms.value, exclude);

    $q.notify({
      type: 'positive',
      message: exclude.length === 0
        ? "Alle Felder mit Beispieldaten ausgefüllt"
        : "Kuratorische Daten erstellt. Restaurierungsspezifische Felder ausfüllen.",
      icon: 'mdi-auto-fix',
    });

  } catch (error) {
    console.error('Error filling fields:', error);
    $q.notify({
      type: 'negative',
      message: 'Error loading example data. Please check if example.json exists.',
      icon: 'mdi-alert-circle-outline',
    });
  }
};

fillAllFields(excludeNotations.value);

const updateOutput = () => {
  if (exportTerms.value.length > 0) {
    if (outputFormat.value === 'json') {
      displayOutput.value = JSON.stringify(exportTerms.value, null, 2);
    } else {
      // Use the new simplified XML function
      displayOutput.value = jsonToSimplifiedXml(exportTerms.value);
    }
  }
};

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(displayOutput.value);
    $q.notify({
      type: 'positive',
      message: `${outputFormat.value.toUpperCase()}-Inhalt in Zwischenablage kopiert`,
      icon: 'mdi-content-copy',
    });
  } catch {
    // Fallback for older Browsers
    const textArea = document.createElement('textarea');
    textArea.value = displayOutput.value;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
      document.execCommand('copy');
      $q.notify({
        type: 'positive',
        message: `${outputFormat.value.toUpperCase()}-Inhalt in Zwischenablage kopiert`,
        icon: 'mdi-content-copy',
      });
    } catch {
      $q.notify({
        type: 'negative',
        message: 'Fehler beim Kopieren in die Zwischenablage',
        icon: 'mdi-alert-circle-outline',
      });
    } finally {
      document.body.removeChild(textArea);
    }
  }
}

const downloadOutput = () => {
  const content = displayOutput.value;
  const filename = outputFormat.value === 'json' ? 'export.json' : 'export.xml';
  const mimeType = outputFormat.value === 'json' ? 'application/json' : 'text/xml';
  
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
  
  $q.notify({
    type: 'positive',
    message: `${filename} erfolgreich heruntergeladen`,
    icon: 'mdi-download',
  });
};

const onSubmit = async () => {
  exportTerms.value = [];
  displayOutput.value = '';
  validationError.value = null;
  
  const errorInfo = validateForm(terms.value);

  if (errorInfo) {
    validationError.value = errorInfo.error;
    $q.notify({
      type: 'negative',
      message: errorInfo.error,
      icon: 'mdi-alert-circle-outline',
    });
    
    expandToPath(errorInfo.path);
    await nextTick();
    
    const errorElementId = `term-${errorInfo.path.join('-')}`;
    const element = document.getElementById(errorElementId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  } else {
    exportTerms.value = transformFormData(terms.value);
    updateOutput(); // Update output based on the selected format
    
    $q.notify({
      type: 'positive',
      message: 'Datensatz erstellt und validiert!',
      icon: 'mdi-check-circle-outline',
    });
    
    await nextTick();
    const resultsElement = document.querySelector('.q-mt-xl');
    if (resultsElement) {
      resultsElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
};

function validateForm(currentTerms) {
  for (const term of currentTerms) {
    if (term.Verpflichtungsgrad === 'Pflicht' && term.Feldwert && !term.value) {
      return { 
        error: `Fehler: '${term.prefLabel}' ist ein verpflichtendes Feld.`,
        path: term.path 
      };
    }
    if (term.narrower) {
      const nestedError = validateForm(term.narrower);
      if (nestedError) {
        return nestedError;
      }
    }
  }
  return null;
}

function transformFormData(currentTerms) {
  const transformedTerms = [];
  for (const term of currentTerms) {
    // Only include terms that have a value OR have children that will be transformed
    const hasValue = term.value || (term.Feldwert && term.value === ''); // Keep even if value is empty string
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

function toggleAll(expand) {
  const recursiveToggle = (nodes) => {
    nodes.forEach(node => {
      if (node.narrower && node.narrower.length > 0) {
        node.isExpanded = expand;
        recursiveToggle(node.narrower);
      }
    });
  };
  recursiveToggle(terms.value);
}

function expandToPath(path) {
  let currentLevel = terms.value;
  for (let i = 0; i < path.length - 1; i++) {
    const index = path[i];
    if (currentLevel[index]) {
      currentLevel[index].isExpanded = true;
      currentLevel = currentLevel[index].narrower;
    }
  }
}

provide('formManager', {
  terms,
  addFieldAtPath(path) {
    let parentArray = terms.value;
    for (let i = 0; i < path.length - 1; i++) {
      parentArray = parentArray[path[i]].narrower;
    }
    const index = path[path.length - 1];
    const node = parentArray[index];

    if (node['Wiederholbar'] === 'Ja') {
      const clone = structuredClone(toRaw(node));
      resetValues(clone);
      parentArray.splice(index + 1, 0, clone);
      recalculatePaths(terms.value);
    }
  },
  removeFieldAtPath(path) {
    let parentArray = terms.value;
    for (let i = 0; i < path.length - 1; i++) {
      parentArray = parentArray[path[i]].narrower;
    }
    const index = path[path.length - 1];
    const notation = parentArray[index].notation;
    const sameNotationCount = parentArray.filter(n => n.notation === notation).length;
    if (sameNotationCount > 1) {
      parentArray.splice(index, 1);
      recalculatePaths(terms.value);
    }
  },
  updateValueAtPath(path, value, field = 'value') {
    let target = terms.value;
    path.forEach((index, i) => {
      target = (i < path.length - 1) ? target[index].narrower : target[index];
    });
    target[field] = value;
  },
  toggleExpansionAtPath(path) {
    let target = terms.value;
    path.forEach((index, i) => {
      target = (i < path.length - 1) ? target[index].narrower : target[index];
    });
    target.isExpanded = !target.isExpanded;
  }
});

function resetValues(node) {
  if ('value' in node) node.value = '';
  if ('UnsicherValue' in node) node.UnsicherValue = '';
  if ('isExpanded' in node) node.isExpanded = false;
  if (Array.isArray(node.narrower)) {
    node.narrower.forEach(child => resetValues(child));
  }
}

function recalculatePaths(nodes, path = []) {
  nodes.forEach((node, index) => {
    const currentPath = [...path, index];
    node.path = currentPath;
    if (Array.isArray(node.narrower)) {
      recalculatePaths(node.narrower, currentPath);
    }
  });
}
</script>

<style scoped>
.form-page {
  max-width: 900px;
  margin: 0 auto;
  background-color: #ffffff;
}

.footer-container {
  border-top: 1px solid #e0e0e0;
}

pre {
  background-color: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 16px;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>