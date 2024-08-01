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
    st.subheader("Inherited houses - Estimated sale price")

    st.write("The house features and estimated sale price (last column) is listed below.")

    # ============ Core ML logic ==============

    # load dataset for training and testing
    df = pd.read_csv("outputs/datasets/collection/house_price_records.csv")

    # split data 80/20
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop(["SalePrice"], axis=1), df["SalePrice"], test_size=0.2, random_state=0
    )

    # load the latest ml model pipeline that is optimised with only few best features
    version = "v5"
    ml_pipeline = load_pkl_file(
        f"outputs/ml_pipeline/predict_price/{version}/regression_pipeline.pkl"
    )

    # load best features from last saved pipeline, i.e. v5's train set
    best_features = pd.read_csv(
        "outputs/ml_pipeline/predict_price/v5/X_train.csv"
    ).columns.to_list()

    # Fit and transform to predict
    ml_pipeline.fit(X_train[best_features], y_train)

    # load raw dataset
    X_inherited_house_data = pd.read_csv(
        "outputs/datasets/collection/inherited_houses.csv"
    )

    # predict house prices
    y_predicted_price = ml_pipeline.predict(X_inherited_house_data[best_features])

    # ==== End of core ML logic ====

    # append the values
    X_inherited_house_data["Predicted Sale Price"] = y_predicted_price

    # convert data to int, as float precision is not relevant
    for col in X_inherited_house_data.select_dtypes(include=["float", "int"]).columns:
        X_inherited_house_data[col] = X_inherited_house_data[col].astype(int)

    # render dataframe on page
    st.dataframe(X_inherited_house_data)

    st.write(
        f"The sum of predicted sale price is {X_inherited_house_data['Predicted Sale Price'].sum()} USD"
    )

    st.header("Predict house sales prices in Ames, Iowa")

    st.write("Let's use our model to predict the price.")

    # == Core logic for live predictions ===

    def run_live_predictions(grLivArea,totalBsmtSF,garageArea,overallQual,bsmtFinSF1):
        """Takes house features values as input from widgets
        and use ML trained model to output estimated price

        Args:
            grLivArea (int): Ground Living Area SqFt
            totalBsmtSF (int): Total Basement SqFt
            garageArea (int): Garage Area SqFt
            overallQual (int): 1 being very poor, 10 being best
            bsmtFinSF1 (int): Basement type 1 finish area in SqFt
        """
        # create an empty dataframe with hold live values
        empty_df=X_train[best_features]
        df = empty_df[0:0].copy()
        
        df.loc[0,'GrLivArea']=grLivArea
        df.loc[0,'TotalBsmtSF']=totalBsmtSF
        df.loc[0,'GarageArea']=garageArea
        df.loc[0,'OverallQual']= overallQual
        df.loc[0,'BsmtFinSF1']= bsmtFinSF1
        live_predict_y=ml_pipeline.predict(df)

        st.write("Prediction resullts for given input data")
        st.dataframe(df)
        st.success(f'Estimated price : {int(live_predict_y[0])} USD')
        


    with st.form(key="input data"):
        col1, col2 = st.beta_columns(2)
        col3, col4 = st.beta_columns(2)

        with col1:
            grLivArea=st.number_input("Above Ground Living Area (SqFt)",key="GrLivArea", min_value=0, max_value=6000, step=50)
        with col2:
            totalBsmtSF=st.number_input("Total Basement Area (SqFt)", key="TotalBsmtSF", min_value=0, max_value=6000, step=50)
        with col3:
            garageArea=st.number_input("Garage Area (SqFt)",key="GarageArea", min_value=0, max_value=6000, step=50)
        
        with col4:
            bsmtFinSF1=st.number_input("Basement Type 1 finished (SqFt)",key="BsmtFinSF1", min_value=0, max_value=6000, step=50)

        overallQual=st.select_slider("Overall Quality", options= [1,2,3,4,5,6,7,8,9,10])
        
        # form submit button
        submitted=st.form_submit_button("Run predictions")

        # result display button
        if (submitted):
            run_live_predictions(grLivArea,totalBsmtSF,garageArea,overallQual,bsmtFinSF1)
    


    # Initialize the DataFrame in the session state if it doesn't exist
    if "df" not in st.session_state or st.session_state.reset_df:
        st.session_state.df = df  # Start with a default value
        st.session_state.reset_df = False





"""
    # Store the initial value of widgets in session state
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
        st.session_state.horizontal = True


    # Start a form
    with st.form("my_form"):
        # Create a number input widget and store input in a session state or local variable
        
        df.loc[0, "OverallQual"] = st.radio(
                                "Overall Quality",
                                [10,9,8,7,6,5,4,3,2,1],
                                index=None)

        col1, col2, col3 = st.beta_columns(3)

        with col1:
            st.header("A cat")
            st.image("https://static.streamlit.io/examples/cat.jpg")

        with col2:
            st.header("A dog")
            st.image("https://static.streamlit.io/examples/dog.jpg")

        with col3:
            st.header("An owl")
            st.image("https://static.streamlit.io/examples/owl.jpg")

        if submitted:
            # Update the DataFrame with the new input upon submission
            st.session_state.df.loc[0, "1stFlrSF"] = df.loc[0, "1stFlrSF"]

    # Display the DataFrame
    st.write("Values in DataFrame:")
    st.radio("choose an option", "hey")
    st.dataframe(df)

    col1, col2 = st.columns(2)

with col1:
    st.checkbox("Disable radio widget", key="disabled")
    st.checkbox("Orient radio options horizontally", key="horizontal")

with col2:
    st.radio(
        "Set label visibility 👇",
        ["visible", "hidden", "collapsed"],
        key="visibility",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        horizontal=st.session_state.horizontal,
    )

"""