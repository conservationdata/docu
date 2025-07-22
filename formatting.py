import json

jsonString2 = """
{
  "label": "Eingriff",
  "children": [
    {
      "label": "Reinigung",
      "children": [
        {
          "label": "Trockenreinigung"
        },
        {
          "label": "Feuchtreinigung"
        },
        {
          "label": "Laserreinigung"
        }
      ]
    },
    {
      "label": "Festigung",
      "children": [
        {
          "label": "temporärer Stabilisierung"
        },
        {
          "label": "Tränkung"
        }
      ]
    },
    {
      "label": "Klebung",
      "children": [
        {
          "label": "Infiltrationsklebung"
        },
        {
          "label": "Aufbaumethode"
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