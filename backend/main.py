import json
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# --- Skema Pydantic ---
class BookCreate(BaseModel):
    judul: str = Field(..., min_length=1)
    penulis: str = Field(..., min_length=1)
    kategori: str = Field(..., min_length=1)
    stok: int = Field(..., ge=0)   # harus angka, tidak boleh negatif

class Book(BookCreate):
    id: int

# --- Data in-memory, di-seed dari JSON saat server start ---
books: list[Book] = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    data = json.loads(Path(__file__).with_name("books.json").read_text(encoding="utf-8"))
    books.clear()
    books.extend(Book(**item) for item in data)
    yield

app = FastAPI(
    title="API Perpustakaan",
    description="Mini dashboard perpustakaan (UTS WAD)",
    lifespan=lifespan,
)

# CORS: izinkan Vite dev server memanggil backend lokal
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoint ---
@app.get("/books", response_model=list[Book], summary="Ambil semua buku")
def get_books():
    return books

@app.post("/books", response_model=Book, status_code=201, summary="Tambah buku baru")
def add_book(payload: BookCreate):
    new_id = max((b.id for b in books), default=0) + 1
    book = Book(id=new_id, **payload.model_dump())
    books.append(book)
    return book

@app.delete("/books/{book_id}", summary="Hapus buku berdasarkan id")
def delete_book(book_id: int):
    for i, b in enumerate(books):
        if b.id == book_id:
            books.pop(i)
            return {"message": f"Buku {book_id} dihapus"}
    raise HTTPException(status_code=404, detail="Buku tidak ditemukan")