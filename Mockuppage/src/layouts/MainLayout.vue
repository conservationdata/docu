<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar class="q-gutter-md">
        <!-- Left Section -->
        <div class="row items-center no-wrap">
          <q-icon name="settings" size="sm" class="q-mr-sm" />
          <span class="text-subtitle1">tools.LEIZA</span>
        </div>

        <!-- Center Section (Title + Subtitle) -->
        <q-toolbar-title class="text-center">
          <div class="column items-center">
            <div class="text-h5 text-bold header-title">Conservation Documentation</div>
            <div class="text-subtitle1 header-subtitle">Metadata Mockup (Beta)</div>
          </div>
        </q-toolbar-title>

        <!-- Right Section -->
        <div class="row items-center no-wrap">
          <span class="text-subtitle2">LEIZA Department of Scientific IT</span>
        </div>

      </q-toolbar>
    </q-header>

    <q-page-container class="bg-grey-2">
      <router-view />
    </q-page-container>
  </q-layout>
</template>


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