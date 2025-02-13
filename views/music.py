import streamlit as st
import random
import time

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
        '37i9dQZF1DX9sIqqvKsjG8',  # Reading and Focus
        '37i9dQZF1DX5trt9i14X7j'  # Coding Mode
        '37i9dQZF1DX8Uebhn9wzrS'  # Chill Lofi Study Beats
        '37i9dQZF1DX0SM0LYsmbMT'  # Jazz Vibes
        '37i9dQZF1DX7K31D69s4M1'  # Piano in the Background
        '37i9dQZF1DXc8kgYqQLMfH'  # Lush Lofi
        '37i9dQZF1DX692WcMwL2yW'  # All-Nighter
        '37i9dQZF1DXaXB8fQg7xif'  # Dance Party
        '37i9dQZF1DWZeKCadgRdKQ'  # Deep Focus
        '37i9dQZF1DX1s9knjP51Oa'  # Calm Vibes
        '37i9dQZF1DWWQRwui0ExPn'  # LoFi Beats
        '37i9dQZF1DX9RwfGbeGQwP'  # Chill Hits
        '37i9dQZF1DWXe9gFZP0gtP'  # Relax & Unwind
        '37i9dQZF1DWZqd5JICZI0u'  # Evening Chill
        '37i9dQZF1DX3PFzdbtx1Us'  # Chillout Lounge
        '37i9dQZF1DX9uKNf5jGX6m'  # Study Break
    ]

    # Initialize session state for playlist and timestamp if they don't exist
    if 'current_playlist' not in st.session_state:
        st.session_state.current_playlist = random.choice(spotify_playlists)
        st.session_state.last_update_time = time.time()

    # Check if 3 minutes have passed and if yes, then we randomly select the next playlist and display it.
    current_time = time.time()
    if current_time - st.session_state.last_update_time >= 180:  # 180 seconds 
        st.session_state.current_playlist = random.choice(spotify_playlists)
        st.session_state.last_update_time = current_time

    iframe_src = f"https://open.spotify.com/embed/playlist/{st.session_state.current_playlist}?utm_source=generator"

    # html and css to display the spotify section at the bottom left corner. We particulary dont need it to be positioned, if we are generating it inside the sidebar.
    # But here we are not generating inside the sidebar, so we have to position it.
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
