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
          <div class="row items-center q-mb-md">
            <p class="text-h6 q-mb-none">{{ outputFormat === 'json' ? 'JSON Proto Datenformat' : 'XML Pseudo LIDO' }}</p>
            <q-space />
            <q-btn-toggle
              v-model="outputFormat"
              toggle-color="primary"
              :options="[
                {label: 'JSON', value: 'json'},
                {label: 'XML', value: 'xml'}
              ]"
              @update:model-value="updateOutput"
            />
          </div>
          <pre>{{ displayOutput }}</pre>
          
          <!-- Action Buttons -->
          <div class="q-mt-md">
            <q-btn
              :label="`Download ${outputFormat.toUpperCase()}`"
              color="primary"
              icon="mdi-download"
              @click="downloadOutput"
              outline
              class="q-mr-sm"
            />
            <q-btn
              label="In Zwischenablage kopieren"
              color="secondary"
              icon="mdi-content-copy"
              @click="copyToClipboard"
              outline
            />
          </div>
        </div>
      </q-page>
    </q-page-container>

    <q-footer bordered class="bg-white text-primary q-pa-sm">
      <q-toolbar class="row justify-center">
        <q-btn-group
        push
        >
          <q-btn
            label="Abschicken"
            type="submit"
            color="primary"
            icon="mdi-check-circle"
            @click="onSubmit"
            flat
          />
          <q-separator vertical class="q-mx-md" />
          <q-btn
            label="Zurücksetzen"
            type="reset"
            color="grey"
            class="q-ml-sm"
            icon="mdi-reload"
            @click="onReset"
            flat
          />
          <q-separator vertical class="q-mx-md" />
          <q-btn
            label="Felder ausfüllen"
            color="accent"
            icon="mdi-auto-fix"
            @click="() => fillAllFields(excludeNotations.value)"
            flat
          />
          <q-separator vertical class="q-mx-md" />
          <q-btn
            label="Ausklappen"
            color="secondary"
            icon="mdi-unfold-more-vertical"
            @click="toggleAll(true)"
            flat
          />
          <q-separator vertical class="q-mx-md" />
          <q-btn
            label="Zusammenklappen"
            color="secondary"
            class="q-ml-sm"
            icon="mdi-unfold-less-vertical"
            @click="toggleAll(false)"
            flat
          />
        </q-btn-group>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<script setup>
import { ref, provide, toRaw, nextTick } from 'vue';
import { useQuasar } from 'quasar';
import TermComponent from 'src/components/termComponent.vue';
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

// XML Konvertierungsfunktionen
function jsonToLidoXml(jsonData, options = {}) {
    const {
        rootElement = 'lido:descriptiveMetadata',
        namespace = 'lido',
        namespaceUri = 'http://www.lido-schema.org',
        termElement = 'lido:term',
        conceptElement = 'lido:conceptID'
    } = options;

    function escapeXml(text) {
        if (!text) return '';
        return String(text)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function processTerms(terms, level = 0) {
        let xml = '';
        const indent = '  '.repeat(level + 2);
        
        for (const term of terms) {
            xml += `${indent}<${termElement}>\n`;
            
            if (term.Identifikator) {
                xml += `${indent}  <${conceptElement} lido:type="uri">${escapeXml(term.Identifikator)}</${conceptElement}>\n`;
            }
            
            if (term.Name) {
                xml += `${indent}  <lido:term xml:lang="de">${escapeXml(term.Name)}</lido:term>\n`;
            }
            
            if (term.value) {
                xml += `${indent}  <lido:termValue>${escapeXml(term.value)}</lido:termValue>\n`;
            }
            
            if (term.Unsicher === 'Ja') {
                xml += `${indent}  <lido:qualifierTerm lido:type="uncertainty">uncertain</lido:qualifierTerm>\n`;
            }
            
            if (term.Untereinträge && term.Untereinträge.length > 0) {
                xml += `${indent}  <lido:subTerms>\n`;
                xml += processTerms(term.Untereinträge, level + 2);
                xml += `${indent}  </lido:subTerms>\n`;
            }
            
            xml += `${indent}</${termElement}>\n`;
        }
        
        return xml;
    }

    let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
    xml += `<${rootElement} xmlns:${namespace}="${namespaceUri}">\n`;
    xml += `  <lido:objectIdentificationWrap>\n`;
    xml += `    <lido:titleWrap>\n`;
    xml += `      <lido:titleSet>\n`;
    
    xml += processTerms(jsonData);
    
    xml += `      </lido:titleSet>\n`;
    xml += `    </lido:titleWrap>\n`;
    xml += `  </lido:objectIdentificationWrap>\n`;
    xml += `</${rootElement}>`;

    return xml;
}

function convertToLidoXml(originalData, options = {}) {
    return jsonToLidoXml(originalData, options);
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
      displayOutput.value = convertToLidoXml(exportTerms.value);
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
    // Fallback für ältere Browser
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
    updateOutput(); // Aktualisiere die Ausgabe basierend auf dem gewählten Format
    
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
    if (term.value || (term.narrower && term.narrower.length > 0)) {
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

      if (term.narrower) {
        const narrowerExport = transformFormData(term.narrower);
        if (narrowerExport.length > 0) {
          exportTerm.Untereinträge = narrowerExport;
        }
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

pre {
  background-color: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 16px;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>