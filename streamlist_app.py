import streamlit as st
import requests

import datetime

# api_key = ""

import matplotlib

# (goes unused)
# import matplotlib.pyplot as plt
# import datetime
# import numpy as np
# import pandas as pd

matplotlib.use("agg")  # Use the 'agg' backend for Matplotlib
api_key = "14e9eb80a218ca240f9e72fd0bfe2c64"


# Function to search for movies and TV shows using an API
def search_media(query):
    # Search for movies
    movie_base_url = "https://api.themoviedb.org/3/search/movie"
    movie_params = {"api_key": api_key, "query": query}
    movie_response = requests.get(movie_base_url, params=movie_params)
    movie_data = movie_response.json().get("results", [])

    # Search for TV shows
    tv_base_url = "https://api.themoviedb.org/3/search/tv"
    tv_params = {"api_key": api_key, "query": query}
    tv_response = requests.get(tv_base_url, params=tv_params)
    tv_data = tv_response.json().get("results", [])

    # Combine movie and TV show results
    media_data = movie_data + tv_data

    return media_data


# Function to get media details by ID (handles both movies and TV shows)
def get_media_details(media_id, media_type):
    # Determine the base URL based on media type
    base_url = f"https://api.themoviedb.org/3/{media_type}/{media_id}"

    params = {"api_key": api_key}
    response = requests.get(base_url, params=params)
    data = response.json()

    return data


# Trending page
def get_popular_movies(api_key, language="en-US", page=1):
    base_url = "https://api.themoviedb.org/3/movie/popular"
    params = {"api_key": api_key, "language": language, "page": page}
    response = requests.get(base_url, params=params)
    data = response.json()
    return data.get("results", [])


def get_popular_shows(api_key, language="en-US", page=1):
    base_url = "https://api.themoviedb.org/3/tv/popular"
    params = {"api_key": api_key, "language": language, "page": page}
    response = requests.get(base_url, params=params)
    data = response.json()
    return data.get("results", [])


st.set_page_config(
    page_title = "HCI -Final Project (change this lol)"
)

page = st.sidebar.selectbox(
    "Pick a page",
    ["Search Page", "Watchlist Page", "Trending Page"]
)

if page == "Search Page":
    # Search bar
    st.title("Media Search and Details")

    # Search bar
    search_query = st.text_input("Search for a movie or TV show:")

    # Search media based on user input
    media_results = search_media(search_query)

    if media_results:
        # Display media options in a selectbox
        selected_media = st.selectbox("Select a media",
                                      [item.get("title", item.get("name", "")) for item in media_results])

        for media_item in media_results:
            if selected_media == media_item.get("title", media_item.get("name", "")):
                media_id = media_item["id"]
                media_type = "movie" if "title" in media_item else "tv"

                # Display media details
                st.header(media_item.get("title", media_item.get("name", "")))

                # Display media poster
                poster_path = media_item.get("poster_path")
                if poster_path:
                    poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
                    st.image(poster_url, caption=media_item.get("title", media_item.get("name", "")),
                             use_column_width=True)

                st.subheader("Description:")
                st.write(media_item.get("overview", ""))

                st.subheader("Rating:")
                st.write(media_item.get("vote_average", ""))

                st.subheader("Actors:" if media_type == "movie" else "Main Cast:")
                credits_url = f"https://api.themoviedb.org/3/{media_type}/{media_id}/credits"
                credits_params = {"api_key": api_key}
                credits_response = requests.get(credits_url, params=credits_params)
                credits_data = credits_response.json()

                cast = credits_data.get("cast", [])[:5]  # Displaying only the first 5 actors/cast members
                for actor in cast:
                    st.write(f"- {actor['name']}")

    else:
        st.warning("No results found.")


elif page == "Watchlist Page":
    st.write("Under Construction")

elif page == "Trending Page":
    st.title("Trending Page")
    # Get popular movies and TV shows
    popular_movies_data = get_popular_movies(api_key)
    popular_shows_data = get_popular_shows(api_key)

    # Calculate the width of each column based on the number of items
    col1_width = len(popular_movies_data) / (len(popular_movies_data) + len(popular_shows_data))
    col2_width = 1 - col1_width

    # Create columns with specified width
    col1, col2 = st.columns((col1_width, col2_width))

    # Display popular movies in the first column
    with col1:
        st.subheader("Popular Movies:")
        for movie in popular_movies_data:
            poster_path = movie.get('poster_path', '')
            if poster_path:
                st.image(f"https://image.tmdb.org/t/p/w500/{poster_path}",
                         caption=f"{movie.get('title', '')} (Rating: {movie.get('vote_average', '')}/10)",
                         use_column_width=True)

    # Display popular TV shows in the second column
    with col2:
        st.subheader("Popular TV Shows:")
        for show in popular_shows_data:
            poster_path = show.get('poster_path', '')
            title = show.get('name', 'Title not available')  # Adjust 'title' to 'name' if that's the correct key
            if poster_path:
                st.image(f"https://image.tmdb.org/t/p/w500/{poster_path}",
                         caption=f"{title} (Rating: {show.get('vote_average', '')}/10)", use_column_width=True)

