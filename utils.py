import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data():
    reps = ['Alex Blaze', 'Sarah Cyan', 'Mike Volt', 'Elena Flux']
    regions = ['North America', 'EMEA', 'APAC', 'LATAM']
    products = ['SaaS Core', 'Intel Add-on', 'API Access', 'Support Pro']
    stages = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won']
    
    data = []
    for i in range(100):
        data.append({
            'Date': (datetime.now() - timedelta(days=np.random.randint(0, 90))).strftime('%Y-%m-%d'),
            'Revenue': np.random.randint(1000, 50000),
            'Rep': np.random.choice(reps),
            'Region': np.random.choice(regions),
            'Product': np.random.choice(products),
            'Stage': np.random.choice(stages)
        })
    return pd.DataFrame(data).to_csv(index=False).encode('utf-8')
