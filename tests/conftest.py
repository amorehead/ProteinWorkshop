"""This file prepares config fixtures for other tests."""

from pathlib import Path

import pyrootutils
import pytest
from graphein.protein.tensor.data import (ProteinBatch, get_random_batch,
                                          get_random_protein)
from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra
from omegaconf import DictConfig, open_dict


@pytest.fixture(scope="package")
def cfg_train_global() -> DictConfig:
    """A pytest fixture for setting up a default Hydra DictConfig for training.

    :return: A DictConfig object containing a default Hydra configuration for training.
    """
    with initialize(version_base="1.3", config_path="../configs"):
        cfg = compose(config_name="train.yaml", return_hydra_config=True, overrides=[])

        # set defaults for all tests
        with open_dict(cfg):
            cfg.env.paths.root_dir = str(
                pyrootutils.find_root(indicator=".project-root")
            )
            cfg.trainer.max_epochs = 1
            cfg.trainer.limit_train_batches = 0.01
            cfg.trainer.limit_val_batches = 0.1
            cfg.trainer.limit_test_batches = 0.1
            cfg.trainer.accelerator = "cpu"
            cfg.trainer.devices = 1
            cfg.dataset.datamodule.num_workers = 0
            cfg.dataset.datamodule.pin_memory = False
            cfg.extras.print_config = False
            cfg.extras.enforce_tags = False
            cfg.logger = None

    return cfg


@pytest.fixture(scope="package")
def cfg_finetune_global() -> DictConfig:
    """A pytest fixture for setting up a default Hydra DictConfig for evaluation.

    :return: A DictConfig containing a default Hydra configuration for evaluation.
    """
    with initialize(version_base="1.3", config_path="../configs"):
        cfg = compose(
            config_name="finetune.yaml",
            return_hydra_config=True,
            overrides=["ckpt_path=."],
        )

        # set defaults for all tests
        with open_dict(cfg):
            cfg.env.paths.root_dir = str(
                pyrootutils.find_root(indicator=".project-root")
            )
            cfg.trainer.max_epochs = 1
            cfg.trainer.limit_test_batches = 0.1
            cfg.trainer.accelerator = "cpu"
            cfg.trainer.devices = 1
            cfg.dataset.datamodule.num_workers = 0
            cfg.dataset.datamodule.pin_memory = False
            cfg.extras.print_config = False
            cfg.extras.enforce_tags = False
            cfg.logger = None

    return cfg


@pytest.fixture(scope="function")
def cfg_train(cfg_train_global: DictConfig, tmp_path: Path) -> DictConfig:
    """A pytest fixture built on top of the `cfg_train_global()` fixture,
    which accepts a temporary logging path `tmp_path` for generating a
    temporary logging path.

    This is called by each test which uses the `cfg_train` arg. Each test
    generates its own temporary logging path.

    :param cfg_train_global: The input DictConfig object to be modified.
    :param tmp_path: The temporary logging path.

    :return: A DictConfig with updated output and log directories corresponding
        to `tmp_path`.
    """
    cfg = cfg_train_global.copy()

    with open_dict(cfg):
        cfg.env.paths.output_dir = str(tmp_path)
        cfg.env.paths.log_dir = str(tmp_path)

    yield cfg

    GlobalHydra.instance().clear()


@pytest.fixture(scope="function")
def cfg_finetune(cfg_finetune_global: DictConfig, tmp_path: Path) -> DictConfig:
    """
    A pytest fixture built on top of the `cfg_finetune_global()` fixture,
    which accepts a temporary logging path `tmp_path` for generating a
    temporary logging path.

    This is called by each test which uses the `cfg_finetune` arg. Each test
    generates its own temporary logging path.

    :param cfg_train_global: The input DictConfig object to be modified.
    :param tmp_path: The temporary logging path.

    :return: A DictConfig with updated output and log directories corresponding
        to `tmp_path`.
    """
    cfg = cfg_finetune_global.copy()

    with open_dict(cfg):
        cfg.env.paths.output_dir = str(tmp_path)
        cfg.env.paths.log_dir = str(tmp_path)

    yield cfg

    GlobalHydra.instance().clear()


@pytest.fixture(scope="function")
def test_batch() -> ProteinBatch:
    """Creates a random batch of proteins for testing"""
    batch = ProteinBatch().from_protein_list(
        [get_random_protein() for _ in range(4)], follow_batch=["coords"]
    )

    batch.batch = batch.coords_batch
    batch.edges("knn_8", cache="edge_index")
    batch.pos = batch.coords[:, 1, :]
    batch.x = batch.residue_type
    return batch
