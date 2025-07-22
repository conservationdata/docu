import json

jsonString2 = """
{
  "label": "Eingriff",
  "uri": "https://www.conservation-science.org/ontology/intervention/CD3353",
  "selectable": false,
  "children": [
    {
      "label": "Reinigung",
      "uri": "https://www.conservation-science.org/ontology/intervention/cleaning",
      "children": [
        {
          "label": "Trockenreinigung",
          "uri": "https://www.conservation-science.org/ontology/intervention/dry-cleaning"
        },
        {
          "label": "Feuchtreinigung",
          "uri": "https://www.conservation-science.org/ontology/intervention/wet-cleaning"
        },
        {
          "label": "Laserreinigung",
          "uri": "https://www.conservation-science.org/ontology/intervention/laser-cleaning"
        }
      ]
    },
    {
      "label": "Festigung",
      "uri": "https://www.conservation-science.org/ontology/intervention/consolidation",
      "children": [
        {
          "label": "temporärer Stabilisierung",
          "uri": "https://www.conservation-science.org/ontology/intervention/temporary-stabilization"
        },
        {
          "label": "Tränkung",
          "uri": "https://www.conservation-science.org/ontology/intervention/impregnation"
        }
      ]
    },
    {
      "label": "Klebung",
      "uri": "https://www.conservation-science.org/ontology/intervention/adhesion",
      "children": [
        {
          "label": "Infiltrationsklebung",
          "uri": "https://www.conservation-science.org/ontology/intervention/infiltration-bonding"
        },
        {
          "label": "Aufbaumethode",
          "uri": "https://www.conservation-science.org/ontology/intervention/build-up-method"
        }
      ]
    }
  ]
}
    """



# read JSON from jsonString
stringer = jsonString2
stringer = stringer.replace("'",'"')
stringer = stringer.replace("False","false")
stringer = stringer.replace("True","true")
#print(stringer)

JSON = json.loads(stringer)
print(json.dumps(JSON))