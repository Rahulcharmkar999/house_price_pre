
import pandas as pd
import joblib


# LOAD TRAINED MODEL

model = joblib.load("house_price_model.pkl")


# HOUSE INFORMATION

house = pd.DataFrame([{

    "propertyType": "Multistorey Apartment",

    "furnishing": "Semi-Furnished",

    "flrNum": 3,

    "facing": "East",

    "totalFlrNum": 6,

    "city": "Bhopal",

    "carpetArea": 1200,

    "bedrooms": 3,

    "bathrooms": 2

}])


# PREDICT HOUSE PRICE

prediction = model.predict(house)

price = float(prediction[0])


# DISPLAY PRICE

print("\n==========================================")
print("       HOUSE PRICE PREDICTION")
print("==========================================")

print(
    f"\nEstimated House Price: ₹{price:,.2f}"
)

# INDIAN PRICE FORMAT

if price >= 10000000:

    print(
        f"Approximate Price: ₹{price / 10000000:.2f} Crore"
    )

elif price >= 100000:

    print(
        f"Approximate Price: ₹{price / 100000:.2f} Lakh"
    )

elif price >= 1000:

    print(
        f"Approximate Price: ₹{price / 1000:.2f} Thousand"
    )

else:

    print(
        f"Approximate Price: ₹{price:.0f}"
    )


print("==========================================")

