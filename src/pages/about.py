import os
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="About", layout="wide", initial_sidebar_state="collapsed")

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
    default_index=1,
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
elif selected == "Corpus":
    st.switch_page("pages/corpus.py")

vert_space = '<div style="padding: 20px 5px;"></div>'
st.markdown(vert_space, unsafe_allow_html=True)

st.header("Overview")
st.write(
    "This project encompasses a corpus consisting of human-annotated explanations that describe the reasoning processes involved in solving ARC problems. This corpus is then used to fine-tune an open-source LLM to integrate it with an understanding of problem-solving strategies that resemble human thought processes."
)

st.header("Inspiration")
st.write(
    "In a paper by François Chollet titled “On the Measure of Intelligence” the author offers a transformative perspective on evaluating and advancing AI systems. He claims that the current “task-specific” approach to measuring the intelligence of these machine-learning systems is inadequate."
)

st.write(
    "According to him, these approaches cannot capture the essence of true intelligence, which is significantly influenced by an entity's skill-acquisition efficiency across varying domains. Based on this, the author created the Abstraction and Reasoning Corpus (ARC), a benchmark to evaluate machine-learning systems on tasks that require human-like general fluid intelligence."
)

st.write(
    "The tasks in the ARC challenge emphasize the importance of innate priors and the ability to generalize from minimal data. Based on Chollet's foundation, in this project, we aim to solve the ARC challenge by leveraging a novel approach that combines human insights with the power of large language models."
)


st.header("Workflow")
st.subheader("Visualization")
st.write(
    "We've developed a script to convert all ARC tasks from JSON to images, which, along with the human annotations, form a part of the corpus. The conversion is necessary to provide a visual aid for manually writing the annotations, which is distributed among annotators."
)
st.subheader("Visual Annotation of training data")
st.write(
    "We provide a high-level overview of our annotation process, focusing on human natural language descriptions for each ARC task. Specifically, we utilize the following methods:"
)
st.markdown("##### High Level Description")
st.write(
    "Informed by Kumar et al.'s findings on neural models learning human inductive bias through natural language abstraction, we prioritize abstract descriptions. For instance, if a pattern resembles an ax, we describe it as such rather than focusing on pixel, row, or column specifics."
)
st.image("./src/static/images/one.png", width=300)
st.write(
    "This approach aims to enhance accuracy in solving ARC tasks, leveraging the handcrafted nature of the dataset."
)
st.markdown("##### Chain of Thought")
st.write(
    "Instead of directly prediction for a standard workflow, our model will generate a step-by-step guide on how to solve the given task for each input from the corpus, and then it will use this guide to predict an output. In LLM literature, such an approach to solving a problem is called chain-of-thought prompting."
)
st.image("./src/static/images/two.png", width=1000)
st.markdown("##### Helper Functions & Instructions")
st.write(
    "As a last step, by annotating each task with specific helper functions and providing program instructions, the gap between human understanding of abstract patterns and machine-readable algorithms would be effectively bridged. Essentially, the helper functions and program instructions distill human insights into a form that machines can learn from, enhancing the models' ability to mimic human problem-solving strategies and improving their performance on abstract reasoning challenges."
)

st.image("./src/static/images/three.png", width=1000)

st.markdown("##### Annotation Specifics")
st.write(
    "Paying attention to the following aspects, we generate sentence-level annotations for each task: Reflection, Pixel/Object Changes, Helper Functions, and Program Instructions. Here's a breakdown of each section:\n1.Reflections: This part outlines the underlying logic or pattern of the problem, providing a high-level understanding of the solution. It describes how a human might generally approach solving the problem based on the observations made from the inputs and outputs.\nPixel/Object Changes: Here, we detail the specific alterations made to the objects or pixels within the grid. This includes identifying relevant objects or groups of pixels and describing the changes they undergo, such as movements, colour changes, expansions, or contractions, to achieve the desired output.\nHelper Functions: We list the predefined helper functions used in the solution. These functions perform object detection, colour replacement, grid manipulation, object merging, and so on. These functions serve as building blocks for constructing the step-by-step solution for the reasoning task.\nProgram Instructions: This section provides a sequential guide for executing the solution using the previously mentioned helper functions. It is a detailed algorithm that, when followed, would lead from the input grid to the output grid."
)
st.subheader("Pilot studies")
st.write(
    "Pilot studies have been conducted on a few annotations, guiding our annotation approach. We conducted two phases of pilot studies, annotating 14 samples in total. Initially, we focused solely on reflections, but subsequent discussions highlighted issues like data alignment and color representation. In the second trial, we annotated all specified sections, streamlined the process with Google Sheets and image conversion scripts, and refined our annotation style to better suit our goals. Additionally, annotator training will cover technical details, such as the meaning of helper functions, and ensure consistency in writing style."
)
st.subheader("Experimenting with annotation options")
st.write(
    "We experimented with different forms of annotation during milestone2. Originally our annotation contained the fields Filename, Reflections, Pixel Changes, Object Changes, Helper Functions, Overall Pattern and Program Instructions. However during our initial annotations, as seen at /data/annotations/archived, we discovered some of the fields are redundant or unclear in purpose. For example, Reflections and Overall Pattern are quite similar. They differ in detailness but the difference is not important in downstream tasks. Therefore we chose to merge them together. We also merged Pixel Changes and Objects Changes to Pixel/Object Changes because most tasks are best described by either one of them."
)
st.subheader("Interface for public access")

st.write(
    'With the desire to showcase the depth of human understanding and computational strategies required to solve ARC tasks, we chose to focus on reflection and helper functions for the annotated search functionality. "Reflections" give a quick, abstract insight into the problem-solving required, appealing to users interested in the cognitive aspects of the dataset. In contrast, helper functions cater to those more interested in the programming challenge, providing a bridge between abstract reasoning and practical coding exercises.'
)

st.header("Impact")
st.write(
    "Our project’s significant impact lies in the unique dataset we created by annotating the Abstraction and Reasoning Corpus (ARC). By integrating detailed, step-by-step human-like logic and reasoning patterns into these annotations, we have hoped to create a link between the few-shot capabilities of human reasoning and machine learning models. This project is a step toward developing AI systems that can understand and mimic human-like thought processes. Furthermore, in this project, we finetuned an LLM to autonomously generate explanations and solve ARC tasks based on the chain of thought prompting, demonstrating a proof of concept for future research and the potential of our annotated dataset."
)
st.header("Team")
team_members = [
    {
        "name": "Robin",
        "image": "./src/static/images/robin.jpg",
        "github": "https://github.com/alice",
    },
    {
        "name": "Prakul",
        "image": "./src/static/images/prakul.jpg",
        "github": "https://github.com/bob",
    },
    {
        "name": "Mandeep",
        "image": "./src/static/images/mandeep.jpg",
        "github": "https://github.com/charlie",
    },
    {
        "name": "Spencer",
        "image": "./src/static/images/spencer.jpg",
        "github": "https://github.com/dave",
    },
]

cols = st.columns(len(team_members))

for i, member in enumerate(team_members):
    with cols[i]:
        st.image(member["image"], use_column_width="auto", caption=member["name"])
        # st.markdown(
        #     f'<a href="{member["github"]}" target="_blank">{member["name"]}</a>',
        #     unsafe_allow_html=True,
        # )
