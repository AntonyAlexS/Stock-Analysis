import streamlit as st
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_db_connection():
    return pymysql.connect(
        host="gateway01.us-west-2.prod.aws.tidbcloud.com",
        port=4000,
        user="4YaRT6wy6Sm9Xtc.root",
        password="Password",
        database="stock_market",
        ssl_verify_cert=True,
        ssl_verify_identity=True,
        ssl_ca=r"D:/Anto/Project/Project1/isrgrootx1.pem"
    )

# Function to run the SQL query and plot the results
def volatility_analysis():
    #SQL query for volatility analysis
    query = "select * from Volatility_Analysis;"
    conn = get_db_connection()
    try:
        df = pd.read_sql(query, conn)
        conn.close()
        
        if df is not None and not df.empty:
            # Plotting the bar chart
            plt.figure(figsize=(10, 5))
            sns.barplot(x="ticker", y="std_dev", data=df)
            plt.xlabel("Stock Ticker")
            plt.ylabel("Volatility (Standard Deviation of Returns)")
            plt.title("Top 10 Most Volatile Stocks Over the Past Year")
            plt.xticks(rotation=45)
            
            # Show the plot in Streamlit
            st.pyplot(plt)
            # Display the DataFrame
            df.index = range(1, len(df) + 1)
            st.write(df)
        
    except pymysql.Error as err:
        st.error(f"Error executing query: {err}")
        conn.close()

# Function for Cumulative Return Over Time Analysis
def cumulative_return_over_time():
    # SQL query to get cumulative return data
    query = "select * from Cumulative_Return;"
    
    conn = get_db_connection()
    try:
        df = pd.read_sql(query, conn)
        conn.close()
        
        if df is not None and not df.empty:
            # Plotting the cumulative returns for the top 10 performing stocks
            plt.figure(figsize=(10, 6))
            sns.lineplot(x='ticker',y='cumulative_return', data=df, marker='o', palette="viridis")
            plt.xlabel("Stocks")
            plt.ylabel("Cumulative Return")
            plt.title("Cumulative Return for Top 5 Performing Stocks Over the Year")
            plt.xticks(rotation=45)
            
            # Show the plot in Streamlit
            st.pyplot(plt)
            # Display the DataFrame
            df.index = range(1, len(df) + 1)
            st.write(df)
        
    except pymysql.Error as err:
        st.error(f"Error executing query: {err}")
        conn.close()

# Function for Sector-wise Performance Analysis
def sector_performance():
    
    # SQL query to get sector performance data
    query = "select * from Sector_Performance;"
    conn = get_db_connection()
    try:
        df = pd.read_sql(query, conn)
        conn.close()

        if df is not None and not df.empty:

            # Plot the sector-wise performance
            plt.figure(figsize=(12, 6))
            sns.barplot(x='sector', y='yearly_return', data=df)
            plt.xlabel("Sector")
            plt.ylabel("Average Yearly Return")
            plt.title("Sector-wise Performance of Stocks")
            plt.xticks(rotation=45)

            # Show plot in Streamlit
            st.pyplot(plt)

            # Display the DataFrame
            df.index = range(1, len(df) + 1)
            st.write(df)
        
    except pymysql.Error as err:
        st.error(f"Error executing query: {err}")
        conn.close()

# Function for Stock Price Correlation Analysis
def stock_correlation():
    # SQL query to get Stock Price Correlation data
    query = "select * from Stock_Price_Correlation;"

    conn = get_db_connection()
    try:
        df = pd.read_sql(query, conn)
        conn.close()

        if df is not None and not df.empty:
            df_final = df.iloc[:, 1:]  # Keep all rows and drop the first column
            # Plot the heatmap
            plt.figure(figsize=(50, 50))
            sns.heatmap(df_final, annot=True, cmap="coolwarm",yticklabels=df_final.columns)
            plt.title("Stock Price Correlation Heatmap")

            # Display heatmap in Streamlit
            st.pyplot(plt)

            # Display correlation matrix in Streamlit
            st.write("### Correlation Matrix")
            df.index = range(1, len(df) + 1)
            st.write(df)

    except pymysql.Error as err:
        st.error(f"Error executing query: {err}")
        conn.close()

# Function for Top 5 Gainers & Losers (Month-wise)
def monthly_gainers_losers():
    st.title("Top 5 Gainers and Losers (Month-wise)")

    # SQL query to get stock prices monthly average return
    query = "select * from monthly_avg_return;"

    conn = get_db_connection()
    try:
        df = pd.read_sql(query, conn)
        conn.close()

        if df is not None and not df.empty:
            # Get unique months
            unique_months = sorted(df["month"].unique())

            # Create plots for each month
            for month in unique_months:
                st.subheader(f"{month} - Top 5 Gainers & Losers")

                # Filter data for the specific month
                month_df = df[df["month"] == month]

                # Identify top 5 gainers and top 5 losers
                top_gainers = month_df.nlargest(5, "monthly_return")
                top_losers = month_df.nsmallest(5, "monthly_return")

                # Plot top gainers
                fig, ax = plt.subplots(1, 2, figsize=(14, 5))
                
                sns.barplot(x="monthly_return", y="ticker", data=top_gainers, ax=ax[0], palette="Greens_r")
                ax[0].set_title(f"Top 5 Gainers - {month}")
                ax[0].set_xlabel("Monthly Return (%)")
                ax[0].set_ylabel("Stock Ticker")

                # Plot top losers
                sns.barplot(x="monthly_return", y="ticker", data=top_losers, ax=ax[1], palette="Reds_r")
                ax[1].set_title(f"Top 5 Losers - {month}")
                ax[1].set_xlabel("Monthly Return (%)")
                ax[1].set_ylabel("Stock Ticker")

                # Show plots in Streamlit
                st.pyplot(fig)

    except pymysql.Error as err:
        st.error(f"Error executing query: {err}")
        conn.close()

# Streamlit App layout for running SQL queries
def stock():
    st.title("Stock Analysis")
    
    analysis = st.selectbox("Choose an analysis", [
        "1. Volatility Analysis",
        "2. Cumulative Return Over Time",
        "3. Sector-wise Performance",
        "4. Stock Price Correlation",
        "5. Top 5 Gainers and Losers (Month-wise)",
    ])

    # Run Volatility Analysis if selected
    if analysis == "1. Volatility Analysis":
        volatility_analysis()
    elif analysis == "2. Cumulative Return Over Time":
        cumulative_return_over_time()
    elif analysis == "3. Sector-wise Performance":
        sector_performance()
    elif analysis == "4. Stock Price Correlation":
        stock_correlation()
    elif analysis == "5. Top 5 Gainers and Losers (Month-wise)":
        monthly_gainers_losers()


# Run the Streamlit app
if __name__ == "__main__":
    stock()
