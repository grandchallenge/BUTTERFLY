from __future__ import annotations

import argparse
import json
from pathlib import Path

from bclosure.benchmarks import benchmark_operator
from bclosure.config import load_config
from bclosure.factories import make_operator
from bclosure.inspection import inspect_closure
from bclosure.trees import tree_from_ordering


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")


def run_inspect(config_path: str) -> Path:
    cfg = load_config(config_path)
    operator = make_operator(cfg.operator)
    inspection = dict(cfg.inspection)
    input_order = str(inspection.pop("input_order", "natural"))
    output_order = str(inspection.pop("output_order", "natural"))
    report = inspect_closure(
        operator,
        input_tree=tree_from_ordering(operator.shape[1], input_order),
        output_tree=tree_from_ordering(operator.shape[0], output_order),
        **inspection,
    )
    path = Path(cfg.output_dir) / f"{cfg.name}.closure.json"
    _write_json(path, report.to_dict())
    print(json.dumps(report.to_dict(), indent=2, default=str))
    return path


def run_benchmark(config_path: str) -> Path:
    cfg = load_config(config_path)
    operator = make_operator(cfg.operator)
    path = Path(cfg.output_dir) / f"{cfg.name}.benchmark.json"
    result = benchmark_operator(operator, artifact_path=str(path), **cfg.benchmark)
    _write_json(path, result.to_dict())
    print(json.dumps(result.to_dict(), indent=2, default=str))
    return path


def main() -> None:
    parser = argparse.ArgumentParser(prog="bclosure")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("inspect", "benchmark"):
        child = sub.add_parser(name)
        child.add_argument("config")
    args = parser.parse_args()
    if args.command == "inspect":
        run_inspect(args.config)
    elif args.command == "benchmark":
        run_benchmark(args.config)


if __name__ == "__main__":
    main()
