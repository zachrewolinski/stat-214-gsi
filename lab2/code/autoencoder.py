import lightning as L
import torch


class Autoencoder(L.LightningModule):
    def __init__(
        self, optimizer_config=None, n_input_channels=8, patch_size=9, embedding_size=8
    ):
        super().__init__()

        if optimizer_config is None:
            optimizer_config = {}
        self.optimizer_config = optimizer_config

        # Below is the definition of the encoder and decoder.
        # Is this the best encoder-decoder architecture to use here?
        # Probably not. It doesn't take advantage of the structure of the data,
        # as it completely flattens the images before encoding.
        # Maybe a convolutional autoencoder would be better?
        # Or maybe this simple architecture with more/fewer layers,
        # more/fewer nodes, or different activation functions would be better?

        input_size = int(n_input_channels * (patch_size**2))
        self.encoder = torch.nn.Sequential(
            torch.nn.Flatten(start_dim=1, end_dim=-1),
            torch.nn.Linear(input_size, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, embedding_size),
        )

        self.decoder = torch.nn.Sequential(
            torch.nn.Linear(embedding_size, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, input_size),
            torch.nn.Unflatten(1, (n_input_channels, patch_size, patch_size)),
        )

    def forward(self, batch):
        """
        Forward pass through the network.
        Args:
            batch: A tensor of shape (batch_size, n_input_channels, width, height)
        Returns:
            A tensor of shape (batch_size, n_input_channels, width, height)
        """

        # all the autencoder does is encode then decode the input tensor
        encoded = self.encoder(batch)
        decoded = self.decoder(encoded)
        return decoded

    def training_step(self, batch, batch_idx):
        """
        Training step for the autoencoder.
        Args:
            batch: A tensor of shape (batch_size, n_input_channels, width, height)
            batch_idx: The index of the batch
        Returns:
            The training loss of the autoencoder on the batch
        """

        # we encode then decode.
        encoded = self.encoder(batch)
        decoded = self.decoder(encoded)

        # the loss I have put is the MSE between the input tensor and the decoded tensor
        loss = torch.nn.functional.mse_loss(batch, decoded)
        # you can consider other possible loss functions, or add additional terms
        # to this loss.
        # for instance, could it be good to add a term that encourages sparsity
        # in the embedding?

        # log the training loss for experiment tracking purposes
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        """
        Validation step for the autoencoder.
        Args:
            batch: A tensor of shape (batch_size, n_input_channels, width, height)
            batch_idx: The index of the batch
        Returns:
            The validation loss of the autoencoder on the batch
        """

        # we encode then decode.
        encoded = self.encoder(batch)
        decoded = self.decoder(encoded)

        # the loss I have put for validation is the MSE
        # between the input tensor and the decoded tensor
        loss = torch.nn.functional.mse_loss(batch, decoded)
        # log the validation loss for experiment tracking purposes
        self.log("val_loss", loss)
        return loss

    def configure_optimizers(self):
        # set up the optimizer.
        optimizer = torch.optim.Adam(self.parameters(), **self.optimizer_config)
        return optimizer

    def embed(self, x):
        """
        Embeds the input tensor.
        Args:
            x: A tensor of shape (batch_size, n_input_channels, width, height)
        Returns:
            A tensor of shape (batch_size, embedding_size)
        """
        return self.encoder(x)
