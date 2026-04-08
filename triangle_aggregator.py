
import pandas as pd

def build_triangle(filepath, metric='paid', segment_filter=None, time_unit='annual', basis='occurrence'):
    """
    Ingests a transactional claims CSV and outputs a cumulative run-off triangle.
    
    Arguments:
    - filepath: String path to the CSV file.
    - metric: 'paid' (Paid Loss) or 'incurred' (Reported/Incurred Loss).
    - segment_filter: Dictionary to subset data, e.g., {'lob': 1} or {'cc': 4}.
    - time_unit: 'annual' or 'quarterly' origin periods.
    - basis: 'occurrence' (Accident Year) or 'claims_made' (Report Year).
    """
    
    df = pd.read_csv(filepath)
    
    
    if segment_filter:
        for column, value in segment_filter.items():
            df = df[df[column] == value]
            
    
    
    if basis == 'claims_made':
        
        df['origin_period'] = df['accident_year'] + df['report_delay']
    else:
        df['origin_period'] = df['accident_year']
        
    
    if time_unit == 'quarterly':
        
        df['origin_period'] = df['origin_period'].astype(int).astype(str) + "-Q" + df['accident_quarter'].astype(str)
    
    
    
    
    target_value = 'paid_loss'
    if metric == 'incurred':
        if 'reported_loss' in df.columns:
            target_value = 'reported_loss'
        else:
            print("Warning: Dataset lacks reported/incurred loss. Defaulting to Paid Loss.")
            
    
    incremental_triangle = pd.pivot_table(
        df,
        values=target_value,
        index='origin_period',
        columns='development_year',
        aggfunc='sum',
        fill_value=0
    )
    
    
    cumulative_triangle = incremental_triangle.cumsum(axis=1)
    
    return cumulative_triangle





file_name = 'sm_100000claims_records.csv'


print("\n--- TEST 1: Standard Annual Occurrence Triangle ---")
standard_tri = build_advanced_triangle(file_name, basis='occurrence', time_unit='annual')
print(standard_tri.head())


print("\n--- TEST 2: Claims-Made Basis (LOB 3 Only) ---")
claims_made_tri = build_advanced_triangle(file_name, basis='claims_made', segment_filter={'lob': 3})
print(claims_made_tri.head())


print("\n--- TEST 3: Quarterly Origin Triangle ---")
quarterly_tri = build_advanced_triangle(file_name, time_unit='quarterly')
print(quarterly_tri.head())
