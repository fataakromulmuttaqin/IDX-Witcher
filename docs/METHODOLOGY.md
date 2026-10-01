# Metodologi IDX Witcher

Halaman ini menjelaskan sumber data, cara membaca angka, indikator, aturan, keterbatasan, dan disclaimer.

## Sumber data dan jadwal

- Harga dan fundamental berasal dari Yahoo Finance melalui pustaka tidak resmi, sehingga dapat terlambat, hilang, atau keliru.
- Data bersifat end-of-day: diperbarui sekali sehari sekitar pukul 17:00 WIB pada hari bursa.
- Fundamental diperbarui mingguan dan mengikuti laporan keuangan yang tersedia di sumber.

## Cara membaca angka

- **bank**: rasio tidak berlaku untuk bank, asuransi, dan perusahaan pembiayaan.
- **no data**: tidak ada laporan keuangan di sumber data.
- **loss**: laba 12 bulan terakhir negatif, sehingga rasio tidak bermakna.
- **n/a**: tidak dilaporkan atau dibuang oleh pemeriksaan kualitas data.
- TTM = jumlah 4 kuartal terakhir. Pertumbuhan pendapatan dan laba dibandingkan kuartal yang sama tahun lalu.
- Market cap = harga penutupan x jumlah saham beredar.
- 1 lot = 100 lembar.

## Indikator

- Return 1D, 1M, 3M, 1Y dihitung dari harga penutupan 1, 21, 63, dan 252 sesi sebelumnya; YTD terhadap penutupan terakhir tahun lalu.
- SMA = rata-rata harga penutupan 20, 50, 150, atau 200 sesi.
- RS Rating (1-99) = peringkat persentil kekuatan harga relatif.

## Disclaimer

IDX Witcher adalah alat riset dan edukasi. Hasil daftar dan screen adalah filter mekanis, bukan rekomendasi membeli atau menjual efek apa pun.
