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
    return Image, Path, av, mo, os, tqdm


@app.cell
def _(mo):
    mo.md(
        r"""
        # Experiment mit Barcodes

        In der Vorlesung wurden einige [Beispiele mit Movie Barcodes](https://www.zachwhalen.net/posts/imj-a-web-based-tool-for-visual-culture-macroanalytics) gezeigt. Dafür möchte ich solche Barcodes in diesem Notebook einmal selber erstellen. Ich verwende hierfür das [Big Buck Bunny Video](https://peach.blender.org/). Aus offensichtlichen Gründen ist das Video nicht Teil des Repositories.
        """
    )
    return


@app.cell
def _(Path):
    # Declare Base dir for file
    BASE_DIR = Path("/Users/linussilberstein/Documents/ca/")
    return (BASE_DIR,)


@app.cell
def _(BASE_DIR, Image, av, tqdm):
    def load_and_resize():
        with av.open(BASE_DIR / "data/BigBuckBunny_640x360.m4v") as f:
            images = []
            # Using a counter to only use every nth image as the barcode. In this case every 10th.
            counter = 0
            for frame in tqdm(f.decode(video=0), total=f.streams.video[0].frames):
                if (counter % 5 == 0):
                    images.append(frame.to_image().resize((1, frame.height), resample=Image.Resampling.HAMMING))
            
                counter += 1

            return images

    imagestrips = load_and_resize()
    return imagestrips, load_and_resize


@app.cell
def _(mo):
    mo.md(r"""Wir können jetzt den gesamten Array aus Barcode-Strips wieder zusammenfügen. Wir haben endgültig dann einen fertigen Barcode.""")
    return


@app.cell
def _(Image, imagestrips, tqdm):
    def create_barcode():
        sx = len(imagestrips)
        sy = imagestrips[0].height
        # Create a new canvas to paste all images on.
        # Technically this is also a montage of resized Images.
        canvas = Image.new("RGB", (sx, sy))

        for (i, image) in tqdm(zip(range(sx), imagestrips), total=sx):
            canvas.paste(
                image, box=(i, 0)
            )

        return canvas

    create_barcode()
    return (create_barcode,)


if __name__ == "__main__":
    app.run()
