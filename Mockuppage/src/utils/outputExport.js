// src/utils/outputExport.js

export function jsonToSimplifiedXml(jsonData) {
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

      xml += `${indent}<Dokumentationseintrag${uncertainAttr}>\n`;
      xml += `${indent}  <Name>${escapeXml(entry.Name)}</Name>\n`;
      xml += `${indent}  <Identifikator>${escapeXml(entry.Identifikator)}</Identifikator>\n`;

      if (hasValue) {
        xml += `${indent}  <Value>${escapeXml(entry.value)}</Value>\n`;
      }

      if (hasChildren) {
        xml += `${indent}  <Untereinträge>\n`;
        xml += processEntries(entry.Untereinträge, level + 2);
        xml += `${indent}  </Untereinträge>\n`;
      }

      xml += `${indent}</Dokumentationseintrag>\n`;
    }
    return xml;
  }

  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
  xml += '<ConservationData>\n';
  xml += processEntries(jsonData, 1);
  xml += '</ConservationData>';
  return xml.trimEnd();
}

export function copyToClipboard(displayOutput, outputFormat, $q) {
  return async () => {
    try {
      await navigator.clipboard.writeText(displayOutput.value);
      $q.notify({
        type: 'positive',
        message: `${outputFormat.value.toUpperCase()}-Inhalt in Zwischenablage kopiert`,
        icon: 'mdi-content-copy',
      });
    } catch (err) {
      console.log(err);
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
  };
}

export function downloadOutput(displayOutput, outputFormat, $q) {
  return () => {
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
}