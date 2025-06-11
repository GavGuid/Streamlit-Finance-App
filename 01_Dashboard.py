import streamlit as st
import time
from datetime import datetime, timedelta, date
import calendar
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(page_title="Dashboard", layout="wide")

# --- Styled Centered Header ---
st.markdown(
    "<h1 style='text-align: center; font-size: 42px; margin-bottom: 10px;'>💰 Guidry Money</h1>",
    unsafe_allow_html=True
)

st.markdown(f"""
<style>
    /* Styling for each individual account box */
    .account-box {{
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem; /* Generous padding for good spacing */
        margin-bottom: 0.75rem; /* Space between boxes */
        background-color: #f9f9f9;
        box-shadow: 0 2px 5px rgba(0,0,0,0.07);
        text-align: center; /* Center align all content */
        overflow: hidden;
    }}

    /* Account Name (subheader) */
    .account-box h3 {{
        font-size: 22px; /* A bit larger for prominence */
        margin-top: 0.2rem;
        margin-bottom: 0.5rem; /* Space below the name */
        color: #333;
        line-height: 1.3;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    /* Current Balance Label */
    .balance-label {{
        font-size: 14px; /* Clear and readable */
        color: grey;
        margin-bottom: -0.2rem; /* Pull label closer to value */
        line-height: 1;
    }}

    /* Current Balance Value */
    .balance-value {{
        font-size: 32px; /* Very prominent balance value */
        font-weight: normal;
        color: #000;
        line-height: 1.2;
    }}

    /* --- Plotly Chart and Global Streamlit Styles (Keep these for consistency) --- */

    /* Plotly Chart Title */
    .modebar-container + div > .plotly-notifier,
    .js-plotly-plot .plotly .main-svg .infolayer .gtitle .g-gtitle {{
        font-size: 16px !important;
    }}
    .js-plotly-plot .plotly .main-svg .infolayer .gtitle .g-gtitle text {{
        font-size: 16px !important;
    }}

    /* Plotly Legend Text */
    .js-plotly-plot .plotly .main-svg .legend .g-gname text {{
        font-size: 10px !important;
    }}

    /* Global Streamlit H2/H4 titles */
    h2 {{
        font-size: 2rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }}
    h4 {{
        font-size: 1.3rem;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
    }}

</style>
""", unsafe_allow_html=True)
################################################################################# SimpleFIN ###############################################################################################
from simplefin_utils import get_simplefin_data

data = get_simplefin_data()

# Use example I created in simplefin_utils.py


############################################################################## Account Balances ############################################################################################
st.markdown("<h2 style='text-align: left;'>Account Balances</h2>", unsafe_allow_html=True)


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
    # Moved inside the spinner so data is loaded after delay
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

    # --- Main Layout: Two Columns (Account Info | Pie Chart) ---
    # Adjust column ratios as needed, e.g., [1, 1.5] for more chart space
    account_info_col, chart_col = st.columns([1, 1])

    with account_info_col:
        st.markdown("#### Account Details")
        # Display Account Summaries Vertically
        for acct_name, data in accounts.items():
            # Keep these calculations for now, as they don't affect display if not used
            income = round(data["income"] * multiplier)
            expenses = round(data["expenses"] * multiplier)
            net_change = income - expenses

            # No need for income_color/expenses_color if not displaying those metrics

            # <<< START COPY FROM HERE (inclusive of the st.markdown line) >>>
            st.markdown(
                f"""
                <div class="account-box">
                    <h3>{acct_name}</h3>
                    <div class="balance-label">Current Balance</div>
                    <div class="balance-value">${data['balance']:,}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with chart_col:
        st.markdown("#### Balance Distribution")

        # Prepare data for the pie chart
        # We need account names (labels) and their current balances (values)
        pie_chart_data = {
            "Account": list(accounts.keys()),
            "Balance": [data["balance"] for data in accounts.values()]
        }

        # Create the pie chart using Plotly Express
        fig = px.pie(
            pie_chart_data,
            values='Balance',
            names='Account',
            title='Current Balance Allocation',
            hole=0.3, # Creates a donut chart
            color_discrete_sequence=px.colors.sequential.RdBu # Choose a color sequence
        )

        # Update layout for better appearance
        fig.update_traces(textinfo='percent+label', pull=[0.05]*len(accounts)) # Show label and percentage, slight pull effect
        fig.update_layout(showlegend=True, margin=dict(l=20, r=20, t=30, b=20)) # Adjust margins

        st.plotly_chart(fig, use_container_width=True)


st.markdown("---")
############################################################################## end of section ############################################################################################




########################################################################## Income & Bills Schedule #######################################################################################

st.markdown("<h2 style='text-align: left;'>Income & Bills Schedule</h2>", unsafe_allow_html=True)

# ---- Configuration ----

# ---- Bill Schedule ----
bill_schedule = [
    #Fixed Days / Amounts
    {"name": "Mortgage: $2321.08", "type": "fixed", "day": 1, "amount": 2321.08},
    {"name": "Car Insurance: $165.26", "type": "fixed", "day": 23, "amount": 165.26},
    {"name": "Internet: $71.40", "type": "fixed", "day": 13, "amount": 71.40},
    {"name": "Student Loan: $141.27", "type": "fixed", "day": 7, "amount": 141.27},
    
    #Range
    # {"name": "Utilities", "type": "range", "start_day": 13, "end_day": 15},

    #Recurring
    {"name": "Prime Membership: $16.19", "type": "recurring", "start_date": date(2025, 1, 29), "interval": 30, "amount": 16.19},

    #Variable Days / Amounts
    {"name": "Utilities: ~$200", "type": "fixed", "day": 13, "amount": 200.00},
    {"name": "Groceries: ~$400", "type": "variable_estimate", "amount": 400.00},
    {"name": "Gas: ~$200", "type": "variable_estimate", "amount": 200.00},
    # {"name": "Dining Out", "type": "variable_estimate", "amount": 150.00},
    # {"name": "Miscellaneous", "type": "variable_estimate", "amount": 100.00},
]

# ---- Income Schedule ----
paycheck_amount = 2122.24  # Hardcoded paycheck amount
income_schedule = [
    {"name": "Paycheck: 2122.24", "type": "recurring", "start_date": date(2025, 1, 7), "interval": 14, "amount": paycheck_amount}
]


# Get today's date
today = datetime.now().date()

# ---- Date Picker ----
this_year = datetime.now().year
months = {calendar.month_name[i]: i for i in range(1, 13)}

# ---- Month Dropdown ----
col1, col2 = st.columns([0.25, 1.8])
with col1:
    month_name = st.selectbox("Select month", list(months.keys()), index=datetime.now().month - 1)
selected_month = months[month_name]
############################################################################## end of section ##########################################################################################



####################################################################### Calculate Income / Expenses ####################################################################################
# Initialize variables
total_monthly_expenses = 0
total_monthly_income = 0
projected_paychecks_in_month = 0

# Initialize lists to store contributions for tooltips
income_contributions = []
expense_contributions = []

# Calculate total days in the selected month
days_in_month = calendar.monthrange(this_year, selected_month)[1]
first_day_of_month = date(this_year, selected_month, 1)
last_day_of_month = date(this_year, selected_month, days_in_month)


# Income
for income_source in income_schedule:
    if income_source["type"] == "recurring": # You can extend this for other income types if needed
        current_income_date = income_source["start_date"]
        # Fast-forward to the first occurrence in or after the current month
        while current_income_date < first_day_of_month:
            current_income_date += timedelta(days=income_source["interval"])

        # Iterate through occurrences within the current month
        while current_income_date <= last_day_of_month:
            total_monthly_income += income_source["amount"]
            income_contributions.append({
                "name": income_source["name"],
                "date": current_income_date.strftime("%b %d"),
                "amount": income_source["amount"]
            })
            current_income_date += timedelta(days=income_source["interval"])

    # If you later add "fixed" income types, you'd add an elif here
    # elif income_source["type"] == "fixed":
    #     if 1 <= income_source["day"] <= days_in_month:
    #         total_monthly_income += income_source["amount"]
    #         income_contributions.append({
    #             "name": income_source["name"],
    #             "date": date(this_year, selected_month, income_source["day"]).strftime("%b %d"),
    #             "amount": income_source["amount"]
    #         })

# Expenses
for bill in bill_schedule:
    if bill["type"] == "fixed":
        # Check if the fixed day falls within the current month
        if 1 <= bill["day"] <= days_in_month: # Ensure day is valid for the month (e.g., no 31st in Feb)
            total_monthly_expenses += bill["amount"]
            expense_contributions.append({
                "name": bill["name"],
                "date": date(this_year, selected_month, bill["day"]).strftime("%b %d"),
                "amount": bill["amount"]
            })
  
    # Not using "Range" bills for now, but keeping the code for future reference
    # elif bill["type"] == "range":
    #     # For range bills, assume they are paid once if any part of the range is in the month
    #     if (bill["start_day"] <= days_in_month and bill["end_day"] >= 1):
    #         total_monthly_expenses += bill["amount"]
    #         expense_contributions.append({
    #             "name": bill["name"],
    #             "date": f"{date(this_year, selected_month, bill['start_day']).strftime('%b %d')} - {date(this_year, selected_month, bill['end_day']).strftime('%b %d')}",
    #             "amount": bill["amount"]
    #         })

    elif bill["type"] == "recurring":
        # Calculate occurrences within the month for recurring bills
        current_recurring_date = bill["start_date"]
        # Fast-forward to the first occurrence in or after the current month
        while current_recurring_date < first_day_of_month:
            current_recurring_date += timedelta(days=bill["interval"])

        # Iterate through occurrences within the current month
        while current_recurring_date <= last_day_of_month:
            total_monthly_expenses += bill["amount"]
            expense_contributions.append({
                "name": bill["name"],
                "date": current_recurring_date.strftime("%b %d"),
                "amount": bill["amount"]
            })
            current_recurring_date += timedelta(days=bill["interval"])

    elif bill["type"] == "variable_estimate":
    # Variable estimates are simply added to the total for the month
        total_monthly_expenses += bill["amount"]
        expense_contributions.append({
            "name": bill["name"],
            "date": "Monthly Estimate", # Indicates it's a general monthly estimate
            "amount": bill["amount"]
        })
############################################################################## end of section ###########################################################################################




################################################################# Custom CSS for Tooltips and Metric Styling ############################################################################
monthly_net_flow = total_monthly_income - total_monthly_expenses
# Determine the color for the Net Flow value (red/green)
net_flow_color = "green" if monthly_net_flow >= 0 else "red"

st.markdown(f"""
<style>
    .centered-heading {{
        text-align: center;
    }} 

    /* General styling for the custom metrics to match st.metric */
    .custom-metric-container {{
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center; /* Centers items horizontally within the flex container */
        justify-content: center; /* Centers items vertically within the flex container */
        height: 100%;
        padding: 10px; /* Adjust padding to roughly match st.metric default */
        position: relative; /* Needed for tooltip positioning */
    }}

    .custom-metric-label {{
        font-size: 14px;
        color: grey;
        margin-bottom: -0.2rem; /* Small negative margin to bring value closer */
    }}

    .custom-metric-value {{
        font-size: 28px; /* Standard st.metric value font size */
        font-weight: normal; /* Standard st.metric value font weight */
        line-height: 1.2;
    }}

    /* Tooltip specific styling */
    .tooltip-wrapper .tooltip-content {{
        visibility: hidden;
        width: max-content; /* Adjust width to content */
        max-width: 300px; /* Prevent excessively wide tooltips */
        background-color: #333;
        color: #fff;
        text-align: left;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1000; /* Ensure tooltip is on top */
        bottom: 120%; /* Position above the metric */
        left: 50%;
        transform: translateX(-50%); /* Center horizontally */
        opacity: 0;
        transition: opacity 0.3s ease-in-out; /* Smooth fade-in/out */
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        pointer-events: none; /* Allows clicks through if not hovering directly on tooltip content */
        overflow: hidden; /* Hide overflow content if it gets too long */
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; /* Match Streamlit's font */
    }}

    .tooltip-wrapper:hover .tooltip-content {{
        visibility: visible;
        opacity: 1;
        pointer-events: auto; /* Re-enable pointer events when visible for interaction */
    }}

    .tooltip-wrapper .tooltip-content ul {{
        list-style-type: none; /* Remove default bullet points */
        padding: 0;
        margin: 0;
    }}

    .tooltip-wrapper .tooltip-content li {{
        margin-bottom: 4px;
        font-size: 13px;
        white-space: nowrap; /* Prevent wrapping for individual list items */
        text-overflow: ellipsis; /* Add ellipsis if content is too long for nowrap */
        overflow: hidden;
    }}
    .tooltip-wrapper .tooltip-content li:last-child {{
        margin-bottom: 0; /* No bottom margin on the last item */
    }}

    /* Tooltip arrow (optional) */
    .tooltip-wrapper .tooltip-content::after {{
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #333 transparent transparent transparent;
    }}

    /* Specific color for Net Flow value */
    .net-flow-value-color {{
        color: {net_flow_color} !important;
    }}
</style>
""", unsafe_allow_html=True)
############################################################################## end of section ##############################################################################################




######################################################################## Display Monthly Projections ########################################################################################
# Allows for hovering over the income and expenses to see details
def generate_tooltip_html(contributions):
    items_html = ""
    if not contributions:
        return "<p style='margin: 0; font-style: italic;'>No contributions this month.</p>"
    for item in contributions:
        # display_date = item.get("date", "") #Taking out the display date
        # if display_date:
        #     display_date = f" ({display_date})"
        # items_html += f"<li>{item['name']}{display_date}: ${item['amount']:,.2f}</li>"

        # items_html += f"<li>{item['name']}: ${item['amount']:,.2f}</li>"
        items_html += f"<li>{item['name']}</li>" #Replacing with amount in name. If you want to change it back, uncomment the above line and comment this one out.
    return f"<ul>{items_html}</ul>"

income_tooltip_content = generate_tooltip_html(income_contributions)
expenses_tooltip_content = generate_tooltip_html(expense_contributions)


st.markdown("<h4 class='centered-heading'>Monthly Projections</h4>", unsafe_allow_html=True)
proj_col1, proj_col2, proj_col3 = st.columns(3)

# Projected Income with Tooltip
with proj_col1:
    st.markdown(
        f"""
        <div class="custom-metric-container tooltip-wrapper">
            <div class="custom-metric-label">Projected Income</div>
            <div class="custom-metric-value">${total_monthly_income:,.2f}</div>
            <div class="tooltip-content">
                <span style='font-weight: normal; margin-bottom: 5px; display: block;'>Income Breakdown:</span>
                {income_tooltip_content}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Projected Expenses with Tooltip
with proj_col2:
    st.markdown(
        f"""
        <div class="custom-metric-container tooltip-wrapper">
            <div class="custom-metric-label">Projected Expenses</div>
            <div class="custom-metric-value">${total_monthly_expenses:,.2f}</div>
            <div class="tooltip-content">
                <span style='font-weight: normal; margin-bottom: 5px; display: block;'>Expense Breakdown:</span>
                {expenses_tooltip_content}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Projected Net Flow (colored, no tooltip for this one)
with proj_col3:
    st.markdown(
        f"""
        <div class="custom-metric-container">
            <div class="custom-metric-label">Projected Net Flow</div>
            <div class="custom-metric-value net-flow-value-color">
                ${monthly_net_flow:,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
############################################################################## end of section ###########################################################################################


st.markdown("---")


########################################################################## Generate Calendar Data ########################################################################################
calendar.setfirstweekday(calendar.SUNDAY)

def generate_calendar_data(year, month):
    num_weeks = calendar.monthcalendar(year, month)
    calendar_grid = []

    for week in num_weeks:
        row = []
        for day in week:
            if day == 0:
                row.append("")
            else:
                current_date = date(year, month, day)
                cell_classes = []

                if current_date == today:
                    cell_classes.append("today")
                elif current_date < today:
                    cell_classes.append("past-day")
                else:
                    cell_classes.append("future-day") # This class isn't strictly necessary as it's the default, but good for clarity

                class_str = " ".join(cell_classes)
                content = f"<div class='day-content {class_str}'><strong>{day}</strong>"




  # ---- Added Income to calendar from income_schedule ----
                for income_source in income_schedule:
                    if income_source["type"] == "recurring":
                        income_start_date = income_source["start_date"]
                        interval = income_source["interval"]

                        # Check if the current day is an occurrence of this recurring income
                        if current_date >= income_start_date: # Only check dates on or after the start date
                            days_since_income_start = (current_date - income_start_date).days
                            if days_since_income_start % interval == 0:
                                content += (
                                    f"<div style='margin-top: 4px; background-color: #b0ff9c; border-radius: 5px; " # Light blue for income
                                    f"padding: 2px 4px; font-size: 12px;'>{income_source['name']}</div>"
                                )
                    # Add other income types if you implement them (e.g., fixed income_source)
                    # elif income_source["type"] == "fixed":
                    #     if current_date.day == income_source["day"]:
                    #         content += (
                    #             f"<div style='margin-top: 4px; background-color: #b0ff9c; border-radius: 5px; "
                    #             f"padding: 2px 4px; font-size: 12px;'>{income_source['name']}</div>"
                    #         )

  # ---- Added Bills to calendar from bill_schedule ----
                for bill in bill_schedule:
                    if bill["type"] == "fixed":
                        if current_date.day == bill["day"]:
                            content += (
                                f"<div style='margin-top: 4px; background-color: #f8d7da; border-radius: 5px; "
                                f"padding: 2px 4px; font-size: 12px;'>{bill['name']}</div>"
                            )
                    elif bill["type"] == "range":
                        if bill["start_day"] <= current_date.day <= bill["end_day"]:
                            content += (
                                f"<div style='margin-top: 4px; background-color: #f8d7da; border-radius: 5px; "
                                f"padding: 2px 4px; font-size: 12px;'>{bill['name']}</div>"
                            )
                    elif bill["type"] == "recurring":
                        days_since_start = (current_date - bill["start_date"]).days
                        if days_since_start >= 0 and days_since_start % bill["interval"] == 0:
                            content += (
                                f"<div style='margin-top: 4px; background-color: #f8d7da; border-radius: 5px; "
                                f"padding: 2px 4px; font-size: 12px;'>{bill['name']}</div>"
                            )

                content += "</div>" # Close day-content div
                row.append(content)
        calendar_grid.append(row)
    return calendar_grid
############################################################################## end of section ############################################################################################




############################################################################# Display Calendar ###########################################################################################
st.markdown(f"### {month_name} {this_year}")

calendar_data = generate_calendar_data(this_year, selected_month)
df = pd.DataFrame(calendar_data, columns=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
calendar_html = df.to_html(escape=False, index=False)

# Inject custom CSS to style the table
styled_calendar_html = f"""
<style>
    table {{
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
    }}
    th, td {{
        border: 1px solid #ddd;
        padding: 10px;
        text-align: center;
        vertical-align: top;
        font-size: 16px;
        word-wrap: break-word;
        height: 100px;
        position: relative; /* Needed for absolute positioning of markers */
    }}

    /* Styles for past days */
    .past-day {{
        background-color: #f0f0f0; /* Slightly darker grey for past days */
        color: #888; /* Dim text for past days */
    }}

    /* Styles for today */
    .today {{
        background-color: #e6f7ff; /* Light blue background for today */
        border: 2px solid #007bff; /* Blue border for today */
        box-shadow: 0 0 5px rgba(0, 123, 255, 0.5); /* Slight shadow for today */
    }}

    /* Optional: Style for future days (default background is fine) */
    .future-day {{
        background-color: #ffffff; /* White background for future days */
    }}

    .day-content {{
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        height: 100%;
    }}

    /* You might want to adjust the top margin for the content within the cell */
    .day-content strong {{
        margin-bottom: 5px; /* Space between day number and event boxes */
    }}
</style>
<div style='width: 100%; overflow-x: auto;'>{calendar_html}</div>
"""

st.markdown(styled_calendar_html, unsafe_allow_html=True)
############################################################################## end of section ############################################################################################

# first_check_minimum = 1500
# second_check_minimum = 4000



# first_transfer_amount = (paycheck_amount + 1500) - first_check_minimum #The 1500 is the amount in needs (SimpleFIN), which is a placeholder for now.
# second_transfer_amount = (paycheck_amount + 2500) - second_check_minimum #The 2500 is the amount in needs (SimpleFIN), which is a placeholder for now.

# st.markdown(f"You are eligible for a ${first_transfer_amount} transfer this check.")
# st.markdown(f"You are eligible for a ${second_transfer_amount} transfer this check.")
