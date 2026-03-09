<template>
  <div class="p-8">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-800">Ausleihen</h2>
      <button @click="showForm = true" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
        + Neue Ausleihe
      </button>
    </div>

    <!-- Form Modal -->
    <div v-if="showForm" class="fixed inset-0 bg-black/50 flex items-center justify-center z-10">
      <div class="bg-white rounded-xl p-6 w-full max-w-md shadow-xl">
        <h3 class="text-lg font-semibold mb-4">{{ editing ? 'Bearbeiten' : 'Neue Ausleihe' }}</h3>
        <form @submit.prevent="save" class="space-y-3">
          <select v-model="form.schluessel_id" required class="w-full border rounded-lg px-3 py-2">
            <option value="" disabled>Schluessel waehlen...</option>
            <option v-for="s in schluesselliste" :key="s.id" :value="s.id">{{ s.schluessel_nr }}</option>
          </select>
          <select v-model="form.kontakt_id" required class="w-full border rounded-lg px-3 py-2">
            <option value="" disabled>Kontakt waehlen...</option>
            <option v-for="k in kontaktliste" :key="k.id" :value="k.id">{{ k.vorname }} {{ k.nachname }}</option>
          </select>
          <label class="block text-sm text-gray-600">Ausgabedatum</label>
          <input v-model="form.ausgabe_datum" type="date" required class="w-full border rounded-lg px-3 py-2" />
          <label class="flex items-center gap-2 text-sm">
            <input v-model="form.befristet" type="checkbox" /> Befristet
          </label>
          <div v-if="form.befristet">
            <label class="block text-sm text-gray-600">Rueckgabe soll</label>
            <input v-model="form.rueckgabe_soll" type="date" class="w-full border rounded-lg px-3 py-2" />
          </div>
          <select v-model="form.status" class="w-full border rounded-lg px-3 py-2">
            <option value="aktiv">Aktiv</option>
            <option value="zurueck">Zurueck</option>
            <option value="ueberfaellig">Ueberfaellig</option>
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
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Schluessel</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Kontakt</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ausgabe</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rueckgabe soll</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            <th class="px-6 py-3"></th>
          </tr>
        </thead>
        <tbody class="divide-y">
          <tr v-for="item in items" :key="item.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 font-medium">{{ schluesselName(item.schluessel_id) }}</td>
            <td class="px-6 py-4 text-gray-600">{{ kontaktName(item.kontakt_id) }}</td>
            <td class="px-6 py-4 text-gray-600">{{ item.ausgabe_datum }}</td>
            <td class="px-6 py-4 text-gray-600">{{ item.rueckgabe_soll ?? '-' }}</td>
            <td class="px-6 py-4">
              <span :class="statusClass(item.status)" class="px-2 py-1 rounded-full text-xs font-medium">{{ item.status }}</span>
            </td>
            <td class="px-6 py-4 text-right space-x-2">
              <button @click="edit(item)" class="text-blue-600 hover:underline text-sm">Bearbeiten</button>
              <button @click="remove(item.id)" class="text-red-600 hover:underline text-sm">Loeschen</button>
            </td>
          </tr>
          <tr v-if="!items.length">
            <td colspan="6" class="px-6 py-8 text-center text-gray-400">Keine Ausleihen vorhanden</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ausleihen as api, schluessel as schluesselApi, kontakte as kontakteApi } from '../api'

const items = ref([])
const schluesselliste = ref([])
const kontaktliste = ref([])
const showForm = ref(false)
const editing = ref(null)

const today = new Date().toISOString().split('T')[0]
const form = ref({ schluessel_id: '', kontakt_id: '', ausgabe_datum: today, rueckgabe_soll: null, rueckgabe_ist: null, befristet: false, unterschrift_base64: null, quittung_pdf_path: null, status: 'aktiv' })

async function load() {
  const [a, s, k] = await Promise.all([api.list(), schluesselApi.list(), kontakteApi.list()])
  items.value = a.data
  schluesselliste.value = s.data
  kontaktliste.value = k.data
}

function schluesselName(id) {
  return schluesselliste.value.find(s => s.id === id)?.schluessel_nr ?? id
}

function kontaktName(id) {
  const k = kontaktliste.value.find(k => k.id === id)
  return k ? `${k.vorname ?? ''} ${k.nachname}`.trim() : id
}

function statusClass(s) {
  return s === 'aktiv' ? 'bg-green-100 text-green-700' : s === 'zurueck' ? 'bg-gray-100 text-gray-700' : 'bg-red-100 text-red-700'
}

function cancel() {
  showForm.value = false
  editing.value = null
  form.value = { schluessel_id: '', kontakt_id: '', ausgabe_datum: today, rueckgabe_soll: null, rueckgabe_ist: null, befristet: false, unterschrift_base64: null, quittung_pdf_path: null, status: 'aktiv' }
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
