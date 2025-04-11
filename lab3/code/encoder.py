import torch
import torch.nn as nn
import torch.nn.functional as F

# --- BERT-STYLE MODEL ---
class MultiHeadSelfAttention(nn.Module):
    def __init__(self, hidden_size, num_heads):
        '''
        TODO: Implement multi-head self-attention
        Args:
            hidden_size: Hidden size of the model
            num_heads: Number of attention heads
        '''
        super().__init__()
        assert hidden_size % num_heads == 0
        pass

    def forward(self, x, mask=None):
        '''
        TODO: Implement forward pass for multi-head self-attention
        Args:
            x: Input
            mask: Attention mask 
        '''
        pass

class FeedForward(nn.Module):
    def __init__(self, hidden_size, intermediate_size):
        '''
        TODO: Implement feed-forward network
        Args:
            hidden_size: Hidden size of the model
            intermediate_size: Intermediate size of the model
        '''
        super().__init__()
        pass

    def forward(self, x):
        pass

class TransformerBlock(nn.Module):
    def __init__(self, hidden_size, num_heads, intermediate_size):
        super().__init__()
        self.attn = MultiHeadSelfAttention(hidden_size, num_heads)
        self.ln1 = nn.LayerNorm(hidden_size)
        self.ffn = FeedForward(hidden_size, intermediate_size)
        self.ln2 = nn.LayerNorm(hidden_size)

    def forward(self, x, mask=None):
        '''
        TODO: Implement forward pass for transformer block
        Args:
            x: Input
            mask: Attention mask
        '''
        pass

class Encoder(nn.Module):
    def __init__(self, vocab_size, hidden_size=256, num_heads=4, num_layers=4,
                 intermediate_size=512, max_len=512):
        '''
        TODO: Implement encoder
        Args:
            vocab_size: Vocabulary size
            hidden_size: Hidden size of the model
            num_heads: Number of attention heads
            num_layers: Number of layers
            intermediate_size: Intermediate size of the model
            max_len: Maximum length of the input
        '''
        super().__init__()
        self.token_emb = nn.Embedding(vocab_size, hidden_size)
        self.pos_emb = nn.Embedding(max_len, hidden_size)
        self.type_emb = nn.Embedding(2, hidden_size)
        self.layers = nn.ModuleList([
            TransformerBlock(hidden_size, num_heads, intermediate_size)
            for _ in range(num_layers)
        ])
        self.norm = nn.LayerNorm(hidden_size)
        self.mlm_head = nn.Linear(hidden_size, vocab_size)

    def forward(self, input_ids, token_type_ids, attention_mask):
       pass
