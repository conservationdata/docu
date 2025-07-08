# Data Structure
The JSON data contains several terms following an extended SKOS Scheme with these
## Properties

### notation
The identifier of the term, generating its URI based on the namespace + notation

### prefLabel 
The prefered label of the term

### altLabel 
Alternative Labels of the term splitted with seperator "|"

### definition 
A definition of the term

### Verwendungshinweis
Further information on how to deal with this specific data

### source
Literary sources for the definition/usage of the term

### Verpflichtungsgrad
- "Pflicht" for mandatory fields
- "bedingte Pflicht", "empfohlen" and "optional" for optional fields or fields just mandatory if existing

### Feldwert
-"Text" for strings
- "URI" for ressources 
- "Text/URI" for both possibilities allowed
- Brackets after "Text" specify the string structure but should be ignored
- terms without a value in Feldwert are bare containers structuring the hierarchy and containing their children elements as forms

### Wiederholbar
Are several entries for this term allowed ("Ja") or not ("Nein")?

### Vokabulare
Recommented controlled Vocabularies for this entry

### narrower 
An array of all children elements, each with all the properties before