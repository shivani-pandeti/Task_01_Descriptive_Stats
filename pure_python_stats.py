import csv  # built-in module that handles CSV parsing correctly (commas inside quotes, etc.)
import math  # only used for sqrt() — everything else we build ourselves
import ast 
from collections import Counter  # built-in tool that counts how often each value appears


def load_data(filepath):
    # newline='' is required when using csv module; encoding avoids weird character errors
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)   # turns each row into a dict using header row as keys
        rows = list(reader)          # pull all rows into memory as a list of dicts
    return rows

def infer_column_type(values):
    # look at only the non-empty values — empty strings mean "missing"
    non_null = [v for v in values if v is not None and v.strip() != '']
    if not non_null:
        return 'empty'  # entire column is missing

    sample = non_null[:200]  # checking 200 values is enough to tell the pattern; no need to scan all 246k

    def is_number(v):
        try:
            float(v)
            return True
        except ValueError:
            return False

    def is_range_dict(v):
        # catches columns like spend: "{'lower_bound': '200', 'upper_bound': '299'}"
        return v.strip().startswith('{') and 'lower_bound' in v

    def is_list_like(v):
        # catches columns like publisher_platforms: "['facebook', 'instagram']"
        return v.strip().startswith('[')

    def is_date(v):
        # crude check for YYYY-MM-DD format
        return len(v) == 10 and v[4] == '-' and v[7] == '-'

    if all(is_range_dict(v) for v in sample):
        return 'range'
    if all(is_list_like(v) for v in sample):
        return 'list'
    if all(is_date(v) for v in sample):
        return 'date'
    if all(is_number(v) for v in sample):
        return 'numeric'
    return 'categorical'

def compute_numeric_stats(values):
    nums = []
    for v in values:
        try:
            nums.append(float(v))
        except (ValueError, TypeError):
            continue  # skip missing / non-numeric values — this IS the missing-value handling

    n = len(nums)
    if n == 0:
        return {'count': 0, 'mean': None, 'min': None, 'max': None, 'stdev': None, 'median': None}

    mean = sum(nums) / n  # textbook definition: sum of values divided by count

    # variance = average squared distance from the mean
    variance = sum((x - mean) ** 2 for x in nums) / n
    stdev = math.sqrt(variance)  # standard deviation = square root of variance

    sorted_nums = sorted(nums)
    mid = n // 2
    if n % 2 == 0:
        # even count: median is the average of the two middle values
        median = (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    else:
        # odd count: median is the single middle value
        median = sorted_nums[mid]

    return {
        'count': n,
        'mean': mean,
        'min': min(nums),
        'max': max(nums),
        'stdev': stdev,
        'median': median,
    }

def parse_range_midpoint(value):
    try:
        d = ast.literal_eval(value)              # turns the string into an actual dict
        lower = float(d['lower_bound'])
        upper = float(d.get('upper_bound', lower))  # some rows might not have an upper_bound; fall back to lower
        return (lower + upper) / 2
    except (ValueError, SyntaxError, KeyError, TypeError):
        return None  # if anything about this value is malformed, treat it as missing rather than crashing
    

def compute_categorical_stats(values):
    non_null = [v for v in values if v is not None and v.strip() != '']
    counts = Counter(non_null)          # e.g. {'Kamala Harris': 55503, 'Donald J. Trump': 23988, ...}
    total = len(non_null)
    unique = len(counts)                # how many distinct values exist
    top5 = counts.most_common(5)        # returns [(value, count), ...] sorted by count, descending
    mode, mode_freq = top5[0] if top5 else (None, 0)   # the single most frequent value
    return {
        'count': total,
        'unique': unique,
        'mode': mode,
        'mode_freq': mode_freq,
        'top5': top5,
    }

if __name__ == '__main__':
    data = load_data('fb_ads_president_scored_anon.csv')
    columns = list(data[0].keys())
    total_rows = len(data)

    print("=" * 60)
    print("DATASET OVERVIEW")
    print("=" * 60)
    print(f"Total rows: {total_rows}")
    print(f"Total columns: {len(columns)}")
    print()

    for col in columns:
        values = [row[col] for row in data]
        missing_count = sum(1 for v in values if v is None or v.strip() == '')
        col_type = infer_column_type(values)

        print("-" * 60)
        print(f"COLUMN: {col}")
        print(f"  Inferred type: {col_type}")
        print(f"  Missing values: {missing_count}")

        if col_type == 'numeric':
            stats = compute_numeric_stats(values)
            print(f"  Count: {stats['count']}, Mean: {stats['mean']:.4f}, "
                  f"Min: {stats['min']}, Max: {stats['max']}, "
                  f"Stdev: {stats['stdev']:.4f}, Median: {stats['median']}")

        elif col_type == 'range':
            midpoints = [parse_range_midpoint(v) for v in values]
            midpoints = [v for v in midpoints if v is not None]
            stats = compute_numeric_stats(midpoints)
            print(f"  (treated as numeric using range midpoint)")
            print(f"  Count: {stats['count']}, Mean: {stats['mean']:.4f}, "
                  f"Min: {stats['min']}, Max: {stats['max']}, "
                  f"Stdev: {stats['stdev']:.4f}, Median: {stats['median']}")

        else:
            # categorical, list, date, or empty — all treated as categorical for counting purposes
            stats = compute_categorical_stats(values)
            print(f"  Count: {stats['count']}, Unique: {stats['unique']}, "
                  f"Mode: {stats['mode']} (appears {stats['mode_freq']} times)")
            print(f"  Top 5: {stats['top5']}")

    print("-" * 60)
