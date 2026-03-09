import { createRouter, createWebHistory } from 'vue-router'
import Liegenschaften from '../views/Liegenschaften.vue'
import Schluessel from '../views/Schluessel.vue'
import Kontakte from '../views/Kontakte.vue'
import Ausleihen from '../views/Ausleihen.vue'

const routes = [
  { path: '/', redirect: '/liegenschaften' },
  { path: '/liegenschaften', component: Liegenschaften },
  { path: '/schluessel', component: Schluessel },
  { path: '/kontakte', component: Kontakte },
  { path: '/ausleihen', component: Ausleihen },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
