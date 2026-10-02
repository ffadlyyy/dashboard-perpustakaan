# Dashboard Perpustakaan

Mini dashboard full-stack untuk mengelola daftar buku perpustakaan.
UTS Web Application Development (Soal A).

**Stack:** Vue 3 (Composition API) + Vite di frontend, FastAPI + Pydantic di backend.

## Fitur

- Daftar buku dari backend (GET), tambah buku (POST), hapus buku (DELETE)
- Pencarian berdasarkan judul atau penulis
- Urutkan judul A-Z / Z-A
- Badge status stok: Tersedia, Menipis, Stok Habis
- 4 tile ringkasan: Total Buku, Stok Menipis + Habis, Jumlah Kategori, Total Eksemplar
- Status UI: loading, kosong, error, berhasil
- Tampilan responsif (desktop, tablet, mobile)

## Cara Menjalankan

Butuh Python 3.10+ dan Node.js 18+. Backend dan frontend dijalankan di dua terminal terpisah.

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend berjalan di `http://127.0.0.1:8000`. Dokumentasi API ada di `http://127.0.0.1:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend berjalan di `http://localhost:5173`. Pastikan port ini tidak berubah,
karena CORS di backend hanya mengizinkan `localhost:5173`.

## Endpoint API

| Method | Path | Fungsi |
|---|---|---|
| GET | `/books` | Ambil semua buku |
| POST | `/books` | Tambah buku baru |
| DELETE | `/books/{id}` | Hapus buku berdasarkan id |

Field buku: `id`, `judul`, `penulis`, `kategori`, `stok` (angka bulat, minimal 0).

## Data Seed

Data awal ada di `backend/books.json` (20 buku buatan sendiri). Data disimpan
sebagai list Python in-memory, sehingga setiap backend di-restart data kembali
ke isi `books.json`. Ini disengaja sesuai ketentuan soal (tanpa database).

## Ambang Batas Status Stok

| Status | Kondisi | Warna badge |
|---|---|---|
| Stok Habis | stok = 0 | Merah |
| Menipis | stok 1 sampai 3 | Kuning |
| Tersedia | stok 4 ke atas | Hijau |

**Alasan:** TULIS ALASANMU DI SINI.

Ambang ini disimpan di konstanta `STOK_MENIPIS_MAX` pada `frontend/src/App.vue`,
sehingga mudah diubah.