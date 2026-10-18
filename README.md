# Pandas Bug Investigation — GH-71159

A practical investigation into a real-world Pandas bug involving
`DataFrame.ffill()` and `DataFrame.bfill()` when using
`axis=1` and `inplace=True`.

This project demonstrates how to reproduce an open-source bug,
write automated regression tests, analyse test failures, and
investigate the official fix.

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [Official References](#-official-references)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Environment Setup](#-environment-setup)
- [Reproducing the Bug](#-reproducing-the-bug)
- [Automated Testing](#-automated-testing)
- [Observed Results](#-observed-results)
- [Root Cause](#-root-cause)
- [Official Resolution](#-official-resolution)
- [Key Learnings](#-key-learnings)
- [Future Improvements](#-future-improvements)
- [Disclaimer](#-disclaimer)

---

## 🔍 Project Overview

Pandas is a widely used Python library for data manipulation and
analysis. Its DataFrame API provides methods for handling missing
values, including forward filling (`ffill`) and backward filling
(`bfill`).

This project investigates a reported issue where horizontal
missing-value filling does not correctly update the original
DataFrame when `inplace=True` is specified.

The investigation includes:

- Reproducing the reported behaviour locally.
- Testing both `ffill()` and `bfill()`.
- Testing different ways of specifying the horizontal axis.
- Writing automated tests using `pytest`.
- Analysing assertion failures.
- Reviewing the official issue and its associated fix.

**Important:** This repository documents a bug investigation. It
does not contain a modification to the official Pandas source code.

---

## 🐛 Problem Statement

**Issue:** `BUG: bfill/ffill with axis=1 ignore inplace=True and leave the original DataFrame unchanged`

When forward filling or backward filling missing values horizontally,
the original DataFrame may remain unchanged even though
`inplace=True` is specified.

### Example

Consider the following DataFrame:

| A | B | C |
|---|---|---|
| 1.0 | NaN | 3.0 |

### Expected behaviour

For forward filling:

```python
df.ffill(axis=1, inplace=True)
```

Expected DataFrame:

| A | B | C |
|---|---|---|
| 1.0 | 1.0 | 3.0 |

For backward filling:

```python
df.bfill(axis=1, inplace=True)
```

Expected DataFrame:

| A | B | C |
|---|---|---|
| 1.0 | 3.0 | 3.0 |

In both cases, the original DataFrame should be updated, and the
method should return the original DataFrame object when
`inplace=True` is used.

---

## 🔗 Official References

This investigation is based on an actual Pandas issue and its
associated pull request.

- **Original issue:** https://github.com/pandas-dev/pandas/issues/71159
- **Official fix:** https://github.com/pandas-dev/pandas/pull/71232
- **Pandas documentation:** https://pandas.pydata.org/docs/user_guide/missing_data.html

These references provide the original report, implementation changes,
and additional information about handling missing values in Pandas.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Pandas | Data manipulation and DataFrame operations |
| NumPy | Creating and handling missing values |
| pytest | Automated testing |
| Git | Version control |
| GitHub | Project hosting and issue tracking |

---

## 📁 Project Structure

```text
pandas-bug-investigation/
│
├── reproduce_bug.py
├── test_bug.py
├── requirements.txt
└── README.md
```

### File descriptions

**`reproduce_bug.py`**

A standalone Python script that demonstrates the reported behaviour
of `ffill()` and `bfill()` when `axis=1` and `inplace=True` are used.

**`test_bug.py`**

Contains parameterized automated tests that check whether the
original DataFrame is updated correctly and whether the returned
object is the original DataFrame.

**`requirements.txt`**

Lists the Python dependencies needed to run the investigation.

**`README.md`**

Documents the issue, reproduction process, test results, and findings.

---

## ⚙️ Environment Setup

### Prerequisites

Install the following before running the project:

- Python 3.11 or a compatible Python version.
- pip, Python's package installer.
- Git, if you want to clone or contribute to the repository.

### Step 1: Clone the repository

```bash
git clone https://github.com/charanreddy0006/pandas-bug-investigation.git
```

Move into the project directory:

```bash
cd pandas-bug-investigation
```

### Step 2: Create a virtual environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the Python commands
using `.venv\Scripts\python.exe` without activating the environment.

### Step 3: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Verify the Pandas version

```bash
python -c "import pandas as pd; print(pd.__version__)"
```

The original investigation was conducted using Pandas 3.0.6.

**Version note:** Pandas 3.0.6 was released before the official fix
was merged. Therefore, the bug's reproduction in that version is
consistent with the timing of the fix.

---

## 🧪 Reproducing the Bug

Run the reproduction script:

```bash
python reproduce_bug.py
```

The script tests both methods:

- `ffill(axis=1, inplace=True)`
- `bfill(axis=1, inplace=True)`

It prints the resulting DataFrame and checks whether the returned
object is the same object as the original DataFrame.

### What to observe

Check the following:

1. Does the original DataFrame contain the filled value?
2. Does the missing value (`NaN`) remain in the original DataFrame?
3. Does the method return the original DataFrame object?

These observations help establish whether the reported behaviour
can be reproduced in the installed Pandas version.

---

## ✅ Automated Testing

The project uses `pytest` to verify the expected behaviour.

Run the tests with:

```bash
python -m pytest test_bug.py -v
```

### Test coverage

The test suite covers four combinations:

| Test | Method | Axis |
|---|---|---|
| 1 | `ffill()` | `1` |
| 2 | `bfill()` | `1` |
| 3 | `ffill()` | `"columns"` |
| 4 | `bfill()` | `"columns"` |

The tests check two important requirements:

**1. Object identity**

```python
assert result is df
```

This verifies that the method returns the original DataFrame object.

**2. DataFrame contents**

```python
assert_frame_equal(df, expected)
```

This verifies that the original DataFrame contains the expected
filled values.

Testing both conditions is important because checking only the
returned values may fail to detect an issue with in-place updates.

---

## 📊 Observed Results

During the investigation, the reproduction script and automated tests
were executed using Pandas 3.0.5 and subsequently Pandas 3.0.6.

The reported behaviour was reproduced in both environments.

### Observations

- The original DataFrame remained unchanged.
- The missing value remained in the original DataFrame.
- The returned object was not the original DataFrame.
- All four automated test cases failed on Pandas 3.0.6.

These results demonstrate the reported behaviour in the tested
environment.

**Interpretation:** The failures were expected because Pandas 3.0.6
was released before the official fix was merged. They do not indicate
that the later upstream fix failed.

---

## 🔬 Root Cause

According to the original issue and the official pull request, the
problem was associated with the implementation path used when
processing a DataFrame horizontally.

When the operation uses `axis=1`, Pandas transposes the DataFrame
to perform the filling operation. The affected implementation could
return the computed result without correctly updating the original
DataFrame when `inplace=True` was specified.

Consequently, the computed values could exist in a separate result
while the original DataFrame remained unchanged.

The official pull request addressed the in-place update behaviour.

---

## 🛠️ Official Resolution

The issue was addressed in the official Pandas pull request:

**PR #71232 — Official fix:** https://github.com/pandas-dev/pandas/pull/71232

The fix updates the original DataFrame with the computed result
when `inplace=True` is used.

The relevant implementation change is conceptually:

```python
if inplace:
    self._update_inplace(result)
    return self
```

This ensures that the computed result is applied to the original
object and that the method returns that object.

The code above illustrates the relevant change; it is not a patch
applied by this repository.

For the exact implementation and merge history, refer to the
official pull request.

---

## 🎓 Key Learnings

This investigation demonstrates several practical software
development concepts.

### 1. Open-source bug investigation

Learned how to identify an existing issue, understand its reported
behaviour, and connect it to an official pull request.

### 2. Reproducing bugs

Learned how to create a small, isolated example to verify a reported
problem locally.

### 3. Parameterized testing

Used `pytest.mark.parametrize` to test multiple combinations without
duplicating the test function.

### 4. Regression testing

Created tests that can be used to check whether the reported
behaviour occurs in a particular Pandas version.

### 5. Object identity

Explored the difference between modifying an existing Python object
and returning a different object containing computed results.

### 6. Understanding `inplace=True`

Investigated why in-place operations must update the original object
rather than merely produce a separate result.

### 7. Reading open-source pull requests

Connected observed behaviour to an upstream implementation change
instead of claiming a fix without supporting evidence.

---

## 🚀 Future Improvements

Possible extensions for this project include:

- Compare behaviour across additional Pandas versions.
- Run the tests against a version containing the official fix.
- Add automated testing through GitHub Actions.
- Expand the investigation to other in-place DataFrame operations.
- Document any additional edge cases discovered during testing.

Any future test results should record the exact Pandas version used.

---

## ⚠️ Disclaimer

This is an independent educational investigation of a reported
Pandas issue.

The repository reproduces and documents the issue; it does not
claim authorship of the official Pandas fix or contain a modified
Pandas implementation.

All original issue reports and implementation changes belong to
the Pandas open-source project and its contributors.

---

## 👨‍💻 Author

**Charan Reddy**

GitHub: https://github.com/charanreddy0006

---

⭐ If you find this investigation useful, consider starring the
repository.
