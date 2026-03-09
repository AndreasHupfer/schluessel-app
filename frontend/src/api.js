import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export const liegenschaften = {
  list: () => api.get('/liegenschaften/'),
  get: (id) => api.get(`/liegenschaften/${id}`),
  create: (data) => api.post('/liegenschaften/', data),
  update: (id, data) => api.put(`/liegenschaften/${id}`, data),
  delete: (id) => api.delete(`/liegenschaften/${id}`),
}

export const schliessungen = {
  list: (params) => api.get('/schliessungen/', { params }),
  get: (id) => api.get(`/schliessungen/${id}`),
  create: (data) => api.post('/schliessungen/', data),
  update: (id, data) => api.put(`/schliessungen/${id}`, data),
  delete: (id) => api.delete(`/schliessungen/${id}`),
}

export const schluessel = {
  list: (params) => api.get('/schluessel/', { params }),
  get: (id) => api.get(`/schluessel/${id}`),
  create: (data) => api.post('/schluessel/', data),
  update: (id, data) => api.put(`/schluessel/${id}`, data),
  delete: (id) => api.delete(`/schluessel/${id}`),
}

export const kontakte = {
  list: () => api.get('/kontakte/'),
  get: (id) => api.get(`/kontakte/${id}`),
  create: (data) => api.post('/kontakte/', data),
  update: (id, data) => api.put(`/kontakte/${id}`, data),
  delete: (id) => api.delete(`/kontakte/${id}`),
}

export const ausleihen = {
  list: (params) => api.get('/ausleihen/', { params }),
  get: (id) => api.get(`/ausleihen/${id}`),
  create: (data) => api.post('/ausleihen/', data),
  update: (id, data) => api.put(`/ausleihen/${id}`, data),
  delete: (id) => api.delete(`/ausleihen/${id}`),
}
