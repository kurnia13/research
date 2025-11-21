import requests
import streamlit as st

# Endpoint OpenAlex
BASE_URL = "https://api.openalex.org"

def search_works(query):
    """Mencari makalah berdasarkan kata kunci."""
    url = f"{BASE_URL}/works?search={query}&per-page=10"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json().get('results', [])
    except Exception as e:
        st.error(f"Gagal menghubungi OpenAlex: {e}")
    return []

def get_details(paper_id):
    """Mengambil detail seed paper dan referensi terkaitnya."""
    # 1. Ambil Seed
    url = f"{BASE_URL}/works/{paper_id}"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return None, []
        
        seed = res.json()
        
        # 2. Ambil Related (Referenced Works)
        related = []
        if seed.get('referenced_works'):
            # Ambil maksimal 20 referensi agar loading cepat
            refs = seed['referenced_works'][:20]
            # Gabungkan ID untuk satu kali panggilan API (Batch Request)
            refs_str = "|".join(refs)
            url_refs = f"{BASE_URL}/works?filter=ids.openalex:{refs_str}&per-page=20"
            
            res_refs = requests.get(url_refs, timeout=15)
            if res_refs.status_code == 200:
                related = res_refs.json().get('results', [])
                
        return seed, related
    except Exception as e:
        st.error(f"Terjadi kesalahan jaringan: {e}")
        return None, []

def reconstruct_abstract(inverted_index):
    """Menyusun kembali abstrak dari Inverted Index."""
    if not inverted_index:
        return "Abstrak tidak tersedia (Hak Cipta Penerbit)."
    
    words = {}
    for word, positions in inverted_index.items():
        for pos in positions:
            words[pos] = word
            
    sorted_pos = sorted(words.keys())
    return " ".join([words[i] for i in sorted_pos])
