import torch
# --- MLM MASKING ---
# --- MLM MASKING ---
def mask_tokens(input_ids, vocab_size, mask_token_id, pad_token_id, mlm_prob=0.15):
    '''
    TODO: Implement MLM masking
    Args:
        input_ids: Input IDs
        vocab_size: Vocabulary size
        mask_token_id: Mask token ID
        pad_token_id: Pad token ID
    '''
    labels = input_ids.clone()
    probability_matrix = torch.full(input_ids.shape, mlm_prob)
    special_tokens_mask = (input_ids == pad_token_id) | (input_ids == mask_token_id)
    probability_matrix.masked_fill_(special_tokens_mask, value=0.0)
    masked_indices = torch.bernoulli(probability_matrix).bool()

    indices_replaced = torch.bernoulli(torch.full(input_ids.shape, 0.8)).bool() & masked_indices
    input_ids[indices_replaced] = mask_token_id

    indices_random = torch.bernoulli(torch.full(input_ids.shape, 0.5)).bool() & masked_indices & ~indices_replaced
    random_words = torch.randint(vocab_size, input_ids.shape, dtype=torch.long)
    input_ids[indices_random] = random_words[indices_random]

    labels[~masked_indices] = -100
    return input_ids, labels


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