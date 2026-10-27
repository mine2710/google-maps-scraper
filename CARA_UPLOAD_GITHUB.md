# 📤 Cara Upload ke GitHub

## Langkah 1: Buat Repository Baru di GitHub

1. Buka [github.com](https://github.com) dan login
2. Klik tombol **+** di pojok kanan atas → **New repository**
3. Isi form:
   - **Repository name**: `google-maps-scraper` (atau nama lain yang Anda suka)
   - **Description**: `Scraper Google Maps untuk ambil data hotel, wisata, restoran dengan harga & review`
   - **Public** ☑️ (agar orang lain bisa lihat dan clone)
   - **JANGAN centang** "Add a README file" (sudah ada di lokal)
4. Klik **Create repository**

## Langkah 2: Push dari Komputer Anda

Setelah repository dibuat, GitHub akan menampilkan instruksi. Jalankan di terminal VSCode (atau PowerShell) di folder `D:\Kerja\Projek\Sraping`:

```bash
# Tambahkan remote GitHub (ganti USERNAME dengan username GitHub Anda)
git remote add origin https://github.com/USERNAME/google-maps-scraper.git

# Push ke GitHub
git branch -M main
git push -u origin main
```

### Jika diminta login:
- **Username**: username GitHub Anda
- **Password**: gunakan **Personal Access Token** (bukan password biasa)

#### Cara buat Personal Access Token:
1. GitHub → Settings (profil) → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token → centang `repo` → Generate
3. Copy token yang muncul (hanya muncul sekali!)
4. Paste sebagai password saat push

---

## Langkah 3: Verifikasi Upload Berhasil

Buka `https://github.com/USERNAME/google-maps-scraper` di browser — semua file sudah muncul ✅

---

## ✅ Selesai! Orang Lain Bisa Clone Repository Anda

Sekarang siapa saja bisa download dan jalankan scraper Anda dengan cara:

```bash
# Clone repository
git clone https://github.com/USERNAME/google-maps-scraper.git
cd google-maps-scraper

# Install dependencies
pip install -r requirements.txt
python -m playwright install chromium

# Jalankan
python scraper.py "Hotel di Bandung" --jumlah 10 --reviews 5
```

---

## 🔄 Update Repository (Jika Ada Perubahan)

Kalau nanti Anda edit kode dan mau update di GitHub:

```bash
git add .
git commit -m "Deskripsi perubahan yang dilakukan"
git push
```

---

## 📌 Tips Tambahan

### Buat file `.github/workflows/` untuk GitHub Actions (opsional)
Bisa buat automated testing atau scheduled scraping otomatis

### Tambahkan badge di README
```markdown
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
```

### Star repository sendiri ⭐
Biar terlihat lebih populer dan orang lain lebih percaya untuk pakai 😄
