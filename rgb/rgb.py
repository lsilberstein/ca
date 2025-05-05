import marimo

__generated_with = "0.12.7"
app = marimo.App(width="medium")


@app.cell
def _():
    from PIL import Image
    import numpy as np
    import matplotlib.pyplot as plt
    return Image, np, plt


@app.cell
def _(Image, np, plt):
    im = Image.fromarray(
        np.array([[
            [1,0,1],
            [0,1,1]   
        ],[
            [1,0,0],
            [0,1,0]
        ]], dtype=np.uint8) * 255)

    imgplot = plt.imshow(im)
    imgplot
    return im, imgplot


@app.cell
def _(Image, im, plt):
    # Bilinear (without gamma correction)

    wgimg = plt.imshow(
        im.resize((255,255), resample=Image.Resampling.BILINEAR)
    )
    wgimg
    return (wgimg,)


@app.cell
def _(Image, im, np, plt):
    # With gamma correction

    def resize_with_gamma_correction(im, gamma):
        from skimage.transform import resize
    
        c1 = np.array(im) / 255
        c2 = np.power(c1, gamma)
        c3 = resize(c2, (255,255), anti_aliasing = True, mode = "edge")
        c4 = np.power(c3, 1/gamma)
        c5 = (c4.clip(0, 1) * 255).astype(np.uint8)
        return Image.fromarray(c5)

    plt.imshow(resize_with_gamma_correction(im, 2.2))
    return (resize_with_gamma_correction,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
