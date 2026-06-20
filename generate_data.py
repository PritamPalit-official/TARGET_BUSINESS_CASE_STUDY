import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

# Directory setup
data_dir = r"C:\Users\prita\.gemini\antigravity\scratch\repos\TARGET_BUSINESS_CASE_STUDY\data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Number of customers and orders
n_customers = 8000
n_orders = 10000

print("Generating customer data...")
# Brazilian states and cities
states = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'DF', 'PE', 'CE', 'AM', 'PA', 'MT', 'MS', 'GO']
state_p = [0.42, 0.13, 0.12, 0.06, 0.05, 0.04, 0.04, 0.02, 0.02, 0.02, 0.02, 0.02, 0.01, 0.01, 0.02]
state_p = np.array(state_p) / sum(state_p) # normalize

cities_by_state = {
    'SP': ['Sao Paulo', 'Campinas', 'Santos', 'Sao Bernardo do Campo', 'Guarulhos'],
    'RJ': ['Rio de Janeiro', 'Niteroi', 'Duque de Caxias', 'Nova Iguacu'],
    'MG': ['Belo Horizonte', 'Uberlandia', 'Contagem', 'Juiz de Fora'],
    'RS': ['Porto Alegre', 'Caxias do Sul', 'Pelotas', 'Canoas'],
    'PR': ['Curitiba', 'Londrina', 'Maringa', 'Ponta Grossa'],
    'SC': ['Florianopolis', 'Joinville', 'Blumenau', 'Chapeco'],
    'BA': ['Salvador', 'Feira de Santana', 'Vitoria da Conquista'],
    'DF': ['Brasilia'],
    'PE': ['Recife', 'Olinda', 'Jaboatao dos Guararapes'],
    'CE': ['Fortaleza', 'Caucaia', 'Juazeiro do Norte'],
    'AM': ['Manaus'],
    'PA': ['Belem', 'Ananindeua', 'Santarem'],
    'MT': ['Cuiaba', 'Varzea Grande'],
    'MS': ['Campo Grande', 'Dourados'],
    'GO': ['Goiania', 'Aparecida de Goiania']
}

customer_ids = [f"c_{i:06d}" for i in range(n_customers)]
customer_uniques = [f"cu_{i:06d}" for i in np.random.randint(0, int(n_customers * 0.9), n_customers)]
cust_states = np.random.choice(states, n_customers, p=state_p)
cust_cities = [np.random.choice(cities_by_state[st]) for st in cust_states]
zip_codes = [int(f"{np.random.randint(1000, 9999)}{np.random.randint(10, 99)}") for _ in range(n_customers)]

customers_df = pd.DataFrame({
    'customer_id': customer_ids,
    'customer_unique_id': customer_uniques,
    'customer_zip_code_prefix': zip_codes,
    'customer_city': cust_cities,
    'customer_state': cust_states
})

print("Generating order data...")
# Start and end date for purchase timestamps (covering Jan 2017 to Aug 2018)
start_date = datetime(2017, 1, 1)
end_date = datetime(2018, 8, 31)

# Generate timestamps with hourly weights (afternoon and night are peak times)
hours = list(range(24))
hour_weights = [0.01, 0.005, 0.005, 0.005, 0.005, 0.01, 0.02, 0.04, 0.05, 0.06, 0.07, 0.07, 0.08, 0.08, 0.08, 0.07, 0.07, 0.06, 0.06, 0.06, 0.05, 0.04, 0.03, 0.02]
hour_weights = np.array(hour_weights) / sum(hour_weights)

# Month weights: 2018 has more orders than 2017
order_dates = []
for _ in range(n_orders):
    # Year: 2017 (40%), 2018 (60%)
    year = np.random.choice([2017, 2018], p=[0.4, 0.6])
    if year == 2017:
        month = np.random.randint(1, 13)
        # Black Friday / End of Year peak
        if month in [11, 12]:
            day = np.random.randint(1, 29)
        else:
            day = np.random.randint(1, 29)
    else:
        month = np.random.randint(1, 9) # Jan to Aug
        day = np.random.randint(1, 29)
    
    hour = np.random.choice(hours, p=hour_weights)
    minute = np.random.randint(0, 60)
    second = np.random.randint(0, 60)
    order_dates.append(datetime(year, month, day, hour, minute, second))

order_ids = [f"o_{i:06d}" for i in range(n_orders)]
order_custs = np.random.choice(customer_ids, n_orders)

# Build orders dataframe
orders_data = []
for oid, cid, purchase_t in zip(order_ids, order_custs, order_dates):
    # Timestamps details
    approved_t = purchase_t + timedelta(minutes=int(np.random.exponential(30)))
    carrier_t = purchase_t + timedelta(days=float(np.random.uniform(0.5, 3)))
    
    # Actual delivery time: mean of 10 days, varies by customer state
    cust_state = customers_df.loc[customers_df['customer_id'] == cid, 'customer_state'].values[0]
    if cust_state == 'SP':
        del_days = np.random.uniform(3, 8)
    elif cust_state in ['RJ', 'MG', 'PR']:
        del_days = np.random.uniform(6, 12)
    elif cust_state in ['AM', 'PA']:
        del_days = np.random.uniform(15, 30) # Remote
    else:
        del_days = np.random.uniform(10, 18)
        
    delivered_t = purchase_t + timedelta(days=del_days)
    estimated_t = purchase_t + timedelta(days=del_days + np.random.uniform(3, 10)) # estimated is usually later
    
    # 2% orders cancelled or shipped but not delivered
    status = np.random.choice(['delivered', 'shipped', 'canceled'], p=[0.98, 0.015, 0.005])
    if status != 'delivered':
        delivered_t = pd.NaT
        if status == 'canceled':
            carrier_t = pd.NaT
            
    orders_data.append({
        'order_id': oid,
        'customer_id': cid,
        'order_status': status,
        'order_purchase_timestamp': purchase_t.strftime('%Y-%m-%d %H:%M:%S'),
        'order_approved_at': approved_t.strftime('%Y-%m-%d %H:%M:%S'),
        'order_delivered_carrier_date': carrier_t.strftime('%Y-%m-%d %H:%M:%S') if pd.notna(carrier_t) else None,
        'order_delivered_customer_date': delivered_t.strftime('%Y-%m-%d %H:%M:%S') if pd.notna(delivered_t) else None,
        'order_estimated_delivery_date': estimated_t.strftime('%Y-%m-%d %H:%M:%S')
    })

orders_df = pd.DataFrame(orders_data)

print("Generating order items data...")
# Build order items
items_data = []
for oid, cid in zip(order_ids, order_custs):
    # Customer state determines freight cost (average freight: SP=10, AM=80)
    cust_state = customers_df.loc[customers_df['customer_id'] == cid, 'customer_state'].values[0]
    if cust_state == 'SP':
        freight_base = 8.5
    elif cust_state in ['RJ', 'MG', 'PR']:
        freight_base = 15.0
    elif cust_state in ['AM', 'PA']:
        freight_base = 65.0
    else:
        freight_base = 25.0
        
    # Number of items in order: mostly 1, occasionally 2 or 3
    num_items = np.random.choice([1, 2, 3], p=[0.88, 0.10, 0.02])
    for item_idx in range(1, num_items + 1):
        price = np.random.exponential(120.0) + 15.0
        freight = freight_base + np.random.uniform(-3, 5)
        
        items_data.append({
            'order_id': oid,
            'order_item_id': item_idx,
            'product_id': f"p_{np.random.randint(1000, 9999):04d}",
            'seller_id': f"s_{np.random.randint(100, 999):03d}",
            'shipping_limit_date': (datetime.strptime(orders_df.loc[orders_df['order_id'] == oid, 'order_purchase_timestamp'].values[0], '%Y-%m-%d %H:%M:%S') + timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S'),
            'price': np.round(price, 2),
            'freight_value': np.round(freight, 2)
        })
        
order_items_df = pd.DataFrame(items_data)

print("Generating payments data...")
# Build payments: payment value matches total price + freight for the order
payments_data = []
order_totals = order_items_df.groupby('order_id').apply(lambda x: (x['price'] + x['freight_value']).sum()).to_dict()

for oid in order_ids:
    total_val = order_totals.get(oid, 100.0)
    # Payment type: credit_card is most popular
    pay_type = np.random.choice(['credit_card', 'boleto', 'voucher', 'debit_card'], p=[0.73, 0.20, 0.05, 0.02])
    
    if pay_type == 'credit_card':
        installments = np.random.choice([1, 2, 3, 4, 6, 8, 10, 12], p=[0.45, 0.15, 0.10, 0.10, 0.08, 0.05, 0.05, 0.02])
    else:
        installments = 1 # boleto, voucher, debit_card always 1 installment
        
    payments_data.append({
        'order_id': oid,
        'payment_sequential': 1,
        'payment_type': pay_type,
        'payment_installments': int(installments),
        'payment_value': np.round(total_val, 2)
    })
    
payments_df = pd.DataFrame(payments_data)

# Save datasets to CSV
customers_df.to_csv(os.path.join(data_dir, "customers.csv"), index=False)
orders_df.to_csv(os.path.join(data_dir, "orders.csv"), index=False)
order_items_df.to_csv(os.path.join(data_dir, "order_items.csv"), index=False)
payments_df.to_csv(os.path.join(data_dir, "payments.csv"), index=False)

print("Walmart shape:", pd.read_csv(r'C:\Users\prita\.gemini\antigravity\scratch\repos\BUSINESS_CASE_STUDY_WALMART\data\walmart_data.csv').shape)
print(f"Target datasets generated successfully in: {data_dir}")
print(f"Customers: {customers_df.shape}")
print(f"Orders: {orders_df.shape}")
print(f"Order Items: {order_items_df.shape}")
print(f"Payments: {payments_df.shape}")
