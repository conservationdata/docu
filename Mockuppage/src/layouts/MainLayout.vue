<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <!-- 
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />
        -->
        <q-toolbar-title>
          <div class="text-center text-bold text-h4 header-title">Conservation Documentation</div>
          <div class="text-center text-bold text-subtitle4 header-subtitle">Metadata Mockup</div>
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <!-- 
    <q-drawer v-model="leftDrawerOpen" side="left" bordered>
      </q-drawer>
    -->

    <q-page-container class="bg-grey-2">
      <router-view />
    </q-page-container>

    <q-footer elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title>
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>

  </q-layout>
</template>

<script>
import { ref } from 'vue'

export default {
  setup () {
    const leftDrawerOpen = ref(true)

    return {
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
}
</script>

<style scoped>
.header-title {
  font-size: 2.0rem; /* Larger font size for the main title */
  letter-spacing: 0.05em; /* Slightly more spaced letters */
}

.header-subtitle {
  font-size: 1rem; /* Appropriate size for a subtitle */
  opacity: 0.8; /* Slightly less prominent */
}
</style>