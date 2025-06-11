from scrapping_modi import scrape_companyprofile_modi
import time
start_time = time.time()

# ======== START ==========
ids =[12289] #insert code of company
scrape_companyprofile_modi(ids)

# ======== FINISH ==========
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Waktu eksekusi: {elapsed_time:.2f} detik")
