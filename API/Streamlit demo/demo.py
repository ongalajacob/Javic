import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
import pickle
import streamlit as st
import matplotlib.pyplot as plt

model = pickle.load(open('regression_model.pkl', 'rb'))

def main():
    numerical_continuous = ['age', 'bmi']
    numerical_discrete = ['children']
    categorical = ['sex', 'smoker', 'region']

    st.title('Insuarance Analysis.')

    selection = st.sidebar.selectbox('Select your analysis option:', 
        ('Analysis', 'Prediction'))

    #data = pd.read_csv('insurance.csv')
    uploaded_file = st.file_uploader("Upload a CSV file:", type = ["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)

        if selection == 'Analysis':

            st.header(selection)
            st.dataframe(data.head())
            st.dataframe(data.info())
            st.dataframe(data.dtypes)
            st.dataframe(data.describe())

            st.subheader('Age Distribution.')
            fig, axis = plt.subplots()
            axis.hist(data['age'], bins = 100)
            st.pyplot(fig)

            st.subheader('Outlier Detection.')
            fig, axis = plt.subplots()
            axis.boxplot(data[numerical_continuous])
            axis.set_xticklabels(numerical_continuous)
            st.pyplot(fig)

        elif selection == 'Prediction':

            st.header(selection)
            thresh = st.number_input('Key in your threshold:', value = 0.3705)

            def modeling(data, threshold = thresh):

                #threshold = 0.3705
                zscore = np.abs(stats.zscore(data[['bmi']]))
                data = data[(zscore > threshold).all(axis = 1)]
                
                encoded_features = {}
                for column in numerical_discrete + categorical:
                    encoded_features[column] = data.groupby([column])['charges'].median().to_dict()
                    data[column] = data[column].map(encoded_features[column])

                X = data.drop(['children', 'charges'], axis = 1)
                scaler = StandardScaler()
                X = scaler.fit_transform(X)
                y_predict = np.exp(model.predict(X))
                
                return pd.DataFrame(y_predict, columns = ['Predictions'])

            y_predict = modeling(data)
            st.write(thresh)
            st.dataframe(y_predict)

if __name__ == '__main__':
    main()