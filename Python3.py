import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Calculate Key Metrics
def calculate_cre_metrics(price, noi, down_payment, financing_cost):
    cap_rate = (noi / price) * 100  # Capitalization Rate
    cash_on_cash_return = ((noi - financing_cost) / down_payment) * 100  # Cash-on-Cash Return
    return cap_rate, cash_on_cash_return

# Step 2: Collect Property Data
def collect_property_data():
    st.title("Commercial Real Estate Analysis Tool")
    st.sidebar.header("Enter Property Details")

    num_properties = st.sidebar.number_input("Number of Properties", min_value=1, value=3)

    properties = []
    for i in range(num_properties):
        st.sidebar.subheader(f"Property {i + 1}")
        price = st.sidebar.number_input(f"Purchase Price of Property {i + 1} ($)", min_value=1)
        noi = st.sidebar.number_input(f"Annual NOI for Property {i + 1} ($)", min_value=1)
        down_payment = st.sidebar.number_input(f"Down Payment for Property {i + 1} ($)", min_value=1)
        financing_cost = st.sidebar.number_input(f"Annual Financing Cost for Property {i + 1} ($)", min_value=0)
        properties.append({"Price": price, "NOI": noi, "Down Payment": down_payment, "Financing Cost": financing_cost})
    
    return pd.DataFrame(properties)

# Step 3: Visualization
def visualize_metrics(properties):
    properties['Cap Rate'], properties['Cash-on-Cash Return'] = zip(
        *properties.apply(lambda row: calculate_cre_metrics(
            row['Price'], row['NOI'], row['Down Payment'], row['Financing Cost']), axis=1)
    )

    # Display the data
    st.write("### Property Data with Metrics")
    st.dataframe(properties)

    # Bar Chart for Cap Rate and Cash-on-Cash Return
    st.write("### Cap Rate vs. Cash-on-Cash Return")
    fig, ax = plt.subplots(figsize=(10, 6))
    properties[['Cap Rate', 'Cash-on-Cash Return']].plot(kind='bar', ax=ax, color=['skyblue', 'orange'])
    ax.set_xticks(range(len(properties)))
    ax.set_xticklabels([f"Property {i+1}" for i in range(len(properties))])
    ax.set_title("Cap Rate vs. Cash-on-Cash Return")
    ax.set_ylabel("Percentage (%)")
    plt.grid(axis='y')
    st.pyplot(fig)

    # Insights
    best_property = properties.loc[properties['Cash-on-Cash Return'].idxmax()]
    st.success(f"🏆 Best Property: Property {properties.index.get_loc(best_property.name) + 1} with a Cash-on-Cash Return of {best_property['Cash-on-Cash Return']:.2f}%")

# Step 4: Main Function
def main():
    properties = collect_property_data()
    if not properties.empty:
        visualize_metrics(properties)

# Step 5: Run the App
if __name__ == "__main__":
    main()
