from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class ExperimentConfig:
    name: str
    operator: dict[str, Any]
    inspection: dict[str, Any]
    benchmark: dict[str, Any]
    output_dir: str = "artifacts"


def load_config(path: str | Path) -> ExperimentConfig:
    with Path(path).open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    for key in ("name", "operator", "inspection", "benchmark"):
        if key not in raw:
            raise ValueError(f"missing required config key: {key}")
    return ExperimentConfig(
        name=str(raw["name"]),
        operator=dict(raw["operator"]),
        inspection=dict(raw["inspection"]),
        benchmark=dict(raw["benchmark"]),
        output_dir=str(raw.get("output_dir", "artifacts")),
    )
