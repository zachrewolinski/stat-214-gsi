# EXAMPLE USAGE:
# python get_embedding.py configs/default.yaml checkpoints/default-epoch=009.ckpt

import sys
import torch
import pandas as pd
import numpy as np
import yaml
from tqdm import tqdm

from autoencoder import Autoencoder
from data import make_data

config_path = sys.argv[1]
checkpoint_path = sys.argv[2]

config = yaml.safe_load(open(config_path, "r"))

print("Loading the saved model")
# initialize the autoencoder class
model = Autoencoder(patch_size=config["data"]["patch_size"], **config["autoencoder"])
# tell PyTorch to load the model onto the CPU if no GPU is available
map_location = None if torch.cuda.is_available() else 'cpu'
# load checkpoint
checkpoint = torch.load(checkpoint_path, map_location=map_location)
# load the checkpoint's state_dict into the model
model.load_state_dict(checkpoint["state_dict"])
# put the model in evaluation mode
model.eval()

print("Making the patch data")
images_long, patches = make_data(patch_size=config["data"]["patch_size"])

print("Obtaining embeddings")
# get the embedding for each patch
embeddings = []  # what we will save
images_embedded = []  # for visualization

for i in tqdm(range(len(images_long))):
    ys = images_long[i][:, 0]
    xs = images_long[i][:, 1]

    # determine the height and width of the image
    miny = min(ys)
    minx = min(xs)
    height = int(max(ys) - miny + 1)
    width = int(max(xs) - minx + 1)

    # to make this faster, we use torch.no_grad() to disable gradient tracking
    with torch.no_grad():
        # get the embedding of array of patches
        emb = model.embed(torch.tensor(np.array(patches[i])))
        # NOTE: if your model is quite big, you may not be able to fit
        # all of the data into the GPU memory at once for inference.
        # In that case, you can loop over smaller bathches of data.

        # in the following line we:
        # - detach the tensor from the computation graph
        # - move it to the cpu
        # - turn it into a numpy array
        emb = emb.detach().cpu().numpy()

    embeddings.append(emb)

    # represent the embedding as an image, if you want
    img_embedded = np.zeros((emb.shape[1], height, width))
    img_embedded[:, (ys - miny).astype(int), (xs - minx).astype(int)] = emb.T
    images_embedded.append(img_embedded)

print("Saving the embeddings")
# save the embeddings as csv
for i in tqdm(range(len(images_long))):
    embedding_df = pd.DataFrame(embeddings[i], columns=[f"ae{i}" for i in range(8)])
    embedding_df["y"] = images_long[i][:, 0]
    embedding_df["x"] = images_long[i][:, 1]
    # move y and x to front
    cols = embedding_df.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    embedding_df = embedding_df[cols]
    # save to csv
    embedding_df.to_csv(f"../data/image{i+1}_ae.csv", index=False)


# here is some code to take a look at the embeddings.
# but you should probably just load the csv files in a jupyter notebook
# and visualize there.

# import matplotlib.pyplot as plt
# plt.imshow(images_embedded[0][0])
# plt.show()
