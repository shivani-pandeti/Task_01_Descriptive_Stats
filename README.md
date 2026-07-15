# Task 1: Descriptive Statistics with and without Pandas

## Project Description

This project is about exploring a real dataset of Facebook political ads from the 2024 US Presidential election. I wrote two scripts that do the same descriptive statistics analysis in two different ways:

1. `pure_python_stats.py` — uses only Python's standard library (csv, math, collections, ast). No pandas, no third-party packages.
2. `pandas_stats.py` — does the same analysis using the pandas library.

The idea behind this task was to first understand how to compute basic statistics manually (mean, median, standard deviation, missing values, etc.) before using a library like pandas that does it for you automatically. This helped me understand what pandas is actually doing behind the scenes.

## Dataset

This project uses the "2024 Facebook Political Ads" dataset. The dataset itself is not included in this repo (as per the assignment instructions), since it is a large file and not meant to be redistributed.

Source: [2024 Facebook Political Ads (Google Drive)](https://drive.google.com/file/d/1gvtvX8fATFrrzraPmTSf205U8u3JExUR/view?usp=sharing)

To run this project yourself:
1. Download the dataset CSV file from the Google Drive link above
2. Place the file in the same folder as the scripts, and name it exactly: `fb_ads_president_scored_anon.csv`

## How to Run

### Requirements

- Python 3.9 or higher
- For `pandas_stats.py` only: pandas (see `requirements.txt`)
- `pure_python_stats.py` needs no installation at all, it only uses Python's built-in modules.

### Setup

Install pandas (only needed for the pandas script):

```bash
pip install -r requirements.txt
```

### Running the scripts

```bash
python3 pure_python_stats.py
```

```bash
python3 pandas_stats.py
```

Both scripts read `fb_ads_president_scored_anon.csv` from the same folder, and print their analysis directly to the terminal.

The actual output from running both scripts is already saved in the `Outputs/` folder (`pure_python_output.txt` and `pandas_output.txt`), so you can look at the results directly without running the scripts yourself if you just want to see what they produce.

## What Each Script Does

**`pure_python_stats.py`**
- Loads the CSV using `csv.DictReader`
- Automatically figures out what type each column is (numeric, date, range, list, or categorical)
- For numeric columns: calculates count, mean, min, max, standard deviation, median, all by hand
- For the tricky "range" columns (`spend`, `impressions`, `estimated_audience_size`, which Facebook reports as ranges like `{'lower_bound': '200', 'upper_bound': '299'}`), it converts each value to its midpoint before computing stats
- For categorical columns: calculates count, number of unique values, most frequent value, and top 5 values
- Also reports missing values for every column

**`pandas_stats.py`**
- Loads the CSV using `pandas.read_csv()`
- Shows shape, dtypes, and `.info()` summary
- Uses `.describe(include='all')` to get statistics for both numeric and categorical columns
- Calculates missing value counts and percentages per column
- Uses `.value_counts()` and `.nunique()` for categorical columns
- Converts the `spend` column to midpoint values (same method as the pure Python script) to double check that both scripts agree on numeric stats

## Findings & Comparison

See `FINDINGS.md` for the full write-up of what I found in the data, and `COMPARISON.md` for the comparison between the pure Python and pandas approaches.

## Files in this Repo

- `pure_python_stats.py` — descriptive stats using only standard library
- `pandas_stats.py` — same analysis using pandas
- `README.md` — this file
- `FINDINGS.md` — narrative write-up of what I found in the data
- `COMPARISON.md` — comparison between the two approaches
- `requirements.txt` — dependencies needed to run `pandas_stats.py`
- `Outputs/pure_python_output.txt` — saved terminal output from running `pure_python_stats.py`
- `Outputs/pandas_output.txt` — saved terminal output from running `pandas_stats.py`