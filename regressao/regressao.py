import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm
import seaborn as sb
import kagglehub
import os


# Load the dataset from Kaggle
path = kagglehub.dataset_download("sijovm/used-cars-data-from-ebay-kleinanzeigen")
df = pd.read_csv(os.path.join(path, "autos.csv"), encoding='latin-1')

print("Primeiros 5 registros:\n", df.head())

df = df[df['yearOfRegistration'].between(1920,2020)]

sb.histplot(df['yearOfRegistration'], kde=True)
plt.title('Distribuição de Carros por Ano de Registro')
plt.xlabel('Ano de Registro')
plt.ylabel('Densidade')
plt.grid()
plt.show()


# Criando o modelo de regressão linear
# previsoes_2 = sb.regplot(x='YearsExperience', y='Salary', data=wage, ci=None, line_kws={'color': 'blue'})
# plt.title('Salário em função da Experiência')
# plt.xlabel('Anos de Experiência')
# plt.ylabel('Salário')
# plt.grid()
# plt.show()

# model = sm.ols('Salary ~ YearsExperience', data=wage).fit()
# print(model.params)
# print(model.predict({'YearsExperience': 5}))