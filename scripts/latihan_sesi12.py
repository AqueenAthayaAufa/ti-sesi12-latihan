# LANGKAH 0 · Menyiapkan alat (import) dan alamat berkas
# "import" = meminjam kotak perkakas yang sudah dibuat orang lain.
# pandas : perkakas utama mengolah tabel (seperti Excel versi kode)
# sqlalchemy + psycopg2 : jembatan Python ke PostgreSQL
# Path : menulis alamat folder/berkas yang aman di Windows & Mac
# datetime: mengolah tanggal
# getpass : meminta password tanpa menampilkannya di layar
from datetime import datetime
from getpass import getpass
from pathlib import Path
import pandas as pd
from sqlalchemy import URL, Date, create_engine, text
# Alamat dihitung dari lokasi skrip ini, sehingga skrip tetap jalan
# walaupun dijalankan dengan tombol Run ( ) di VS Code.
# __file__ = berkas skrip ini; .parent = folder di atasnya.
FOLDER_REPO = Path(__file__).resolve().parent.parent
BERKAS_MENTAH = FOLDER_REPO / "data" / "daftar_arsip_fakultas.csv"
FOLDER_OUTPUT = FOLDER_REPO / "output"
FOLDER_OUTPUT.mkdir(exist_ok=True) # buat folder bila belum ada
# Tanggal acuan penilaian retensi: akhir tahun 2026, saat unit arsip
# biasanya menyusun daftar usul musnah. Dibuat tetap (bukan "hari
# ini") agar hasil semua mahasiswa sama dan bisa dicocokkan.
TANGGAL_ACUAN = pd.Timestamp("2026-12-31")

# LANGKAH 1 · Membaca CSV dan mengenali isinya
# dtype=str : baca semua kolom sebagai teks dulu, supaya tidak ada
# nilai yang "diubah diam-diam" oleh pandas.
# keep_default_na=False : sel kosong dibaca sebagai "" (teks kosong).
df = pd.read_csv(BERKAS_MENTAH, dtype=str, keep_default_na=False)
print("=== LANGKAH 1 · Kenali data ===")
print("Jumlah baris, kolom :", df.shape) # (baris, kolom)
print("Nama kolom :", list(df.columns))
print(df.head()) # 5 baris pertama
# LANGKAH 2 · Merapikan teks: buang spasi berlebih
# Spasi di awal/akhir tidak terlihat, tetapi membuat "Akademik" dan
# " Akademik" dianggap dua nilai berbeda oleh komputer.
# for ... in ... : ulangi perintah yang sama untuk setiap kolom.
for kolom in df.columns:
    df[kolom] = df[kolom].str.strip() # strip = buang spasi tepi
# Ganti spasi ganda di tengah judul menjadi satu spasi.
df["judul"] = df["judul"].str.replace(r"\s+", " ", regex=True)