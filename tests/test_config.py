from pathlib import Path

from bclosure.config import load_config


def test_load_reference_config() -> None:
    path = Path(__file__).parents[1] / "configs" / "synthetic_hadamard.yaml"
    config = load_config(path)
    assert config.name == "synthetic_hadamard_1024"
    assert config.operator["size"] == 1024
