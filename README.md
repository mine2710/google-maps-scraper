# 🗺️ Google Maps Scraper

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Playwright](https://img.shields.io/badge/playwright-1.48+-orange.svg)](https://playwright.dev/)

Scraper sederhana untuk mengambil data tempat dari Google Maps (hotel, tempat wisata, restoran, dll), termasuk:
- ⭐ Rating & jumlah ulasan
- 📍 Alamat, kategori, website, telepon
- 💰 **Harga** (terendah, tertinggi, rata-rata) — khusus hotel/penginapan
- 💬 **Review/komentar** dari pengunjung (nama, rating, teks ulasan)

Hasil disimpan dalam format **CSV** dan **Excel** yang siap dianalisis.

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/USERNAME/google-maps-scraper.git
cd google-maps-scraper

# 2. Install dependencies
pip install -r requirements.txt
python -m playwright install chromium

# 3. Jalankan!
python scraper.py "Hotel di Bandung" --jumlah 10 --reviews 5
```

**Output**: File `hasil_scraping.csv` dan `hasil_scraping.xlsx` siap dibuka! 📊

> 💡 **Lihat contoh output lengkap** → [CONTOH_OUTPUT.md](CONTOH_OUTPUT.md)

---

## ⚠️ Peringatan Penting

**Scraping Google Maps melanggar Terms of Service Google** dan bisa diblokir atau dibatasi. 

- ✅ **Gunakan untuk belajar** dan keperluan pribadi dengan wajar
- ❌ **Jangan untuk produksi** atau scraping massal (ratusan/ribuan data sekaligus)
- 💡 **Alternatif resmi**: Untuk kebutuhan bisnis/skala besar, gunakan [Google Places API](https://developers.google.com/maps/documentation/places/web-service) (berbayar tapi legal)

---

## 📋 Prerequisites

Pastikan sudah terinstal:
- **Python 3.8+** ([Download di sini](https://www.python.org/downloads/))
- **pip** (biasanya sudah termasuk dalam instalasi Python)

---

## 🚀 Instalasi

### 1. Clone repository ini

```bash
git clone https://github.com/USERNAME/google-maps-scraper.git
cd google-maps-scraper
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install browser Chromium untuk Playwright

```bash
python -m playwright install chromium
```

> ℹ️ Perintah ini mengunduh Chromium (~150MB) hanya sekali. Playwright butuh ini untuk mengotomasi browser.

---

## 📖 Cara Menggunakan

### Format Dasar

```bash
python scraper.py "KATA_KUNCI_PENCARIAN" [OPSI]
```

### Contoh Penggunaan

```bash
# Hotel dengan harga
python scraper.py "Hotel di Bandung" --jumlah 20 --reviews 10

# Tempat wisata
python scraper.py "tempat wisata Yogyakarta" --jumlah 15 --reviews 5

# Restoran tanpa review
python scraper.py "restoran Padang Jakarta" --jumlah 10 --reviews 0 

# Custom nama file output
python scraper.py "penginapan Bali" --jumlah 25 --reviews 8 --output penginapan_bali
```

### Opsi yang Tersedia

| Opsi         | Fungsi                                        | Default           |
|--------------|-----------------------------------------------|-------------------|
| `--jumlah`   | Berapa banyak tempat yang diambil             | 20                |
| `--reviews`  | Berapa review per tempat (0 = tanpa review)   | 5                 |
| `--output`   | Nama file hasil (tanpa ekstensi)              | hasil_scraping    |
| `--headless` | Jalankan tanpa menampilkan jendela browser    | Tampil (off)      |

---

## 📊 Output

Setelah selesai, akan muncul 2 file:

- `hasil_scraping.csv` — bisa dibuka di Excel / Google Sheets
- `hasil_scraping.xlsx` — langsung format Excel

### Kolom Data yang Dihasilkan

| Kolom | Keterangan |
|-------|------------|
| `nama` | Nama tempat/hotel |
| `rating` | Rating bintang (contoh: 4.5) |
| `jumlah_ulasan` | Total ulasan |
| `kategori` | Jenis tempat (Hotel, Tujuan Wisata, Restoran, dll) |
| `alamat` | Alamat lengkap |
| `website` | Website resmi (jika ada) |
| `telepon` | Nomor telepon (jika ada) |
| `harga_terendah` | Harga termurah (khusus hotel) |
| `harga_tertinggi` | Harga termahal (khusus hotel) |
| `harga_rata_rata` | Rata-rata harga dari berbagai platform |
| `sumber_harga` | Detail harga per platform (Agoda, Traveloka, dll) |
| `reviews` | Kumpulan review (format: `[rating] penulis: teks`) |

### Contoh Data Review

```
[5 bintang] Andi: Hotel bagus, pelayanan ramah dan kamar bersih
[4 bintang] Budi: Lokasi strategis tapi parkir kurang luas
[5 bintang] Citra: Worth it! Breakfast enak dan view bagus
```

---

## 💡 Tips Penggunaan

1. **Jalankan tanpa `--headless` di awal** agar bisa melihat proses scraping dan memastikan tidak ada CAPTCHA
   ```bash
   python scraper.py "Hotel Jakarta" --jumlah 5
   ```

2. **Jangan scraping terlalu banyak sekaligus** — pecah jadi beberapa kali (misal 20-30 tempat per run) agar tidak diblokir Google

3. **Gunakan kata kunci spesifik** untuk hasil lebih relevan:
   - ✅ "Hotel murah di Bandung"
   - ✅ "Restoran Jepang Jakarta Selatan"
   - ❌ "Hotel" (terlalu umum)

4. **Kalau hasil kosong/error**, kemungkinan:
   - Google menampilkan CAPTCHA → tunggu beberapa saat lalu coba lagi
   - Kata kunci tidak ditemukan → coba kata kunci lain
   - Internet lambat → tingkatkan timeout di kode

---

## 🛠️ Troubleshooting

### Error: `playwright not found`
```bash
pip install playwright
python -m playwright install chromium
```

### Error: `openpyxl not found` (file .xlsx gagal dibuat)
```bash
pip install openpyxl
```

### Browser tidak muncul saat jalankan
Tambahkan flag tanpa `--headless`:
```bash
python scraper.py "kata kunci" --jumlah 10
```

### Hasil scraping kosong
- Coba kata kunci lain yang lebih spesifik
- Jalankan tanpa headless untuk lihat apakah ada CAPTCHA
- Tunggu beberapa menit sebelum coba lagi (mungkin terkena rate limit)

---

## 🤝 Kontribusi

Pull request dan issue sangat diterima! Kalau ada bug atau saran fitur baru, silakan buat issue di GitHub.

### Ide Fitur yang Bisa Ditambahkan
- [ ] Analisis sentimen otomatis untuk review (positif/negatif)
- [ ] Export ke format JSON
- [ ] Filter hasil berdasarkan rating minimum
- [ ] Scraping foto tempat
- [ ] Multi-threading untuk scraping lebih cepat

---

## 📄 Lisensi

MIT License - Bebas digunakan untuk keperluan pribadi dan komersial.

---

## 👨‍💻 Author

Dibuat untuk keperluan magang dan belajar web scraping.

**Disclaimer**: Gunakan dengan bijak. Scraping berlebihan dapat membebani server Google dan melanggar ToS mereka.
