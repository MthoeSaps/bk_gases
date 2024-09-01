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
            # If the file doesn't exist or is empty, create a new DataFrame
            df = pd.DataFrame(columns=['amount sold', 'kgs gas sold', 'gas price', 'time stamp'])

        # Create a new row with the current data
        new_row = {
            'amount sold': amount_paid,
            'kgs gas sold': gas_sold,
            'gas price': 20,
            'time stamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Append the new row to the DataFrame
        df.loc[len(df)] = new_row

        # Save the updated DataFrame to the ZAR Excel file
        df.to_excel('pos_system/dbs/zar_payments.xlsx', index=False)
    else:
        # Load the existing USD Excel file
        try:
            df = pd.read_excel('pos_system/dbs/t1gases_dbs.xlsx')
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # If the file doesn't exist or is empty, create a new DataFrame
            df = pd.DataFrame(columns=['amount sold', 'kgs gas sold', 'gas price', 'time stamp'])

        # Create a new row with the current data
        new_row = {
            'amount sold': amount_paid,
            'kgs gas sold': gas_sold,
            'gas price': 1.80,
            'time stamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Append the new row to the DataFrame
        df.loc[len(df)] = new_row

        # Save the updated DataFrame to the USD Excel file
        df.to_excel('pos_system/dbs/t1gases_dbs.xlsx', index=False)

def delete_last_entry(is_zar):
    if is_zar:
        # Load the existing ZAR Excel file
        try:
            df = pd.read_excel('pos_system/dbs/zar_payments.xlsx')
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # If the file doesn't exist or is empty, do nothing
            return

        # Drop the last row
        df = df.iloc[:-1]

        # Save the updated DataFrame to the ZAR Excel file
        df.to_excel('pos_system/dbs/zar_payments.xlsx', index=False)
    else:
        # Load the existing USD Excel file
        try:
            df = pd.read_excel('pos_system/dbs/t1gases_dbs.xlsx')
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # If the file doesn't exist or is empty, do nothing
            return

        # Drop the last row
        df = df.iloc[:-1]

        # Save the updated DataFrame to the USD Excel file
        df.to_excel('pos_system/dbs/t1gases_dbs.xlsx', index=False)

def reset_database(is_zar):
    if is_zar:
        # Create a new empty DataFrame
        df = pd.DataFrame(columns=['amount sold', 'kgs gas sold', 'gas price', 'time stamp'])

        # Save the empty DataFrame to the ZAR Excel file
        df.to_excel('pos_system/dbs/zar_payments.xlsx', index=False)
    else:
        # Create a new empty DataFrame
        df = pd.DataFrame(columns=['amount sold', 'kgs gas sold', 'gas price', 'time stamp'])

        # Save the empty DataFrame to the USD Excel file
        df.to_excel('pos_system/dbs/t1gases_dbs.xlsx', index=False)

def main():
    st.title("Gas Selling App")
    st.write("Price: $1.80/kg or 20 ZAR/kg")

    # Load the existing USD Excel file
    try:
        df = pd.read_excel('pos_system/dbs/t1gases_dbs.xlsx')
    except (FileNotFoundError, pd.errors.EmptyDataError):
        # If the file doesn't exist or is empty, create a new DataFrame
        df = pd.DataFrame(columns=['amount sold', 'kgs gas sold', 'gas price', 'time stamp'])

    # Load the existing ZAR Excel file
    try:
        df_zar = pd.read_excel('pos_system/dbs/zar_payments.xlsx')
    except (FileNotFoundError, pd.errors.EmptyDataError):
        # If the file doesn't exist or is empty, create a new DataFrame
        df_zar = pd.DataFrame(columns=['amount sold', 'kgs gas sold', 'gas price', 'time stamp'])

    # Calculate the totals
    total_gas_sold = df['kgs gas sold'].sum() + df_zar['kgs gas sold'].sum()
    total_sales = df['amount sold'].sum() + df_zar['amount sold'].sum()

    # Display the totals in Streamlit metric cards
    st.metric(label="Total Gas Sold (kg)", value=f"{total_gas_sold:.2f}")
    st.metric(label="Total Sales ($)", value=f"{total_sales:.2f}")

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