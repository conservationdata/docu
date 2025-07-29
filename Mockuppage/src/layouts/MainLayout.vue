<template>
  <DialogueComponent/>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar class="q-gutter-md">
        <div class="row items-center no-wrap">
          <!-- 
          <q-icon name="settings" size="sm" class="q-mr-sm" />
          <span class="text-subtitle1">tools.LEIZA</span>
          -->
           <img src="icons/02_Blau_Claim_kurz.svg" width="100" height="75"/>
        </div>
        <q-toolbar-title class="text-center">
          <div class="column items-center">
            <div class="text-h5 text-bold header-title text-secondary">Conservation Documentation</div>
            <div class="text-subtitle1 header-subtitle text-secondary">Metadata Mockup (Beta)</div>
          </div>
        </q-toolbar-title>
        <div class="row items-center no-wrap">
          <span class="text-subtitle2 text-secondary">LEIZA Department of Scientific IT</span>
        </div>
      </q-toolbar>
    </q-header>
    <q-page-container class="bg-grey-2">
      <router-view />
    </q-page-container>
    <q-footer bordered class="bg-primary text-secondary footer-container">
      <q-toolbar class="column q-py-md">
        <q-breadcrumbs  separator="|" separator-color="secondary" active-color="" >
          <q-breadcrumbs-el label="Leibniz-Zentrum für Archäologie (LEIZA) 2025" />
          <q-breadcrumbs-el label="Lasse Mempel-Länger & Kristina Fischer & Nathaly Witt" />
        </q-breadcrumbs>
        <q-breadcrumbs separator="" separator-color="secondary" active-color="">
          <a href="https://www.leiza.de/impressum" target="_blank" style="">
            <q-breadcrumbs-el label="Impressum"/>
          </a>
          <ContactComponent></ContactComponent>
          <a href="https://www.leiza.de/datenschutz" target="_blank" style="">
            <q-breadcrumbs-el label="Datenschutz" />
          </a>
        </q-breadcrumbs>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<script setup>
  import DialogueComponent from 'src/components/dialogueComponent.vue';
  import ContactComponent from 'src/components/contactComponent.vue';
</script>

<style scoped>
.header-title {
  font-size: 2rem;
  letter-spacing: 0.05em;
}

.header-subtitle {
  font-size: 1.1rem;
  opacity: 0.8;
}

</style>