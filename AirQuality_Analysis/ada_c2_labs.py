"""Utility functions used throughout the air quality analysis labs."""

from __future__ import annotations

import random
import string
from typing import Any, Literal

import pandas as pd

EPAKey = Literal["state", "county", "aqi"]
ALPHANUMERIC = string.ascii_lowercase + string.digits


def fetch_epa(key: EPAKey) -> list[Any]:
    """Return a column from the EPA air quality dataset.

    Args:
        key: One of ``"state"``, ``"county"`` or ``"aqi"`` identifying the
            column to read from the dataset.

    Returns:
        A list containing the requested column values.

    Raises:
        KeyError: If ``key`` is not recognised.
    """
    epa = pd.read_csv("c2_epa_air_quality.csv")
    epa_dict = {
        "state": epa["state_name"].tolist(),
        "county": epa["county_name"].tolist(),
        "aqi": epa["aqi"].tolist(),
    }
    return epa_dict[key]


def id_gen(n_chars_id: int, n_samples: int) -> list[str]:
    """Generate deterministic random-looking identifiers.

    Args:
        n_chars_id: Number of characters each identifier should contain.
        n_samples: Number of identifiers to generate.

    Returns:
        A list of alphanumeric identifier strings.
    """
    return [
        "".join(random.Random(index).choices(ALPHANUMERIC, k=n_chars_id))
        for index in range(n_samples)
    ]


def lists_gen(
    n_chars_id: int,
    n_pool: int,
    n_feedback_ids: int,
    n_verified_ids: int,
    seed: int | None = None,
) -> tuple[list[str], list[str]]:
    """Return two ID subsets representing verified and feedback IDs.

    Args:
        n_chars_id: Length of each generated identifier.
        n_pool: Size of the ID pool to sample from.
        n_feedback_ids: Number of IDs assigned to the feedback list.
        n_verified_ids: Number of IDs assigned to the verified list.
        seed: Optional seed value to make sampling reproducible.

    Returns:
        A tuple containing the verified IDs and feedback IDs in that order.
    """
    if n_pool < max(n_feedback_ids, n_verified_ids):
        msg = "Pool size must be large enough to satisfy sample sizes."
        raise ValueError(msg)

    pool = id_gen(n_chars_id, n_pool)
    rng = random.Random(seed)
    verified_ids = rng.sample(pool, k=n_verified_ids)
    feedback_ids = rng.sample(pool, k=n_feedback_ids)
    return verified_ids, feedback_ids


def sales_data_generator(n_customers: int, seed: int) -> list[list[float]]:
    """Create simulated sales histories for a set of customers.

    Args:
        n_customers: Number of customers to simulate.
        seed: Seed value for deterministic random number generation.

    Returns:
        A nested list where each inner list contains the purchases for a
        customer. Individual purchase amounts are rounded to two decimals.
    """
    rng = random.Random(seed)
    sales_data: list[list[float]] = []
    for _ in range(n_customers):
        n_sales = rng.randint(0, 6)
        customer_sales = [
            round(rng.lognormvariate(2.5, 1.5), 2) for _ in range(n_sales)
        ]
        sales_data.append(customer_sales)

    return sales_data
