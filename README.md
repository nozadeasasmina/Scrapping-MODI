# Scrapping-MODI
Scrapping-Modi adalah project untuk melakukan scrapping data dari situ resmi Minerba One Data Indonesia (MODI)
Project ini mengumpulkan data company profile dan data perizinan secara otomatis dengan memasukan kode perusahaan.
Kode perusahaan didapat pada web MODI https://modi.esdm.go.id/.
scrapping menggunakan `selenium` dan sudah dalam mode headless.
File scrapping akan disimpan dalam format JSON.

### 1. Clone repository

```bash
git clone https://github.com/nozadeasasmina/Scrapping-MODI
cd Scrapping-MODI
```

### 2. Install dependency

```bash
pip install -r requirements.txt
```

### 3. Add company code in main.py script
```bash
# if only one company code
ids = [12289]

# if having more than one company code
ids = [53, 1608, 3973]
```

### 4. Run main script
```bash
python main.py
```