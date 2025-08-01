import time
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import base64
import os

st.set_page_config(
    page_title="Corpus", layout="wide", initial_sidebar_state="collapsed"
)

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
# st.sidebar.caption("ARCOT 2024")

# navigation bar
selected = option_menu(
    None,
    ["Home", "About", "Corpus"],
    menu_icon="cast",
    default_index=2,
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

if selected == "Home":
    st.switch_page("main.py")
elif selected == "About":
    st.switch_page("pages/about.py")

vert_space = '<div style="padding: 20px 5px;"></div>'
st.markdown(vert_space, unsafe_allow_html=True)


def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def create_image_html(filename):
    image_path = os.path.join("data/images/training", filename)
    if os.path.exists(image_path):
        encoded_image = get_image_base64(image_path)
        return f'<img src="data:image/png;base64,{encoded_image}" width="100">'
    return "Image not found"


st.header("Annotations")

with st.spinner("Loading data..."):
    df = pd.read_csv("./data/annotations/annotations.csv", index_col=0)
    df["Image"] = df["Filename"].apply(create_image_html)
    df.replace(to_replace=r"\n", value="<br>", regex=True, inplace=True)
    df = df.loc[
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

df_html = df.to_html(escape=False)
st.markdown(df_html, unsafe_allow_html=True)
