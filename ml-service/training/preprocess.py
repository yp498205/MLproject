from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the dataset by deriving features and removing outliers:
    - Calculates age_years from age (days / 365.25)
    - Calculates BMI from height and weight
    - Filters realistic blood pressure ranges and height/weight outliers
    - Removes unneeded columns like 'id'
    """
    print("Cleaning dataset and filtering outliers...")
    initial_rows = len(df)
    
    df = df.copy()
    
    # Feature engineering
    df['age_years'] = (df['age'] / 365.25).round(2)
    df['bmi'] = (df['weight'] / ((df['height'] / 100) ** 2)).round(2)
    
    # Remove unneeded identifier column if present
    if 'id' in df.columns:
        df = df.drop(columns=['id'])
        
    # Filter outliers based on clinical plausibility
    valid_mask = (
        (df['ap_hi'] >= 50) & (df['ap_hi'] <= 250) &
        (df['ap_lo'] >= 30) & (df['ap_lo'] <= 150) &
        (df['ap_hi'] > df['ap_lo']) &
        (df['height'] >= 100) & (df['height'] <= 220) &
        (df['weight'] >= 30) & (df['weight'] <= 200)
    ) 
    
    df_cleaned = df[valid_mask].copy()
    print(f"Data cleaned. Rows reduced from {initial_rows} to {len(df_cleaned)}.")
    return df_cleaned

def run_preprocessing():
    data_path = BASE_DIR / "dataset" / "cardio_train.csv"
    output_path = BASE_DIR / "dataset" / "processed" / "cardio_cleaned.csv"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if data_path.exists():
        df = pd.read_csv(data_path, sep=';')
        print(f"Loaded raw data: {df.shape}")
        
        df_cleaned = clean_data(df)
        df_cleaned.to_csv(output_path, index=False, sep=';')
        print(f"Cleaned dataset saved to {output_path}")
        return df_cleaned
    else:
        raise FileNotFoundError(f"Dataset not found at {data_path}.")

if __name__ == "__main__":
    run_preprocessing()
