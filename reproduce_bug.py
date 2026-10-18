import pandas as pd

print("Pandas version:", pd.__version__)

for method in ("ffill", "bfill"):
    df = pd.DataFrame(
        [[1.0, float("nan"), 3.0]],
        columns=["A", "B", "C"],
    )

    print(f"\nTesting {method}...")

    result = getattr(df, method)(axis=1, inplace=True)

    print("DataFrame:")
    print(df)

    print("Returned object is original DataFrame:", result is df)