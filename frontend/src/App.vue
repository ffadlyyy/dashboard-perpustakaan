<script setup>
import { ref, computed, onMounted } from 'vue'

const API_URL = 'http://127.0.0.1:8000'

const books = ref([])           // data dari backend disimpan sebagai ref
const status = ref('loading')   // 'loading' | 'error' | 'success'

async function fetchBooks() {
  status.value = 'loading'
  try {
    const res = await fetch(`${API_URL}/books`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    books.value = await res.json()
    status.value = 'success'
  } catch (err) {
    console.error(err)
    status.value = 'error'
  }
}

const isEmpty = computed(() => status.value === 'success' && books.value.length === 0)

onMounted(fetchBooks)
</script>

<template>
  <main>
    <h1>Dashboard Perpustakaan</h1>

    <p v-if="status === 'loading'">Memuat data...</p>

    <div v-else-if="status === 'error'">
      <p>Gagal terhubung ke backend.</p>
      <button @click="fetchBooks">Coba lagi</button>
    </div>

    <p v-else-if="isEmpty">Belum ada buku.</p>

    <ul v-else>
      <li v-for="b in books" :key="b.id">
        {{ b.judul }} - {{ b.penulis }} ({{ b.kategori }}) | stok: {{ b.stok }}
      </li>
    </ul>
  </main>
</template>