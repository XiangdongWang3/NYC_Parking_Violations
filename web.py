import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NYC Vehicle Violation Dashboard", page_icon="🚗")

st.title("🚗 NYC Vehicle Violation Dashboard")
st.write("Explore vehicle-related violations in NYC: parking, speeding, bus lane, and more.")

# menu
menu = st.sidebar.radio("Choose a feature", [
    "📅 Violation Summary",
    "📊 Violation visualization",
    "🔍 Search by Summons Number"
])

base_url = "http://127.0.0.1:5004" 

# M1
if menu == "📅 Violation Summary":
    date = st.date_input("Select a date")
    date_str = date.strftime("%Y-%m-%d")

    if st.button("Search Summary"):
        url = f"{base_url}/violations/summary?date={date_str}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Data fetched successfully!")
                st.metric("Total Violations", data["total_violations"])
                st.metric("Total Fine", f"${data['total_fine']:,.2f}")
            elif response.status_code == 404:
                st.warning("No violations found for this date.")
            else:
                st.error("Error fetching summary data.")
        except Exception as e:
            st.error(f"Connection failed: {e}")

# M2
elif menu == "📊 Violation visualization":
    date = st.date_input("Select a date")
    date_str = date.strftime("%Y-%m-%d")

    if st.button("Search Breakdown"):
    
        ##### type distribution #####
        type_url = f"{base_url}/violations/type-distribution?date={date_str}"
        try:
            res_type = requests.get(type_url)
            
            if res_type.status_code == 200:
                df_type = pd.DataFrame(res_type.json())
                st.subheader("📊 Violation Type Distribution")
                fig_type = px.bar(df_type, x="violation", y="count", title="Violation Types on Selected Date")
                st.plotly_chart(fig_type)
                
            else:
                st.warning("No violation type data available.")
                
        except Exception as e:
            st.error(f"Violation type fetch failed: {e}")


        ##### state dis (bar) #####
        state_url = f"{base_url}/violations/state-distribution?date={date_str}"
        
        try:
            res_state = requests.get(state_url)
            
            if res_state.status_code == 200:
                df_state = pd.DataFrame(res_state.json())
                st.subheader("🗺️ State Distribution")
                fig_state = px.pie(df_state, names="state", values="count", title="Vehicle License State Share")
                st.plotly_chart(fig_state)
                
            else:
                st.warning("No state distribution data available.")
                
        except Exception as e:
            st.error(f"State data fetch failed: {e}")



# M3
elif menu == "🔍 Search by Summons Number":
    summons_number = st.text_input("Enter a Summons Number")

    if st.button("Search Summons"):
        if not summons_number:
            st.warning("Please enter a summons number.")
        else:
            url = f"{base_url}/violations/details?summons_number={summons_number}"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    st.subheader("📄 Violation Details")
                    record = response.json()
                    for key, value in record.items():
                        st.markdown(f"**{key.replace('_', ' ').title()}**: {value}")
                elif response.status_code == 404:
                    st.warning("No record found for this summons number.")
                else:
                    st.error("Error retrieving violation details.")
            except Exception as e:
                st.error(f"Failed to connect to server: {e}")
