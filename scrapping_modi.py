import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_companyprofile_modi(ids, output_file='companyprofile_modi.json'):
    """
    scrapping company profile and lisence (perizinan) from minerba one data indonesia (MODI)
    :param ids: kode of company
    :param output_file:
    :return:
    """
    # Load existing data if file exists
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = []
    else:
        all_data = []

    # Convert list to dict by ID for easy replacement
    data_dict = {entry['ID']: entry for entry in all_data}

    for id_ in ids:
        url = f"https://modi.esdm.go.id/portal/detailPerusahaan/{id_}?jp=1"

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)

        wait = WebDriverWait(driver, 10)
        print(f"🔍 Memproses ID: {id_} ...")
        driver.get(url)

        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.nav-link")))
        tabs = driver.find_elements(By.CSS_SELECTOR, "a.nav-link")

        profile_data = {}
        perizinan_list = []

        for tab in tabs:
            tab_name = tab.text.strip()

            if 'Profil Perusahaan' in tab_name:
                try:
                    print(f"➡️ Klik tab: {tab_name}")
                    tab.click()
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table")))
                    time.sleep(1)

                    table = driver.find_element(By.CSS_SELECTOR, "table.table")
                    rows = table.find_elements(By.TAG_NAME, "tr")
                    for row in rows:
                        cells = row.find_elements(By.XPATH, ".//*")
                        if len(cells) >= 3:
                            label = cells[0].text.strip().replace(":", "")
                            value = cells[2].text.strip()
                            profile_data[label] = value

                    # Ambil data pemilik saham (div ke-2)
                    try:
                        all_tables = driver.find_elements(By.CSS_SELECTOR, "div.col-md-9.table-responsive")
                        if len(all_tables) >= 2:
                            shareholder_div = all_tables[1]
                            table = shareholder_div.find_element(By.TAG_NAME, "table")
                            rows = table.find_elements(By.TAG_NAME, "tr")

                            if len(rows) > 1:
                                first_row_cells = rows[1].find_elements(By.TAG_NAME, "td")
                                if len(first_row_cells) >= 3:
                                    pemilik_nama = first_row_cells[2].text.strip()
                                    profile_data["Pemegang Saham/Pemilik"] = pemilik_nama
                                    print("✅ Pemegang Saham:", pemilik_nama)

                    except Exception as e:
                        print(f"⚠️ Gagal mengambil data pemilik saham: {e}")

                except Exception as e:
                    print(f"❌ Gagal mengambil data profil: {e}")

            elif 'Perizinan' in tab_name:
                try:
                    print(f"➡️ Klik tab: {tab_name}")
                    tab.click()
                    wait.until(EC.presence_of_element_located((By.XPATH, "//table")))
                    time.sleep(1)

                    headers = driver.find_elements(By.XPATH, "//table/thead//th")
                    columns = [h.text.strip() for h in headers if h.text.strip() != '']

                    rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
                    for row in rows:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        values = [c.text.strip() for c in cells]
                        if len(values) == len(columns):
                            izin = dict(zip(columns, values))
                            perizinan_list.append(izin)

                except Exception as e:
                    print(f"❌ Gagal memproses tab '{tab_name}': {e}")
                    continue

        driver.quit()

        # Replace or add new entry
        data_dict[id_] = {
            "ID": id_,
            "Profil": profile_data,
            "Perizinan": perizinan_list
        }

    # Convert back to list and save
    final_data = list(data_dict.values())
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

    print(f"✅ Data berhasil disimpan dan diperbarui ke '{output_file}'")
