import requests
import pandas as pd
import json

link = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRb0tjnjkyjzReZ_--dYJOD4rbl1_iV8EdVTFXATh9ie6u3bRAeEYYrMNKZF0AcM_PQJkQbmZyGFfYe/pub?gid=0&single=true&output=csv"
csv = text = requests.get(link).text.encode("ISO-8859-1").decode()
propertyMatchDict = {"identifier":"notation","description":"definition","parent":"broader", "note (source)": "source"}

with open("data.csv", "w", encoding="utf-8") as f:
    f.write(csv)

df = pd.read_csv("data.csv", encoding="utf-8")
df.rename(columns=propertyMatchDict, inplace=True) # rename columns according to propertyMatchDict

# delete column "source" from df
df = df.drop(columns=["source", "MMS", "Empfohlene Vokabulare"])
topDf = df[df["broader"] == "top"]
docuArray = []

def getChildren(notation):
    # Fixed: Use the parameter value, not the string literal
    childrenDf = df[df["broader"] == notation]
    childrenArray = []
    for index, row in childrenDf.iterrows():
        if row["prefLabel"] and isinstance(row["prefLabel"], str) and row["notation"] and isinstance(row["notation"], str):
            notation_child, prefLabel, altLabel, definition, broader, Verpflichtungsgrad, Feldwert, Wiederholbar, source, Vokabulare = row["notation"], row["prefLabel"], row["altLabel"], row["definition"], row["broader"], row["Verpflichtungsgrad"], row["Feldwert"], row["Wiederholbar"], row["note (source)"], row["Empfohlene Vokabulare"]
            # Fixed: Use notation_child to avoid variable name conflict
            narrower = getChildren(notation_child)
            propertyTuples = [("notation", notation_child), ("prefLabel", prefLabel), ("altLabel", altLabel), ("definition", definition), ("broader", broader), ("Verpflichtungsgrad",Verpflichtungsgrad), ("Feldwert",Feldwert), ("Wiederholbar",Wiederholbar), ("narrower", narrower), ("source", source), ("Vokabulare",Vokabulare)]
            childJSON = {}
            for key, value in propertyTuples:
                if value and isinstance(value, str):
                    childJSON[key] = value
                elif key == "narrower" and value:  # Handle narrower array
                    childJSON[key] = value
            childrenArray.append(childJSON)
    return childrenArray

for index, row in topDf.iterrows():
    if row["prefLabel"] and isinstance(row["prefLabel"], str) and row["notation"] and isinstance(row["notation"], str):
        notation, prefLabel, altLabel, definition, broader, Verpflichtungsgrad, Feldwert, Wiederholbar, source, Vokabulare = row["notation"], row["prefLabel"], row["altLabel"], row["definition"], row["broader"], row["Verpflichtungsgrad"], row["Feldwert"], row["Wiederholbar"], row["note (source)"], row["Empfohlene Vokabulare"]
        narrower = getChildren(notation)
        propertyTuples = [("notation", notation), ("prefLabel", prefLabel), ("altLabel", altLabel), ("definition", definition), ("broader", broader), ("Verpflichtungsgrad",Verpflichtungsgrad), ("Feldwert",Feldwert), ("Wiederholbar",Wiederholbar), ("narrower", narrower), ("source", source), ("Vokabulare",Vokabulare)]
        topJSON = {}
        for key, value in propertyTuples:
            if value and isinstance(value, str):
                topJSON[key] = value
            elif key == "narrower" and value:  # Handle narrower array
                topJSON[key] = value
        docuArray.append(topJSON)

print(docuArray)
with open("docu.json", "w", encoding="utf-8") as f:
    json.dump(docuArray, f, ensure_ascii=False, indent=2)