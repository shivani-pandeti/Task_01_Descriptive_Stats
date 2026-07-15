# Comparison: Pure Python vs Pandas

## Do the results agree?

# Comparison: Pure Python vs Pandas

## Do the results agree?

Yes, mostly. When I checked the numbers from both scripts side by side, almost everything matched.

For missing values, both scripts gave me the exact same counts:
- `ad_delivery_stop_time`: 2159 missing in both
- `bylines`: 1009 missing in both
- `estimated_audience_size`: 579 missing in both

For categorical columns also, both scripts agreed completely. Same top 5 values, same counts, for columns like `page_name`, `currency`, `publisher_platforms`, etc. For example, both scripts told me Kamala Harris page has 55503 ads, which is the highest.

For numeric columns, the mean, min, max and median were basically identical in both scripts (small difference only in decimal places, which is just rounding). But there was one place where the numbers did not match exactly: the standard deviation.

For `spend` column (after converting the range to midpoint):
- Pure Python stdev: 4992.5506
- Pandas stdev: 4992.5607

These are close but not the same. This is not a mistake, it is because of how each one calculates standard deviation by default.

## Why the stdev is different

In my pure Python script, I calculated standard deviation by dividing by `n` (total count). This is called population standard deviation, basically it assumes my data is the whole population I care about.

Pandas by default divides by `n-1` when calculating `.std()`. This is called sample standard deviation, it assumes my data is only a sample taken from a bigger population.

Since my dataset has 246745 rows, dividing by n vs n-1 makes very little practical difference, but it is not zero, that is why I am seeing this small mismatch. This was actually a good learning for me, I did not know pandas makes this assumption silently until I compared it with my own manual calculation.

## Where pure Python forced me to make decisions that pandas hid

The biggest one was the range columns: `spend`, `impressions` and `estimated_audience_size`. These columns do not contain plain numbers, they contain values like `{'lower_bound': '200', 'upper_bound': '299'}` because Facebook only reports these in ranges, not exact numbers.

When I loaded this into pandas using `read_csv()`, pandas quietly treated these columns as plain text (`str` dtype) and did not complain at all. If I had only used pandas and never written the manual script, I probably would not have noticed this issue and might have tried to run `.mean()` directly on these columns and gotten wrong results or an error, without understanding why.

But in my pure Python script, I was forced to write my own `infer_column_type()` function, and I had to specifically write code to catch this "range" pattern and decide what to do with it. I chose to take the midpoint of the lower and upper bound as a single representative number. This was a decision I had to make manually, pandas never forced me to think about it.

## What writing the manual version taught me

Writing `pure_python_stats.py` first actually helped me understand the dataset much better before I even touched pandas. Some things I noticed only because I was writing the logic myself:

- The range columns issue (mentioned above), I would have missed this completely if I started with pandas directly.
- I had to think about what happens when a column is completely a list (like `publisher_platforms` and `illuminating_mentions`), pandas also treats these as plain text strings, so `nunique()` and `value_counts()` count the whole list as one value, for example `['facebook', 'instagram']` is treated as one single category, not two separate platforms. Both scripts have this same limitation actually.
- I had to explicitly decide how to skip missing/non-numeric values while calculating mean, pandas does this automatically with `NaN` handling, so I never had to think about it unless I built it myself first.

Overall, I feel like doing the pure Python version first genuinely made me understand my own dataset better, and made me trust the pandas output more, because now I know exactly what pandas is doing behind the `.describe()` and `.mean()` calls.