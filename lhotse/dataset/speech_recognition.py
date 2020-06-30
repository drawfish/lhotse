from pathlib import Path
from typing import Dict, Optional, Tuple, List

import torch
from torch.utils.data import Dataset

from lhotse.cut import CutSet, Cut, AnyCut
from lhotse.utils import Pathlike

EPS = 1e-8


class SpeechRecognitionDataset(Dataset):
    """
    The PyTorch Dataset for the speech recognition task.
    Contains acoustic features and the corresponding text.
    """

    def __init__(
            self,
            cuts: CutSet,
            root_dir: Optional[Pathlike] = None
    ):
        super().__init__()
        self.cuts = cuts.cuts
        self.root_dir = Path(root_dir) if root_dir else None
        self.cut_ids = list(self.cuts.keys())

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        cut_id = self.cut_ids[idx]
        cut = self.cuts[cut_id]

        feature = torch.from_numpy(cut.load_features(root_dir=self.root_dir))

        return {
            'feature': feature,
            'text': cut.supervisions[0].text
        }

    def __len__(self):
        return len(self.cut_ids)
