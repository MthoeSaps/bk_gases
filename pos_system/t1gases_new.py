import streamlit as st
import pandas as pd
from datetime import datetime

def calculate_gas_sold(amount_paid):
    gas_price = 1.80  # $1.80 per 1kg of gas
    return amount_paid / gas_price

def calculate_gas_sold_zar(amount_paid):
    gas_price = 20  # 20 ZAR per 1kg of gas
    return amount_paid / gas_price

def save_to_excel(amount_paid, gas_sold, is_zar):
    file_path = 'pos_system/dbs/zar_payments.xlsx' if is_zar else 'pos_system/dbs/t1gases_dbs.xlsx'
    gas_price = 20 if is_zar else 1.80

    try:
        df = pd.read_excel(file_path)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df = pd.DataFrame(columns=['amount sold', 'kgs gas sold', 'gas price', 'time stamp'])

    new_row = {
        'amount sold': amount_paid,
        'kgs gas sold': gas_sold,
        'gas price': gas_price,
        'time stamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    df.loc[len(df)] = new_row
    df.to_excel(file_path, index=False)

def delete_last_entry(is_zar):
    file_path = 'pos_system/dbs/zar_payments.xlsx' if is_zar else 'pos_system/dbs/t1gases_dbs.xlsx'
    try:
        df = pd.read_excel(file_path)
        df = df.iloc[:-1]
        df.to_excel(file_path, index=False)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return

def reset_database(is_zar):
    df = pd.DataFrame(columns=['amount sold', 'kgs gas sold', 'gas price', 'time stamp'])
    file_path = 'pos_system/dbs/zar_payments.xlsx' if is_zar else 'pos_system/dbs/t1gases_dbs.xlsx'
    df.to_excel(file_path, index=False)

def main():
    st.set_page_config(page_title="Gas Selling App", layout="wide")
    st.title("🚀 Gas Selling App")
    st.write("**Price:** $1.80/kg or 20 ZAR/kg")

    # Load data
    try:
        df_usd = pd.read_excel('pos_system/dbs/t1gases_dbs.xlsx')
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df_usd = pd.DataFrame(columns=['amount sold', 'kgs gas sold', 'gas price', 'time stamp'])

    try:
        df_zar = pd.read_excel('pos_system/dbs/zar_payments.xlsx')
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df_zar = pd.DataFrame(columns=['amount sold', 'kgs gas sold', 'gas price', 'time stamp'])

    # Calculate totals
    total_gas_sold = df_usd['kgs gas sold'].sum() + df_zar['kgs gas sold'].sum()
    total_sales_usd = df_usd['amount sold'].sum()
    total_sales_zar = df_zar['amount sold'].sum()

    # Display metrics with custom styling
    st.markdown("""
    <style>
        .metric {
            font-size: 24px;
            font-weight: bold;
            color: #1e90ff;
        }
        .stButton > button {
            background-color: #1e90ff; /* Button color */
            color: white; /* Text color */
            border: none; /* Remove border */
            border-radius: 8px; /* Rounded corners */
            padding: 10px 20px; /* Padding */
            font-size: 16px; /* Font size */
            cursor: pointer; /* Pointer cursor */
            transition: background-color 0.3s; /* Transition effect */
        }
        .stButton > button:hover {
            background-color: #63a4ff; /* Lighter shade on hover */
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<p class='metric'>Total Gas Sold (kg): {total_gas_sold:.2f}</p>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<p class='metric'>Total Sales (USD): ${total_sales_usd:.2f}</p>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<p class='metric'>Total Sales (ZAR): {total_sales_zar:.2f} ZAR</p>", unsafe_allow_html=True)

    payment_type = st.radio("Select Payment Type:", ("USD", "ZAR"))

    if payment_type == "USD":
        amount_paid = st.number_input("Enter the amount paid (in $):", min_value=0.0, step=0.01)
        if st.button("Enter Payment"):
            gas_sold = calculate_gas_sold(amount_paid)
            save_to_excel(amount_paid, gas_sold, False)
            st.success(f"You bought {gas_sold:.2f} kg of gas.")
    else:
        amount_paid = st.number_input("Enter the amount paid (in ZAR):", min_value=0.0, step=0.01)
        if st.button("Enter Payment"):
            gas_sold = calculate_gas_sold_zar(amount_paid)
            save_to_excel(amount_paid, gas_sold, True)
            st.success(f"You bought {gas_sold:.2f} kg of gas.")

    # Action buttons in a styled layout
    st.subheader("Manage Database")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Delete Last Entry"):
            delete_last_entry(payment_type == "ZAR")
            st.success("Last entry deleted from the database.")
    with col2:
        if st.button("Reset Database"):
            reset_database(payment_type == "ZAR")
            st.success("Database has been reset.")

if __name__ == "__main__":
    main()
