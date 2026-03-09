<template>
  <div class="p-8">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-800">Kontakte</h2>
      <button @click="showForm = true" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
        + Neuer Kontakt
      </button>
    </div>

    <!-- Form Modal -->
    <div v-if="showForm" class="fixed inset-0 bg-black/50 flex items-center justify-center z-10">
      <div class="bg-white rounded-xl p-6 w-full max-w-md shadow-xl">
        <h3 class="text-lg font-semibold mb-4">{{ editing ? 'Bearbeiten' : 'Neuer Kontakt' }}</h3>
        <form @submit.prevent="save" class="space-y-3">
          <select v-model="form.typ" required class="w-full border rounded-lg px-3 py-2">
            <option value="handwerker">Handwerker</option>
            <option value="mieter">Mieter</option>
          </select>
          <input v-model="form.firma" placeholder="Firma (optional)" class="w-full border rounded-lg px-3 py-2" />
          <div class="flex gap-2">
            <input v-model="form.vorname" placeholder="Vorname" class="flex-1 border rounded-lg px-3 py-2" />
            <input v-model="form.nachname" placeholder="Nachname" required class="flex-1 border rounded-lg px-3 py-2" />
          </div>
          <input v-model="form.email" type="email" placeholder="E-Mail" class="w-full border rounded-lg px-3 py-2" />
          <input v-model="form.telefon" placeholder="Telefon" class="w-full border rounded-lg px-3 py-2" />
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
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Typ</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Firma</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Kontakt</th>
            <th class="px-6 py-3"></th>
          </tr>
        </thead>
        <tbody class="divide-y">
          <tr v-for="item in items" :key="item.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 font-medium">{{ item.vorname }} {{ item.nachname }}</td>
            <td class="px-6 py-4">
              <span class="px-2 py-1 bg-gray-100 rounded-full text-xs">{{ item.typ }}</span>
            </td>
            <td class="px-6 py-4 text-gray-600">{{ item.firma ?? '-' }}</td>
            <td class="px-6 py-4 text-gray-600 text-sm">
              <div v-if="item.email">{{ item.email }}</div>
              <div v-if="item.telefon">{{ item.telefon }}</div>
            </td>
            <td class="px-6 py-4 text-right space-x-2">
              <button @click="edit(item)" class="text-blue-600 hover:underline text-sm">Bearbeiten</button>
              <button @click="remove(item.id)" class="text-red-600 hover:underline text-sm">Loeschen</button>
            </td>
          </tr>
          <tr v-if="!items.length">
            <td colspan="5" class="px-6 py-8 text-center text-gray-400">Keine Kontakte vorhanden</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { kontakte as api } from '../api'

const items = ref([])
const showForm = ref(false)
const editing = ref(null)
const form = ref({ typ: 'mieter', firma: '', vorname: '', nachname: '', email: '', telefon: '' })

async function load() {
  const res = await api.list()
  items.value = res.data
}

function cancel() {
  showForm.value = false
  editing.value = null
  form.value = { typ: 'mieter', firma: '', vorname: '', nachname: '', email: '', telefon: '' }
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
