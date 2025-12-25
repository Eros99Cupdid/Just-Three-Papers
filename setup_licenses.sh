#!/bin/bash
# Skrip setup lisensi TP-OCM

echo "📦 Menyiapkan struktur lisensi TP-OCM..."

# 1. Buat folder jika belum ada
mkdir -p docs/education docs/formal_logic

# 2. Salin GPL v3 ke root (sudah ada)
echo "✅ LICENSE (GPL v3) sudah di root"

# 3. Buat lisensi pendidikan
cat > docs/education/LICENSE_EDUCATION << 'EOF'
TP-OCM Educational Materials - CC BY 4.0
[Isi lengkap seperti di atas]
EOF
echo "✅ docs/education/LICENSE_EDUCATION dibuat (CC BY 4.0)"

# 4. Buat lisensi formal logic
cat > docs/formal_logic/LICENSE_FORMAL << 'EOF'
TP-OCM Formal Logic Papers - CC BY-ND 4.0
[Isi lengkap seperti di atas]
EOF
echo "✅ docs/formal_logic/LICENSE_FORMAL dibuat (CC BY-ND 4.0)"

# 5. Buat file penjelasan di setiap folder
echo "Source code in this folder is licensed under GPL v3" > src/LICENSE_INFO.txt
echo "Educational materials: CC BY 4.0 (free for teaching)" > docs/education/README.txt
echo "Formal logic papers: CC BY-ND 4.0 (citation only)" > docs/formal_logic/README.txt

echo "🎉 Setup lisensi selesai!"
echo "Struktur:"
echo "  /LICENSE              → GPL v3 (kode)"
echo "  /docs/education/      → CC BY 4.0"
echo "  /docs/formal_logic/   → CC BY-ND 4.0"