<template>
  <q-layout view="lHh Lpr lFf">
    <q-dialog v-model="showIntroDialog" persistent>
      <q-card style="min-width: 400px; max-width: 600px;">
        <q-card-section class="bg-primary text-white row items-center q-pb-none">
          <div class="text-h6 q-pa-sm">Willkommen auf der Mockup-App für Konservierungsdaten</div>
          <q-space />
        </q-card-section>

        <q-card-section class="q-pa-md">
          <p>Dieses Tool dient zur beispielhaften Erstellung strukturierter Daten zur Dokumentation von Konservierungs- und Restaurierungsmaßnahmen.</p>
          <p>Grundlage hierfür ist der Entwurf für einen Konservierungs- und Restaurierungs Metadatensatz der Temporary Working Group <i>Community-Standards für kontrollierte Vokabulare und Austauschformate im Bereich der Erhaltung und Pflege des kulturellen Erbes</i> innerhalb des Konsortiums NFDI4Objects. </p>
          <p><strong> Funktionen:</strong></p>
          <ul>
            <li><strong>Datenfelder:</strong> Geben Sie Informationen in die bereitgestellten Felder ein.</li>
            <li><strong>Bestandsdaten:</strong> Kuratorische Daten sind bereits exemplarisch vorgeladen.</li>
            <li><strong>Validieren:</strong> Klicken Sie auf "Abschicken", um die Eingaben zu prüfen.</li>
            <li><strong>Hinweise:</strong> Fehlermeldungen weisen auf ausgelassene Pflichtfelder (markiert mit rotem *) hin .</li>
            <li><strong>Datengenerierung:</strong> Nach erfolgreicher Validierung werden strukturierte Daten erstellt.</li>
            <li><strong>Exportieren:</strong> Diese lassen sich im JSON oder XML-Format kopieren und herunterladen.</li>
            <li><strong>Keine Zeit?:</strong> Nutzen Sie den Knopf "Felder ausfüllen", um Beispieldaten zu laden.</li>
            <li><strong>Helfer:</strong> "Ausklappen/Zusammenklappen" für die Navigation, und "Zurücksetzen" zum Leeren des Formulars.</li>
          </ul>
          <p>Beginnen Sie, indem Sie die benötigten Felder "Zustandserfassung" und "Konservierungskonzept" ausfüllen. Anschließend auf "Abschicken" klicken.</p>
        </q-card-section>

        <q-card-actions align="right" class="q-pr-md q-pb-md">
          <q-btn
            label="Verstanden"
            color="primary"
            @click="
              showIntroDialog = false;
            "
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
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
            <p class="text-h6 q-mb-none">{{ outputFormat === 'json' ? 'JSON Proto Austauschformat' : 'XML Proto Austauschformat' }}</p>
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
        </div>
        <div v-if="exportTerms.length > 0" class="q-pb-xl"></div>
      </q-page>
    </q-page-container>
    <div v-if="exportTerms.length > 0" class="fixed-bottom bg-white" style="bottom: 65px; left: 0; right: 0; z-index: 1000; border-top: 1px solid #e0e0e0;">
      <div class="flex flex-center q-pa-sm">
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
<q-footer bordered class="bg-white text-primary">
  <q-toolbar class="column q-py-sm">
    <!-- Button group -->
    <div class="row justify-center q-mb-sm">
      <q-btn-group push>
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
          icon="mdi-unfold-less-vertical"
          @click="toggleAll(false)"
          flat
        />
      </q-btn-group>
    </div>
    
  <div class="row justify-center items-center q-pa-md">

    <q-btn
      v-if="!showEmails"
      label="Kontakt"
      @click="showEmails = true"
      color="primary"
      icon="email"
      unelevated
    />

    <div v-if="showEmails" class="row items-center">
      <a
        v-for="(email, index) in decodedEmails"
        :key="email"
        :href="'mailto:' + email"
        class="q-ml-sm text-primary"
        style="text-decoration: none;"
      >
        {{ email }}<span v-if="index < decodedEmails.length - 1">,</span>
      </a>
    </div>

  </div>
  </q-toolbar>
</q-footer>
  </q-layout>
</template>

<script setup>
import { ref, provide, toRaw, nextTick, onMounted, computed } from 'vue';
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
const showIntroDialog = ref(true);
const showEmails = ref(false);
const obfuscatedEmails = ref([
  "7l4a9s2s1e6x3m5e8m0p4e2l7l9a1e6n3g8e5r2x9l7e4i1z6a8x2d5e9",
  "7k4r9i2s1t6i3n5a8x0f4i2s7c9h1e6r3x8l5e2i9z7a4x1d6e8",
  "7n4a9t2h1a6l3y5x8w0i4t2t7x9l1e6i3z8a5x2d9e7"
])

const decodedEmails = computed(() => {
  return obfuscatedEmails.value.map(email => {
    let decoded = email.replace(/\d/g, '');
    let parts = decoded.split('x').filter(part => part.length > 0);
    if (parts.length >= 4) {
      const firstName = parts[0];
      const lastName = parts[1];
      const domain = parts[2];
      const tld = parts[3];
      return `${firstName}.${lastName}@${domain}.${tld}`;
    }
    return email;
  });
});

const pageStyle = (offset) => {
  return { paddingBottom: `${offset + 16}px` };
};

onMounted(() => {
  const hasSeenIntro = localStorage.getItem('hasSeenIntro');
  if (hasSeenIntro) {
    showIntroDialog.value = false;
  }
});

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

pre {
  background-color: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 16px;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>