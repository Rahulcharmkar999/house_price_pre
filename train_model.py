
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

import numpy as np


# LOAD DATASET

DATASET = "Scraped_Data.csv"

print("==========================================")
print("Loading Dataset...")
print("==========================================")

df = pd.read_csv(DATASET)

print("Dataset Shape:", df.shape)


# FEATURES AND TARGET

FEATURES = [

    "propertyType",
    "furnishing",
    "flrNum",
    "facing",
    "totalFlrNum",
    "city",
    "carpetArea",
    "bedrooms",
    "bathrooms"

]

TARGET = "exactPrice"


# CHECK REQUIRED COLUMNS

required_columns = FEATURES + [TARGET]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    print("\nERROR: Missing columns:")

    for column in missing_columns:
        print("-", column)

    raise ValueError(
        "Required columns are missing from Scraped_Data.csv"
    )


# SELECT REQUIRED DATA

df = df[
    required_columns
].copy()


# CLEAN TARGET

df[TARGET] = pd.to_numeric(
    df[TARGET],
    errors="coerce"
)


# Remove invalid / missing prices
df = df[
    df[TARGET].notna()
]

df = df[
    df[TARGET] > 9
]


# CLEAN NUMERIC COLUMNS

numeric_features = [

    "flrNum",
    "totalFlrNum",
    "carpetArea",
    "bedrooms",
    "bathrooms"

]


for column in numeric_features:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# FLOOR CLEANING

def clean_floor(value):

    if pd.isna(value):
        return np.nan

    value = str(value).strip().lower()

    if value == "ground":
        return 0

    try:
        return float(value)

    except:
        return np.nan


df["flrNum"] = df["flrNum"].apply(
    clean_floor
)


# CLEAN CATEGORICAL COLUMNS

categorical_features = [

    "propertyType",
    "furnishing",
    "facing",
    "city"

]


for column in categorical_features:

    df[column] = (
        df[column]
        .astype(str)
        .str.strip()
    )


# Convert fake "nan" strings back to missing
for column in categorical_features:

    df[column] = df[column].replace(
        ["nan", "NaN", "", "None"],
        np.nan
    )


# REMOVE DUPLICATES

df = df.drop_duplicates()


print("\nCleaned Dataset Shape:", df.shape)


# INPUT AND TARGET

X = df[FEATURES]

y = df[TARGET]


# TRAIN / TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42

)


print("\n==========================================")
print("Training Model...")
print("==========================================")


# NUMERIC PIPELINE

numeric_transformer = Pipeline(
    steps=[

        (
            "imputer",
            SimpleImputer(
                strategy="median"
            )
        )

    ]
)


# CATEGORICAL PIPELINE

categorical_transformer = Pipeline(
    steps=[

        (
            "imputer",
            SimpleImputer(
                strategy="most_frequent"
            )
        ),

        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )

    ]
)


# PREPROCESSOR

preprocessor = ColumnTransformer(

    transformers=[

        (
            "numeric",
            numeric_transformer,
            numeric_features
        ),

        (
            "categorical",
            categorical_transformer,
            categorical_features
        )

    ]

)


# RANDOM FOREST MODEL

regressor = RandomForestRegressor(

    n_estimators=300,

    max_depth=25,

    min_samples_split=2,

    min_samples_leaf=1,

    random_state=42,

    n_jobs=-1

)


# COMPLETE ML PIPELINE

model = Pipeline(

    steps=[

        (
            "preprocessor",
            preprocessor
        ),

        (
            "regressor",
            regressor
        )

    ]

)


# TRAIN

model.fit(

    X_train,
    y_train

)


print("\nModel Training Completed!")


# TEST PREDICTION

predictions = model.predict(
    X_test
)


# MODEL EVALUATION

mae = mean_absolute_error(
    y_test,
    predictions
)


rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions
    )
)


r2 = r2_score(
    y_test,
    predictions
)


# DISPLAY RESULTS

print("\n==========================================")
print("MODEL PERFORMANCE")
print("==========================================")

print(
    f"Mean Absolute Error : ₹{mae:,.2f}"
)

print(
    f"Root Mean Squared Error : ₹{rmse:,.2f}"
)

print(
    f"R² Score : {r2:.4f}"
)

print("==========================================")


# SAVE MODEL

MODEL_FILE = "house_price_model.pkl"

joblib.dump(
    model,
    MODEL_FILE
)


print(
    f"\nModel saved successfully as: {MODEL_FILE}"
)

print("==========================================")

