import pickle
import re
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
import ast

def get_project_root():
    current = os.getcwd()
    root = current
    while True:
        if os.path.exists(os.path.join(root, 'data_processed')):
            break
        new_root = os.path.dirname(root)
        if new_root == root:
            root = current
            break
        root = new_root
    return root

PROJECT_ROOT = get_project_root()

app = FastAPI(title="House Price Prediction API", version="1.0")

print("Загрузка модели...")
with open(os.path.join(PROJECT_ROOT, 'models/rf_model_all.pkl'), 'rb') as f:
    model = pickle.load(f)
print("✅ Модель загружена")

class HouseFeatures(BaseModel):
    status: str
    propertyType: str
    street: str
    baths: str
    homeFacts: Optional[str] = None
    fireplace: Optional[str] = None
    city: str
    schools: Optional[str] = None
    sqft: str
    zipcode: str
    beds: str
    state: str
    stories: str

def to_numeric_safe(series):
    return pd.to_numeric(series, errors='coerce')

def parse_homefacts(hf_str):
    if pd.isna(hf_str) or hf_str == '' or hf_str == '{}':
        return {}
    try:
        if isinstance(hf_str, str):
            hf_dict = ast.literal_eval(hf_str)
        else:
            hf_dict = hf_str
        result = {}
        facts = hf_dict.get('atAGlanceFacts', [])
        for fact in facts:
            label = fact.get('factLabel', '')
            value = fact.get('factValue', '')
            if label == 'Year built':
                result['year_built'] = value
            elif label == 'Heating':
                result['heating'] = value
            elif label == 'Parking':
                result['parking'] = value
            elif label == 'lotsize':
                result['lot_size'] = value
        return result
    except:
        return {}

def parse_schools(schools_str):
    if pd.isna(schools_str) or schools_str == '' or schools_str == '{}':
        return {'schools_count': 0, 'avg_school_rating': np.nan, 'nearest_school_dist': np.nan}
    try:
        if isinstance(schools_str, str):
            schools_data = ast.literal_eval(schools_str)
        else:
            schools_data = schools_str
        if not schools_data or len(schools_data) == 0:
            return {'schools_count': 0, 'avg_school_rating': np.nan, 'nearest_school_dist': np.nan}
        ratings = []
        distances = []
        for item in schools_data:
            rating_list = item.get('rating', [])
            for r in rating_list:
                if r and r != 'NR':
                    try:
                        ratings.append(float(r))
                    except:
                        pass
            dist_data = item.get('data', {}).get('Distance', [])
            for d in dist_data:
                if d and isinstance(d, str):
                    match = re.search(r'(\d+\.?\d*)', d)
                    if match:
                        distances.append(float(match.group(1)))
        return {
            'schools_count': len(schools_data),
            'avg_school_rating': np.mean(ratings) if ratings else np.nan,
            'nearest_school_dist': min(distances) if distances else np.nan
        }
    except:
        return {'schools_count': 0, 'avg_school_rating': np.nan, 'nearest_school_dist': np.nan}

def normalize_property_type(pt):
    synonyms = {
        'single family': 'single-family', 'single-family home': 'single-family',
        'townhome': 'townhouse', 'town house': 'townhouse',
        'condo': 'condo', 'apartment': 'apartment', 'lot/land': 'lot/land',
        'mobile': 'manufactured', 'manufactured': 'manufactured'
    }
    if pd.isna(pt):
        return 'other'
    pt = str(pt).lower().strip()
    for key, value in synonyms.items():
        if key in pt:
            return value
    return pt

def normalize_status(status):
    groups = {
        'active': ['active', 'for sale', 'activated'],
        'pending': ['pending', 'under contract'],
        'sold': ['sold', 'closed']
    }
    if pd.isna(status):
        return 'other'
    status = str(status).lower().strip()
    for group, keywords in groups.items():
        for keyword in keywords:
            if keyword in status:
                return group
    return 'other'

def preprocess_input(data):
    df = pd.DataFrame([data])
    
    # 1. Преобразование числовых полей
    for col in ['baths', 'beds', 'stories', 'sqft']:
        df[col] = to_numeric_safe(df[col])
    
    # 2. Парсинг homeFacts
    homefacts_parsed = df['homeFacts'].apply(parse_homefacts)
    homefacts_df = pd.json_normalize(homefacts_parsed)
    df = pd.concat([df, homefacts_df], axis=1)
    
    # 3. Парсинг schools
    schools_parsed = df['schools'].apply(parse_schools)
    schools_df = pd.json_normalize(schools_parsed)
    df = pd.concat([df, schools_df], axis=1)
    
    # 4. ГАРАНТИРУЕМ НАЛИЧИЕ ВСЕХ НЕОБХОДИМЫХ КОЛОНОК
    required_cols = ['year_built', 'heating', 'parking', 'lot_size']
    for col in required_cols:
        if col not in df.columns:
            df[col] = np.nan
    
    # 5. Заполнение пропусков
    df['year_built'] = pd.to_numeric(df['year_built'], errors='coerce').fillna(1985)
    df['heating'] = df['heating'].fillna('unknown')
    df['parking'] = df['parking'].fillna('unknown')
    df['lot_size'] = pd.to_numeric(df['lot_size'], errors='coerce').fillna(9060)
    
    # 6. Нормализация
    df['propertyType'] = df['propertyType'].apply(normalize_property_type)
    df['status'] = df['status'].apply(normalize_status)
    
    # 7. Дополнительные признаки
    df['has_fireplace_info'] = df['fireplace'].notna().astype(int)
    df['fireplace'] = df['fireplace'].fillna('no_fireplace')
    df['house_age'] = 2024 - df['year_built']
    df['house_age'] = df['house_age'].clip(lower=0)
    df['is_land'] = df['propertyType'].str.contains('lot|land', case=False, na=False).astype(int)
    df['rooms_per_1000sqft'] = (df['beds'] + df['baths']) / (df['sqft'] / 1000)
    df['rooms_per_1000sqft'] = df['rooms_per_1000sqft'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
    # 8. Кодирование
    df['status'] = df['status'].map({'active': 0, 'pending': 1, 'sold': 2}).fillna(3)
    df['propertyType'] = df['propertyType'].map({'single-family': 0, 'condo': 1, 'townhouse': 2, 'lot/land': 3}).fillna(4)
    df['city'] = 0
    df['state'] = 0
    df['heating'] = df['heating'].map({'central': 0, 'electric': 1, 'gas': 2}).fillna(3)
    df['parking'] = df['parking'].map({'garage': 0, 'carport': 1}).fillna(2)
    df['fireplace'] = df['fireplace'].map({'yes': 0, 'no_fireplace': 1}).fillna(2)
    df['street_group'] = 0
    df['zipcode'] = pd.to_numeric(df['zipcode'], errors='coerce').fillna(0).astype(int)
    
    # 9. Schools признаки
    df['schools_count'] = df['schools_count'].fillna(0)
    df['avg_school_rating'] = df['avg_school_rating'].fillna(5.0)
    df['nearest_school_dist'] = df['nearest_school_dist'].fillna(10.0)
    
    # 10. Выбор колонок
    feature_cols = ['status', 'propertyType', 'baths', 'fireplace', 'city', 'sqft', 'zipcode',
                    'beds', 'state', 'stories', 'has_fireplace_info', 'year_built', 'heating',
                    'parking', 'lot_size', 'schools_count', 'avg_school_rating', 'nearest_school_dist',
                    'street_group', 'house_age', 'is_land', 'rooms_per_1000sqft']
    
    result = df[feature_cols].fillna(0)
    
    return result

@app.get("/")
def root():
    return {"message": "House Price Prediction API", "version": "1.0"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(house: HouseFeatures):
    try:
        processed = preprocess_input(house.dict())
        price = model.predict(processed)[0]
        return {"predicted_price": round(price, 2), "currency": "USD"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
