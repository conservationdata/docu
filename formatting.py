import json

jsonString2 = """
{'label': 'Werkzeug', 'uri': 'https://www.conservation-science.org/ontology/tool/F87124', 'selectable': False, 'children': [{'label': 'Skalpell (Scalpel)', 'uri': 'https://www.conservation-science.org/ontology/tool/scalpel'}, {'label': 'Pinsel (Brush)', 'uri': 'https://www.conservation-science.org/ontology/tool/brush'}, {'label': 'Luftpistole (Airbrush)', 'uri': 'https://www.conservation-science.org/ontology/tool/airbrush'}]}

    """



# read JSON from jsonString
stringer = jsonString2
stringer = stringer.replace("'",'"')
stringer = stringer.replace("False","false")
stringer = stringer.replace("True","true")
#print(stringer)

JSON = json.loads(stringer)
print(json.dumps(JSON))