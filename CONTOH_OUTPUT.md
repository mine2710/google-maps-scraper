# Contoh Output Scraping

## Terminal Output

```
Mencari: Hotel di Lampung
Target: 10 tempat, 5 review per tempat

Ditemukan 10 tempat. Mulai mengambil detail...

[1/10] Hotel Golden Tulip Springhill Lampung - 4,9 (11.818) | Rp 520,880 - Rp 850,048
[2/10] Aston Lampung City Hotel - 4,3 (7.359) | Rp 363,520 - Rp 895,853
[3/10] Hotel Horison Lampung - 4,5 (9.134) | Rp 468,832 - Rp 898,752
[4/10] Yunna Hotel Lampung - 4,3 (2.299) | Rp 270,912 - Rp 787,840
[5/10] Hotel Arte Bandar Lampung - 4,3 (4.642) | Rp 411,776 - Rp 567,201
[6/10] Novotel Lampung - 4,7 (12.844) | Rp 1,046,522 - Rp 1,124,992
[7/10] Amalia Hotel - 4,4 (4.063) | Rp 399,648 - Rp 505,072
[8/10] Swiss-Belhotel Lampung - 4,7 (11.954) | Rp 653,984 - Rp 829,984
[9/10] Hotel Santika Premiere Lampung - 4,8 (3.038) | Rp 721,958 - Rp 850,900
[10/10] POP! Hotel Tanjung Karang - Lampung - 4,2 (5.574) | Rp 269,068 - Rp 298,971

Tersimpan: hotel_lampung.csv dan hotel_lampung.xlsx
Selesai! Total 10 tempat tersimpan.
```

## File Excel Output

| nama | rating | jumlah_ulasan | kategori | alamat | harga_terendah | harga_rata_rata | reviews |
|------|--------|---------------|----------|--------|----------------|-----------------|---------|
| Hotel Golden Tulip Springhill | 4,9 | 11.818 | Hotel | Jl. Z.A. Pagar Alam No.92... | Rp 520,880 | Rp 610,234 | [5 bintang] Andi: Hotelnya bagus... |
| POP! Hotel Tanjung Karang | 4,2 | 5.574 | Hotel | Jl. Kartini No.11... | Rp 269,068 | Rp 283,450 | [4 bintang] Budi: Murah dan bersih... |
| Novotel Lampung | 4,7 | 12.844 | Hotel | Jl. Wolter Monginsidi No.175 | Rp 1,046,522 | Rp 1,085,450 | [5 bintang] Citra: Breakfast enak... |

## Contoh Review di CSV

```
reviews
[5 bintang] Andi Wijaya: Hotel yang sangat bagus dengan pelayanan ramah. Kamar bersih dan fasilitas lengkap. ||| [4 bintang] Budi Santoso: Lokasi strategis di pusat kota, dekat dengan mall. Hanya saja parkir agak sempit saat weekend. ||| [5 bintang] Citra Dewi: Worth it banget! Breakfast buffet-nya enak dan bervariasi. View dari kamar juga bagus.
```

## Analisis Data

Dari data yang didapat, Anda bisa:

### 1. Urutkan berdasarkan rating tertinggi
```python
import pandas as pd
df = pd.read_csv('hotel_lampung.csv')
df_sorted = df.sort_values('rating', ascending=False)
print(df_sorted[['nama', 'rating', 'jumlah_ulasan']])
```

### 2. Filter hotel berdasarkan harga
```python
# Konversi harga ke angka
df['harga_min'] = df['harga_terendah'].str.replace('Rp ', '').str.replace(',', '').astype(float)
hotel_murah = df[df['harga_min'] < 500000]
print(hotel_murah[['nama', 'harga_terendah', 'rating']])
```

### 3. Analisis sentimen review (manual)
Baca kolom `reviews` untuk menilai apakah komentar:
- ✅ **Positif**: "bagus", "enak", "bersih", "recommended", "worth it"
- ❌ **Negatif**: "kotor", "jorok", "buruk", "kecewa", "tidak recommend"
