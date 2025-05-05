import streamlit as st
import av
import numpy as np
import altair as alt
import pandas as pd
from sklearn import preprocessing


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
                    #progress_bar.progress(counter / frame_counter)
    
    df = pd.DataFrame(images)
    minmaxScaler = preprocessing.MinMaxScaler()
    print(df["lightness"].values)
    df["lightness_norm"] = minmaxScaler.fit_transform(df["lightness"].values.reshape(-1, 1))
    df["entropy_norm"] = minmaxScaler.fit_transform(df["entropy"].values.reshape(-1, 1))
    return df

st.markdown(
    """
    # Basic Video Processing App
    """
)

with st.sidebar:
    st.title("Settings")
    file = st.file_uploader("Select a video file", type=["mp4", "avi", "mov", "mkv", "m4v"])
    if file is not None:
        images = load_images(file)

dv, imsel, cv = st.tabs(["Distant Viewing", "Image Selection", "Close View"])

with dv:
    linechart = alt.Chart(images.reset_index()).encode(x="x")
    st.altair_chart(
        alt.layer(
            linechart.mark_line(color="grey").encode(y="lightness_norm:Q", x="index:Q"),
            linechart.mark_line(color="black").encode(y="entropy_norm:Q", x="index:Q"),
        ), use_container_width=True
    )
    scatterplot = alt.Chart(images.reset_index()).encode(x="x")
    st.altair_chart(
        scatterplot.mark_circle().encode(
            x="lightness_norm:Q",
            y="entropy_norm:Q",
        ), use_container_width=True
    )

with imsel:
    selectedFrame = st.slider("Timestamp", 0, len(images) - 1, 0, key="timestamp_slider")
    st.image(images.at[selectedFrame, "frame"], use_column_width=True)

with cv:
    col1, col2 = st.columns(2)

    with col1:
        st.image(images.at[selectedFrame, "frame"], use_column_width=True)

    with col2:
        arr = np.array(images.at[selectedFrame, "frame"])
        r = arr[:, :, 0].flatten()
        g = arr[:, :, 1].flatten()
        b = arr[:, :, 2].flatten()
        img_df = pd.DataFrame({"r": r, "g": g, "b": b})
        #st.dataframe(img_df)

        chart = alt.Chart(img_df).mark_bar().encode(
            alt.X("r:Q", bin=True),
            y="count()",
        )
        st.altair_chart(
            alt.layer(
                chart.mark_line(color="red").encode(y="count()", x="r:Q"),
                chart.mark_line(color="green").encode(y="count()", x="g:Q"),
                chart.mark_line(color="blue").encode(y="count()", x="b:Q"),
            ), use_container_width=True
        )