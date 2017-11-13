import json
from pathlib import Path
from typing import NamedTuple
from typing import Union

from .param import Param


class DatasetConfig(NamedTuple):
    param: Param
    input_glob: str
    target_glob: str
    input_mean_path: Path
    input_var_path: Path
    target_mean_path: Path
    target_var_path: Path
    seed: int
    num_test: int


class ModelConfig(NamedTuple):
    in_channels: int
    conv_bank_out_channels: int
    conv_bank_k: int
    max_pooling_k: int
    conv_projections_hidden_channels: int
    highway_layers: int
    out_channels: int
    out_size: int


class LossConfig(NamedTuple):
    l1: float


class TrainConfig(NamedTuple):
    batchsize: int
    gpu: int
    log_iteration: int
    snapshot_iteration: int
    output: Path


class Config(NamedTuple):
    dataset: DatasetConfig
    model: ModelConfig
    loss: LossConfig
    train: TrainConfig

    def save_as_json(self, path):
        d = _namedtuple_to_dict(self)
        json.dump(d, open(path, 'w'), indent=2, sort_keys=True, default=_default_path)


def _default_path(o):
    if isinstance(o, Path):
        return str(o)
    raise TypeError(repr(o) + " is not JSON serializable")


def _namedtuple_to_dict(o: NamedTuple):
    return {
        k: v if not hasattr(v, '_asdict') else _namedtuple_to_dict(v)
        for k, v in o._asdict().items()
    }


def create_from_json(s: Union[str, Path]):
    try:
        d = json.loads(s)
    except TypeError:
        d = json.load(open(s))

    return Config(
        dataset=DatasetConfig(
            param=Param(),
            input_glob=d['dataset']['input_glob'],
            target_glob=d['dataset']['target_glob'],
            input_mean_path=Path(d['dataset']['input_mean_path']).expanduser(),
            input_var_path=Path(d['dataset']['input_var_path']).expanduser(),
            target_mean_path=Path(d['dataset']['target_mean_path']).expanduser(),
            target_var_path=Path(d['dataset']['target_var_path']).expanduser(),
            seed=d['dataset']['seed'],
            num_test=d['dataset']['num_test'],
        ),
        model=ModelConfig(
            in_channels=d['model']['in_channels'],
            conv_bank_out_channels=d['model']['conv_bank_out_channels'],
            conv_bank_k=d['model']['conv_bank_k'],
            max_pooling_k=d['model']['max_pooling_k'],
            conv_projections_hidden_channels=d['model']['conv_projections_hidden_channels'],
            highway_layers=d['model']['highway_layers'],
            out_channels=d['model']['out_channels'],
            out_size=d['model']['out_size'],
        ),
        loss=LossConfig(
            l1=d['loss']['l1'],
        ),
        train=TrainConfig(
            batchsize=d['train']['batchsize'],
            gpu=d['train']['gpu'],
            log_iteration=d['train']['log_iteration'],
            snapshot_iteration=d['train']['snapshot_iteration'],
            output=Path(d['train']['output']).expanduser(),
        ),
    )