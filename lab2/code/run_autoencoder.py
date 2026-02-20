# EXAMPLE USAGE:
# python run_autoencoder.py configs/default.yaml

import numpy as np
import sys
import os
import yaml  # pip install pyyaml
import gc
import torch
import lightning as L

from torch.utils.data import DataLoader
from lightning.pytorch.loggers import WandbLogger
from lightning.pytorch.callbacks import ModelCheckpoint
# pip install torchinfo
# from torchinfo import summary

from autoencoder import Autoencoder
from patchdataset import PatchDataset
from data import make_data


print("loading config file")
config_path = sys.argv[1]
assert os.path.exists(config_path), f"Config file {config_path} not found"
config = yaml.safe_load(open(config_path, "r"))

# clean up memory
gc.collect()
torch.cuda.empty_cache()

print("making the patch data")
# get the patches
_, patches = make_data(patch_size=config["data"]["patch_size"])
# let's just combine the patches from all images into one list
all_patches = [patch for image_patches in patches for patch in image_patches]

# randomly do train/val split by individual patches
# (is this the best idea?)
train_bool = np.random.rand(len(all_patches)) < 0.8
train_idx = np.where(train_bool)[0]
val_idx = np.where(~train_bool)[0]

# create train and val datasets
train_patches = [all_patches[i] for i in train_idx]
val_patches = [all_patches[i] for i in val_idx]
train_dataset = PatchDataset(train_patches)
val_dataset = PatchDataset(val_patches)

# create train and val dataloaders
dataloader_train = DataLoader(train_dataset, **config["dataloader_train"])
dataloader_val = DataLoader(val_dataset, **config["dataloader_val"])

print("initializing model")
# Initialize an autoencoder object
model = Autoencoder(
    optimizer_config=config["optimizer"],
    patch_size=config["data"]["patch_size"],
    **config["autoencoder"],
)
print(model)
# print(summary(model, (8, 9, 9)))

print("preparing for training")
# configure the settings for making checkpoints
checkpoint_callback = ModelCheckpoint(**config["checkpoint"])

# if running in slurm, add slurm job id info to the config file
if "SLURM_JOB_ID" in os.environ:
    config["slurm_job_id"] = os.environ["SLURM_JOB_ID"]

# initialize the wandb logger, giving it our config file
# to save, and also configuring the logger itself.
wandb_logger = WandbLogger(config=config, **config["wandb"])

# initialize the trainer
trainer = L.Trainer(
    logger=wandb_logger, callbacks=[checkpoint_callback], **config["trainer"]
)

print("training")
trainer.fit(model, train_dataloaders=dataloader_train, val_dataloaders=dataloader_val)

# clean up memory
gc.collect()
torch.cuda.empty_cache()
