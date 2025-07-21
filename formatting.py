import json

jsonString2 = """
{
  "label": "Werkzeug (Tool)",
  "uri": "https://www.conservation-science.org/ontology/tool/F87124",
  "selectable": false,
  "children": [
    {
      "label": "Manuelle Reinigungswerkzeuge (Manual Cleaning Tools)",
      "uri": "https://www.conservation-science.org/ontology/tool/manual-cleaning-tools",
      "children": [
        {
          "label": "Skalpell (Scalpel)",
          "uri": "https://www.conservation-science.org/ontology/tool/scalpel"
        },
        {
          "label": "Pinsel (Brush)",
          "uri": "https://www.conservation-science.org/ontology/tool/brush"
        },
        {
          "label": "Wattestäbchen (Cotton Swab)",
          "uri": "https://www.conservation-science.org/ontology/tool/cotton-swab"
        },
        {
          "label": "Schwamm (Sponge)",
          "uri": "https://www.conservation-science.org/ontology/tool/sponge"
        },
        {
          "label": "Radiergummi (Eraser)",
          "uri": "https://www.conservation-science.org/ontology/tool/eraser"
        }
      ]
    },
    {
      "label": "Applikationswerkzeuge (Application Tools)",
      "uri": "https://www.conservation-science.org/ontology/tool/application-tools",
      "children": [
        {
          "label": "Pinsel (Brush - for application)",
          "uri": "https://www.conservation-science.org/ontology/tool/brush-application"
        },
        {
          "label": "Spritze (Syringe)",
          "uri": "https://www.conservation-science.org/ontology/tool/syringe"
        },
        {
          "label": "Pipette (Pipette)",
          "uri": "https://www.conservation-science.org/ontology/tool/pipette"
        },
        {
          "label": "Spachtel (Spatula)",
          "uri": "https://www.conservation-science.org/ontology/tool/spatula"
        },
        {
          "label": "Luftpistole (Airbrush)",
          "uri": "https://www.conservation-science.org/ontology/tool/airbrush"
        },
        {
          "label": "Rolle (Roller)",
          "uri": "https://www.conservation-science.org/ontology/tool/roller"
        }
      ]
    },
    {
      "label": "Formgebende Werkzeuge (Shaping Tools)",
      "uri": "https://www.conservation-science.org/ontology/tool/shaping-tools",
      "children": [
        {
          "label": "Modellierwerkzeuge (Modeling Tools)",
          "uri": "https://www.conservation-science.org/ontology/tool/modeling-tools"
        },
        {
          "label": "Schleifwerkzeuge (Sanding Tools)",
          "uri": "https://www.conservation-science.org/ontology/tool/sanding-tools"
        }
      ]
    },
    {
      "label": "Messwerkzeuge (Measuring Tools)",
      "uri": "https://www.conservation-science.org/ontology/tool/measuring-tools",
      "children": [
        {
          "label": "Messschieber (Caliper)",
          "uri": "https://www.conservation-science.org/ontology/tool/caliper"
        },
        {
          "label": "Mikrometer (Micrometer)",
          "uri": "https://www.conservation-science.org/ontology/tool/micrometer"
        },
        {
          "label": "Waage (Scale)",
          "uri": "https://www.conservation-science.org/ontology/tool/scale"
        }
      ]
    },
    {
      "label": "Beleuchtung und Optik (Lighting and Optics)",
      "uri": "https://www.conservation-science.org/ontology/tool/lighting-optics",
      "children": [
        {
          "label": "Lupe (Magnifying Glass)",
          "uri": "https://www.conservation-science.org/ontology/tool/magnifying-glass"
        },
        {
          "label": "Stirnlupe (Headband Magnifier)",
          "uri": "https://www.conservation-science.org/ontology/tool/headband-magnifier"
        },
        {
          "label": "Arbeitsleuchte (Work Light)",
          "uri": "https://www.conservation-science.org/ontology/tool/work-light"
        }
      ]
    },
    {
      "label": "Spezialwerkzeuge (Specialized Tools)",
      "uri": "https://www.conservation-science.org/ontology/tool/specialized-tools",
      "children": [
        {
          "label": "Heißluftföhn (Heat Gun)",
          "uri": "https://www.conservation-science.org/ontology/tool/heat-gun"
        },
        {
          "label": "Ultraschallreiniger (Ultrasonic Cleaner)",
          "uri": "https://www.conservation-science.org/ontology/tool/ultrasonic-cleaner"
        },
        {
          "label": "Niederdruck-Saugplatte (Low Pressure Suction Table)",
          "uri": "https://www.conservation-science.org/ontology/tool/low-pressure-suction-table"
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