# Findings: 2024 Facebook Political Ads Dataset

## About the data

This dataset has 246745 rows and 40 columns, and each row is one Facebook ad that mentions at least one of the 2024 US presidential candidates. While going through this dataset, I found some patterns which I think are worth talking about.

## Spending is not evenly distributed

When I looked at the `page_name` column, I found that there are 4546 unique pages in this dataset, but the ads are not spread evenly across them at all. Just the top 5 pages account for a huge chunk of all ads:

- Kamala Harris: 55503 ads
- Donald J. Trump: 23988 ads
- Joe Biden: 14822 ads
- The Daily Scroll: 10461 ads
- Kamala HQ: 7564 ads

So basically a handful of big accounts (mostly the candidates' own official pages, plus a few large PACs like "HARRIS FOR PRESIDENT" and "HARRIS VICTORY FUND") are running a huge share of all ad activity, while thousands of smaller pages are running only a few ads each.

I also looked at the `spend` column (I converted the range values to midpoints to get a usable number). The mean spend per ad is about 1061.79, but the median is only 49.5, and even the 75th percentile is only 449.5. This tells me that most ads are actually quite cheap, and it is a small number of very expensive ads that are pulling the average up. This is called a right-skewed distribution, few big spenders, many small ones.

## Ads mostly ran close to the election

Looking at `ad_creation_time` and `ad_delivery_start_time`, most ads were created and started running in late October 2024, right before the election (which was on November 5, 2024). The single busiest day for `ad_delivery_stop_time` is 2024-11-05, election day itself, which makes sense, a lot of campaigns probably scheduled their ads to stop running exactly then.

## Not every ad mentions a candidate by name

This one surprised me a bit. Looking at `illuminating_mentions`, the single most common value is actually an empty list `[]`, which appears 73205 times, meaning around 30% of ads in this "presidential ads" dataset do not mention any candidate's name directly in the ad text, even though the ad was still categorized as related to the presidential race.

Among ads that do mention a candidate, Donald Trump is mentioned the most (53182 times as `['Donald Trump']`), followed by Kamala Harris (31019 times). There are also separate entries like `['President Trump']` (14580) which is really also about Trump but got counted as a different combination since the exact wording is different. If I wanted an accurate "who is mentioned the most" count, I would need to go through each list and count individual names rather than treating whole combinations as one category, this is something both of my scripts currently do not do.

## Most ads run on Facebook and Instagram together

Looking at `publisher_platforms`, the huge majority of ads (214434 out of 246745) run on both Facebook and Instagram together. Only 23259 ran on Facebook alone, and 8395 ran on Instagram alone. So cross-posting on both platforms seems to be the default strategy for most advertisers in this dataset.

## A small data quality surprise: non-USD currency

Almost all ads (246599) are billed in USD, which makes sense for a US election. But I did find 63 ads billed in INR, 17 in GBP, 11 in EUR, and 8 in PKR. This is a small number compared to the whole dataset, but it made me curious, why would ads about the US presidential election be billed in Indian Rupees or Pakistani Rupees? It could be diaspora-focused advertising, or accounts run from outside the US, but the dataset alone does not tell me the reason, this could be a good direction for further research.

## Missing data

Two columns have a meaningful number of missing values:
- `ad_delivery_stop_time`: 2159 missing. My guess is these are ads that were still actively running when this data was collected, so there was no stop date yet.
- `bylines`: 1009 missing.
- `estimated_audience_size`: 579 missing.

All other columns had zero missing values, which was a bit surprising to me given how messy real-world data usually is, but it also makes sense since this dataset looks like it was already cleaned and scored (given all the `illuminating_*` columns) before it was shared with us.

## What surprised me most

The biggest surprise for me was the ~30% of ads that don't mention any candidate by name at all, and the fact that a handful of pages are responsible for such a large share of all ad volume. Both of these tell me that "political ad" does not always mean "an ad naming a candidate", a lot of the advertising in this space is more about issues, fundraising asks, or general messaging rather than directly naming who the ad is about.