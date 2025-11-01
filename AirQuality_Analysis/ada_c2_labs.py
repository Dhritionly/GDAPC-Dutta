from __future__ import annotations

"""Utilities for working with EPA air-quality data and generating synthetic IDs.

This module collects helper functions originally created for Coursera lab
exercises and updates them with modern Python best practices. The public API
remains backwards compatible while the implementations now provide stronger
validation, clearer documentation, and better performance characteristics.
"""

import random
import string
from functools import lru_cache
from pathlib import Path
from typing import Sequence

import pandas as pd

DEFAULT_EPA_DATA_PATH = Path(__file__).resolve().parent / "c2_epa_air_quality.csv"

EPA_KEY_TO_COLUMN = {
    "state": "state_name",
    "county": "county_name",
    "aqi": "aqi",
}

_ALLOWED_ID_CHARACTERS: tuple[str, ...] = tuple(string.ascii_lowercase + string.digits)
_LOGNORMAL_LOCATION = 2.5
_LOGNORMAL_SCALE = 1.5
_MAX_PURCHASES_PER_CUSTOMER = 6

__all__ = ["fetch_epa", "id_gen", "lists_gen", "sales_data_generator"]


class AirQualityDataError(RuntimeError):
    """Raised when EPA air-quality data cannot be loaded or parsed."""


def _ensure_integer(name: str, value: int, *, minimum: int | None = None) -> None:
    """Validate that ``value`` is an integer and optionally enforce a minimum."""

    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer, got {type(value).__name__}.")
    if minimum is not None and value < minimum:
        raise ValueError(
            f"{name} must be at least {minimum}, received {value}."
        )


def _resolve_dataset_path(csv_path: str | Path) -> Path:
    """Return a resolved path to the EPA dataset, ensuring the file exists."""

    path = Path(csv_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(
            f"EPA air-quality dataset not found at '{path}'. "
            "Provide a valid path via the 'csv_path' argument."
        )
    return path


@lru_cache(maxsize=1)
def _cached_epa_dataframe(path_str: str) -> pd.DataFrame:
    """Load and cache the EPA dataset to avoid redundant disk I/O."""

    try:
        dataframe = pd.read_csv(
            path_str,
            usecols=list(EPA_KEY_TO_COLUMN.values()),
            dtype={
                "state_name": "category",
                "county_name": "category",
                "aqi": "float32",
            },
        )
    except pd.errors.EmptyDataError as exc:  # pragma: no cover - defensive branch
        raise AirQualityDataError(
            f"EPA dataset at '{path_str}' is empty or corrupted."
        ) from exc
    except ValueError as exc:  # pragma: no cover - defensive branch
        raise AirQualityDataError(
            f"EPA dataset at '{path_str}' could not be parsed: {exc}"
        ) from exc

    return dataframe


def fetch_epa(key: str, csv_path: str | Path = DEFAULT_EPA_DATA_PATH) -> list[str | float]:
    """Return values for the requested EPA dataset column.

    Parameters
    ----------
    key:
        One of ``"state"`, ``"county"``, or ``"aqi"``.
    csv_path:
        Optional path to the EPA dataset CSV. Defaults to the dataset
        distributed alongside this module.

    Returns
    -------
    list[str | float]
        A list containing the column values.

    Raises
    ------
    FileNotFoundError
        If the dataset cannot be located.
    KeyError
        If ``key`` is not a supported column identifier.
    AirQualityDataError
        If the dataset is empty or cannot be parsed.
    """

    if not isinstance(key, str):
        raise TypeError(f"key must be a string, got {type(key).__name__}.")

    normalized_key = key.strip().lower()
    if normalized_key not in EPA_KEY_TO_COLUMN:
        expected = ", ".join(sorted(EPA_KEY_TO_COLUMN))
        raise KeyError(f"Invalid key '{key}'. Expected one of: {expected}.")

    dataset_path = _resolve_dataset_path(csv_path)
    dataframe = _cached_epa_dataframe(dataset_path.as_posix())
    column_name = EPA_KEY_TO_COLUMN[normalized_key]
    return dataframe[column_name].tolist()


def id_gen(
    n_chars_id: int,
    n_samples: int,
    *,
    seed: int | None = 0,
    characters: Sequence[str] | None = None,
) -> list[str]:
    """Generate ``n_samples`` synthetic IDs comprised of lowercase letters and digits.

    Parameters
    ----------
    n_chars_id:
        Number of characters for each ID. Must be greater than zero.
    n_samples:
        Number of IDs to generate. Must be zero or greater.
    seed:
        Optional integer seed controlling deterministic output. If ``None``,
        system randomness is used.
    characters:
        Optional custom character pool. When ``None`` the pool defaults to all
        lowercase letters and digits.

    Returns
    -------
    list[str]
        Generated IDs.
    """

    _ensure_integer("n_chars_id", n_chars_id, minimum=1)
    _ensure_integer("n_samples", n_samples, minimum=0)

    if characters is None:
        character_pool = _ALLOWED_ID_CHARACTERS
    else:
        character_pool = tuple(characters)
        if not character_pool:
            raise ValueError("characters must contain at least one character.")

    if seed is None:
        rng = random.SystemRandom()
        return ["".join(rng.choices(character_pool, k=n_chars_id)) for _ in range(n_samples)]

    base_seed = seed
    return [
        "".join(random.Random(base_seed + index).choices(character_pool, k=n_chars_id))
        for index in range(n_samples)
    ]


def lists_gen(
    n_chars_id: int,
    n_pool: int,
    n_feedback_ids: int,
    n_verified_ids: int,
    *,
    seed: int | None = None,
) -> tuple[list[str], list[str]]:
    """Create ``feedback`` and ``verified`` ID lists sampled from a shared pool.

    Parameters
    ----------
    n_chars_id:
        Number of characters in each ID.
    n_pool:
        Size of the intermediate ID pool from which samples are drawn.
    n_feedback_ids:
        Number of feedback IDs to sample.
    n_verified_ids:
        Number of verified IDs to sample.
    seed:
        Optional seed applied to both ID generation and sampling steps.

    Returns
    -------
    tuple[list[str], list[str]]
        Two lists containing the sampled IDs.
    """

    _ensure_integer("n_pool", n_pool, minimum=0)
    _ensure_integer("n_feedback_ids", n_feedback_ids, minimum=0)
    _ensure_integer("n_verified_ids", n_verified_ids, minimum=0)

    if n_feedback_ids > n_pool or n_verified_ids > n_pool:
        raise ValueError(
            "n_pool must be greater than or equal to both n_feedback_ids and n_verified_ids."
        )

    pool = id_gen(n_chars_id, n_pool, seed=seed)
    rng = random.Random(seed) if seed is not None else random.SystemRandom()

    verified_ids = rng.sample(pool, k=n_verified_ids)
    feedback_ids = rng.sample(pool, k=n_feedback_ids)
    return verified_ids, feedback_ids


def sales_data_generator(n_customers: int, seed: int | None = None) -> list[list[float]]:
    """Generate synthetic purchase histories for ``n_customers``.

    Each customer receives between zero and six purchases. Purchase values are
    drawn from a log-normal distribution and rounded to two decimal places.

    Parameters
    ----------
    n_customers:
        Number of customers to generate. Must be zero or greater.
    seed:
        Optional integer seed controlling determinism. When ``None`` the global
        random generator chooses a seed based on system entropy.

    Returns
    -------
    list[list[float]]
        A nested list where each inner list contains the sales amounts for a
        single customer.
    """

    _ensure_integer("n_customers", n_customers, minimum=0)

    rng = random.Random(seed) if seed is not None else random.Random()

    sales_records: list[list[float]] = []
    for _ in range(n_customers):
        n_sales = rng.randint(0, _MAX_PURCHASES_PER_CUSTOMER)
        customer_sales = [
            round(rng.lognormvariate(_LOGNORMAL_LOCATION, _LOGNORMAL_SCALE), 2)
            for _ in range(n_sales)
        ]
        sales_records.append(customer_sales)

    return sales_records
