import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from functions_model import rate_to_num, price_treatment

# Load data file
df = pd.read_csv('../books.csv')

# Map rating text to numerical value
df['Rate_Num'] = df['Rate'].apply(rate_to_num)

# Clean 'Price' column removing currency symbol and converting to float
df['Price'] = df['Price'].apply(price_treatment)

# Drop rows with missing values
df = df.dropna(subset=['Price', 'Rate_Num'])

# Define input(x) and target(y)
X = df[['Price']]
y = df['Rate_Num']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=42)

# Train linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Tested with {len(y_test)} books")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"R-squared (R²): {r2:.2f}")

# Round predictions to the nearest whole rating and calculate accuracy
y_pred_round = y_pred.round().clip(1, 5).astype(int)
correct = (y_pred_round == y_test).sum()
accuracy = (correct / len(y_test)) * 100
print(f"Accuracy: {accuracy:.0f}%")
print(f"coefficient: {model.coef_}")
