from torch.utils.data import Dataset


class PatchDataset(Dataset):
    """
    Wrapper dataset class for our datasets of patches
    """

    def __init__(self, patches, transform=None):
        self.patches = patches
        self.transform = transform
        # self.transform is for any torchvision transforms
        # you want to apply to the patches (for data augmentation)

    def __len__(self):
        return len(self.patches)

    def __getitem__(self, idx):
        sample = self.patches[idx]
        if self.transform:
            sample = self.transform(sample)
        return sample
