from fastapi import APIRouter
import pickle
import numpy as np
from pathlib import Path

router = APIRouter(prefix="/models", tags=["models"])
MODELS_DIR = Path(__file__).parent.parent.parent.parent / "models"
_scatter_cache = None

@router.get("/metrics")
async def get_metrics():
    return {
        "regression": [
            {"name": "Linear Regression", "rmse": 0.1348, "r2": 0.9018, "mae": 0.0783},
            {"name": "Decision Tree", "rmse": 0.1888, "r2": 0.8074, "mae": 0.1123},
            {"name": "Random Forest", "rmse": 0.1175, "r2": 0.9254, "mae": 0.0812},
        ],
        "classification": [
            {"name": "Logistic Regression", "accuracy": 0.86, "f1": 0.86},
            {"name": "Decision Tree", "accuracy": 0.78, "f1": 0.78},
            {"name": "Random Forest", "accuracy": 0.87, "f1": 0.87},
        ]
    }

@router.get("/clusters")
async def get_clusters():
    return {
        "clusters": [
            {"id": 0, "name": "Mid-range", "avg_price": 194155, "avg_sf": 0.16, "count": 823},
            {"id": 1, "name": "Affordable", "avg_price": 147507, "avg_sf": -0.36, "count": 756},
            {"id": 2, "name": "Luxury", "avg_price": 314704, "avg_sf": 1.52, "count": 412},
            {"id": 3, "name": "Budget", "avg_price": 117039, "avg_sf": -0.75, "count": 939},
        ]
    }

@router.get("/feature-importance")
async def get_feature_importance():
    with open(MODELS_DIR / "rf_regressor.pkl", "rb") as f:
        rf = pickle.load(f)
    importances = rf.feature_importances_
    feature_names = rf.feature_names_in_
    indices = np.argsort(importances)[-10:][::-1]
    return {
        "features": [
            {"name": str(feature_names[i]), "importance": float(importances[i])}
            for i in indices
        ]
    }

@router.get("/clusters/scatter")
async def get_clusters_scatter():
    global _scatter_cache
    if _scatter_cache:
        return _scatter_cache

    import pandas as pd
    from sklearn.decomposition import PCA
    from src.data_engineering.ingestion.loader import load_raw_data
    from src.data_engineering.transformation.cleaners import MissingValueHandler
    from src.data_engineering.feature_store.features import FeatureCreator

    df = load_raw_data("AmesHousing.csv")
    df = MissingValueHandler().fit_transform(df)
    df = FeatureCreator().fit_transform(df)

    cluster_features = ['Total_SF', 'Total_Quality', 'House_Age',
                        'Total_Bathrooms', 'Total_Porch_SF',
                        'Has_Garage', 'Has_Fireplace',
                        'Overall Qual', 'Gr Liv Area']

    with open(MODELS_DIR / "kmeans.pkl", "rb") as f:
        kmeans = pickle.load(f)

    X = df[cluster_features]
    clusters = kmeans.predict(X).tolist()
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    _scatter_cache = {
        "points": [
            {
                "x": float(X_pca[i, 0]),
                "y": float(X_pca[i, 1]),
                "cluster": clusters[i],
                "price": int(df['SalePrice'].iloc[i])
            }
            for i in range(len(clusters))
        ]
    }
    return _scatter_cache