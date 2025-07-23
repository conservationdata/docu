import json

jsonString2 = """
{
    "label": "Schadensphänomen (Damage Phenomenon)",
    "uri": "https://www.conservation-science.org/ontology/damage-phenomena/DAC996",
    "selectable": false,
    "children": [
        {
            "label": "Formänderung (Change in Form)",
            "uri": "https://www.conservation-science.org/ontology/damage-phenomena/B224CD",
            "children": [
                {
                    "label": "aufgeraut (Schadensphänomen)",
                    "uri": "https://www.conservation-science.org/ontology/damage-phenomena/A21DB2"
                },
                {
                    "label": "deformiert",
                    "uri": "https://www.conservation-science.org/ontology/damage-phenomena/A8D9GF",
                    "children": [
                        {
                            "label": "geknickt",
                            "uri": "https://www.conservation-science.org/ontology/damage-phenomena/ABB9FA"
                        },
                        {
                            "label": "gewellt",
                            "uri": "https://www.conservation-science.org/ontology/damage-phenomena/B89818"
                        },
                        {
                            "label": "verbogen",
                            "uri": "https://www.conservation-science.org/ontology/damage-phenomena/C535G6"
                        },
                        {
                            "label": "verdreht",
                            "uri": "https://www.conservation-science.org/ontology/damage-phenomena/CF4199"
                        },
                        {
                            "label": "verworfen",
                            "uri": "https://www.conservation-science.org/ontology/damage-phenomena/FC4DGB"
                        },
                        {
                            "label": "eingedrückt (Schadensphänomen)",
                            "uri": "https://www.conservation-science.org/ontology/damage-phenomena/GAC37B"
                        }
                    ]
                }
            ]
        },
        {
            "label": "Kohäsionsverlust",
            "uri": "https://www.conservation-science.org/ontology/damage-phenomena/KOHA123",
            "selectable": false,
            "children": [
                {
                    "label": "fragmentiert",
                    "uri": "https://www.conservation-science.org/ontology/damage-phenomena/FRAG456"
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