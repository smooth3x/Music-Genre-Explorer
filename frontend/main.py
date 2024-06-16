import requests
import pandas as pd
import streamlit as st
import urllib.parse
from PIL import Image

import io
import base64

# Function to fetch genres from the FastAPI backend
def fetch_genres():
    response = requests.get("http://backend:8000/v1/genres")
    return response.json()

# Function to fetch bands for a specific genre from the FastAPI backend
def fetch_genre_bands(genre_name):
    response = requests.get(f"http://backend:8000/v1/genre/{genre_name.replace(' ', '').lower()}")
    bands_data = response.json()
    return bands_data

# Function to fetch genres by artist from the FastAPI backend
def fetch_genres_by_artist(artist):
    response = requests.get(f"http://backend:8000/v1/genres_by_artist/{artist}")
    genres = response.json()
    return genres

# Function to render the table with audio previews
def render_table(dataframe):
    dataframe = dataframe.copy()
    for i, row in dataframe.iterrows():
        if row['Audio Preview'] != 'N/A':
            audio_tag = f'<audio controls src="{row["Audio Preview"]}" id="audio{i}"></audio>'
        else:
            audio_tag = 'No audio preview available'
        dataframe.at[i, 'Audio Preview'] = audio_tag
    
    dataframe.reset_index(drop=True, inplace=True)
    dataframe.index = dataframe.index + 1

    table_html = dataframe.to_html(escape=False, index=True, classes="dataframe", justify="center")
    table_html = table_html.replace('<table', '<table style="width:100%; text-align:center"')

    return table_html

def render_artists_page(selected_genre): 

    genre_data = fetch_genre_bands(selected_genre)
    bands_data = genre_data['bands']
    spotify_playlist = genre_data['spotify_playlist']
    
    bands_df = pd.DataFrame(bands_data)

    st.set_page_config(layout="wide", page_title="Music Genre Explorer", page_icon="🎵")

    with st.columns(3)[1]:
        render_logo()

        style = "<style>h3 {text-align: center;}</style>"
        st.markdown(style, unsafe_allow_html=True)
        st.subheader(f"Popular Artists in \"{selected_genre}\"")

    # Pagination for bands data
    items_per_page = 12
    total_band_pages = (len(bands_df) + items_per_page - 1) // items_per_page
    band_pages = list(range(1, total_band_pages + 1))

    if 'current_band_page' not in st.session_state:
        st.session_state.current_band_page = 1

    def update_band_page():
        st.session_state.current_band_page = st.session_state.band_page_select

    st.selectbox(
        f'Page {st.session_state.current_band_page}/{total_band_pages}, Artists {(st.session_state.current_band_page-1)*items_per_page + 1}-{min(st.session_state.current_band_page*items_per_page, len(bands_df))}/{len(bands_df)}',
        band_pages,
        index=st.session_state.current_band_page - 1,
        key='band_page_select',
        on_change=update_band_page
    )

    start_idx = (st.session_state.current_band_page - 1) * items_per_page
    end_idx = start_idx + items_per_page

    band_page_data = bands_df.iloc[start_idx:end_idx]

    # Create two columns
    col1, col2 = st.columns(2)

    # Display the table in the first column
    with col1:
        st.write(render_table(band_page_data), unsafe_allow_html=True)

    # Display the Spotify playlist in the second column
    with col2:
        st.write(f'<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/{spotify_playlist}?utm_source=generator" width="100%" height="720" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>', unsafe_allow_html=True)

def render_genres_page(): 
    genres_data = fetch_genres()
    df = pd.DataFrame(genres_data)

    st.set_page_config(layout="centered", page_title="Music Genre Explorer", page_icon="🎵")

    render_logo()

    def update_query_params():
        selected_genres = st.session_state.selected_genres

        if selected_genres:
            # Assuming you want to set the first selected genre in the query parameter
            st.query_params["genre"] = selected_genres.lower()
        else:
            st.query_params()

    col1, col2, col3 = st.columns(3)

    with col1:
        # Search bar
        search_query = st.selectbox(
            "Search Genres", 
            df['Genre'].unique().tolist(),
            key='selected_genres',
            on_change=update_query_params,
            index=None,
            placeholder="Search for a genre")
        
        # Filter the DataFrame based on search query
        if search_query:
            filtered_df = df[df['Genre'].str.contains('|'.join(search_query), case=False, na=False)]
        else:
            filtered_df = df

    with col3: 
        search_artists_query = st.text_input(
            "Search Genres by Artist", 
            "")
        
        if search_artists_query:
            st.session_state.current_page = 1

            genres = fetch_genres_by_artist(search_artists_query)
            filtered_df = df[df['Genre'].isin(genres)]
        else:
            filtered_df = df


    # Pagination variables
    items_per_page = 12
    total_pages = (len(filtered_df) + items_per_page - 1) // items_per_page
    pages = list(range(1, total_pages + 1))

    # Session state to keep track of the current page
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1

    def update_page():
        st.session_state.current_page = st.session_state.page_select

    if total_pages > 0:
        start_idx = (st.session_state.current_page - 1) * items_per_page

        if len(filtered_df) > start_idx + items_per_page:
            end_idx = start_idx + items_per_page
        else: 
            end_idx = len(filtered_df)

        # Get the data for the current page
        page_data = filtered_df.iloc[start_idx:end_idx]

        with col2:
            st.selectbox(
                f'Page {st.session_state.current_page}/{total_pages}, Genres {start_idx + 1}-{end_idx}/{len(filtered_df)}',
                pages,
                index=st.session_state.current_page - 1,
                key='page_select',
                on_change=update_page
            )

        # Display the DataFrame in a table with genre links
        def make_clickable(val):
            params = {'genre': val.lower()}
            encoded_val = urllib.parse.urlencode(params)
            return f'<a href="/?{encoded_val}" target="_self" style="color:#FFAF69; text-decoration:none">{val}</a>'
        
        page_data = filtered_df.iloc[start_idx:end_idx].copy()
        page_data.loc[:, 'Genre'] = page_data['Genre'].apply(make_clickable)

        st.write(render_table(page_data), unsafe_allow_html=True)

def render_logo():
    image = Image.open('design/logo.png')  # Path within the Docker container
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_str = base64.b64encode(img_bytes.getvalue()).decode()

    st.markdown(
        f"""
        <a href="http://localhost:8501/" target="_self">
            <img src="data:image/png;base64,{img_str}" width="100%" alt="Logo">
        </a>
        """,
        unsafe_allow_html=True
    )


def main():
    # Extract query parameters
    selected_genre = st.query_params.get("genre", None)

    if selected_genre:
        render_artists_page(selected_genre)
    else:
        render_genres_page()
    
if __name__ == "__main__":
    main()
