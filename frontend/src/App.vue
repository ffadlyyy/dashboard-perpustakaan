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

// BARU: state pencarian & urutan
const search = ref('')
const sortOrder = ref('asc')   // 'asc' = A-Z, 'desc' = Z-A

// BARU computed #1: filter berdasarkan judul atau penulis
const filteredBooks = computed(() => {
  const q = search.value.trim().toLowerCase()
  return books.value.filter(b =>
    b.judul.toLowerCase().includes(q) || b.penulis.toLowerCase().includes(q)
  )
})

// BARU computed #2: berantai, mengurutkan hasil computed #1
const sortedBooks = computed(() => {
  const list = [...filteredBooks.value]
  return list.sort((a, b) =>
    sortOrder.value === 'asc'
      ? a.judul.localeCompare(b.judul)
      : b.judul.localeCompare(a.judul)
  )
})

// BARU: status "kosong" khusus hasil pencarian
const noSearchResult = computed(
  () => status.value === 'success' && books.value.length > 0 && sortedBooks.value.length === 0
)

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

    <template v-else>
      <div class="toolbar">
        <input v-model="search" placeholder="Cari judul atau penulis..." />
        <button @click="sortOrder = 'asc'">A-Z</button>
        <button @click="sortOrder = 'desc'">Z-A</button>
      </div>

      <p v-if="noSearchResult">Tidak ada buku yang cocok dengan "{{ search }}".</p>

      <ul v-else>
        <li v-for="b in sortedBooks" :key="b.id">
          {{ b.judul }} - {{ b.penulis }} ({{ b.kategori }}) | stok: {{ b.stok }}
        </li>
      </ul>
    </template>
  </main>
</template>