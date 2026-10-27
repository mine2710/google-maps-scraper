# 📁 Struktur Project

```
google-maps-scraper/
│
├── scraper.py              # ⭐ File utama - program scraper
├── requirements.txt        # 📦 Daftar library Python yang diperlukan
├── README.md               # 📖 Panduan lengkap penggunaan
├── LICENSE                 # ⚖️ Lisensi MIT
├── CONTOH_OUTPUT.md        # 📊 Contoh hasil scraping
├── CARA_UPLOAD_GITHUB.md   # 📤 Panduan upload ke GitHub
├── STRUKTUR_PROJECT.md     # 📁 File ini (penjelasan struktur)
│
├── .gitignore              # 🚫 File yang diabaikan Git (hasil scraping, cache)
├── .vscode/                # ⚙️ Konfigurasi VSCode (opsional)
│   └── launch.json         # ▶️ Setup untuk run/debug di VSCode
│
└── .git/                   # 🔧 Folder Git (jangan diedit manual)
```

---

## 📄 Penjelasan File

### `scraper.py`
File Python utama yang berisi seluruh logika scraping:
- **Kelas `Review`**: Menyimpan data review (penulis, rating, teks)
- **Kelas `Tempat`**: Menyimpan semua data tempat (nama, rating, alamat, harga, dll)
- **Fungsi `scroll_hasil_pencarian()`**: Scroll feed Google Maps untuk load lebih banyak tempat
- **Fungsi `scrape_harga()`**: Ambil harga dari tab "Harga" (khusus hotel)
- **Fungsi `scrape_reviews()`**: Ambil review dari tab "Ulasan"
- **Fungsi `scrape_detail_tempat()`**: Gabung semua data dari 1 tempat
- **Fungsi `simpan_hasil()`**: Export ke CSV dan Excel
- **Fungsi `main()`**: Entry point program (parsing argumen & orkestrasi)

### `requirements.txt`
Daftar library yang dibutuhkan:
```
playwright>=1.48.0   # Automasi browser
pandas>=2.2.0        # Manipulasi data & export Excel
openpyxl>=3.1.0      # Engine untuk Excel (.xlsx)
```

### `.gitignore`
File yang **tidak** ditrack Git:
- File hasil scraping (`*.csv`, `*.xlsx`)
- Cache Python (`__pycache__/`, `*.pyc`)
- Folder IDE (`.vscode/`, `.idea/`)
- File sistem (`.DS_Store`, `Thumbs.db`)

### `.vscode/launch.json`
Konfigurasi untuk menjalankan scraper di VSCode dengan tombol F5:
- Preset "Hotel di Lampung"
- Preset "Tempat Wisata Bandung"
- Bisa ditambah sendiri untuk kata kunci lain

---

## 🔄 Alur Kerja Scraper

```
1. Input kata kunci pencarian
   ↓
2. Buka Google Maps & cari
   ↓
3. Scroll feed untuk load lebih banyak hasil
   ↓
4. Kumpulkan URL tempat
   ↓
5. LOOP untuk setiap tempat:
   ├─ Buka halaman detail
   ├─ Ambil data utama (nama, rating, alamat, dll)
   ├─ [Jika hotel] Ambil harga dari tab "Harga"
   ├─ [Jika --reviews > 0] Ambil review dari tab "Ulasan"
   └─ Simpan ke list
   ↓
6. Export semua data ke CSV & Excel
   ↓
7. Selesai! 🎉
```

---

## 🛠️ Modifikasi & Kustomisasi

### Tambah kolom data baru
Edit class `Tempat` di `scraper.py`:
```python
@dataclass
class Tempat:
    nama: str = ""
    rating: str = ""
    # ... kolom lain ...
    jam_buka: str = ""  # ← tambah kolom baru
```

Lalu ambil datanya di fungsi `scrape_detail_tempat()`:
```python
tempat.jam_buka = ambil_teks(page, 'selector_jam_buka')
```

### Ubah jumlah default
Edit argumen di fungsi `main()`:
```python
parser.add_argument("--jumlah", type=int, default=50)  # ← ganti 20 jadi 50
```

### Tambah delay antar scraping
Tambahkan `time.sleep()` di loop utama untuk menghindari rate limit:
```python
for i, url in enumerate(links, 1):
    tempat = scrape_detail_tempat(page, url, args.reviews)
    daftar_tempat.append(tempat)
    time.sleep(3)  # ← tunggu 3 detik sebelum scrape tempat berikutnya
```

---

## 📊 File Output yang Dihasilkan

Setelah scraping, akan muncul file baru (tidak masuk Git karena ada di `.gitignore`):

```
hasil_scraping.csv       # Format CSV (bisa dibuka Excel/Google Sheets)
hasil_scraping.xlsx      # Format Excel native
hotel_lampung.csv        # Contoh output dengan custom nama
hotel_lampung.xlsx
```

---

## 🐛 Debugging

### Print halaman HTML mentah
```python
print(page.content())  # Tampilkan HTML lengkap
```

### Screenshot halaman
```python
page.screenshot(path="debug.png")
```

### Jalankan tanpa headless
Hilangkan flag `--headless` agar browser terlihat:
```bash
python scraper.py "kata kunci" --jumlah 5
```

### Breakpoint di VSCode
Tambahkan breakpoint di kode → tekan F5 untuk debug step-by-step
