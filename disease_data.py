"""
TomatoCare AI - Basis Data Pengetahuan 9 Kelas Kondisi Daun Tomat
Informasi disajikan untuk keperluan edukasi dan panduan observasi awal.
"""

EDUCATIONAL_DISCLAIMER = (
    "Informasi dan rekomendasi penanganan ini disajikan sebagai panduan agronomi "
    "edukatif untuk tindakan awal observasi visual. Selalu konsultasikan dengan petugas penyuluh "
    "pertanian lapangan (PPL) atau ahli proteksi tanaman setempat sebelum mengaplikasikan pestisida kimia skala luas."
)

DISEASE_DATA = {
    "Early Blight": {
        "id": 0,
        "name_en": "Early Blight",
        "name_id": "Bercak Kering (Early Blight)",
        "scientific_name": "Alternaria solani",
        "category": "Jamur (Fungi)",
        "severity": "Sedang",
        "badge_color": "#FF9F1C",
        "theme_color": "warning",
        "mascot_emotion": "concerned",
        "description": "Penyakit jamur umum yang menyerang daun tomat tua di bagian bawah kanopi, sering muncul saat kondisi hangat berselang hujan.",
        "visual_symptoms": [
            "Bercak cokelat gelap hingga hitam berukuran 1-2 cm pada daun bagian bawah.",
            "Pola lingkaran konsentris khas yang menyerupai papan sasaran tembak (bullseye).",
            "Tepi daun di sekeliling bercak menguning (halo klorotik).",
            "Pada serangan parah, daun mengering, layu, dan gugur sebelum waktunya."
        ],
        "causes": "Spora jamur Alternaria solani yang bertahan di sisa tanaman atau tanah, menyebar lewat percikan air hujan dan angin pada suhu 24-29°C.",
        "organic_treatment": [
            "Pangkas dan musnahkan daun-daun tua terbawah yang menunjukkan gejala bercak.",
            "Semprotkan larutan biofungisida berbahan aktif Trichoderma atau fungisida nabati (ekstrak mimba / serai wangi).",
            "Pasang mulsa plastik atau jerami setebal 5-7 cm untuk mencegah percikan tanah saat penyiraman."
        ],
        "chemical_treatment": [
            "Gunakan fungisida protektif berbahan aktif Mankozeb atau Klorotalonil sesuai dosis label.",
            "Rotasikan dengan fungisida sistemik berbahan aktif Difenokonazol jika bercak mulai menyebar ke daun muda."
        ],
        "prevention": [
            "Lakukan rotasi tanaman minimal 2-3 tahun dengan tanaman bukan famili Solanaceae (terung/cabai/kentang).",
            "Gunakan irigasi tetes (drip) di area perakaran dan hindari membasahi dedaunan pada sore hari.",
            "Atur jarak tanam ideal (50-60 cm) untuk kelancaran sirkulasi udara."
        ]
    },
    "Healthy": {
        "id": 1,
        "name_en": "Healthy",
        "name_id": "Daun Sehat (Healthy)",
        "scientific_name": "Solanum lycopersicum",
        "category": "Optimal",
        "severity": "Aman",
        "badge_color": "#2EC4B6",
        "theme_color": "success",
        "mascot_emotion": "happy",
        "description": "Daun tomat dalam kondisi prima, segar, memiliki klorofil optimal, dan bebas dari gejala serangan hama atau patogen.",
        "visual_symptoms": [
            "Warna hijau segar dan merata di seluruh helaian daun.",
            "Tekstur daun lentur, bersih dari bercak nekrotik, lubang, maupun alur hama.",
            "Tulang daun kokoh dan pertumbuhan pucuk berlangsung normal."
        ],
        "causes": "Keseimbangan nutrisi makro/mikro yang baik, penyinaran matahari cukup, kelembapan seimbang, dan sanitasi kebun yang terjaga.",
        "organic_treatment": [
            "Pertahankan penyiraman teratur sesuai kelembapan tanah.",
            "Beri pupuk organik cair (POC) atau pupuk hayati setiap 7-10 hari sekali.",
            "Semprot ekstrak daun nimba encer berkala sebagai langkah proteksi preventif."
        ],
        "chemical_treatment": [
            "Tidak memerlukan perlakuan bahan kimia apa pun."
        ],
        "prevention": [
            "Lakukan pemantauan rutin 2 kali seminggu untuk deteksi dini kemungkinan hama.",
            "Pertahankan kebersihan drainase bedengan agar perakaran tidak tergenang."
        ]
    },
    "Late Blight": {
        "id": 2,
        "name_en": "Late Blight",
        "name_id": "Hawar Daun / Busuk Daun (Late Blight)",
        "scientific_name": "Phytophthora infestans",
        "category": "Oomycete",
        "severity": "Kritis",
        "badge_color": "#E71D36",
        "theme_color": "danger",
        "mascot_emotion": "alarmed",
        "description": "Penyakit paling merusak pada tanaman tomat dan kentang yang mampu merontokkan seluruh tanaman hanya dalam hitungan hari pada cuaca basah dan dingin.",
        "visual_symptoms": [
            "Bercak basah berwarna hijau pucat berminyak yang cepat meluas menjadi cokelat gelap basah.",
            "Lapisan beludru putih keabuan (miselium jamur) muncul di permukaan bawah daun saat kelembapan tinggi.",
            "Tangkai daun dan batang membusuk kecokelatan serta mudah patah.",
            "Menimbulkan bau busuk khas tanaman basah membusuk."
        ],
        "causes": "Patogen Phytophthora infestans yang berkembang sangat pesat dalam cuaca dingin (15-20°C) dengan kelembapan di atas 90% atau berkabut.",
        "organic_treatment": [
            "Cabut segera tanaman yang terinfeksi berat dan kubur dalam atau bakar (jangan dibuat kompos!).",
            "Semprot larutan Bubur Bordeaux (tembaga sulfat + kapur tohor) pada tanaman sekitar yang masih sehat.",
            "Hentikan sementara penyiraman di atas tajuk daun."
        ],
        "chemical_treatment": [
            "Segera aplikasikan fungisida sistemik kuratif khusus oomycete (bahan aktif Simoksanil, Dimetomorf, atau Metalaksil).",
            "Kombinasikan dengan fungisida kontak Mankozeb untuk menekan spora bebas."
        ],
        "prevention": [
            "Pilih benih/bibit tomat bersertifikat yang memiliki ketahanan terhadap Phytophthora.",
            "Beri jarak tanam yang longgar (minimal 60-70 cm) agar sinar matahari menjangkau lantai kebun.",
            "Hindari menanam tomat berdekatan dengan lahan kentang."
        ]
    },
    "Leaf Miner": {
        "id": 3,
        "name_en": "Leaf Miner",
        "name_id": "Ulat Penggorok Daun (Leaf Miner)",
        "scientific_name": "Liriomyza spp.",
        "category": "Hama Serangga",
        "severity": "Ringan-Sedang",
        "badge_color": "#FFB703",
        "theme_color": "warning",
        "mascot_emotion": "confused",
        "description": "Serangan larva lalat penggorok daun yang membuat koridor alur di dalam jaringan mesofil daun, mengurangi kapasitas fotosintesis.",
        "visual_symptoms": [
            "Garis putih berkelok-kelok (alur terowongan transparan) pada helaian daun.",
            "Bintik putih kecil (tusukan oviposisi lalat betina) di ujung helai daun.",
            "Daun mengering menyerupai kertas terbakar jika terdapat banyak liang koridor larva."
        ],
        "causes": "Lalat kecil hitam-kuning genus Liriomyza meletakkan telur di dalam daun, lalu larva menetas dan mengikis jaringan daun dari dalam.",
        "organic_treatment": [
            "Remas bagian ujung liang daun untuk mematikan larva yang masih berada di dalam alur.",
            "Pasang perangkap likat kuning (yellow sticky trap) setinggi tajuk tanaman untuk menangkap lalat dewasa.",
            "Semprot insektisida nabati ekstrak biji mimba (azadirachtin) atau tembakau."
        ],
        "chemical_treatment": [
            "Aplikasi insektisida translaminar sistemik berbahan aktif Abamektin atau Siromazin jika tingkat serangan melebihi 15% kanopi."
        ],
        "prevention": [
            "Pasang jaring serangga halus (insect screen net 40-50 mesh) di pembibitan.",
            "Bersihkan gulma liar famili Asteraceae dan Solanaceae di sekitar lahan kebun."
        ]
    },
    "Leaf Mold": {
        "id": 4,
        "name_en": "Leaf Mold",
        "name_id": "Kapang Daun (Leaf Mold)",
        "scientific_name": "Passalora fulva (Fulvia fulva)",
        "category": "Jamur (Fungi)",
        "severity": "Sedang",
        "badge_color": "#06D6A0",
        "theme_color": "info",
        "mascot_emotion": "concerned",
        "description": "Infeksi jamur daun yang sangat umum dijumpai di rumah kaca (greenhouse) atau lahan terbuka dengan kelembapan udara sangat tinggi dan sirkulasi terbatas.",
        "visual_symptoms": [
            "Bercak kuning kehijauan dengan batas tidak tegas di permukaan atas daun.",
            "Lapisan beludru lebat berwarna cokelat zaitun atau abu-abu di permukaan bawah daun.",
            "Daun yang terinfeksi menggulung, menguning, dan perlahan gugur."
        ],
        "causes": "Spora jamur Passalora fulva yang aktif dan berkecambah optimal pada kelembapan relatif tinggi (>85%) dan suhu moderat 22-26°C.",
        "organic_treatment": [
            "Tingkatkan ventilasi dan pasang kipas sirkulasi jika menanam dalam naungan/greenhouse.",
            "Rempel (pruning) daun-daun bagian bawah yang padat untuk mengurangi kelembapan mikro.",
            "Semprot larutan biofungisida berbahan aktif Bacillus subtilis atau Streptomyces."
        ],
        "chemical_treatment": [
            "Aplikasikan fungisida berbahan aktif Difenokonazol, Tiofanat-metil, atau Klorotalonil."
        ],
        "prevention": [
            "Hindari penyiraman malam hari yang menyebabkan daun basah hingga pagi.",
            "Gunakan varietas tahan terhadap strain Passalora fulva."
        ]
    },
    "Mosaic Virus": {
        "id": 5,
        "name_en": "Mosaic Virus",
        "name_id": "Virus Mosaik Tomat (Tomato Mosaic Virus)",
        "scientific_name": "Tomato Mosaic Tobamovirus (ToMV)",
        "category": "Virus",
        "severity": "Tinggi",
        "badge_color": "#8338EC",
        "theme_color": "primary",
        "mascot_emotion": "sad",
        "description": "Penyakit virus yang sangat stabil dan menular cepat melalui gesekan fisik, perkakas kebun, atau benih yang terinfeksi.",
        "visual_symptoms": [
            "Pola belang-belang warna hijau tua berselang hijau muda atau kuning pada daun.",
            "Helaian daun mengerut, bergelombang, atau menyempit seperti tali (shoestring leaf).",
            "Pertumbuhan tanaman kerdil dan pembentukan buah terhambat."
        ],
        "causes": "Partikel virus ToMV yang bertahan lama di sisa tanaman kering, benih, dan menular melalui tangan pekerja serta alat pangkas.",
        "organic_treatment": [
            "Eradikasi (cabut dan bakar) segera tanaman yang menunjukkan gejala mosaik.",
            "Cuci tangan dan celupkan alat pangkas ke dalam larutan susu skim 10% atau sabun desinfektan sebelum menyentuh tanaman sehat.",
            "Jangan merokok di sekitar tanaman (tembakau dapat membawa virus mosaik terkait TMV)."
        ],
        "chemical_treatment": [
            "Tidak ada obat/pestisida kimia yang dapat mematikan virus di dalam jaringan tanaman hidup. Fokus pada pencegahan penyebaran."
        ],
        "prevention": [
            "Gunakan benih unggul bersertifikat yang teruji bebas virus.",
            "Rendam benih dalam larutan trisodium fosfat (TSP) 10% sebelum disemai jika dicurigai membawa virus."
        ]
    },
    "Septoria": {
        "id": 6,
        "name_en": "Septoria",
        "name_id": "Bercak Daun Septoria (Septoria Leaf Spot)",
        "scientific_name": "Septoria lycopersici",
        "category": "Jamur (Fungi)",
        "severity": "Sedang",
        "badge_color": "#FB5607",
        "theme_color": "warning",
        "mascot_emotion": "concerned",
        "description": "Penyakit jamur daun bercak kecil yang sering muncul setelah tanaman mulai berbunga dan dapat menyebabkan defoliasi tajuk daun bawah.",
        "visual_symptoms": [
            "Bercak melingkar kecil banyak berdiameter 2-3 mm.",
            "Tepi bercak berwarna cokelat tua kehitaman dengan bagian tengah berwarna abu-abu terang.",
            "Terdapat titik-titik hitam sangat kecil (piknidia spora jamur) di tengah bercak.",
            "Daun berubah kuning dan rontok secara berurutan dari bawah ke atas."
        ],
        "causes": "Jamur Septoria lycopersici yang bertahan pada gulma solanaceous dan tanah, berkecambah cepat saat periode basah berkepanjangan.",
        "organic_treatment": [
            "Rempel dan buang daun yang terinfeksi di awal kemunculan gejala.",
            "Pasang mulsa untuk meredam cipratan air hujan dari permukaan tanah.",
            "Semprot fungisida nabati atau tembaga organik bersertifikat."
        ],
        "chemical_treatment": [
            "Aplikasi fungisida kontak Mankozeb, Klorotalonil, atau Azoksistrobin secara teratur tiap 7 hari pada musim hujan."
        ],
        "prevention": [
            "Bersihkan seluruh sisa-sisa tanaman cabai dan terung liar di sekitar petak kebun.",
            "Hindari menyiram daun di siang atau sore hari."
        ]
    },
    "Spider Mites": {
        "id": 7,
        "name_en": "Spider Mites",
        "name_id": "Tungau Merah (Spider Mites)",
        "scientific_name": "Tetranychus urticae",
        "category": "Hama Acarina (Tungau)",
        "severity": "Sedang-Tinggi",
        "badge_color": "#EF233C",
        "theme_color": "danger",
        "mascot_emotion": "scared",
        "description": "Hama berukuran mikroskopis mirip laba-laba kecil yang mengisap cairan sel daun dari bawah permukaan, berkembang biak kilat saat cuaca panas terik.",
        "visual_symptoms": [
            "Bintik-bintik kuning atau keputihan halus (stippling) seperti taburan jarum pada permukaan atas daun.",
            "Daun menguning kusam, kehilangan kilau, dan rapuh mengering seperti terbakar.",
            "Jaring sutra halus terlihat melintang di bawah helaian daun dan pucuk tanaman saat serangan berat."
        ],
        "causes": "Koloni tungau Tetranychus urticae yang populasinya meledak saat cuaca panas, kering, dan berdebu.",
        "organic_treatment": [
            "Semprotkan air bertekanan ke sisi bawah daun untuk merontokkan koloni dan merusak jaring tungau.",
            "Semprotkan larutan minyak mimba (neem oil) atau sabun kalium insektisida organik ke bawah daun di pagi hari.",
            "Lepaskan musuh alami seperti tungau predator Phytoseiulus persimilis jika tersedia."
        ],
        "chemical_treatment": [
            "Gunakan akarisida khusus berbahan aktif Piridaben, Abamektin, atau Heksitiazoks. Jangan gunakan insektisida sembarangan yang membunuh musuh alami."
        ],
        "prevention": [
            "Jaga kecukupan air tanaman agar tidak mengalami stres kekeringan.",
            "Kurangi akumulasi debu di pinggiran bedengan kebun."
        ]
    },
    "Yellow Leaf Curl Virus": {
        "id": 8,
        "name_en": "Yellow Leaf Curl Virus",
        "name_id": "Virus Daun Keriting Kuning (TYLCV)",
        "scientific_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "category": "Virus",
        "severity": "Kritis",
        "badge_color": "#FF006E",
        "theme_color": "danger",
        "mascot_emotion": "alarmed",
        "description": "Salah satu penyakit virus paling destruktif pada tomat di iklim tropis, ditularkan oleh vektor serangga kutu kebul (whitefly).",
        "visual_symptoms": [
            "Daun pucuk baru mengecil drastis dan mengerut kaku menyerupai cawan/mangkuk menghadap ke atas.",
            "Klorosis (menguning terang) mencolok di sela-sela tulang daun.",
            "Ruas batang memendek, tanaman menjadi sangat kerdil dan rimbun abnormal.",
            "Bunga mudah rontok sehingga tanaman tidak mampu membentuk buah."
        ],
        "causes": "Begomovirus TYLCV yang ditularkan oleh kutu kebul (Bemisia tabaci) saat mengisap cairan tanaman.",
        "organic_treatment": [
            "Cabut dan musnahkan tanaman yang terinfeksi di awal masa tanam agar tidak menjadi sumber penularan bagi tanaman sehat.",
            "Kendalikan kutu kebul dengan memasang banyak perangkap lekat kuning (yellow sticky traps) di kebun.",
            "Semprotkan cendawan entomopatogen Beauveria bassiana untuk mematikan kutu kebul secara hayati."
        ],
        "chemical_treatment": [
            "Kendalikan vektor kutu kebul menggunakan insektisida sistemik berbahan aktif Tiametoksam, Imidakloprid, atau Spiromesifen."
        ],
        "prevention": [
            "Tanam varietas tomat hibrida yang memiliki sifat tahan/toleran terhadap virus TYLCV.",
            "Tutup persemaian bibit dengan kain kasa anti-serangga halus (screen net 50 mesh)."
        ]
    }
}


def get_disease_info(class_name: str) -> dict:
    """Mengambil informasi detail penyakit berdasarkan nama kelas model YOLO."""
    return DISEASE_DATA.get(class_name, {
        "id": -1,
        "name_en": class_name,
        "name_id": f"Kondisi: {class_name}",
        "scientific_name": "Tidak terdaftar",
        "category": "Umum",
        "severity": "Tidak Diketahui",
        "badge_color": "#6C757D",
        "theme_color": "secondary",
        "mascot_emotion": "confused",
        "description": "Kondisi daun tomat terdeteksi tetapi belum memiliki profil agronomi lengkap.",
        "visual_symptoms": ["Informasi gejala visual belum tersedia."],
        "causes": "Perlu pemeriksaan lanjutan oleh tenaga ahli.",
        "organic_treatment": ["Lakukan pengamatan visual secara berkala."],
        "chemical_treatment": ["Hindari penggunaan bahan kimia sebelum diagnosis terkonfirmasi."],
        "prevention": ["Jaga sanitasi kebun dan perhatikan pertumbuhan tanaman."]
    })


def get_all_diseases() -> list:
    """Mengembalikan daftar seluruh penyakit untuk katalog ensiklopedia."""
    return list(DISEASE_DATA.values())
