# Modul KKA: Uninformed dan Informed Search

## Isi modul

- [Modul_Pembelajaran_Uninformed_KKA.ipynb](Modul_Pembelajaran_Uninformed_KKA.ipynb): DFS, BFS, UCS, DLS, IDS, dan pencarian dua arah.
- [Modul_Pembelajaran_Informed_KKA.ipynb](Modul_Pembelajaran_Informed_KKA.ipynb): GBFS, A*, IDA*, RBFS, heuristik, dan frontier terbatas.

## Susunan notebook

Semua impor berada pada sel persiapan. Algoritma ditulis langsung pada bagian
materinya, diikuti contoh pemanggilan dan latihan TODO. Fungsi pembanding dengan
penghitung juga ditampilkan pada bagian eksperimen.

Folder `data/` menyediakan data contoh, gambar, dan visualisasi. Untuk membaca
algoritma, ikuti definisi fungsi di notebook.

## Menjalankan di komputer

Gunakan Python 3.11 atau lebih baru. Buka terminal pada folder modul, lalu jalankan:

```console
python -m pip install -r requirements.txt
python -m jupyter lab
```

Buka notebook dan pilih kernel Python yang telah dipasangi pustaka tersebut.
Pertahankan folder `data/` pada lokasi yang sama dengan notebook.

## Menjalankan di Google Colab

1. Buka notebook di Colab.
2. Jalankan `%pip install numpy matplotlib pillow` pada sel baru.
3. Unggah ZIP paket modul dan ekstrak melalui sel berikut. Pilih berkas ZIP saat diminta.

```python
from google.colab import files
from zipfile import ZipFile

uploaded = files.upload()
with ZipFile(next(iter(uploaded))) as archive:
    archive.extractall('/content')
```

Kemudian pindah ke folder hasil ekstraksi:

```python
%cd /content/modul-uninformed-informed-search
```

Jalankan sel persiapan pada notebook sebelum melanjutkan ke materi.

## Mengerjakan latihan

- Isi nama dan NRP pada awal notebook.
- Jalankan sel secara berurutan. Bagian tugas diberi komentar `# TODO [kode]` dan penanda `________("kode")`.
- Ganti seluruh pemanggilan penanda tersebut dengan jawaban sesuai komentar. Untuk fungsi utuh, isi blok `__ MULAI JAWABAN __` sampai `__ AKHIR JAWABAN __` dan hapus baris penandanya.
- Sel bertanda PENGUJIAN dan fungsi penanda latihan tidak perlu diubah.
- Jalankan kembali definisi fungsi dan sel pengujian setelah mengubah kode.
- Jika muncul **BELUM DIISI**, cari kode TODO yang disebut pada pesan tersebut. Jika `assert` gagal, periksa hasil dan implementasinya.
- Jawab pertanyaan dan sertakan hasil percobaan pada latihan lanjutan.
- Sebelum dikumpulkan, simpan notebook dan jalankan **Restart Kernel & Run All** untuk memeriksa hasil dari awal.

## Referensi

Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, edisi ke-4,
Bab 3. [Daftar isi](https://aima.cs.berkeley.edu/contents.html).
