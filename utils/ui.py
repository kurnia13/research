import streamlit as st

def inject_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #0f172a;
        }
        
        /* Header Styling */
        .main-header {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        .text-blue { color: #2563eb; }
        .text-gray { color: #64748b; }
        
        /* Card Styling */
        .paper-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
            transition: all 0.2s;
        }
        .paper-card:hover {
            border-color: #2563eb;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.1);
        }
        .card-title { font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem; }
        .card-meta { font-size: 0.85rem; color: #64748b; }
        
        /* Badge */
        .badge-retracted {
            background: #fef2f2; color: #991b1b;
            padding: 4px 8px; border-radius: 4px;
            font-size: 0.8rem; font-weight: bold;
            border: 1px solid #fca5a5;
            display: inline-block; margin-bottom: 8px;
        }
    </style>
    """, unsafe_allow_html=True)

def render_card_html(paper):
    title = paper.get('title', 'No Title')
    year = paper.get('publication_year', 'N/A')
    citations = paper.get('cited_by_count', 0)
    retracted = paper.get('is_retracted', False)
    
    alert = '<div class="badge-retracted">⚠️ RETRACTED</div>' if retracted else ''
    
    return f"""
    <div class="paper-card">
        {alert}
        <div class="card-title">{title}</div>
        <div class="card-meta">📅 {year} • 🔗 {citations} Sitasi</div>
    </div>
    """
