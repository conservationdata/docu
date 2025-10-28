I want to implement a new feature in my App.
Add a checkbox labeled "Nur Pflichtfelder", that is checked on Page load.

If the checkbox is checked, just render terms with term.Verpflichtungsgrad === "Pflicht" or "bedingte Pflicht"
This should mainly be done in the termComponent.vue as it is called by IndexPage.vue with:

      <TermComponent
        v-for="term in terms"
        :key="term.path.join('-')"
        :term="term"
      />

But there is more complexity: As we are using nested termComponents, recursively adding child terms, we need to make sure, that later child terms with term.Verpflichtungsgrad === "Pflicht" or "bedingte Pflicht" get rendered, even if their parent terms don't have term.Verpflichtungsgrad === "Pflicht" or "bedingte Pflicht".
Can this be done without needing additional functions like looking up the whole term path tree and checking which parents we need to render their children matching the requirements (In this we need to decide if the parent labels get rendered for the container. Surely their input component  should not be called)? Maybe we can use existing path finding functions.

Take a look at the relevant files, come up with plans to realize the new feature and present them to me, before acting, so i can decide which route to take.

The project is documented in docu/Mockuppage/project.md, look this up first.

If acting later, modifiy the document according to the relevant changes, so it is up to date.
