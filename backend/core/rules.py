from pathlib import Path

import pandas as pd
import yaml

RULES_DIR = Path(__file__).resolve().parent.parent / "rules"


def load_rules(name: str) -> list[dict]:
    path = RULES_DIR / f"{name}.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return data
    return data


def apply_rule(df: pd.DataFrame, expr: str, **env) -> pd.DataFrame:
    return df.query(expr, local_dict=env, engine="python")
