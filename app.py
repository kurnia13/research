import streamlit as st
import pandas as pd
# Import modul buatan sendiri
from utils import api, graph, ui

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="KurniaResearch",
    page_icon="🔍",
    layout="wide"
)

# 2. Inisialisasi Session State (Memori)
if 'page' not in st.session_state: st.session_state.page = 'landing'
if 'seed' not in st.session_state: st.session_state.seed = None
if 'related' not in st.session_state: st.session_state.related = []
if 'collection' not in st.session_state: st.session_state.collection = []

# 3. Load CSS
ui.inject_css()

# --- HALAMAN 1: LANDING PAGE ---
def show_landing():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="main-header">Riset Akademik Jadi <span class="text-blue">Lebih Cerdas</span></div>', unsafe_allow_html=True)
        st.markdown('<p class="text-gray">Temukan makalah benih, visualisasikan jaringan, dan cek integritas jurnal dalam satu platform.</p>', unsafe_allow_html=True)
        
        with st.form("search"):
            query = st.text_input("Cari topik atau DOI...", placeholder="Contoh: Deep Learning in Education")
            if st.form_submit_button("Mulai Riset", type="primary", use_container_width=True):
                if query:
                    with st.spinner("Mencari di OpenAlex..."):
                        results = api.search_works(query)
                        st.session_state.results = results
                        
    with col2:
        # Ilustrasi (Gambar placeholder yang aman)
        st.image("https://img.freepik.com/free-vector/online-document-concept-illustration_114360-5455.jpg", use_container_width=True)

    # Hasil Pencarian
    if 'results' in st.session_state and st.session_state.results:
        st.divider()
        st.subheader("Hasil Pencarian")
        for p in st.session_state.results:
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(ui.render_card_html(p), unsafe_allow_html=True)
            with c2:
                st.write("") # Spacer
                st.write("")
                if st.button("Pilih Seed", key=p['id']):
                    st.session_state.seed = p
                    with st.spinner("Membuat Jaringan..."):
                        seed_full, related = api.get_details(p['id'])
                        st.session_state.seed = seed_full
                        st.session_state.related = related
                        st.session_state.page = 'workspace'
                        st.rerun()

# --- HALAMAN 2: WORKSPACE ---
def show_workspace():
    seed = st.session_state.seed
    related = st.session_state.related
    
    # Sidebar
    with st.sidebar:
        if st.button("← Cari Baru", use_container_width=True):
            st.session_state.page = 'landing'
            st.rerun()
        st.markdown("---")
        st.markdown("### 📂 Koleksi")
        for item in st.session_state.collection:
            st.caption(f"📄 {item['title'][:30]}...")
            
    # Konten Utama
    st.subheader(f"Workspace: {seed['title']}")
    
    tab1, tab2, tab3 = st.tabs(["🕸️ Graf", "📊 Timeline", "📝 Detail"])
    
    with tab1:
        if related:
            fig = graph.create_graph(seed, related)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Data referensi tidak cukup untuk membuat graf.")
            
    with tab2:
        if related:
            years = [r.get('publication_year') for r in related if r.get('publication_year')]
            if years:
                df = pd.DataFrame(years, columns=['Tahun'])
                st.bar_chart(df['Tahun'].value_counts())
    
    with tab3:
        st.markdown("#### Abstrak")
        st.write(api.reconstruct_abstract(seed.get('abstract_inverted_index')))
        
        st.markdown("#### Metadata")
        st.info(f"DOI: {seed.get('doi')}")
        
        if st.button("Simpan ke Koleksi"):
            if seed not in st.session_state.collection:
                st.session_state.collection.append(seed)
                st.success("Tersimpan!")

# --- ROUTER ---
if st.session_state.page == 'landing':
    show_landing()
else:
    show_workspace()
