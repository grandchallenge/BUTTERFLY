from pathlib import Path

from bclosure.cli import run_benchmark, run_inspect


def main() -> None:
    root = Path(__file__).parents[1]
    for name in ("synthetic_hadamard.yaml", "global_low_rank.yaml", "random_dense_control.yaml"):
        path = root / "configs" / name
        run_inspect(str(path))
        run_benchmark(str(path))


if __name__ == "__main__":
    main()
