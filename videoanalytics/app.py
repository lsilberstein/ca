import streamlit as st
import av
from pathlib import Path
from PIL import Image
import numpy as np
import altair as alt
import pandas as pd


@st.cache_resource
def load_images(file):
    images = []
    if file is not None:
        with st.spinner("Loading video..."):
            with av.open(file) as f:
                counter = 0
                for frame in f.decode(video=0):
                    lightness = np.mean(np.array(frame.to_image().convert("L")) / 255)
                    images.append({
                        "frame": frame.to_image(),
                        "timestamp": frame.time,
                        "index": counter,
                        "lightness": lightness,
                        "width": frame.width,
                        "height": frame.height,
                        "entropy": frame.to_image().entropy(),
                    })
                    # append more imformation to the images if needed
                    counter += 1
    
    df = pd.DataFrame(images)
    return df

st.markdown(
    """
    # Basic Video Processing App
    """
)

with st.sidebar:
    st.title("Settings")
    file = st.file_uploader("Select a video file", type=["mp4", "avi", "mov", "mkv"])
    if file is not None:
        images = load_images(file)

dv, imsel, cv = st.tabs(["Distant Viewing", "Image Selection", "Close View"])

with dv:
    #st.dataframe(images)
    linechart = alt.Chart(images.reset_index()).encode(x="x")
    st.altair_chart(
        alt.layer(
            linechart.mark_line(color="grey").encode(y="lightness:Q", x="index:Q"),
            linechart.mark_line(color="black").encode(y="entropy:Q", x="index:Q"),
        ), use_container_width=True
    )
    scatterplot = alt.Chart(images.reset_index()).encode(x="x")
    st.altair_chart(
        scatterplot.mark_circle().encode(
            x="lightness:Q",
            y="entropy:Q",
            color=alt.condition(alt.datum.entropy > 3, alt.value("grey"), alt.value("black")),
        ), use_container_width=True
    )

with imsel:
    selectedFrame = st.slider("Timestamp", 0, len(images) - 1, 0, key="timestamp_slider")
    st.image(images.at[selectedFrame, "frame"], use_column_width=True)

with cv:
    st.image(images.at[selectedFrame, "frame"], use_column_width=True)