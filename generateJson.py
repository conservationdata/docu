import requests
import pandas as pd
import json

def sortNotation(df):
    # generate an array of uuids from the notation column
    uuids = df['notation'].tolist()
    # delete all empty elements
    uuids = [x.strip() for x in uuids if x != "" and not isinstance(x, float)]
    # sort the uuids alphanumerically
    uuids.sort() 
    # iterate over every row and build a notation change dictionary
    i = 0
    changeDict = {}
    for index, row in df.iterrows():
        if row["prefLabel"] and isinstance(row["prefLabel"], str) and row["notation"] and isinstance(row["notation"], str):
            oldNotation = row['notation'].strip()
            newNotation = uuids[i]
            i += 1
            changeDict[oldNotation] = newNotation
    # replace all notations in the df with the new notation
    df.replace(changeDict, inplace=True)
    print("exporting sorted csv...")
    df.to_csv('sortedData.csv', index=False, encoding="utf-8")
    return df

link = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRb0tjnjkyjzReZ_--dYJOD4rbl1_iV8EdVTFXATh9ie6u3bRAeEYYrMNKZF0AcM_PQJkQbmZyGFfYe/pub?gid=0&single=true&output=csv"
csv = text = requests.get(link).text.encode("ISO-8859-1").decode()
propertyMatchDict = {"identifier":"notation","description":"definition","parent":"broader", "note (source)": "source"}

with open("data.csv", "w", encoding="utf-8") as f:
    f.write(csv)

df = pd.read_csv("data.csv", encoding="utf-8")
df.rename(columns=propertyMatchDict, inplace=True) # rename columns according to propertyMatchDict

# delete column "source" from df
df = df.drop(columns=["source", "MMS", "Empfohlene Vokabulare"])
df = sortNotation(df)

topDf = df[df["broader"] == "top"]
docuArray = []

def getChildren(notation):
    # Fixed: Use the parameter value, not the string literal
    childrenDf = df[df["broader"] == notation]
    childrenArray = []
    for index, row in childrenDf.iterrows():
        if row["prefLabel"] and isinstance(row["prefLabel"], str) and row["notation"] and isinstance(row["notation"], str):
            notation_child, prefLabel, altLabel, definition, broader, Verpflichtungsgrad, Feldwert, Wiederholbar, Verwendungshinweis = row["notation"], row["prefLabel"], row["altLabel"], row["definition"], row["broader"], row["Verpflichtungsgrad"], row["Feldwert"], row["Wiederholbar"], row["Verwendungshinweis"]
            # Fixed: Use notation_child to avoid variable name conflict
            narrower = getChildren(notation_child)
            propertyTuples = [("notation", notation_child), ("prefLabel", prefLabel), ("altLabel", altLabel), ("definition", definition), ("Verpflichtungsgrad",Verpflichtungsgrad), ("Feldwert",Feldwert), ("Wiederholbar",Wiederholbar), ("narrower", narrower), ("Verwendungshinweis", Verwendungshinweis)]
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
        notation, prefLabel, altLabel, definition, broader, Verpflichtungsgrad, Feldwert, Wiederholbar, Verwendungshinweis = row["notation"], row["prefLabel"], row["altLabel"], row["definition"], row["broader"], row["Verpflichtungsgrad"], row["Feldwert"], row["Wiederholbar"], row["Verwendungshinweis"]
        narrower = getChildren(notation)
        propertyTuples = [("notation", notation), ("prefLabel", prefLabel), ("altLabel", altLabel), ("definition", definition), ("Verpflichtungsgrad",Verpflichtungsgrad), ("Feldwert",Feldwert), ("Wiederholbar",Wiederholbar), ("narrower", narrower), ("Verwendungshinweis", Verwendungshinweis)]
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