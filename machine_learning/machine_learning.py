from functions_machine_learning import rate_to_num, price_treatment, availability_number
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pandas as pd

df = pd.read_csv('../books.csv')
df['rating_numeric'] = df['Rate'].apply(rate_to_num)
df['price_numeric'] = df['Price'].apply(price_treatment)
df['high_rating'] = (df['rating_numeric'] >= 4).astype(int)
df['availability_numeric'] = df['Availability'].apply(availability_number)
df['num_reviews_numeric'] = pd.to_numeric(df['Number of Reviews'], errors='coerce').fillna(0)

features = ['price_numeric', 'availability_numeric', 'num_reviews_numeric']
X = df[features]
y = df['high_rating']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

model = RandomForestClassifier(random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)



acertos = sum(y_pred == y_test)
print(f'Acertamos {acertos} previsões')
erros = sum(y_pred != y_test)
print(f'Erramos {erros} previsões')

taxa_acerto = (acertos/len(y_test)) * 100

print(taxa_acerto)
print(classification_report(y_test, y_pred, target_names=['Baixa avaliação', 'Alta avaliação']))