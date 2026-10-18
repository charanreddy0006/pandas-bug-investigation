import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal


@pytest.mark.parametrize(
    ("method", "expected_values"),
    [
        ("ffill", [1.0, 1.0, 3.0]),
        ("bfill", [1.0, 3.0, 3.0]),
    ],
)
@pytest.mark.parametrize("axis", [1, "columns"])
def test_fill_missing_values_inplace(method, expected_values, axis):
    df = pd.DataFrame(
        [[1.0, np.nan, 3.0]],
        columns=["A", "B", "C"],
    )

    expected = pd.DataFrame(
        [expected_values],
        columns=["A", "B", "C"],
    )

    result = getattr(df, method)(axis=axis, inplace=True)

    assert result is df
    assert_frame_equal(df, expected)