import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizerFast
import random

# --- DATASET ---
class TextDataset(Dataset):
    def __init__(self, texts, tokenizer, max_len=32):
        '''
        Args:
            texts: List of stories
            tokenizer: Tokenizer
            max_len: Maximum length of the story # THIS IS JUST AN EXAMPLE
        '''
        self.encodings = tokenizer(
            texts,
            padding="max_length",
            truncation=True,
            max_length=max_len,
            return_tensors="pt"
        )

    def __len__(self):
        return len(self.encodings["input_ids"])

    def __getitem__(self, idx):
        return {
            "input_ids": self.encodings["input_ids"][idx],
            "token_type_ids": self.encodings["token_type_ids"][idx],
            "attention_mask": self.encodings["attention_mask"][idx].unsqueeze(0).unsqueeze(0)
        }

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Load tokenizer
    tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")  # or your trained tokenizer path

    # Example dataset
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Transformers are powerful models for NLP tasks.",
        "Masked language modeling trains BERT to understand context.",
        "Pretraining is followed by task-specific fine-tuning."
    ]

    dataset = TextDataset(texts, tokenizer, max_len=32)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
