<template>
  <div class="p-8">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-800">Ausleihen</h2>
      <button @click="startCheckout" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
        + Neue Ausleihe
      </button>
    </div>

    <!-- ═══════════════════════════════════════════════
         CHECKOUT WIZARD MODAL
    ════════════════════════════════════════════════ -->
    <div v-if="wizard.open" class="fixed inset-0 bg-black/60 flex items-center justify-center z-20 p-4">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg max-h-[95vh] overflow-y-auto">

        <!-- Step indicator -->
        <div class="flex border-b">
          <div v-for="(label, i) in ['Formular', 'Unterschrift', 'Fertig']" :key="i"
               :class="['flex-1 py-3 text-center text-sm font-medium transition-colors',
                        wizard.step === i + 1 ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-400']">
            <span class="inline-flex items-center justify-center w-6 h-6 rounded-full mr-1 text-xs"
                  :class="wizard.step > i ? 'bg-blue-600 text-white' : wizard.step === i + 1 ? 'border-2 border-blue-600 text-blue-600' : 'border-2 border-gray-300 text-gray-400'">
              {{ wizard.step > i ? '✓' : i + 1 }}
            </span>
            {{ label }}
          </div>
        </div>

        <!-- ── STEP 1: FORM ── -->
        <div v-if="wizard.step === 1" class="p-6 space-y-4">
          <h3 class="text-lg font-semibold text-gray-800">Schlüsselausgabe erfassen</h3>

          <!-- Schlüssel -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Schlüssel *</label>
            <select v-model="form.schluessel_id" required class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="">Schlüssel wählen...</option>
              <option v-for="s in verfuegbareSchluessel" :key="s.id" :value="s.id">
                {{ s.schluessel_nr }}{{ s.laufnummer ? ` (Nr. ${s.laufnummer})` : '' }}
              </option>
            </select>
            <p v-if="verfuegbareSchluessel.length === 0" class="text-xs text-amber-600 mt-1">Keine verfügbaren Schlüssel</p>
          </div>

          <!-- Kontakt -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Kontakt *</label>
            <div class="flex gap-2">
              <select v-model="form.kontakt_id" class="flex-1 border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500">
                <option value="">Kontakt wählen...</option>
                <option v-for="k in kontaktliste" :key="k.id" :value="k.id">
                  {{ k.vorname ? k.vorname + ' ' : '' }}{{ k.nachname }}{{ k.firma ? ` – ${k.firma}` : '' }}
                </option>
              </select>
              <button type="button" @click="showNeuerKontakt = !showNeuerKontakt"
                      class="px-3 py-2 border rounded-lg text-sm text-blue-600 hover:bg-blue-50 whitespace-nowrap">
                + Neu
              </button>
            </div>
          </div>

          <!-- Neuer Kontakt inline form -->
          <div v-if="showNeuerKontakt" class="border rounded-xl p-4 bg-gray-50 space-y-3">
            <p class="text-sm font-semibold text-gray-700">Neuer Kontakt</p>
            <select v-model="neuerKontakt.typ" class="w-full border rounded-lg px-3 py-2 text-sm">
              <option value="mieter">Mieter</option>
              <option value="handwerker">Handwerker</option>
            </select>
            <div class="flex gap-2">
              <input v-model="neuerKontakt.vorname" placeholder="Vorname" class="flex-1 border rounded-lg px-3 py-2 text-sm" />
              <input v-model="neuerKontakt.nachname" placeholder="Nachname *" required class="flex-1 border rounded-lg px-3 py-2 text-sm" />
            </div>
            <input v-model="neuerKontakt.firma" placeholder="Firma (optional)" class="w-full border rounded-lg px-3 py-2 text-sm" />
            <input v-model="neuerKontakt.email" type="email" placeholder="E-Mail" class="w-full border rounded-lg px-3 py-2 text-sm" />
            <input v-model="neuerKontakt.telefon" placeholder="Telefon" class="w-full border rounded-lg px-3 py-2 text-sm" />
            <button type="button" @click="saveNeuerKontakt"
                    class="w-full py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700">
              Kontakt speichern
            </button>
          </div>

          <!-- Frist -->
          <div>
            <label class="flex items-center gap-2 text-sm font-medium text-gray-700 cursor-pointer">
              <input v-model="form.befristet" type="checkbox" class="rounded" />
              Rückgabe-Frist setzen
            </label>
            <div v-if="form.befristet" class="mt-2">
              <input v-model="form.rueckgabe_soll" type="date" :min="today"
                     class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500" />
            </div>
          </div>

          <!-- Bemerkung -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Bemerkung</label>
            <textarea v-model="form.bemerkung" rows="2" placeholder="Optional..."
                      class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 resize-none"></textarea>
          </div>

          <div class="flex gap-2 justify-end pt-2">
            <button type="button" @click="closeWizard" class="px-4 py-2 border rounded-lg hover:bg-gray-50">Abbrechen</button>
            <button type="button" @click="goToSignature"
                    :disabled="!form.schluessel_id || (!form.kontakt_id)"
                    class="px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-40">
              Weiter →
            </button>
          </div>
        </div>

        <!-- ── STEP 2: SIGNATURE PAD ── -->
        <div v-if="wizard.step === 2" class="p-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-1">Unterschrift des Empfängers</h3>
          <p class="text-sm text-gray-500 mb-4">Bitte im Feld unten unterschreiben (Maus oder Touch)</p>

          <div class="border-2 border-dashed border-gray-300 rounded-xl overflow-hidden bg-gray-50"
               style="touch-action: none;">
            <canvas ref="sigCanvas"
                    class="w-full cursor-crosshair"
                    style="height: 220px; display: block;"
                    @mousedown="startDraw" @mousemove="draw" @mouseup="stopDraw" @mouseleave="stopDraw"
                    @touchstart.prevent="touchStart" @touchmove.prevent="touchMove" @touchend="stopDraw">
            </canvas>
          </div>

          <div class="flex justify-between mt-3">
            <button type="button" @click="clearSignature" class="text-sm text-gray-500 hover:text-gray-700">
              ✕ Löschen
            </button>
            <span class="text-xs text-gray-400 self-center">Feld berühren oder mit Maus zeichnen</span>
          </div>

          <div class="flex gap-2 justify-end mt-5">
            <button type="button" @click="wizard.step = 1" class="px-4 py-2 border rounded-lg hover:bg-gray-50">← Zurück</button>
            <button type="button" @click="submitCheckout" :disabled="wizard.saving"
                    class="px-5 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-40">
              <span v-if="wizard.saving">Wird gespeichert...</span>
              <span v-else>Ausleihe bestätigen</span>
            </button>
          </div>
        </div>

        <!-- ── STEP 3: SUCCESS ── -->
        <div v-if="wizard.step === 3" class="p-6 text-center">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Ausleihe gespeichert!</h3>
          <p class="text-gray-500 mb-6">
            Ausleihe-Nr. <strong>#{{ wizard.createdId }}</strong> wurde erfolgreich angelegt und die Quittung wurde generiert.
          </p>
          <div class="flex gap-3 justify-center">
            <button type="button" @click="openPdf" class="px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
              PDF öffnen / drucken
            </button>
            <button type="button" @click="closeWizard" class="px-5 py-2 border rounded-lg hover:bg-gray-50">Schliessen</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════
         TABLE
    ════════════════════════════════════════════════ -->
    <div class="bg-white rounded-xl shadow overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Schlüssel</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Kontakt</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ausgabe</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Frist</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            <th class="px-6 py-3"></th>
          </tr>
        </thead>
        <tbody class="divide-y">
          <tr v-for="item in items" :key="item.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 font-medium">{{ schluesselName(item.schluessel_id) }}</td>
            <td class="px-6 py-4 text-gray-600">{{ kontaktName(item.kontakt_id) }}</td>
            <td class="px-6 py-4 text-gray-600">{{ fmtDate(item.ausgabe_datum) }}</td>
            <td class="px-6 py-4 text-gray-600">{{ item.rueckgabe_soll ? fmtDate(item.rueckgabe_soll) : '–' }}</td>
            <td class="px-6 py-4">
              <span :class="statusClass(item.status)" class="px-2 py-1 rounded-full text-xs font-medium">
                {{ statusLabel(item.status) }}
              </span>
            </td>
            <td class="px-6 py-4 text-right space-x-2 whitespace-nowrap">
              <button v-if="item.quittung_pdf_path" @click="openPdfFor(item.id)"
                      class="text-blue-600 hover:underline text-sm">PDF</button>
              <button v-if="item.status === 'aktiv'" @click="doRueckgabe(item)"
                      class="text-green-600 hover:underline text-sm">Rückgabe</button>
              <button @click="remove(item.id)" class="text-red-600 hover:underline text-sm">Löschen</button>
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
import { ref, onMounted, nextTick } from 'vue'
import { ausleihen as api, schluessel as schluesselApi, kontakte as kontakteApi } from '../api'

// ── Data ──────────────────────────────────────────────────────────────────────
const items = ref([])
const schluesselliste = ref([])
const kontaktliste = ref([])
const verfuegbareSchluessel = ref([])

const today = new Date().toISOString().split('T')[0]

// ── Wizard state ──────────────────────────────────────────────────────────────
const wizard = ref({ open: false, step: 1, saving: false, createdId: null })

const emptyForm = () => ({
  schluessel_id: '',
  kontakt_id: '',
  befristet: false,
  rueckgabe_soll: '',
  bemerkung: '',
})
const form = ref(emptyForm())

// ── New contact inline form ───────────────────────────────────────────────────
const showNeuerKontakt = ref(false)
const neuerKontakt = ref({ typ: 'mieter', vorname: '', nachname: '', firma: '', email: '', telefon: '' })

// ── Signature pad ─────────────────────────────────────────────────────────────
const sigCanvas = ref(null)
let isDrawing = false
let lastX = 0
let lastY = 0

// ── Load data ─────────────────────────────────────────────────────────────────
async function load() {
  const [a, s, k] = await Promise.all([api.list(), schluesselApi.list(), kontakteApi.list()])
  items.value = a.data
  schluesselliste.value = s.data
  kontaktliste.value = k.data
  verfuegbareSchluessel.value = s.data.filter(s => s.status === 'verfuegbar')
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function schluesselName(id) {
  const s = schluesselliste.value.find(s => s.id === id)
  return s ? s.schluessel_nr : `#${id}`
}

function kontaktName(id) {
  const k = kontaktliste.value.find(k => k.id === id)
  return k ? `${k.vorname ?? ''} ${k.nachname}`.trim() : `#${id}`
}

function fmtDate(d) {
  if (!d) return '–'
  const [y, m, day] = d.split('-')
  return `${day}.${m}.${y}`
}

function statusClass(s) {
  return {
    aktiv: 'bg-green-100 text-green-700',
    zurueck: 'bg-gray-100 text-gray-700',
    ueberfaellig: 'bg-red-100 text-red-700',
  }[s] ?? 'bg-gray-100 text-gray-600'
}

function statusLabel(s) {
  return { aktiv: 'Aktiv', zurueck: 'Zurückgegeben', ueberfaellig: 'Überfällig' }[s] ?? s
}

// ── Wizard control ────────────────────────────────────────────────────────────
function startCheckout() {
  form.value = emptyForm()
  showNeuerKontakt.value = false
  neuerKontakt.value = { typ: 'mieter', vorname: '', nachname: '', firma: '', email: '', telefon: '' }
  wizard.value = { open: true, step: 1, saving: false, createdId: null }
}

function closeWizard() {
  wizard.value.open = false
  load()
}

function goToSignature() {
  if (!form.value.schluessel_id || !form.value.kontakt_id) return
  wizard.value.step = 2
  nextTick(() => initCanvas())
}

// ── New contact ───────────────────────────────────────────────────────────────
async function saveNeuerKontakt() {
  if (!neuerKontakt.value.nachname) return
  const res = await kontakteApi.create(neuerKontakt.value)
  kontaktliste.value.push(res.data)
  form.value.kontakt_id = res.data.id
  showNeuerKontakt.value = false
}

// ── Signature canvas ──────────────────────────────────────────────────────────
function initCanvas() {
  const canvas = sigCanvas.value
  if (!canvas) return
  canvas.width = canvas.offsetWidth
  canvas.height = canvas.offsetHeight
  const ctx = canvas.getContext('2d')
  ctx.fillStyle = '#f9fafb'
  ctx.fillRect(0, 0, canvas.width, canvas.height)
  ctx.strokeStyle = '#1e3a8a'
  ctx.lineWidth = 2.5
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
}

function getPos(e, canvas) {
  const rect = canvas.getBoundingClientRect()
  const scaleX = canvas.width / rect.width
  const scaleY = canvas.height / rect.height
  return {
    x: (e.clientX - rect.left) * scaleX,
    y: (e.clientY - rect.top) * scaleY,
  }
}

function startDraw(e) {
  isDrawing = true
  const pos = getPos(e, sigCanvas.value)
  lastX = pos.x
  lastY = pos.y
}

function draw(e) {
  if (!isDrawing) return
  const canvas = sigCanvas.value
  const ctx = canvas.getContext('2d')
  const pos = getPos(e, canvas)
  ctx.beginPath()
  ctx.moveTo(lastX, lastY)
  ctx.lineTo(pos.x, pos.y)
  ctx.stroke()
  lastX = pos.x
  lastY = pos.y
}

function stopDraw() {
  isDrawing = false
}

function touchStart(e) {
  const touch = e.touches[0]
  startDraw(touch)
}

function touchMove(e) {
  const touch = e.touches[0]
  draw(touch)
}

function clearSignature() {
  const canvas = sigCanvas.value
  const ctx = canvas.getContext('2d')
  ctx.fillStyle = '#f9fafb'
  ctx.fillRect(0, 0, canvas.width, canvas.height)
}

function getSignatureBase64() {
  return sigCanvas.value ? sigCanvas.value.toDataURL('image/png') : null
}

// ── Submit checkout ───────────────────────────────────────────────────────────
async function submitCheckout() {
  wizard.value.saving = true
  try {
    const payload = {
      schluessel_id: form.value.schluessel_id,
      kontakt_id: form.value.kontakt_id,
      befristet: form.value.befristet,
      rueckgabe_soll: form.value.befristet && form.value.rueckgabe_soll ? form.value.rueckgabe_soll : null,
      bemerkung: form.value.bemerkung || null,
      unterschrift_base64: getSignatureBase64(),
    }
    const res = await api.checkout(payload)
    wizard.value.createdId = res.data.id
    wizard.value.step = 3
    await load()
  } catch (err) {
    alert(err.response?.data?.detail ?? 'Fehler beim Speichern')
  } finally {
    wizard.value.saving = false
  }
}

// ── PDF ───────────────────────────────────────────────────────────────────────
function openPdf() {
  window.open(api.pdfUrl(wizard.value.createdId), '_blank')
}

function openPdfFor(id) {
  window.open(api.pdfUrl(id), '_blank')
}

// ── Rückgabe ──────────────────────────────────────────────────────────────────
async function doRueckgabe(item) {
  const name = schluesselName(item.schluessel_id)
  if (!confirm(`Rückgabe von Schlüssel "${name}" bestätigen?`)) return
  await api.rueckgabe(item.id)
  load()
}

// ── Delete ────────────────────────────────────────────────────────────────────
async function remove(id) {
  if (confirm('Ausleihe wirklich löschen?')) {
    await api.delete(id)
    load()
  }
}

onMounted(load)
</script>
