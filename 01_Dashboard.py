import streamlit as st
import time

# --- Page Configuration ---
st.set_page_config(page_title="Dashboard", layout="wide")

# --- Styled Centered Header ---
st.markdown(
    "<h1 style='text-align: center; font-size: 42px; margin-bottom: 10px;'>💰 Guidry Money</h1>",
    unsafe_allow_html=True
)

# --- Time Range Selector (Dropdown) ---
st.markdown("###### Select time range")
col_select, _ = st.columns([0.25, 2])  # make the dropdown smaller
with col_select:
    time_range = st.selectbox(
        "Select time range",
        options=["Last 7 days", "Last 14 days", "Last 30 days"],
        index=2,
        label_visibility="collapsed"
    )


# --- Simulate a Loading Spinner ---
with st.spinner("Loading your dashboard..."):
    time.sleep(0.85)

    # --- Simulated Account Data ---
    accounts = {
        "Needs": {"balance": 2500, "income": 4000, "expenses": 3200},
        "Wants": {"balance": 1500, "income": 1200, "expenses": 900},
        "Planned": {"balance": 800, "income": 500, "expenses": 200},
        "HYSA": {"balance": 10000, "income": 50, "expenses": 0},
    }

    # --- Adjust Net Change Based on Time Range ---
    days_factor = {
        "Last 7 days": 0.25,
        "Last 14 days": 0.5,
        "Last 30 days": 1
    }
    multiplier = days_factor[time_range]

    # --- Display Account Summaries in Columns ---
    with st.container():
        cols = st.columns(4)

        for i, (acct_name, data) in enumerate(accounts.items()):
            income = round(data["income"] * multiplier)
            expenses = round(data["expenses"] * multiplier)
            net_change = income - expenses

            with cols[i]:
                st.subheader(acct_name)
                st.metric(label="Balance", value=f"${data['balance']:,}")
                st.metric(
                    label="Net Change",
                    value=f"${net_change:,}",
                    delta=f"${net_change:,}",
                    delta_color="normal"
                )

