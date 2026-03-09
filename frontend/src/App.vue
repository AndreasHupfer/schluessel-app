<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-900 text-white flex flex-col">
      <div class="p-6 border-b border-gray-700">
        <h1 class="text-xl font-bold">Schluessel-Manager</h1>
      </div>
      <nav class="flex-1 p-4 space-y-1">
        <RouterLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-300 hover:bg-gray-700 hover:text-white transition-colors"
          active-class="bg-gray-700 text-white"
        >
          <span class="text-lg">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>
    </aside>

    <!-- Main content -->
    <main class="flex-1 overflow-auto">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
const navItems = [
  { path: '/liegenschaften', label: 'Liegenschaften', icon: '🏢' },
  { path: '/schluessel', label: 'Schluessel', icon: '🔑' },
  { path: '/kontakte', label: 'Kontakte', icon: '👥' },
  { path: '/ausleihen', label: 'Ausleihen', icon: '📋' },
]
</script>
