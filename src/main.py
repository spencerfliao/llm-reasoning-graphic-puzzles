# """
# Project ARCOT
# COLX 523 Advanced Corpus Linguistics
# Streamlit Web App
# """

import base64
import os
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import time
from keyword_search import KeywordSearch
from context_search import ReflectionsEmbedder, ContextSearch

# Set the page configuration
st.set_page_config(page_title="Home", layout="wide", initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
    .stApp a:first-child {
        display: none;
    }

    .css-15zrgzn {display: none}
    .css-eczf16 {display: none}
    .css-jn99sy {display: none}
</style>
""",
    unsafe_allow_html=True,
)


# Display the pages in the sidebar and handle navigation
# show_pages(
#     [
#         Page("main.py", "Home"),
#         Page("pages/about.py", "About"),
#         Page("pages/corpus.py", "Corpus"),
#     ]
# )

# st.markdown(
#     """
#     <style>
#         section[data-testid="stSidebar"] {
#             width: 200px !important; # Set the width to your desired value
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# Sidebar caption
# st.sidebar.caption("ARCOT 2024")


# navigation bar
selected = option_menu(
    None,
    ["Home", "About", "Corpus"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "width": "300px",
            "padding": "0!important",
            "background-color": "#FFFFFF",
            "margin-top": 0,
        },
        "icon": {"color": "orange", "font-size": "0px"},
        "nav-link": {
            "font-size": "15px",
            "text-align": "center",
            "margin": "0px",
            "font-family": "helvetica",
            # "--hover-color": "#EEEEEE",
        },
        "nav-link-selected": {"background-color": "#FFF", "color": "black"},
    },
)

if selected == "About":
    st.switch_page("pages/about.py")
elif selected == "Corpus":
    st.switch_page("pages/corpus.py")

vert_space = '<div style="padding: 20px 5px;"></div>'
st.markdown(vert_space, unsafe_allow_html=True)

# Main content of the home page
st.markdown("<h1 style='text-align: center;'>ARCOT</h1>", unsafe_allow_html=True)

st.markdown(
    "<h5 style='text-align: center;'>Welcome to the ARC corpus integrated with the chain-of-thoughts paradigm!</h5>",
    unsafe_allow_html=True,
)

st.markdown('<div style="padding: 30px 5px;"></div>', unsafe_allow_html=True)


def perform_search(query):
    time.sleep(2)  # Simulate a calculation or processing time
    result = f"Results for '{query}'"
    return result


embeddings_path = "./data/embeddings/embeddings.pkl"
context_search = ContextSearch(embeddings_path)
file_path = "./data/annotations/annotations.csv"
keyword_search = KeywordSearch(file_path)


def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def create_image_html(filename):
    image_path = os.path.join("data/images/training", filename)
    if os.path.exists(image_path):
        encoded_image = get_image_base64(image_path)
        return f'<img src="data:image/png;base64,{encoded_image}" width="100">'
    return "Image not found"


df = pd.read_csv("./data/annotations/annotations.csv", index_col=0)


def create_html_df(file_list):
    df_temp = df.copy()
    df_temp = df_temp.set_index("Filename")
    df_temp = df_temp.loc[file_list, :]
    df_temp = df_temp.reset_index()
    df_temp["Image"] = df_temp["Filename"].apply(create_image_html)
    df_temp.replace(to_replace=r"\n", value="<br>", regex=True, inplace=True)
    df_temp = df_temp.loc[
        :,
        [
            "Filename",
            "Image",
            "Reflections",
            "Pixel/Object Changes",
            "Helper Functions",
            "Program Instructions",
        ],
    ]

    df_temp = df_temp.to_html(escape=False)
    return df_temp


def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def create_image_html(filename):
    image_path = os.path.join("data/images/training", filename)
    if os.path.exists(image_path):
        encoded_image = get_image_base64(image_path)
        return f'<img src="data:image/png;base64,{encoded_image}" width="100">'
    return "Image not found"


col1, col2, col3 = st.columns([1, 2, 1])

with col2:

    search_type = st.radio(
        "Select search type:",
        ("Search the context", "Search the helper function"),
        horizontal=True,
    )

    st.markdown('<div style="padding: 10px 5px;"></div>', unsafe_allow_html=True)

    search_query = st.text_input(
        "E.g. 'Tasks that involve changing the size of the objects' or 'function1, function2' (both included)",
        placeholder="Search the corpus",
        key="search_query",
    )
    search_button = st.button("Search", key="search")

if search_button:
    with st.spinner("Searching..."):
        if search_type == "Search the context":
            results = context_search.search(search_query, num_results=5)
        else:
            keywords = [k.strip() for k in search_query.split(",")]
            results = keyword_search.search(
                keywords, relationship="AND", num_results="all"
            )
    if not results:
        st.write("No results")
    else:
        df_html = create_html_df(results)
        st.markdown('<div style="padding: 20px 5px;"></div>', unsafe_allow_html=True)
        st.header("Results")
        st.markdown(df_html, unsafe_allow_html=True)


# /project-root/
# │
# ├── main.py  # Main application file, the entry point of your app
# │
# ├── pages/   # Directory for individual pages
# │   ├── about.py
# │   └── corpus.py
# │
# ├── static/  # Directory for static files like images, CSS, JS, etc.
# │   └── images/  # Directory specifically for images
# │       └── logo.png  # Your logo or other images
# │
# └── data/  # Directory for storing dataframes
#     ├── df1.csv  # Example dataframe file
#     └── df2.csv  # Another example dataframe file
