# 🚀 Dokumentasi Belajar: Membuat Animasi AI dengan Claude Code, Gemini, dan Antigravity

> **Catatan Belajar & Blueprint Produksi Animasi 2D / Video-as-Code Berbasis AI**  
> *Tanggal Rilis: 18 November 2026*  
> **Penulis:** Bagaskara Amukti Palapa — Teknik Informatika, Universitas Bina Darma, Palembang  
> **Instagram:** [@bgskara_ap](https://www.instagram.com/bgskara_ap) · **GitHub:** [@BagaskaraAP-Dev](https://github.com/BagaskaraAP-Dev)  
> **Live Web Documentation:** [https://bagaskaraap-dev.github.io/Belajar-Animasi-AI/](https://bagaskaraap-dev.github.io/Belajar-Animasi-AI/)

---

## 📌 Ringkasan Proyek

Dokumentasi ini merangkum metodologi, arsitektur teknis, dan pengalaman langsung saya dalam memproduksi **animasi berbasis kecerdasan buatan (AI)** tanpa software editing video konvensional. Seluruh animasi, pergerakan karakter, transisi, hingga efek audio dan musik latar dibangun melalui **sinergi tiga pilar AI**:

1. **Google Gemini:** *The Creative Vision & Multimodal Director* — Konseptualisasi narasi, perancangan storyboard, menjaga konsistensi visual (*character & room anchoring*), serta rekayasa prompt B-roll.
2. **Claude Code:** *The Algorithmic Animator & Math Engine* — Penulisan kode prosedural Python (`pycairo`), kinematika terbalik (*Inverse Kinematics* 2-tulang), sintesis audio matematis murni (`NumPy`), serta pipeline rendering raw-frame ke `FFmpeg`.
3. **Google Antigravity:** *The Autonomous Orchestrator & Modern Video-as-Code Engine* — Eksekusi agentic mandiri (*vibe coding*), manajemen *timeline* terprogram (Remotion React), sinkronisasi ucapan presisi milidetik (*WordBoundary cue points*), serta *guard* area aman platform (*Instagram Safe Zone*).

> **Catatan Deployment (18 November 2026):**  
> Sesuai arsitektur *lightweight documentation repository*, file video render final (`.mp4`) berukuran besar telah dibersihkan/dihapus pasca-deployment agar repositori tetap gesit, bersih, dan berfokus pada fondasi instruksi, logika matematika, serta reproduktibilitas kode.

---

## 🏛️ Sinergi Tripartit AI (Framework Kerja)

```
┌────────────────────────────────────────────────────────────────────────┐
│                        1. GOOGLE GEMINI                                │
│          - Naskah Suara (5 Menit / 42 Detik Reels)                     │
│          - Konsistensi Karakter & Anchoring Multimodal                 │
│          - Prompt Storyboard & Desain Visual Referensi                 │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        2. CLAUDE CODE                                  │
│          - Rig Karakter: Inverse Kinematics (Hukum Cosinus)            │
│          - Vector Drawing Prosedural (PyCairo: Tiap Frame f(t))        │
│          - Sintesis Musik & SFX Prosedural (NumPy Arrays)              │
│          - Fast Parallel BGRA Piping ke FFmpeg Demuxer                 │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     3. GOOGLE ANTIGRAVITY                              │
│          - Multi-Agent Orchestration & CLI Automation                  │
│          - Remotion Video-as-Code (React Keyframes & Springs)          │
│          - Whisper & Edge-TTS Timestamp Alignment (Cue Points)         │
│          - Safe-Zone Validation (Reels 9:16 vs Feed 4:5) & Deploy      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Pembagian Peran & Komparasi Teknologi

| Parameter | Google Gemini | Claude Code | Google Antigravity |
|---|---|---|---|
| **Fokus Utama** | Ideasi kreatif, storyboard, konsistensi visual | Logika grafis matematika, kode prosedural | Orkestrasi sub-agent, video-as-code |
| **Keluaran** | Prompt, naskah narasi, acuan visual | Skrip Python (`pycairo`, `numpy`, `ffmpeg`) | Proyek Remotion, otomatisasi alur |
| **Gaya Animasi** | Generasi gambar konsisten & klip transisi | Vektor 2D dinamis, kartun matematis murni | Komponen React animasi, motion grafis |
| **Audio** | Naskah & panduan intonasi | Sintesis gelombang sinus, akor, low-pass filter | Sinkronisasi timestamp suara (*cue points*) |
| **Keunggulan** | Memahami konteks visual multimodal | Presisi frame-by-frame tanpa batas software | Eksekusi otonom, pipeline modular |

---

## 💡 Bedah Fitur & Logika Teknis Utama

### 1. Animasi Adalah Fungsi Waktu Murni: $Frame = f(t)$
Dalam proyek ini, tidak ada file gambar bitmap eksternal. Semua elemen—mulai dari Jembatan Ampera, meja ngoding, monitor laptop, pion catur, hingga kembang api—adalah path vektor `pycairo`.

Tiap adegan didefinisikan sebagai fungsi yang menerima variabel waktu detik $t$:
```python
def frame(ctx, t):
    CLOCK[0] = t
    scene_at(ctx, t)   # Render adegan sesuai timeline
    wipe(ctx, t)       # Efek transisi antar adegan
```
**Keuntungan:**
- **Zero Memory Bottleneck:** Setiap frame dihitung secara instan tanpa menyimpan cache PNG di hard drive.
- **Render Paralel Bebas Konflik:** Frame adegan 1 tidak bergantung pada adegan 2, sehingga dapat dibagi rata ke banyak core CPU menggunakan `xargs -P`.

---

### 2. Rigging Karakter dengan Inverse Kinematics (IK 2-Tulang)
Menggerakkan sendi karakter kartun satu per satu (Forward Kinematics) memakan waktu lama dan sering terlihat kaku. Dengan bantuan Claude Code, kami mengimplementasikan **Inverse Kinematics (IK)** analitik berbasis Hukum Cosinus:

```python
def ik(sh, tg, l1, l2, elbow='down'):
    """
    sh: Posisi pangkal bahu (x, y)
    tg: Titik target sentuhan tangan (x, y)
    l1: Panjang lengan atas
    l2: Panjang lengan bawah
    """
    dx, dy = tg[0] - sh[0], tg[1] - sh[1]
    d = math.hypot(dx, dy)
    d = clamp(d, abs(l1 - l2) + 1, l1 + l2 - 0.5)
    phi = ang_of(dx, dy)
    
    # Hukum Cosinus
    c = clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1, 1)
    al = math.degrees(math.acos(c))
    
    best = None
    for a1 in (phi + al, phi - al):
        ex, ey = sh[0] + l1 * vdir(a1)[0], sh[1] + l1 * vdir(a1)[1]
        a2 = ang_of(tg[0] - ex, tg[1] - ey)
        key = ey if elbow == 'down' else -ey
        if best is None or key > best[0]:
            best = (key, a1, a2)
    return best[1], best[2]  # Sudut bahu dan siku
```
Dengan IK ini, kita cukup menentukan posisi target: *mengetik di keyboard*, *mengangkat bidak catur*, *memegang stang motor*, atau *memakan popcorn*.

---

### 3. Musik Latar & Efek Suara Prosedural (NumPy)
Daripada bergantung pada audio berhak cipta, audio latar dibuat dari nol menggunakan array `numpy`:
- **Progresi Akor Lo-Fi:** Fmaj7 – G7 – Em7 – Am7 pada tempo 100 BPM.
- **Synthesized Percussion:** Kick drum (pitch drop eksponensial), Snare (filtered Gaussian noise + resonansi 190 Hz), dan Hi-hat.
- **Automatic Audio Ducking:** Musik otomatis mengecil saat voiceover aktif dengan menghitung *rolling envelope*:
```python
e = np.abs(vo)
k = int(0.15 * SR)
e = np.convolve(e, np.ones(k) / k, mode='same')
e = np.clip(e / 0.08, 0, 1)

# Ducking: musik direduksi hingga 50% saat narator berbicara
out = (out / np.max(np.abs(out))) * 0.6 * (1 - 0.5 * e) + (vo * 0.85)
```
- **Loudness Normalization:** Disesuaikan ke standar Instagram Reels (**-14 LUFS**, True Peak -1.5 dB) menggunakan filter `loudnorm` pada FFmpeg.

---

### 4. Pipeline Rendering Cepat (Zero-Disk Overhead)
Alih-alih menyimpan puluhan ribu file gambar PNG sementara:
1. Python (`pycairo`) menghasilkan raw buffer `BGRA`.
2. Buffer langsung di-pipe ke `stdin` FFmpeg (`-f rawvideo -pix_fmt bgra`).
3. FFmpeg merender tiap segmen adegan (`seg0.mp4`, `seg1.mp4`, dst.) secara paralel.
4. Segmen digabung menggunakan **concat demuxer** tanpa proses *re-encode* (`-c copy`), menghemat waktu render hingga 85%.

---

## 📱 Panduan Safe-Zone Instagram (9:16 vs 4:5)

Salah satu pelajaran penting dalam produksi video vertikal:
- Resolusi asli: **1080 × 1920** (Rasio 9:16).
- Tampilan Feed & Grid Instagram dipotong menjadi rasio **4:5** (**1080 × 1350**).
- **Safe Zone Vertikal:** Area tengah $y \approx 285\text{ px}$ sampai $y \approx 1635\text{ px}$.
- Teks penting (tagline, notifikasi, nama akun) harus selalu berada di dalam safe zone agar tidak tertutup header, caption, atau tombol like/share Instagram.

---

## 🏃 Cara Menjalankan Repositori

### Prasyarat
- Sistem Operasi: Linux, macOS, atau Windows (via WSL2 / Git Bash / PowerShell)
- Python 3.10+
- FFmpeg terpasang di sistem (`ffmpeg -version`)
- Font: *Bangers*, *Poppins*, *DejaVu Sans Mono*

### Instalasi & Render
```bash
# 1. Pasang dependensi Python
pip install -r requirements.txt

# 2. Pasang font pendukung
./setup_fonts.sh

# 3. Render video secara paralel
./build.sh
```

### Preview Frame Tertentu (Layout Checking)
Cek tampilan visual pada detik ke-41:
```bash
cd src && python3 still.py 41.0
```

---

## 🎓 Pelajaran Berharga (*Lessons Learned*)

1. **AI adalah Rekan Kolaborasi, Bukan Pengambil Alih:** Arahan artistik, storyboard, timing komedi, dan pemilihan tone suara tetap membutuhkan sensitivitas manusia. AI mempercepat eksekusi dari berhari-hari menjadi hitungan jam.
2. **Kekuatan Kode Prosedural:** Animasi yang ditulis dengan kode memiliki keunggulan deterministik—revisi satu angka di timeline langsung memperbarui seluruh adegan terkait tanpa risiko regresi visual.
3. **Pentingnya Audio Hygiene:** Visual yang bagus akan kehilangan 50% dampaknya jika audio tidak ter-mix dengan rapi. Ducking dan normalisasi loudness adalah langkah wajib.
4. **Desain Multi-Format Sejak Awal:** Memikirkan aspek rasio Feed (4:5) dan Reels (9:16) sejak perancangan canvas menyelamatkan video dari terpotongnya informasi penting.

---

## 📄 Lisensi & Hak Cipta

- Kode sumber: Berlisensi [MIT](LICENSE).
- Konsep cerita, naskah narasi, karakter Bagaskara, dan dokumentasi © 2026 Bagaskara Amukti Palapa.
- Dibuat dengan bangga di Palembang 🌉 — *dari laptop sampai Ampera!*
