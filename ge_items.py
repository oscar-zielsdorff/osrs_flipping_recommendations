import requests
import pandas as pd
import numpy as np


url = 'https://prices.runescape.wiki/api/v1/osrs'


# Get item prices
response = requests.get(url + '/1h')
parsed = response.json()
price_df = pd.DataFrame.from_dict(parsed['data'], orient='index')
price_df.reset_index(names='id', inplace=True)
price_df['id'] = price_df['id'].astype('int64')


# Get item mapping
response = requests.get(url + '/mapping')
parsed = response.json()
mapping_df = pd.DataFrame(parsed)
mapping_df['id'] = mapping_df['id'].astype('int64')


# Combine dataframes into final dataframe
df = pd.merge(price_df, mapping_df, on='id')
df.dropna(subset=['avgLowPrice', 'avgHighPrice'], inplace=True)


# Calculate cost
df['potentialCost'] = df['avgLowPrice'] * df['limit']


# Calculate profit
tax_rate = 0.02 # 2% (rounded down)
df['tax'] = df['avgHighPrice'] * tax_rate
df['tax'] = np.floor(pd.to_numeric(df["tax"], errors="coerce"))
df['profit'] = df['avgHighPrice'] - df['avgLowPrice'] - df['tax']
df['potentialProfit'] = df['profit'] * df['limit']

# Remove no profit items
df = df[df['profit'] > 0]


# Calculate ROI percentage
df['roi (%)'] = df['profit'] / df['avgLowPrice'] * 100


#################################################################
# Filters                                                     ###
#################################################################
## Set to None or False to disable (depending on filter)      ###
#################################################################
enable_filters = True

if enable_filters:

    min_volume = 60
    if min_volume is not None:
        df = df[df['lowPriceVolume'] >= min_volume]
        df = df[df['highPriceVolume'] >= min_volume]

    min_low_volume = None
    if min_low_volume is not None:
        df = df[df['lowPriceVolume'] >= min_low_volume]

    higher_high_volume = True
    if higher_high_volume:
        df = df[df['highPriceVolume'] >= df['lowPriceVolume']]

    max_buy_price = 4000000
    if max_buy_price is not None:
        df = df[df['avgLowPrice'] <= max_buy_price]

    max_potential_cost = None
    if max_potential_cost is not None:
        df = df[df['potentialCost'] <= max_potential_cost]

    max_limit = None
    if max_limit is not None:
        df = df[df['limit'] <= max_limit]

    min_roi = 20
    if min_roi is not None:
        df = df[df['roi (%)'] >= min_roi]

    min_profit = None
    if min_profit is not None:
        df = df[df['profit'] >= min_profit]

    min_potential_profit = None
    if min_potential_profit is not None:
        df = df[df['potentialProfit'] >= min_potential_profit]

    free_to_play_only = False
    if free_to_play_only:
        df = df[df['members'] == False]

##################################################################
##################################################################

# Sort values
df = df.sort_values(by=['potentialProfit'], ascending=False)


# Organize dataframe
df = df.drop(columns=[
    'examine',
    'members',
    'icon',
    'lowalch',
    'highalch',
    'value',
    'id'
])
df = df.reindex(columns=[
    'name',
    'avgLowPrice',
    'avgHighPrice',
    'tax',
    'profit',
    'limit',
    'potentialCost',
    'potentialProfit',
    'roi (%)',
    'lowPriceVolume',
    'highPriceVolume'
])


# Save table to file
with pd.ExcelWriter('ge_items.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='Sheet1')

    # Access workbook and worksheet
    wb = writer.book
    ws = writer.sheets['Sheet1']

    # Define formats
    int_fmt = wb.add_format({'num_format': '#,##0'})
    
    # Autosize & format columns
    padding = 0
    for i, col in enumerate(df.columns):
        series = df[col].astype(object).where(df[col].notna(), "")  # avoid 'nan' text
        max_len = max(len(str(col)), series.astype(str).map(len).max())
        if pd.api.types.is_numeric_dtype(df[col]):
            ws.set_column(i, i, max_len + padding, int_fmt)
        else:
            ws.set_column(i, i, max_len + padding)

    # Freeze first (header) row
    ws.freeze_panes(1, 0)


# Success message
print('created \'ge_items.xlsx\'')
