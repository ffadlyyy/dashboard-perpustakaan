<script setup>
import { ref, computed, onMounted } from 'vue'

const API_URL = 'http://127.0.0.1:8000'
const STOK_MENIPIS_MAX = 3   // stok 1..3 = Menipis, 0 = Stok Habis, >3 = Tersedia

const books = ref([])
const status = ref('loading')

// BARU: parameter showLoading, false untuk refresh diam-diam
async function fetchBooks(showLoading = true) {
  if (showLoading) status.value = 'loading'
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

function stockStatus(stok) {
  if (stok === 0) return { label: 'Stok Habis', cls: 'habis' }
  if (stok <= STOK_MENIPIS_MAX) return { label: 'Menipis', cls: 'menipis' }
  return { label: 'Tersedia', cls: 'tersedia' }
}

const totalBuku = computed(() => books.value.length)
const menipisHabis = computed(() => books.value.filter(b => b.stok <= STOK_MENIPIS_MAX).length)
const jumlahKategori = computed(() => new Set(books.value.map(b => b.kategori)).size)
const totalEksemplar = computed(() => books.value.reduce((sum, b) => sum + b.stok, 0))

// BARU: state lokal form tambah buku
const form = ref({ judul: '', penulis: '', kategori: '', stok: 0 })
const actionError = ref('')

// BARU: POST ke backend, lalu refresh daftar
async function addBook() {
  actionError.value = ''
  const f = form.value
  if (!f.judul.trim() || !f.penulis.trim() || !f.kategori.trim()
      || !Number.isInteger(f.stok) || f.stok < 0) {
    actionError.value = 'Semua kolom wajib diisi, stok harus angka bulat 0 atau lebih.'
    return
  }
  try {
    const res = await fetch(`${API_URL}/books`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        judul: f.judul.trim(),
        penulis: f.penulis.trim(),
        kategori: f.kategori.trim(),
        stok: f.stok,
      }),
    })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    form.value = { judul: '', penulis: '', kategori: '', stok: 0 }
    await fetchBooks(false)
  } catch (err) {
    console.error(err)
    actionError.value = 'Gagal menambah buku. Cek koneksi ke backend.'
  }
}

// BARU: DELETE ke backend, lalu refresh daftar
async function deleteBook(id) {
  actionError.value = ''
  try {
    const res = await fetch(`${API_URL}/books/${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    await fetchBooks(false)
  } catch (err) {
    console.error(err)
    actionError.value = 'Gagal menghapus buku. Cek koneksi ke backend.'
  }
}

onMounted(fetchBooks)
</script>

<template>
  <main>
    <h1>Dashboard Perpustakaan</h1>

    <p v-if="status === 'loading'">Memuat data...</p>

    <div v-else-if="status === 'error'">
      <p>Gagal terhubung ke backend.</p>
      <button @click="fetchBooks()">Coba lagi</button>
    </div>

    <template v-else>
      <section class="tiles">
        <div class="tile"><span>Total Buku</span><strong>{{ totalBuku }}</strong></div>
        <div class="tile"><span>Stok Menipis + Habis</span><strong>{{ menipisHabis }}</strong></div>
        <div class="tile"><span>Jumlah Kategori</span><strong>{{ jumlahKategori }}</strong></div>
        <div class="tile"><span>Total Eksemplar</span><strong>{{ totalEksemplar }}</strong></div>
      </section>

      <!-- BARU: form tambah buku -->
      <form class="add-form" @submit.prevent="addBook">
        <input v-model="form.judul" placeholder="Judul" />
        <input v-model="form.penulis" placeholder="Penulis" />
        <input v-model="form.kategori" placeholder="Kategori" />
        <input v-model.number="form.stok" type="number" min="0" placeholder="Stok" />
        <button type="submit">Tambah</button>
      </form>
      <p v-if="actionError" class="error">{{ actionError }}</p>

      <p v-if="isEmpty">Belum ada buku.</p>

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
            <span class="badge" :class="stockStatus(b.stok).cls">
              {{ stockStatus(b.stok).label }}
            </span>
            <!-- BARU: tombol hapus -->
            <button class="delete-btn" @click="deleteBook(b.id)">Hapus</button>
          </li>
        </ul>
      </template>
    </template>
  </main>
</template>