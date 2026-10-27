"""
Google Maps Scraper
-------------------
Mengambil data tempat (wisata, penginapan, dll) dari Google Maps:
- Nama tempat
- Rating (bintang)
- Jumlah ulasan
- Kategori
- Alamat
- Beberapa komentar/review teratas

Hasil disimpan ke file CSV dan Excel.

CATATAN: Scraping Google Maps melanggar ToS Google dan bisa diblokir.
Gunakan dengan wajar (jeda antar aksi, jangan terlalu banyak sekaligus).
Untuk keperluan produksi/skala besar, gunakan Google Places API resmi.
"""

import argparse
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path

import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout


# ---------- Struktur data ----------

@dataclass
class Review:
    penulis: str = ""
    rating: str = ""
    teks: str = ""


@dataclass
class Tempat:
    nama: str = ""
    rating: str = ""
    jumlah_ulasan: str = ""
    kategori: str = ""
    alamat: str = ""
    website: str = ""
    telepon: str = ""
    harga_terendah: str = ""
    harga_tertinggi: str = ""
    harga_rata_rata: str = ""
    sumber_harga: str = ""
    reviews: list = field(default_factory=list)


# ---------- Fungsi bantu ----------

def scroll_hasil_pencarian(page, max_tempat):
    """Scroll panel hasil pencarian sampai jumlah tempat terkumpul cukup."""
    feed_selector = 'div[role="feed"]'
    try:
        page.wait_for_selector(feed_selector, timeout=15000)
    except PWTimeout:
        print("Panel hasil tidak ditemukan. Coba kata kunci lain.")
        return []

    tempat_links = []
    percobaan_mentok = 0

    while len(tempat_links) < max_tempat and percobaan_mentok < 5:
        kartu = page.query_selector_all('a[href*="/maps/place/"]')
        href_baru = []
        for k in kartu:
            href = k.get_attribute("href")
            if href and href not in tempat_links:
                href_baru.append(href)

        sebelum = len(tempat_links)
        tempat_links.extend(href_baru)
        tempat_links = list(dict.fromkeys(tempat_links))  # buang duplikat, jaga urutan

        if len(tempat_links) == sebelum:
            percobaan_mentok += 1
        else:
            percobaan_mentok = 0

        # scroll ke bawah di dalam panel feed
        page.eval_on_selector(feed_selector, "el => el.scrollBy(0, 1200)")
        time.sleep(1.5)

    return tempat_links[:max_tempat]


def ambil_teks(page, selector):
    """Ambil teks dari elemen pertama yang cocok, aman kalau tidak ada."""
    el = page.query_selector(selector)
    if el:
        return (el.inner_text() or "").strip()
    return ""


def ambil_atribut(page, selector, atribut):
    el = page.query_selector(selector)
    if el:
        return (el.get_attribute(atribut) or "").strip()
    return ""


def scrape_harga(page):
    """Klik tab Harga dan ambil daftar harga dari berbagai platform."""
    harga_list = []
    sumber_list = []

    try:
        # Cari tab Harga
        tab_harga = None
        for t in page.query_selector_all('button[role="tab"]'):
            label = t.get_attribute('aria-label') or ''
            if 'harga' in label.lower() or 'price' in label.lower():
                tab_harga = t
                break

        if not tab_harga:
            return {}, ""   # Tempat ini tidak punya tab harga

        tab_harga.click()
        time.sleep(3)

        # Ambil semua baris platform+harga (div.fontLabelMedium berisi harga bersih)
        kartu = page.query_selector_all('div.Vyt0me')
        for kartu_item in kartu:
            teks = (kartu_item.inner_text() or '').replace('\xa0', '').strip()
            baris = [b.strip() for b in teks.split('\n') if b.strip()]
            if len(baris) < 2:
                continue
            platform = baris[0]
            # Cari nilai Rp
            harga_el = kartu_item.query_selector('div.fontLabelMedium')
            if not harga_el:
                continue
            harga_txt = (harga_el.inner_text() or '').replace('\xa0', '').replace('Rp', '').replace('.', '').replace(',', '').strip()
            try:
                angka = int(''.join(filter(str.isdigit, harga_txt)))
                harga_list.append(angka)
                sumber_list.append(f"{platform}: Rp {angka:,}")
            except ValueError:
                continue

    except Exception:
        pass

    if not harga_list:
        return {}, ""

    hasil = {
        "harga_terendah": f"Rp {min(harga_list):,}",
        "harga_tertinggi": f"Rp {max(harga_list):,}",
        "harga_rata_rata": f"Rp {int(sum(harga_list)/len(harga_list)):,}",
    }
    sumber = " | ".join(sumber_list[:5])  # Tampilkan max 5 sumber
    return hasil, sumber


def scrape_reviews(page, max_reviews):
    """Buka tab Ulasan dan ambil beberapa review teratas."""
    reviews = []

    # Klik tab "Ulasan"/"Reviews" (jangan tertukar dengan tombol "Tulis ulasan").
    try:
        tab = None
        for sel in (
            'button[role="tab"][aria-label^="Ulasan"]',
            'button[role="tab"][aria-label^="Reviews"]',
            'button[role="tab"][aria-label*="Ulasan"]',
            'button[role="tab"][aria-label*="Reviews"]',
        ):
            kandidat = page.query_selector(sel)
            if kandidat and "Tulis" not in (kandidat.get_attribute("aria-label") or ""):
                tab = kandidat
                break
        if not tab:
            return reviews
        tab.click()
        time.sleep(3)
    except Exception:
        return reviews

    # Scroll panel review agar lebih banyak kartu termuat.
    for _ in range(5):
        kartu_review = page.query_selector_all('div[data-review-id]')
        if len(kartu_review) >= max_reviews:
            break
        if kartu_review:
            try:
                kartu_review[-1].scroll_into_view_if_needed()
            except Exception:
                pass
        page.mouse.wheel(0, 3000)
        time.sleep(1.5)

    kartu_review = page.query_selector_all('div[data-review-id]')
    id_terlihat = set()
    for kr in kartu_review:
        if len(reviews) >= max_reviews:
            break
        try:
            # Lewati kartu duplikat (review yang sama kadang muncul 2x)
            rid = kr.get_attribute("data-review-id") or ""
            if rid and rid in id_terlihat:
                continue
            id_terlihat.add(rid)

            # Klik "Lihat lainnya"/"More" agar teks penuh termuat
            more = kr.query_selector('button[aria-label="Lihat lainnya"], button[aria-label="See more"]')
            if more:
                try:
                    more.click()
                    time.sleep(0.3)
                except Exception:
                    pass

            # Nama penulis
            penulis_el = kr.query_selector('div.d4r55, button[class*="al6Kxe"] div')
            penulis = penulis_el.inner_text().strip() if penulis_el else ""

            # Rating bintang review (span.kvMYJc dgn aria-label "4 bintang")
            rating = ""
            rating_el = kr.query_selector('span.kvMYJc[aria-label], span[role="img"][aria-label*="bintang"], span[role="img"][aria-label*="star"]')
            if rating_el:
                rating = (rating_el.get_attribute("aria-label") or "").strip()

            # Teks ulasan
            teks_el = kr.query_selector('span[class*="wiI7pd"]')
            teks = teks_el.inner_text().strip() if teks_el else ""
            teks = " ".join(teks.split())

            reviews.append(Review(penulis=penulis, rating=rating, teks=teks))
        except Exception:
            continue

    return reviews


def scrape_detail_tempat(page, url, max_reviews):
    """Buka halaman detail satu tempat dan ambil informasinya."""
    page.goto(url, timeout=30000)
    time.sleep(3)

    tempat = Tempat()
    tempat.nama = ambil_teks(page, "h1")
    tempat.rating = ambil_teks(page, 'div.F7nice span[aria-hidden="true"]')

    # Jumlah ulasan: coba beberapa pola selector yang berbeda
    jumlah = ambil_atribut(page, 'div.F7nice span[aria-label*="ulasan"]', "aria-label")
    if not jumlah:
        jumlah = ambil_atribut(page, 'div.F7nice span[aria-label*="reviews"]', "aria-label")
    if not jumlah:
        # Pola "(1.234)" langsung sebagai teks
        jumlah = ambil_teks(page, 'div.F7nice span:has-text("(")')
    if not jumlah:
        jumlah = ambil_atribut(page, 'button[aria-label*="ulasan"]', "aria-label")
    # Ambil hanya angkanya
    import re
    angka = re.findall(r"[\d.,]+", jumlah)
    tempat.jumlah_ulasan = angka[0] if angka else jumlah
    tempat.kategori = ambil_teks(page, 'button[jsaction*="category"]')
    tempat.alamat = ambil_atribut(page, 'button[data-item-id="address"]', "aria-label")
    tempat.website = ambil_atribut(page, 'a[data-item-id="authority"]', "href")
    tempat.telepon = ambil_atribut(page, 'button[data-item-id^="phone"]', "aria-label")

    # Bersihkan prefiks aria-label ("Alamat: ", "Nomor telepon: ")
    for atr in ("alamat", "telepon"):
        val = getattr(tempat, atr)
        if ":" in val:
            setattr(tempat, atr, val.split(":", 1)[1].strip())

    # Ambil harga (hanya muncul di hotel/penginapan)
    harga, sumber = scrape_harga(page)
    if harga:
        tempat.harga_terendah = harga.get("harga_terendah", "")
        tempat.harga_tertinggi = harga.get("harga_tertinggi", "")
        tempat.harga_rata_rata = harga.get("harga_rata_rata", "")
        tempat.sumber_harga = sumber

    if max_reviews > 0:
        tempat.reviews = scrape_reviews(page, max_reviews)

    return tempat


def simpan_hasil(daftar_tempat, nama_file):
    """Simpan ke CSV dan Excel. Satu baris per tempat + kolom review digabung."""
    baris = []
    for t in daftar_tempat:
        data = asdict(t)
        reviews = data.pop("reviews")
        # Gabung review jadi satu kolom teks yang mudah dibaca
        data["reviews"] = " ||| ".join(
            f"[{r['rating']}] {r['penulis']}: {r['teks']}" for r in reviews
        )
        baris.append(data)

    df = pd.DataFrame(baris)

    csv_path = f"{nama_file}.csv"
    xlsx_path = f"{nama_file}.xlsx"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    try:
        df.to_excel(xlsx_path, index=False)
        print(f"Tersimpan: {csv_path} dan {xlsx_path}")
    except Exception:
        print(f"Tersimpan: {csv_path} (Excel gagal, pastikan 'openpyxl' terinstal)")

    return df


# ---------- Program utama ----------

def main():
    parser = argparse.ArgumentParser(description="Scraper Google Maps sederhana.")
    parser.add_argument("kata_kunci", help='Contoh: "tempat wisata Bandung"')
    parser.add_argument("--jumlah", type=int, default=20, help="Jumlah tempat (default 20)")
    parser.add_argument("--reviews", type=int, default=5, help="Jumlah review per tempat (default 5, 0 = tanpa review)")
    parser.add_argument("--output", default="hasil_scraping", help="Nama file output (tanpa ekstensi)")
    parser.add_argument("--headless", action="store_true", help="Jalankan tanpa menampilkan browser")
    args = parser.parse_args()

    output_path = str(Path(__file__).parent / args.output)

    print(f"Mencari: {args.kata_kunci}")
    print(f"Target: {args.jumlah} tempat, {args.reviews} review per tempat\n")

    daftar_tempat = []

    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        context = browser.new_context(
            user_agent=user_agent,
            locale="id-ID",
            viewport={"width": 1366, "height": 900},
        )
        page = context.new_page()

        # Buka Google Maps dengan kata kunci
        search_url = f"https://www.google.com/maps/search/{args.kata_kunci.replace(' ', '+')}"
        page.goto(search_url, timeout=30000)
        time.sleep(4)

        # Setujui cookie jika muncul (versi EU)
        try:
            btn = page.query_selector('button[aria-label*="Setuju"], button[aria-label*="Accept all"]')
            if btn:
                btn.click()
                time.sleep(2)
        except Exception:
            pass

        links = scroll_hasil_pencarian(page, args.jumlah)
        print(f"Ditemukan {len(links)} tempat. Mulai mengambil detail...\n")

        for i, url in enumerate(links, 1):
            try:
                tempat = scrape_detail_tempat(page, url, args.reviews)
                daftar_tempat.append(tempat)
                harga_info = f" | {tempat.harga_terendah} - {tempat.harga_tertinggi}" if tempat.harga_terendah else ""
                print(f"[{i}/{len(links)}] {tempat.nama} - {tempat.rating} ({tempat.jumlah_ulasan}){harga_info}")
            except Exception as e:
                print(f"[{i}/{len(links)}] Gagal: {e}")
            time.sleep(1)

        browser.close()

    if daftar_tempat:
        simpan_hasil(daftar_tempat, output_path)
        print(f"\nSelesai! Total {len(daftar_tempat)} tempat tersimpan.")
    else:
        print("Tidak ada data yang berhasil diambil.")


if __name__ == "__main__":
    main()
