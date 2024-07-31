import streamlit as st
import pandas as pd
from datetime import date
from src.data_management import load_housing_data, load_pkl_file
from sklearn.model_selection import train_test_split


def page_sale_price_prediction():
    """
    Displays sale price prediction for inherited
    as well as property with any given feautures in Iowa
    """

    # Business Requirement info
    st.info(
        """
        **Business Requirement-2**

        The client is interested in predicting the house sale prices from her 4 inherited houses\
            and any other house in Ames, Iowa.
        """
    )
    # subheader
    st.subheader("Estimated sale price for client's inherited houses")

    # ============ Core ML logic ==============

    # load dataset for training and testing
    df = pd.read_csv("outputs/datasets/collection/house_price_records.csv")

    # split data 80/20
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop(["SalePrice"], axis=1), df["SalePrice"], test_size=0.2, random_state=0
    )

    # load the latest ml model pipeline that is optimised
    version = "v4"
    ml_pipeline = load_pkl_file(
        f"outputs/ml_pipeline/predict_price/{version}/regression_pipeline.pkl"
    )
    house_features = pd.read_csv(
        "outputs/datasets/collection/inherited_houses.csv"
    ).columns.to_list()

    st.write("Find below 4 inherited houses profile and their estimated sale price")

    # Fit and transform to predict
    ml_pipeline.fit(X_train, y_train)
    
    # load raw dataset
    X_inherited_house_data=pd.read_csv("outputs/datasets/collection/inherited_houses.csv")

    # predict house prices
    y_predicted_price=ml_pipeline.predict(X_inherited_house_data)

    # ==== End of core ML logic ====

    # append the values
    X_inherited_house_data['Predicted Sale Price']=y_predicted_price
    
    # convert data to int, as float precision is not relevant
    for col in X_inherited_house_data.select_dtypes(include=['float', 'int']).columns:
        X_inherited_house_data[col] = X_inherited_house_data[col].astype(int)

    # render dataframe on page
    st.dataframe(X_inherited_house_data)

    st.write(f"The sum of predicted sale price is {X_inherited_house_data['Predicted Sale Price'].sum()} USD")

    st.subheader("Predict house sales prices in Ames, Iowa")

    # draw input widgets
    def DrawInputsWidgets():

    # load dataset
        df = load_housing_data()
        df['TotalSF'] = df['TotalBsmtSF'] + df['1stFlrSF'] + df['2ndFlrSF']

        percentageMin, percentageMax = 0.4, 2.0

        # we create input widgets only for 6 features	
        col1, col2, col3, col4 = st.columns(4)
        col5, col6, col7, col8 = st.columns(4)

        # We are using these features to feed the ML pipeline - values copied from check_variables_for_UI() result
            

        # create an empty DataFrame, which will be the live data
        X_live = pd.DataFrame([], index=[0]) 

        # from here on we draw the widget based on the variable type (numerical or categorical)
        # and set initial values
        with col1:
            feature = "GarageArea"
            st_widget = st.number_input(
                label= feature,
                min_value= int(df[feature].min()*percentageMin), 
                max_value= int(df[feature].max()*percentageMax),
                value= int(df[feature].median()), 
                step= 50
                )
            
        X_live[feature] = st_widget


        with col2:
            feature = "GrLivArea"
            st_widget = st.number_input(
                label= feature,
                min_value= int(df[feature].min()*percentageMin), 
                max_value= int(df[feature].max()*percentageMax),
                value= int(df[feature].median()), 
                step= 50
                )
        X_live[feature] = st_widget

        with col3:
            feature = "OverallQual"
            st_widget = st.number_input(
                label= feature,
                min_value= 1, 
                max_value= 10,
                value= 5, 
                step=1
                )
        X_live[feature] = st_widget

        with col4:
            feature = "TotalBsmtSF"
            st_widget = st.number_input(
                label= feature,
                min_value= int(df[feature].min()*percentageMin), 
                max_value= int(df[feature].max()*percentageMax),
                value= int(df[feature].median()), 
                step= 50
                )
        X_live[feature] = st_widget

        with col5:
            feature = "YearBuilt"
            st_widget = st.number_input(
                label= feature,
                min_value= int(df[feature].min()*percentageMin), 
                max_value= date.today().year,
                value= int(df[feature].median()), 
                step= 1
                )
        X_live[feature] = st_widget

        return X_live
    st.info(f"The predicted sale price for this house in Iowa is")
