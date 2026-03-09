<template>
  <div class="p-8">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-800">Schluessel</h2>
      <button @click="showForm = true" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
        + Neuer Schluessel
      </button>
    </div>

    <!-- Form Modal -->
    <div v-if="showForm" class="fixed inset-0 bg-black/50 flex items-center justify-center z-10">
      <div class="bg-white rounded-xl p-6 w-full max-w-md shadow-xl">
        <h3 class="text-lg font-semibold mb-4">{{ editing ? 'Bearbeiten' : 'Neuer Schluessel' }}</h3>
        <form @submit.prevent="save" class="space-y-3">
          <select v-model="form.schliessung_id" required class="w-full border rounded-lg px-3 py-2">
            <option value="" disabled>Schliessung waehlen...</option>
            <option v-for="s in schliessungen" :key="s.id" :value="s.id">{{ s.bezeichnung }}</option>
          </select>
          <input v-model="form.schluessel_nr" placeholder="Schluessel-Nr." required class="w-full border rounded-lg px-3 py-2" />
          <input v-model.number="form.laufnummer" type="number" placeholder="Laufnummer" class="w-full border rounded-lg px-3 py-2" />
          <select v-model="form.typ" class="w-full border rounded-lg px-3 py-2">
            <option v-for="t in typen" :key="t" :value="t">{{ t }}</option>
          </select>
          <select v-model="form.status" class="w-full border rounded-lg px-3 py-2">
            <option v-for="s in stati" :key="s" :value="s">{{ s }}</option>
          </select>
          <div class="flex gap-2 justify-end pt-2">
            <button type="button" @click="cancel" class="px-4 py-2 border rounded-lg hover:bg-gray-50">Abbrechen</button>
            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Speichern</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-xl shadow overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nr.</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Schliessung</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Typ</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            <th class="px-6 py-3"></th>
          </tr>
        </thead>
        <tbody class="divide-y">
          <tr v-for="item in items" :key="item.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 font-medium">{{ item.schluessel_nr }}</td>
            <td class="px-6 py-4 text-gray-600">{{ schliessungName(item.schliessung_id) }}</td>
            <td class="px-6 py-4">
              <span class="px-2 py-1 bg-gray-100 rounded-full text-xs">{{ item.typ }}</span>
            </td>
            <td class="px-6 py-4">
              <span :class="statusClass(item.status)" class="px-2 py-1 rounded-full text-xs font-medium">{{ item.status }}</span>
            </td>
            <td class="px-6 py-4 text-right space-x-2">
              <button @click="edit(item)" class="text-blue-600 hover:underline text-sm">Bearbeiten</button>
              <button @click="remove(item.id)" class="text-red-600 hover:underline text-sm">Loeschen</button>
            </td>
          </tr>
          <tr v-if="!items.length">
            <td colspan="5" class="px-6 py-8 text-center text-gray-400">Keine Schluessel vorhanden</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { schluessel as api, schliessungen as schliessungenApi } from '../api'

const items = ref([])
const schliessungen = ref([])
const showForm = ref(false)
const editing = ref(null)
const typen = ['general', 'hauswart', 'lift', 'wohnung', 'sonstige']
const stati = ['verfuegbar', 'ausgeliehen', 'verloren']
const form = ref({ schliessung_id: '', schluessel_nr: '', laufnummer: null, typ: 'general', status: 'verfuegbar' })

async function load() {
  const [k, s] = await Promise.all([api.list(), schliessungenApi.list()])
  items.value = k.data
  schliessungen.value = s.data
}

function schliessungName(id) {
  return schliessungen.value.find(s => s.id === id)?.bezeichnung ?? id
}

function statusClass(s) {
  return s === 'verfuegbar' ? 'bg-green-100 text-green-700' : s === 'ausgeliehen' ? 'bg-yellow-100 text-yellow-700' : 'bg-red-100 text-red-700'
}

function cancel() {
  showForm.value = false
  editing.value = null
  form.value = { schliessung_id: '', schluessel_nr: '', laufnummer: null, typ: 'general', status: 'verfuegbar' }
}

function edit(item) {
  editing.value = item.id
  form.value = { ...item }
  showForm.value = true
}

async function save() {
  if (editing.value) {
    await api.update(editing.value, form.value)
  } else {
    await api.create(form.value)
  }
  cancel()
  load()
}

async function remove(id) {
  if (confirm('Wirklich loeschen?')) {
    await api.delete(id)
    load()
  }
}

onMounted(load)
</script>
