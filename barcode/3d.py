import marimo

__generated_with = "0.12.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    import av
    import os
    from tqdm import tqdm
    from pathlib import Path
    from PIL import Image
    import plotly.express as px
    import pandas as pd
    import numpy as np
    return Image, Path, av, mo, np, os, pd, px, tqdm


@app.cell
def _(mo):
    mo.md(
        r"""
        # 3D-Plots von Videos

        Ich möchte einen interaktiven 3d Plot über die spatial und zeitachse eines Videos erzeugen. Dafür werde ich Plotly verwenden.
        """
    )
    return


@app.cell
def _(Path):
    # Declare Base dir for file
    BASE_DIR = Path("/Users/linussilberstein/Documents/ca/")
    return (BASE_DIR,)


@app.cell
def _(BASE_DIR, av, np, pd, tqdm):
    def load_images():
        with av.open(BASE_DIR / "data/bad apple.mp4") as f:
            images = []
            n = total=f.streams.video[0].frames
            width, height = f.streams.video[0].width, f.streams.video[0].height
            for (i, frame) in tqdm(zip(range(n), f.decode(video=0)), total=f.streams.video[0].frames):
                if i % 1000 == 0:
                    frame_as_arr = np.asarray(frame.to_image().convert("L"))
                    for (x, row) in zip(range(len(frame_as_arr)), frame_as_arr):
                        for (y, val) in zip(range(len(row)), row):
                            if val <= 200: 
                                images.append({"i": i, "x": x, "y": y, "val":val})
    
        return images

    df = pd.DataFrame(load_images())
    df
    return df, load_images


@app.cell
def _(df, mo, px):
    mo.ui.plotly(
        figure=px.scatter_3d(df, x="x", y="y", z="i", color_continuous_scale="Viridis", color="val")
    )
    return


if __name__ == "__main__":
    app.run()
