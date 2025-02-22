import glob
import numpy as np


def make_data(patch_size=9):
    """
    Load the image data and create patches from it.
    Feel free to play around with the choice of patch size.
    Args:
        patch_size: The size of the patches to create
    Returns:
        images_long: A list of numpy arrays of the original images
        patches: A list of lists of patches for each image
    """

    # load images
    # find all .npz files in the directory
    filepaths = glob.glob("../data/*.npz")
    images_long = []
    for fp in filepaths:
        npz_data = np.load(fp)
        # assuming the array is stored under the first key:
        key = list(npz_data.files)[0]
        data = npz_data[key]
        if data.shape[1] == 11:
            data = data[:,:-1]  # remove labels
        images_long.append(data)

    # use first column as y and second column as x
    y = images_long[0][:, 0]
    x = images_long[0][:, 1]

    # calculate width and height of images
    width = int(max(x) - min(x) + 1)
    height = int(max(y) - min(y) + 1)

    # calculate number of channels
    nchannels = images_long[0].shape[1] - 2

    # reshape each image
    images = []
    for img in images_long:
        image = np.zeros((nchannels, int(height), int(width)))
        y = img[:, 0].astype(int)
        x = img[:, 1].astype(int)

        # Compute relative coordinates
        y_rel = y - min(y)
        x_rel = x - min(x)

        # Create a mask to filter out out-of-bounds values
        valid_mask = (y_rel >= 0) & (y_rel < int(height)) & (x_rel >= 0) & (x_rel < int(width))

        # Apply the mask
        y_valid = y_rel[valid_mask]
        x_valid = x_rel[valid_mask]
        img_valid = img[valid_mask]  # Keep only valid rows

        # Fill image array
        for i in range(nchannels):
            image[i, y_valid, x_valid] = img_valid[:, i + 2]

        images.append(image)

    print('done reshaping images')

    # convert to 4d array (nimages, nchannels, height, width)
    images = np.array(images)

    # for every pixel in every image, we will get a 9x9 normalized
    # patch around it containing all channels
    pad_len = patch_size // 2

    # get normalization constants for the channels
    means = np.mean(images, axis=(0, 2, 3))[:, None, None]
    stds = np.std(images, axis=(0, 2, 3))[:, None, None]
    images = (images - means) / stds

    patches = []
    for i in range(len(images_long)):
        if (i%10 == 0):
            print(f'working on image {i}')
        patches_img = []

        # pad the image by mirroring across the border.
        # Is mirroring the best choice?
        img_mirror = np.pad(
            images[i],
            ((0, 0), (pad_len, pad_len), (pad_len, pad_len)),
            mode="reflect",
        )

        # get the coordinates of the pixels in the original image
        ys = images_long[i][:, 0]
        miny = min(ys)
        xs = images_long[i][:, 1]
        minx = min(xs)

        # iterating over pixels, get the patch around each pixel.
        for y, x in zip(ys, xs):
            y_idx = int(y - miny + pad_len)
            x_idx = int(x - minx + pad_len)
            patch = img_mirror[
                :,
                y_idx - pad_len : y_idx + pad_len + 1,
                x_idx - pad_len : x_idx + pad_len + 1,
            ]
            patches_img.append(patch.astype(np.float32))
        patches.append(patches_img)

    return images_long, patches
