import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_management import load_pkl_file
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


def page_ml_sale_predict_body():
    st.info(
        """
        - The pipeline was tunes aiming for R2 score of at least 0.7 on train and test set.

        - The pipeline performance on train and test set is 0.87 and 0.79 respectively.

        - Additional efforts were made to reduce R2 score difference between train and test set
        to reduce overfitting.

        - Additional efforts were made to reduce complexity of pipeline while maintaining performance.
        """
    )

    st.subheader("Pipeline steps")

    st.write("Aftre reducing complexity, the pipeline is comprised of three steps")

    st.write(
        """
        1. Feature engineering step ( Winsoriser for dealing with outliers)
        2. Scaling (StandardScaler for reducing the scale effect)
        3. Model (GradientBoostingRegressor)
        """
    )

    st.write("**Pipeline**")

    st.code(
        """
        Pipeline(
        steps=[
            (
                "Winsoriser_iqr",
                Winsorizer(
                    capping_method="iqr",
                    tail="both",
                    variables=["GarageArea", "GrLivArea", "TotalBsmtSF"],
                ),
            ),
            ("feat_scaling", StandardScaler()),
            (
                "model",
                GradientBoostingRegressor(
                    min_samples_leaf=50, n_estimators=140, random_state=0
                ),
            ),
        ]
    )
        """
    )

    st.write(
        """
        The following steps were removed from v4 to v5 after selecting most correlated features,
        which lead to such simplication.

        - Drop Columns
        - Transformers
        - Missing data imputations
        - Select from model 
        """
    )

    st.info(
        "PS : There is no performance difference between v4 and v5 of pipeline,\
        just complexity reduction"
    )

    st.subheader("ML pipeline development summary")

    st.markdown(
        """
        | **Pipeline**                                 	| **Version** 	| Mean R2  (Train) 	| Mean R2  (Test) 	| delta R2 	|
|----------------------------------------------	|-------------	|------------------	|-----------------	|----------	|
| gradientboost with default hyper param       	| v1          	| 0.94             	| 0.81            	| 0.13     	|
| parameter optimised                          	| v2          	| 0.91             	| 0.81            	| 0.10     	|
| additional feature selelection pipeline step 	| v3          	| 0.83             	| 0.76            	| 0.7      	|
| feature selection optimised                  	| v4          	| 0.87             	| 0.79            	| 0.8      	|
| rewrite PL with only selected input features  	| v5          	| 0.87             	| 0.79            	| 0.8      	|

        """
    )
    st.write("\n")
    st.write("The features used by pipeline and its imporatnce is displayed below")

    st.image(
        "docs/images/features_importance.png",
        caption="ML pipeline feature and importance",
    )

    st.subheader("Pipeline Performance")

    # ========== Data and Pipeline import =========

    # Import dataset and split into train and test
    from sklearn.model_selection import train_test_split

    # load dataset for training and testing
    df = pd.read_csv("outputs/datasets/collection/house_price_records.csv")

    # split data 80/20
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop(["SalePrice"], axis=1), df["SalePrice"], test_size=0.2, random_state=0
    )

    # Import pipeline
    version = "v4"  # Note that there no perf difference between v4 and v5
    ml_pipeline = load_pkl_file(
        f"outputs/ml_pipeline/predict_price/{version}/regression_pipeline.pkl"
    )

    # ========== Regression Performance check =========

    def regression_performance(X_train, y_train, X_test, y_test, pipeline):
        st.write("* Train Set")
        regression_evaluation(X_train, y_train, pipeline)
        st.write("* Test Set")
        regression_evaluation(X_test, y_test, pipeline)

    def regression_evaluation(X, y, pipeline):
        prediction = pipeline.predict(X)
        st.write("R2 Score:", r2_score(y, prediction).round(3))
        st.write("Mean Absolute Error:", mean_absolute_error(y, prediction).round(3))
        st.write("Mean Squared Error:", mean_squared_error(y, prediction).round(3))
        st.write(
            "Root Mean Squared Error:",
            np.sqrt(mean_squared_error(y, prediction)).round(3),
        )
        st.write("\n")

    def regression_evaluation_plots(
        X_train, y_train, X_test, y_test, pipeline, alpha_scatter=0.5
    ):
        pred_train = pipeline.predict(X_train)
        pred_test = pipeline.predict(X_test)

        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
        sns.scatterplot(x=y_train, y=pred_train, alpha=alpha_scatter, ax=axes[0])
        sns.lineplot(x=y_train, y=y_train, color="red", ax=axes[0])
        axes[0].set_xlabel("Actual")
        axes[0].set_ylabel("Predictions")
        axes[0].set_title("Train Set")

        sns.scatterplot(x=y_test, y=pred_test, alpha=alpha_scatter, ax=axes[1])
        sns.lineplot(x=y_test, y=y_test, color="red", ax=axes[1])
        axes[1].set_xlabel("Actual")
        axes[1].set_ylabel("Predictions")
        axes[1].set_title("Test Set")
        # plt.savefig(f'docs/regression_plots/regression_performance.png', bbox_inches='tight')
        st.pyplot(fig)

    # check its regression performance
    regression_performance(X_train, y_train, X_test, y_test, ml_pipeline)
    regression_evaluation_plots(X_train, y_train, X_test, y_test, ml_pipeline)
