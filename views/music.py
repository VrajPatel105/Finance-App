import streamlit as st
import random

def create_floating_music_player():
    spotify_playlists = [
        '37i9dQZF1DWZeKCadgRdKQ',  # Deep Focus
        '37i9dQZF1DX4sWSpwq3LiO',  # Peaceful Piano
        '37i9dQZF1DWWQRwui0ExPn',  # LoFi Beats
        '37i9dQZF1DX2TRYkJECvfC',  # Deep House Focus
        '37i9dQZF1DX8NTLI2TtZa6',  # Instrumental Study
        '37i9dQZF1DWV7EzJMK2FUI',  # Jazz in the Background
        '37i9dQZF1DX3XuTDjo5z5z',  # Electronic Focus
        '37i9dQZF1DWXHQpqStiWL4',  # Classical Focus
        '37i9dQZF1DX4PP3DA4J0N8',  # Nature Sounds
        '37i9dQZF1DX3Ogo9pFvBkY',  # Ambient Relaxation
        '37i9dQZF1DWZZbwlv3Vmtr',  # Focus Flow
        '37i9dQZF1DWXLeA8Omikj7',  # Brain Food
        '37i9dQZF1DWUZ5bk6qqDSy',  # White Noise
        '37i9dQZF1DX0tFt8BAdFgM',  # Focus Space
        '37i9dQZF1DX9sIqqvKsjG8'   # Reading and Focus
        '37i9dQZF1DX5trt9i14X7j',
        '37i9dQZF1DX8Uebhn9wzrS',
        '37i9dQZF1DX0SM0LYsmbMT',
        '37i9dQZF1DX7K31D69s4M1',
        '37i9dQZF1DXc8kgYqQLMfH',
        '37i9dQZF1DX692WcMwL2yW',
        '37i9dQZF1DXaXB8fQg7xif',
        '37i9dQZF1DWZeKCadgRdKQ',
        '37i9dQZF1DX1s9knjP51Oa',
        '37i9dQZF1DWWQRwui0ExPn',
        '37i9dQZF1DX9RwfGbeGQwP',
        '37i9dQZF1DWXe9gFZP0gtP',
        '37i9dQZF1DWZqd5JICZI0u',
        '37i9dQZF1DX3PFzdbtx1Us',
        '37i9dQZF1DX9uKNf5jGX6m'   
    ]

    random_playlist = random.choice(spotify_playlists)
    iframe_src = f"https://open.spotify.com/embed/playlist/{random_playlist}?utm_source=generator"

    st.markdown(f"""
    <style>
        .floating-player {{
            position: fixed;
            left: 20px;
            bottom: 20px;
            width: 320px;
            background: linear-gradient(135deg, rgba(30, 30, 35, 0.95), rgba(20, 20, 25, 0.95));
            border-radius: 16px;
            padding: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            z-index: 9999;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(168, 85, 247, 0.2);
            transition: all 0.3s ease;
        }}
        
        .floating-player:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(168, 85, 247, 0.15);
            border-color: rgba(168, 85, 247, 0.4);
        }}
        
        .playlist-container {{
            background: rgba(15, 15, 20, 0.6);
            border-radius: 12px;
            overflow: hidden;
        }}
    </style>
    
    <div class="floating-player" id="musicPlayer">
        <div class="playlist-container" id="playlistContainer">
            <iframe 
                id="spotifyEmbed"
                style="border-radius:12px" 
                src="{iframe_src}"
                width="100%" 
                height="152" 
                frameBorder="0" 
                allowfullscreen="" 
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                loading="lazy">
            </iframe>
        </div>
    </div>
    """, unsafe_allow_html=True)