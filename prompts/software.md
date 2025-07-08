# quasar app 
The app takes a JSON-File with the structure defined in datastructure.md to produce the following 

## requirements

### forms
- Generate forms for the terms in the file
- forms should have the prefLabel of the term as title
- mouseover over title should show the definition of the term
- mouseover over form should show Verwendungshinweis of the term
- Wiederholbar with value "Ja" means there can be more than one entry, so the form can be removed or an additional one added
- The hierarchy is represented in the forms. Parent elements without Feldwert values are just containers of their children elements. Parents with Feldwert are a form containing other children forms. Hierarchy can be several levels. 

### buttons
- a button to save the resulting data as JSON
- a button to reset all forms
- a button to fill all fields 

### data
- a term json with the terms and their properties (docu.json)
- a json (exemplary.json) with exemplary AI generated data imitating archeological convervation science (key = notation of term to be filled, value = data to be filled)
- a json with AI generated hierarchical normdata (normdata.json) for forms with URI possibility (key = notation of term to be filled, value = JSON with hierarchy of normdata)

### features
- data can't be saved while a term with Verpflichtungsgrad "Pflicht" has no value. An error names the term and jumps to the form
- filling all fields takes a json containing exemplary data and puts it in the form
- when starting the app the main hierarchy branches of notations [A13CD1, ADD53A, CCCC7G, F2244D, G814D2, K343FVC, F58F6D] are always prefilled using the json containing exemplary data
- terms allowing URI Feldwerte offer a tree where terms can be selected to fill the form, fueled by the normdata.json

### components
the form elements are developed as components following their specific data needs and hierarchy and allow the following
#### containers without values/with values
#### removable/addable forms
#### forms with different types, date picker, string, treeview for normdata etc.