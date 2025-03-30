# frontend/src/App.vue
<template>
  <div class="p-6 max-w-3xl mx-auto">
    <div v-if="!token">
      <h1 class="text-2xl font-bold mb-4">Login</h1>
      <form @submit.prevent="login" class="mb-6 flex flex-col gap-2 max-w-sm">
        <input v-model="credentials.username" placeholder="Username" required class="border p-2 rounded" />
        <input v-model="credentials.password" type="password" placeholder="Password" required class="border p-2 rounded" />
        <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Login</button>
      </form>
    </div>

    <div v-else>
      <h1 class="text-2xl font-bold mb-4">Employee Roster</h1>
      <form @submit.prevent="addShift" class="mb-6 flex flex-wrap gap-2">
        <input v-model="form.employee_name" placeholder="Employee Name" required class="border p-2 rounded" />
        <input type="date" v-model="form.date" required class="border p-2 rounded" />
        <input type="time" v-model="form.start_time" required class="border p-2 rounded" />
        <input type="time" v-model="form.end_time" required class="border p-2 rounded" />
        <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">Add Shift</button>
      </form>

      <ul>
        <li v-for="shift in shifts" :key="shift.id" class="mb-2">
          {{ shift.employee_name }} — {{ shift.date }} {{ shift.start_time }} to {{ shift.end_time }}
          <button @click="deleteShift(shift.id)" class="text-red-600 ml-2">❌</button>
        </li>
      </ul>

      <div class="mt-6">
        <button @click="exportData" class="bg-green-500 text-white px-4 py-2 rounded">Export</button>
        <input type="file" @change="importData" class="ml-4" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API = 'http://localhost:8000'
const token = ref(localStorage.getItem('token'))
const shifts = ref([])
const form = ref({ employee_name: '', date: '', start_time: '', end_time: '' })
const credentials = ref({ username: '', password: '' })

axios.interceptors.request.use(config => {
  if (token.value) {
    config.headers.Authorization = `Bearer ${token.value}`
  }
  return config
})

const login = async () => {
  const formData = new URLSearchParams()
  formData.append('username', credentials.value.username)
  formData.append('password', credentials.value.password)
  const res = await axios.post(`${API}/login`, formData)
  token.value = res.data.access_token
  localStorage.setItem('token', token.value)
  fetchShifts()
}

const fetchShifts = async () => {
  const res = await axios.get(`${API}/shifts`)
  shifts.value = res.data
}

const addShift = async () => {
  await axios.post(`${API}/shifts`, form.value)
  form.value = { employee_name: '', date: '', start_time: '', end_time: '' }
  fetchShifts()
}

const deleteShift = async (id) => {
  await axios.delete(`${API}/shifts/${id}`)
  fetchShifts()
}

const exportData = async () => {
  const res = await axios.post(`${API}/export`, {}, { responseType: 'blob' })
  const url = URL.createObjectURL(new Blob([res.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', 'roster_export.zip')
  document.body.appendChild(link)
  link.click()
}

const importData = async (e) => {
  const file = e.target.files[0]
  const formData = new FormData()
  formData.append('file', file)
  await axios.post(`${API}/import`, formData)
  fetchShifts()
}

onMounted(() => {
  if (token.value) fetchShifts()
})
</script>

<style>
@tailwind base;
@tailwind components;
@tailwind utilities;
</style>

