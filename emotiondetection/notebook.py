import marimo

__generated_with = "0.13.10"
app = marimo.App(width="medium")


@app.cell
def _():
    from fer import FER
    from fer import Video
    import pandas as pd
    import marimo as mo
    from tqdm import tqdm
    from pathlib import Path
    return FER, Path, Video, mo, tqdm


@app.cell
def _(mo):
    mo.md(r"""# Emotiondetection Test""")
    return


@app.cell
def _(Path):
    # Declare Base dir for file
    BASE_DIR = Path("/Users/linussilberstein/Documents/ca/emotiondetection/")
    return (BASE_DIR,)


@app.cell
def _(FER):
    # Define pre-trained emotion detector
    emotion_detector = FER(mtcnn=True)
    return (emotion_detector,)


@app.cell
def _(BASE_DIR, Video):
    video_path = BASE_DIR / "Heidi Reichinnek Rede.mp4"
    video = Video(str(video_path))
    return (video,)


@app.cell
def _(emotion_detector, tqdm, video):
    with tqdm([]):
        result = video.analyze(emotion_detector, display=True)
    return (result,)


@app.cell
def _(result, video):
    emotions_df = video.to_pandas(result)
    emotions_df.head()
    return


if __name__ == "__main__":
    app.run()
