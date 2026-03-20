import torch
# --- MLM MASKING ---
# --- MLM MASKING ---
def mask_tokens(input_ids, vocab_size, mask_token_id, pad_token_id, mlm_prob=0.15 ):
    '''
    TODO: Implement MLM masking
    Args:
        input_ids: Input IDs
        vocab_size: Vocabulary size
        mask_token_id: Mask token ID
        pad_token_id: Pad token ID
        mlm_prob: Probability of masking
    '''
    pass

def train_bert(model, dataloader, tokenizer, epochs=3, lr=5e-4, device='cuda'):
    '''
    TODO: Implement training loop for BERT
    Args:
        model: BERT model
        dataloader: Data loader
        tokenizer: Tokenizer
        epochs: Number of epochs
        lr: Learning rate
        device: Device to run the model on
    '''
    pass