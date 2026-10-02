<script setup>
import { ref, computed, onMounted } from 'vue'

const API_URL = 'http://127.0.0.1:8000'

// BARU: ambang batas status stok (jelaskan di README)
const STOK_MENIPIS_MAX = 3   // stok 1..3 = Menipis, 0 = Stok Habis, >3 = Tersedia

const books = ref([])
const status = ref('loading')

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

const search = ref('')
const sortOrder = ref('asc')

const filteredBooks = computed(() => {
  const q = search.value.trim().toLowerCase()
  return books.value.filter(b =>
    b.judul.toLowerCase().includes(q) || b.penulis.toLowerCase().includes(q)
  )
})

const sortedBooks = computed(() => {
  const list = [...filteredBooks.value]
  return list.sort((a, b) =>
    sortOrder.value === 'asc'
      ? a.judul.localeCompare(b.judul)
      : b.judul.localeCompare(a.judul)
  )
})

const noSearchResult = computed(
  () => status.value === 'success' && books.value.length > 0 && sortedBooks.value.length === 0
)

// BARU: label & class badge, dipakai di template
function stockStatus(stok) {
  if (stok === 0) return { label: 'Stok Habis', cls: 'habis' }
  if (stok <= STOK_MENIPIS_MAX) return { label: 'Menipis', cls: 'menipis' }
  return { label: 'Tersedia', cls: 'tersedia' }
}

// BARU: 4 tile ringkasan, dihitung dari books (semua data, bukan hasil pencarian)
const totalBuku = computed(() => books.value.length)

const menipisHabis = computed(
  () => books.value.filter(b => b.stok <= STOK_MENIPIS_MAX).length
)

const jumlahKategori = computed(
  () => new Set(books.value.map(b => b.kategori)).size
)

const totalEksemplar = computed(
  () => books.value.reduce((sum, b) => sum + b.stok, 0)
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
      <!-- BARU: 4 tile ringkasan -->
      <section class="tiles">
        <div class="tile"><span>Total Buku</span><strong>{{ totalBuku }}</strong></div>
        <div class="tile"><span>Stok Menipis + Habis</span><strong>{{ menipisHabis }}</strong></div>
        <div class="tile"><span>Jumlah Kategori</span><strong>{{ jumlahKategori }}</strong></div>
        <div class="tile"><span>Total Eksemplar</span><strong>{{ totalEksemplar }}</strong></div>
      </section>

      <div class="toolbar">
        <input v-model="search" placeholder="Cari judul atau penulis..." />
        <button @click="sortOrder = 'asc'">A-Z</button>
        <button @click="sortOrder = 'desc'">Z-A</button>
      </div>

      <p v-if="noSearchResult">Tidak ada buku yang cocok dengan "{{ search }}".</p>

      <ul v-else>
        <li v-for="b in sortedBooks" :key="b.id">
          {{ b.judul }} - {{ b.penulis }} ({{ b.kategori }}) | stok: {{ b.stok }}
          <!-- BARU: badge dengan conditional class binding -->
          <span class="badge" :class="stockStatus(b.stok).cls">
            {{ stockStatus(b.stok).label }}
          </span>
        </li>
      </ul>
    </template>
  </main>
</template>