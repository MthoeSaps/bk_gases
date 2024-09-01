import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import io

# Read the Excel files
file1 = 'c:/Users/mthoe/OneDrive/Desktop/pos_system/dbs/t1gases_dbs.xlsx'  # USD payments
file2 = 'c:/Users/mthoe/OneDrive/Desktop/pos_system/dbs/zar_payments.xlsx'  # ZAR payments

df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

# Combine the DataFrames
df = pd.concat([df1, df2], ignore_index=True)

# Streamlit app
st.set_page_config(layout="wide")

st.title("Gas Sales Data")

# Sidebar filters
st.sidebar.title("Filters")
payment_type = st.sidebar.selectbox("Payment Type", ["All", "USD", "ZAR"])
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

# Filter the data based on the selected options
if payment_type == "USD":
    df = df1
elif payment_type == "ZAR":
    df = df2
elif payment_type == "All":
    df = pd.concat([df1, df2], ignore_index=True)

df = df.loc[(df['time stamp'] >= start_date) & (df['time stamp'] <= end_date)]

# Display the data
st.subheader("Raw Data")
st.dataframe(df)

# Create Plotly charts
st.subheader("Plots")

# Amount Sold vs Time
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df['time stamp'], y=df['amount sold'], mode='lines+markers'))
fig1.update_layout(title='Amount Sold vs Time', xaxis_title='Time Stamp', yaxis_title='Amount Sold')
st.plotly_chart(fig1, use_container_width=True)

# KGs Gas Sold vs Time
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df['time stamp'], y=df['kgs gas sold'], mode='lines+markers'))
fig2.update_layout(title='KGs Gas Sold vs Time', xaxis_title='Time Stamp', yaxis_title='KGs Gas Sold')
st.plotly_chart(fig2, use_container_width=True)

# Gas Price vs Time
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=df['time stamp'], y=df['gas price'], mode='lines+markers'))
fig3.update_layout(title='Gas Price vs Time', xaxis_title='Time Stamp', yaxis_title='Gas Price')
st.plotly_chart(fig3, use_container_width=True)

# Display payment type information
st.subheader("Payment Type Information")
st.write(f"File 1 contains USD payments.")
st.write(f"File 2 contains ZAR payments.")

# Download button
#if st.sidebar.subheader("Download Data"):
    # Create an in-memory buffer to store the Excel file

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='openpyxl', mode='w') as writer:
    df.to_excel(writer, sheet_name='Gas Sales Data', index=False)
    st.download_button(
    label="Download data as Excel",
    data=buffer.getvalue(),
    file_name="gas_sales_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)