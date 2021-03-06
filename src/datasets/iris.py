import os
import numpy as np
import pandas as pd
import torch
from pytorch_lightning import LightningDataModule
from torch.utils.data import DataLoader, random_split
from src.datasets.base_dataset import BaseSagemakerDataset


class IrisDataset(BaseSagemakerDataset):

    name = "IRIS"

    def __init__(
        self,
        val_split: float = 0.3,
        num_workers: int = 16,
        seed: int = 42,
        P=None,
        *args,
        **kwargs,
    ):
        super().__init__(val_split=val_split, P=P, *args, **kwargs)
        self.num_workers = num_workers
        self._seed = seed

    @property
    def num_features(self):
        return 4

    @property
    def num_classes(self):
        return 3

    @property
    def hyper_parameters(self):
        return {"num_features": self.num_features, "num_classes": self.num_classes}

    def _labelize(self, raw_data):
        labels = raw_data[:, 0]
        self.unique_labels = np.unique(labels)
        self._num_classes = len(self.unique_labels)
        for idx, u in enumerate(self.unique_labels):
            labels[labels == u] = idx

    @staticmethod
    def process(raw_data):
        return torch.from_numpy(raw_data.values.astype(np.float)).float()

