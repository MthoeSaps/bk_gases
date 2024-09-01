import streamlit as st
import pandas as pd
from datetime import datetime

def calculate_gas_sold(amount_paid):
    gas_price = 1.80  # $1.80 per 1kg of gas
    gas_sold = amount_paid / gas_price
    return gas_sold

def calculate_gas_sold_zar(amount_paid):
    gas_price = 20  # 20 ZAR per 1kg of gas
    gas_sold = amount_paid / gas_price
    return gas_sold

def save_to_excel(amount_paid, gas_sold, is_zar):
    if is_zar:
        # Load the existing ZAR Excel file
        try:
            df = pd.read_excel('pos_system/dbs/zar_payments.xlsx')
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=['amount sold', 'kgs gas sold', 'gas price', 'time stamp'])

        new_row = {
            'amount sold': amount_paid,
            'kgs gas sold': gas_sold,
            'gas price': 20,
            'time stamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        df.loc[len(df)] = new_row
        df.to_excel('pos_system/dbs/zar_payments.xlsx', index=False)
    else:
        # Load the existing USD Excel file
        try:
            df = pd.read_excel('pos_system/dbs/t1gases_dbs.xlsx')
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=['amount sold', 'kgs gas sold', 'gas price', 'time stamp'])

        new_row = {
            'amount sold': amount_paid,
            'kgs gas sold': gas_sold,
            'gas price': 1.80,
            'time stamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        df.loc[len(df)] = new_row
        df.to_excel('pos_system/dbs/t1gases_dbs.xlsx', index=False)

def delete_last_entry(is_zar):
    if is_zar:
        try:
            df = pd.read_excel('pos_system/dbs/zar_payments.xlsx')
            df = df.iloc[:-1]
            df.to_excel('pos_system/dbs/zar_payments.xlsx', index=False)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return
    else:
        try:
            df = pd.read_excel('pos_system/dbs/t1gases_dbs.xlsx')
            df = df.iloc[:-1]
            df.to_excel('pos_system/dbs/t1gases_dbs.xlsx', index=False)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return

def reset_database(is_zar):
    df = pd.DataFrame(columns=['amount sold', 'kgs gas sold', 'gas price', 'time stamp'])
    if is_zar:
        df.to_excel('pos_system/dbs/zar_payments.xlsx', index=False)
    else:
        df.to_excel('pos_system/dbs/t1gases_dbs.xlsx', index=False)

def main():
    st.title("Gas Selling App")
    st.write("Price: $1.80/kg or 20 ZAR/kg")

    # Load both Excel files
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

    # Display metrics
    st.metric(label="Total Gas Sold (kg)", value=f"{total_gas_sold:.2f}")
    st.metric(label="Total Sales (USD)", value=f"{total_sales_usd:.2f}")
    st.metric(label="Total Sales (ZAR)", value=f"{total_sales_zar:.2f}")

    payment_type = st.radio("Select Payment Type:", ("USD", "ZAR"))

    if payment_type == "USD":
        amount_paid = st.number_input("Enter the amount paid (in $):", min_value=0.0, step=0.01)
        if st.button("Enter Payment"):
            gas_sold = calculate_gas_sold(amount_paid)
            save_to_excel(amount_paid, gas_sold, False)
            st.write(f"You bought {gas_sold:.2f} kg of gas.")
    else:
        amount_paid = st.number_input("Enter the amount paid (in ZAR):", min_value=0.0, step=0.01)
        if st.button("Enter Payment"):
            gas_sold = calculate_gas_sold_zar(amount_paid)
            save_to_excel(amount_paid, gas_sold, True)
            st.write(f"You bought {gas_sold:.2f} kg of gas.")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Delete Last Entry"):
            delete_last_entry(payment_type == "ZAR")
            st.write("Last entry deleted from the database.")
    with col2:
        if st.button("Reset Database"):
            reset_database(payment_type == "ZAR")
            st.write("Database has been reset.")

if __name__ == "__main__":
    main()