import pandas as pd
import numpy as np
import os

def generate_synthetic_cdms(num_samples=10000):
    # Dynamically find the absolute path to your ml_pipeline folder
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_dir = os.path.join(base_dir, 'datasets')
    data_path = os.path.join(dataset_dir, 'synthetic_cdms.csv')

    np.random.seed(42)
    
    # Generate realistic ranges for orbital approach metrics
    miss_distance = np.random.exponential(scale=15.0, size=num_samples) 
    miss_distance = np.clip(miss_distance, 0.1, 100.0)
    
    rel_velocity = np.random.normal(loc=10.0, scale=3.0, size=num_samples)
    rel_velocity = np.clip(rel_velocity, 1.0, 20.0)
    
    bstar_1 = np.random.normal(loc=0.0001, scale=0.00005, size=num_samples)
    bstar_2 = np.random.normal(loc=0.0001, scale=0.00005, size=num_samples)
    
    # Create a non-linear target variable (Probability of Collision / Risk Score)
    dist_factor = np.exp(-0.5 * miss_distance)
    vel_factor = rel_velocity / 15.0
    drag_factor = 1.0 + (np.abs(bstar_1) + np.abs(bstar_2)) * 1000
    
    raw_risk = dist_factor * (0.6 + 0.4 * vel_factor) * drag_factor
    target_risk = np.clip(raw_risk, 0.0, 1.0)
    
    df = pd.DataFrame({
        'miss_distance_km': miss_distance,
        'relative_velocity_km_s': rel_velocity,
        'bstar_1': bstar_1,
        'bstar_2': bstar_2,
        'target_risk_score': target_risk
    })
    
    # Ensure directories exist using absolute paths
    os.makedirs(dataset_dir, exist_ok=True)
    df.to_csv(data_path, index=False)
    print(f"Successfully generated {num_samples} synthetic CDMs at {data_path}")

if __name__ == "__main__":
    generate_synthetic_cdms()