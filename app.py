import streamlit as st
import pandas as pd
import plotly.express as px
# Load dataset
bayut_df = pd.read_csv("final_bayut.csv")

# Drop to the Unnamed column from the dataset
bayut_df.drop(columns="Unnamed: 0", inplace=True)

# Setup streamlit app layout
st.title("Bayut Webscraping dataset EDA")
st.write("Today i will make a Simple EDA Application for Bayut houses dataset.")
website_link = "https://www.bayut.eg/en/egypt/properties-for-sale/"
st.write("The Website link: [Bayut Website](%s)" % website_link)
st.sidebar.header("Navigation")
st.sidebar.markdown("Created by [Ahmed Yusri](https://www.linkedin.com/in/ahmed-yusri-499a67313)")
st.sidebar.image("bayut_logo.png")
# Create an set of options for user to select
sidebar_option = st.sidebar.radio("Choose an Option:", ["Data Overview", "EDA", "Visualizations", "Recommendations"])
# 1. Data Overview part 
if sidebar_option == "Data Overview":
    st.header("Data Overview")
    st.write("A random sample from the dataset that shows some data description about property description, property type, price, etc...")
    st.write(bayut_df.sample(5))
    st.markdown("### Dataset Summary")
    st.write(bayut_df.describe())
    st.markdown("### Data Quality")
    st.write("See if there is an missing values")
    st.write(bayut_df.isnull().sum())

elif sidebar_option == "EDA":
     st.header("Exploratory Data Analysis")
     
     # 1. Put a select radio to choose to see a uni or bivariant analysis
     analysis_type_option = st.sidebar.radio("Choose type of Analysis:", ["Univariant analysis", "Bivariant analysis"])
     if analysis_type_option == "Univariant analysis":
         st.subheader("Interactive Univariant analysis for each Numerical column") 
         num_df = bayut_df.drop(columns=["Property description", "Property type", "Property location"])
         column_names = list(num_df.columns)
         selected_col = st.sidebar.selectbox(f"Select column for analysis", column_names)
         st.write(f"The {selected_col} Mean: {round(bayut_df[selected_col].mean(), 2)}")
         st.write(f"The {selected_col} Standard deviation: {round(bayut_df[selected_col].std(), 2)}")
         fig1 = px.histogram(num_df, x=f"{selected_col}", nbins=30, title=f"Histogram of {selected_col}")
         st.plotly_chart(fig1)
         st.write("Most of the columns are Left skwed So if there any NaNs in this columns must fill by `mean()`")
         fig6 = px.box(data_frame=num_df, x=f"{selected_col}")
         st.plotly_chart(fig6)
         st.write("Most of them has Outliers values ecxpect Baths columns have no upper bound because the median and q3 and upper bound are the same.")
     elif analysis_type_option == "Bivariant analysis":
             st.subheader("Bivariant analysis")
             st.markdown("### Plot the Highest  Property house type in price")
             price_per_house = bayut_df.groupby("Property type")["Property price"].max()
             highest_house_price = price_per_house.sort_values(ascending=False)
             fig5 = px.bar(
                 data_frame=highest_house_price,
                 x=highest_house_price.values / 1e6,  # Convert values to millions
                 y=highest_house_price.index,        # Use the index for the y-axis
                 orientation='h',                    # Horizontal orientation
                 labels={'x': 'Price (in millions)', 'y': 'Houses'},  # Label axes
                 title='House Prices (Highest to Lowest)'            # Add a title
                 )
             fig5.update_layout(
                yaxis={'categoryorder':'total ascending'}  # Sort categories by total values in ascending order
                )
             st.plotly_chart(fig5)
             st.write("It seems that villa is the most high in the price")
             fig2 = px.scatter(data_frame=bayut_df, x="Property Area", y="Number of Baths ", title="Corrlation between the Independent feature Number of Bath and dependent feature Area")
             st.plotly_chart(fig2)
             st.write("See the relation between Number of Baths and Area is below the avarage so i makes the area is full sure dependent")
             fig3 = px.scatter(data_frame=bayut_df, x="Property price", y="Property Area", title="Correlation between Property Price and Area")
             st.plotly_chart(fig3)
             st.write("The correlation between Property Price and Area is very high so most of high houses in each type must be high in Area size and in Price")
             st.markdown("### Heatmap plot")
             corr_matrix = bayut_df.corr(numeric_only=True) # To get the numertic values 
             fig4 = px.imshow(
                 corr_matrix,
                 text_auto=True,             # Display correlation values on the heatmap
                 color_continuous_scale="peach",
                 zmin=-1, 
                 zmax=1,
                 labels=dict(x="Features", y="Features", color="Correlation")
                 )
             st.plotly_chart(fig4)
             st.write("The relationship between the features is high this is because the two Independent features  Beds, Baths and dependent features Area, Price")
             
# Visualizations with Interactive Widgets        
elif sidebar_option == "Visualizations":
    st.header("Interactive Visualizations")
    type_option = st.selectbox("Select Property Type", bayut_df["Property type"].unique())
    filitered_df = bayut_df[bayut_df["Property type"] == type_option]
    price_on_location = filitered_df.groupby("Property location")["Property price"].max()
    most_10_high_price = price_on_location.sort_values(ascending=False)[:10]
    fig7 = px.bar(
    data_frame=most_10_high_price,
    x=most_10_high_price.values / 1e6, 
    y=most_10_high_price.index,      
    orientation='h',                    # Horizontal orientation
    labels={'x': 'Price (in millions)', 'y': 'Houses'},  
    title='Most 10 high House Prices depend on Location'
    )
    fig7.update_layout(
    yaxis={'categoryorder':'total ascending'}  # Sort categories by total values in ascending order
    )
    st.plotly_chart(fig7)
    most_10_cheap_price = price_on_location.sort_values(ascending=True)[:10]
    fig8 = px.bar(
    data_frame=most_10_cheap_price,
    x=most_10_cheap_price.values / 1e6, 
    y=most_10_cheap_price.index,        
    orientation='h',                    # Horizontal orientation
    labels={'x': 'Price (in millions)', 'y': 'Houses'},  
    title='Most 10 cheap House Prices depend on Location'
    )
    fig8.update_layout(
    yaxis={'categoryorder':'total ascending'}  # Sort categories by total values in ascending order
    )
    st.plotly_chart(fig8)
    st.write("It seem the price is doesn't depend on Area only but the location is also a great factor that the price depends on.")
                    
             
elif sidebar_option == "Recommendations":
    st.header("My Recommendations for bayut")
    st.write("1. Make the website more user friendly like to add some price options like minimum and maximum price in the front page not make it more Filters")
    st.write("2. They mainly focus on some compounds in Cairo and 6-October they must spread their products in more wide ranges of cities")
    st.write("3. Make some sales in the house prices and notify the user about this sales price")