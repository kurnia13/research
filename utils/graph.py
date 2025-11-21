import networkx as nx
import plotly.graph_objects as go
import numpy as np

def create_graph(seed, related):
    """Membuat objek Figure Plotly dari data paper."""
    G = nx.Graph()
    
    # 1. Tambahkan Node Utama (Seed)
    seed_id = seed['id']
    G.add_node(seed_id, 
               label="SEED", 
               title=seed.get('title', 'No Title'), 
               size=35, 
               color='#2563eb', # Biru Utama
               year=seed.get('publication_year', '-'))
    
    # 2. Tambahkan Node Referensi
    for p in related:
        p_id = p['id']
        is_retracted = p.get('is_retracted', False)
        
        # Logika Visual: Merah jika retracted, Abu jika aman
        color = '#ef4444' if is_retracted else '#94a3b8'
        # Ukuran berdasarkan sitasi (Logarithmic scale agar tidak terlalu timpang)
        size = 12 + (np.log(p.get('cited_by_count', 0) + 1) * 3)
        
        G.add_node(p_id, 
                   label="REF", 
                   title=p.get('title', 'No Title'), 
                   size=size, 
                   color=color, 
                   year=p.get('publication_year', '-'))
        
        # Hubungkan ke seed
        G.add_edge(seed_id, p_id)
    
    # 3. Hitung Posisi (Physics Layout)
    pos = nx.spring_layout(G, seed=42, k=0.6)
    
    # 4. Render Edge (Garis)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#cbd5e1'),
        hoverinfo='none',
        mode='lines')

    # 5. Render Node (Lingkaran)
    node_x, node_y, node_text, node_color, node_size = [], [], [], [], []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        data = G.nodes[node]
        
        # Tooltip saat hover
        info = f"<b>{data['title']}</b><br>Tahun: {data['year']}<br>Tipe: {data['label']}"
        node_text.append(info)
        node_color.append(data['color'])
        node_size.append(data['size'])

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=False,
            color=node_color,
            size=node_size,
            line_width=2,
            line_color='white'))

    # 6. Finalisasi Layout
    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=0,l=0,r=0,t=0),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    plot_bgcolor='white',
                    height=600
                 ))
    return fig
