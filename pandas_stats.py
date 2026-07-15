import pandas as pd  # the industry-standard library for tabular data analysis
import ast

# read the whole CSV into a DataFrame — pandas' version of a spreadsheet/table in memory
df = pd.read_csv('fb_ads_president_scored_anon.csv')

print("Shape (rows, columns):", df.shape)
print()
print("Data types per column:")
print(df.dtypes)
print()
print("Full info summary:")
df.info()

print()
print("Summary statistics (numeric + categorical):")
print(df.describe(include='all'))

#/opt/homebrew/bin/python3 pandas_stats.pyMissing values (count + percentage)
print()
print("Missing values per column:")
missing_counts = df.isnull().sum()               # count of nulls per column
missing_pct = (missing_counts / len(df)) * 100    # convert to percentage of total rows
missing_summary = pd.DataFrame({'missing_count': missing_counts, 'missing_pct': missing_pct})
print(missing_summary)

#Categorical columns — value_counts() and nunique()
print()
print("Categorical column details:")
categorical_cols = df.select_dtypes(include='object').columns
if len(categorical_cols) == 0:
    categorical_cols = df.select_dtypes(include='str').columns  

for col in categorical_cols:
    print(f"\n--- {col} ---")
    print("Unique values:", df[col].nunique())
    print(df[col].value_counts().head(5))


def get_midpoint(value):
    try:
        d = ast.literal_eval(value)
        lower = float(d['lower_bound'])
        upper = float(d.get('upper_bound', lower))
        return (lower + upper) / 2
    except (ValueError, SyntaxError, KeyError, TypeError):
        return None

#Verifing numeric results actually match 
print()
print("Spend (parsed as midpoint) — pandas version:")
df['spend_midpoint'] = df['spend'].apply(get_midpoint)  # apply() runs get_midpoint() on every row's spend value
print(df['spend_midpoint'].describe())