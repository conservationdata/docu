import json

jsonString = """
{
  "label": "Ansprechpartner*in",
  "uri": "https://www.conservation-science.org/ontology/contact-person",
  "selectable": false,
  "children": [
    {
      "label": "Max Mustermann",
      "uri": "https://www.example.org/contact-person/max-mustermann"
    },
    {
      "label": "Unbekannte*r Ansprechpartner*in (Unknown Contact Person)",
      "uri": "https://www.conservation-science.org/ontology/contact-person/unknown"
    }
  ]
}
    """

# read JSON from jsonString
JSON = json.loads(jsonString)
print(JSON)