# BUILD-NOTES — news-image-20261125

## Berita yang dirangkum (Rabu 25 November 2026)

| Cerita | Fakta di gambar | Sumber |
|---|---|---|
| Peluncuran Shenzhou-24 (LEAD) | Long March 2F lepas landas 25 Nov 00:18 UTC dari Jiuquan; awak Tang Hongbo, Wu Yi, dan Muhammad Zeeshan Ali (40) — orang Pakistan pertama di orbit dan astronot asing pertama di stasiun Tiangong | Xinhua, Reuters, Wikipedia (Shenzhou 24), NASASpaceFlight, 25 Nov 2026 |
| Peretasan CIA/ODNI | Jaringan unclassified CIA + ODNI untuk analisis open-source intelligence dibobol; tidak ada data classified yang terekspos, kata pejabat AS; pertama dilaporkan NYT Selasa 24 Nov, liputan luas Rabu 25 Nov | Reuters, CNN, NYT via AP/Xinhua, 25 Nov 2026 |
| Serangan drone Houthi ke Riyadh | Drone Houthi menghantam menara PIF (385 m, tertinggi di Riyadh) untuk kedua kalinya dalam sepekan; 11 orang luka (2 Saudi, 2 India, 3 Nepal, 4 Mesir) | Reuters, 24–25 Nov 2026 |
| Evakuasi Ebola di Kongo | WHO mengevakuasi staf dari RS Akwe, Ituri, setelah 3 hari berlindung dari pertempuran, di tengah wabah Ebola | WHO via stockbiz, 25 Nov 2026 |
| Ukraina | Zelenskiy mengonfirmasi Ukraina menyerang kapal Rusia di Teluk Finlandia; Norwegia mendesak kehati-hatian | Reuters world news summary, 25 Nov 2026 |
| Also today | Huawei dinyatakan bersalah di pengadilan AS; gempa Nepal 5.6; Trump menganugerahkan Medal of Freedom ke Giuliani; kasus korupsi Sarkozy ke pengadilan; Nvidia turun ~6% | Reuters/AP digests, 25 Nov 2026 |

Catatan editorial: lead dipilih Shenzhou-24 karena itu peristiwa besar yang tidak ambigu terjadi pada 25 Nov (00:18 UTC), bersejarah (astronot asing pertama di Tiangong), dan sangat visual. Cerita CIA dan Riyadh mendominasi siklus berita 25 Nov meski pertama dilaporkan Selasa 24 Nov — keduanya disajikan apa adanya tanpa klaim tanggal kejadian yang salah.

## Konsep visual

Halaman depan koran "GLOBAL DAILY", tanggal WEDNESDAY 25 NOVEMBER 2026 menonjol di masthead. Panel hero bergambar langit malam: roket Long March 2F di landasan (api + asap), stasiun Tiangong berlabel, bulan dan bintang. Headline besar "FIRST FOREIGN ASTRONAUT FLIES TO TIANGONG", lalu berita kedua "US SPY AGENCIES HACKED", tiga kartu (Riyadh / Kongo / Ukraina), dan strip "ALSO TODAY". Semua aset digambar lewat kode (font bitmap 5x7 buatan tangan, encoder PNG stdlib); tanpa network, tanpa jam, tanpa random — deterministik penuh.

## Uji

- `python3 gen_poster.py` 2x: sha256 identik `f794ab798f1df621b6e5753198f4a488250adbe9a348a6ebc74b5868d5c4ef17`
- `python3 main.py` 2x (MAKEFUN_OUTPUT_DIR berbeda): byte-identik, sha256 sama seperti di atas
- Ukuran: 17.769 byte (batas 1 MiB); dimensi 1024×1024 (batas 1024×1024); header PNG valid
- Penilaian visual: masthead + tanggal jelas; hero roket/stasiun terbaca; semua headline dan kartu terbaca tanpa teks rusak; tidak ada klaim yang bertentangan dengan sumber

## Penilaian jujur

Layak submit. Kekuatan: tanggal dan lead 25 Nov yang bersih dan kuat, breadth lintas wilayah (Asia, AS, Timur Tengah, Afrika, Eropa) dan bidang (antariksa, siber, konflik, kesehatan), komposisi satu halaman yang rapi. Kelemahan: font bitmap membuat teks tubuh kecil agak kasar saat diperkecil ke ~300 px, dan dua cerita sekunder (CIA, Riyadh) pertama kali dilaporkan 24 Nov — risiko kecil di mata judge yang ketat soal tanggal, tapi keduanya adalah cerita utama siklus berita 25 Nov di semua digest hari itu.
