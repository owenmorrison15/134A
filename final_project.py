import numpy as np
import streamlit as st
import plotly.graph_objects as go

# ------------------------------
# Hardcoded Financial Data
# ------------------------------
market_cap = 115830000000
total_debt = 70760000000
cash_investments = 9410000000
outstanding_shares = 1800000000
interest_expense = 4400000000
net_debt = total_debt - cash_investments

# Pre-discounted Free Cash Flows (already included in total valuation)
fcf_sum = sum([7.81e9, 7.64e9, 6.52e9, 5.95e9, 5.44e9])

# Final Year Cash Flow for Terminal Value Calculation
final_year_fcf = 5378414444.78
terminal_growth = 0.03  # 3%

# ------------------------------
# Function to Calculate Intrinsic Share Price
# ------------------------------
def calculate_intrinsic_price(wacc):
    if wacc <= terminal_growth:
        return None
    
    # Terminal Value Calculation (discounted)
    terminal_value = (final_year_fcf * (1 + terminal_growth)) / (wacc - terminal_growth)


    # Enterprise and Equity Value
    enterprise_value = fcf_sum + terminal_value
    equity_value = enterprise_value - net_debt

    # Intrinsic Share Price
    intrinsic_share_price = equity_value / outstanding_shares

    return round(intrinsic_share_price, 2)

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="Anheuser-Busch Valuation", layout="wide")
st.title("🍻 Anheuser-Busch Intrinsic Share Price Calculator")
st.caption("A Discounted Cash Flow (DCF) Analysis, By Owen Morrison")


# Display financial summary
with st.expander("📊 Financial Summary (Click to Expand)"):
    st.write(f"**Market Capitalization:** ${market_cap:,.2f}")
    st.write(f"**Total Debt:** ${total_debt:,.2f}")
    st.write(f"**Cash & Short-Term Investments:** ${cash_investments:,.2f}")
    st.write(f"**Net Debt:** ${net_debt:,.2f}")
    st.write(f"**Outstanding Shares:** {outstanding_shares:,}")
    st.write(f"**Interest Expense:** ${interest_expense:,.2f}")
    st.write(f"**Final Year Free Cash Flow (for Terminal Value):** ${final_year_fcf:,.2f}")
    st.write(f"**Terminal Growth Rate:** {terminal_growth * 100}%")

st.markdown("---")

# WACC Slider Input
st.header("📈 Customize WACC")
wacc_input = st.slider("Select a WACC value (%)", min_value=3.5, max_value=12.0, value=9.45, step=0.01)
wacc_input /= 100  # Convert to decimal

# Calculate and display intrinsic share price
new_share_price = calculate_intrinsic_price(wacc_input)

# Display prominent intrinsic share price
if new_share_price is None:
    st.error("⚠️ WACC must be greater than the Terminal Growth Rate (3%). Please adjust the slider.")
else:
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; border: 2px solid #4CAF50; border-radius: 10px;">
            <h1 style="font-size: 72px; color: #4CAF50;">${new_share_price}</h1>
            <h3 style="color: gray;">Intrinsic Share Price</h3>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ------------------------------
# Interactive Plot with Plotly
# ------------------------------
wacc_values = np.linspace(3.5, 12, 100) / 100
share_prices = [calculate_intrinsic_price(w) for w in wacc_values]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=wacc_values * 100,
    y=share_prices,
    mode='lines+markers',
    name='Intrinsic Share Price',
    line=dict(color='blue')
))

fig.add_trace(go.Scatter(
    x=[wacc_input * 100],
    y=[new_share_price] if new_share_price else [None],
    mode='markers',
    marker=dict(color='red', size=12),
    name=f'Selected WACC: {wacc_input * 100:.2f}%'
))

fig.update_layout(
    title="Intrinsic Share Price vs. WACC",
    xaxis_title="WACC (%)",
    yaxis_title="Intrinsic Share Price ($)",
    template="plotly_white",
    hovermode="x unified",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# About Section
# ------------------------------
with st.expander("ℹ️ About this Calculator"):
    st.write("""
    This calculator estimates the **intrinsic share price** of Anheuser-Busch based on the **Discounted Cash Flow (DCF)** model.

    Adjust the **WACC slider** to dynamically see the intrinsic share price change.
    """)
# ------------------------------
# Project Information Section
# ------------------------------
with st.expander("📚 Project Information"):
    st.markdown("""
    **Project Overview**  
    In this project, I analyzed the most recent MarketWatch data on Anheuser-Busch InBev, dated **December 31, 2023**. At this time, the actual share price of the firm was **$64.35**. 
                
    My calculations, however, resulted in a share price of **$32.17** at a WACC of 9.45%, a figure significantly lower than the actual share price. 

    **Assumptions Used**  
    - **Risk-Free Rate:** 4.63% (10-year government bond in 2023)  
    - **Terminal Growth Rate:** 3% (WallStreetPrep)  
    - **Beta for AB InBev:** 0.81  
    - **Market Risk Premium:** 9.52% (Equity Valuation of Anheuser-Busch InBev S.A./N.V., Diego Horta e Costa)

    **Discrepancy Explanation**  
    The discrepancy in share price is likely due to intangible inputs into the firm’s value, including:
    - Global brand recognition.
    - Customer loyalty.
    - Intellectual property such as trademarks and exclusive recipes.

    Additional factors contributing to the discrepancies include the assumptions used. Notably, adjusting the **WACC slider to around 6.85%** brings the intrinsic share price closer to AB InBev's actual share price of **$64.35**.

    **Discounted Cash Flows Analysis**  
    Two separate analyses were performed using the average sums and final discounted cash flows.

    ---
    ### **High FCF Growth Rate (7.06%)**
    | Year | Discounted Free Cash Flow (FCF) |
    |------|--------------------------------|
    | 2024 | $7,805,886,506.61              |
    | 2025 | $7,635,571,949.13              |
    | 2026 | $6,516,380,523.28              |
    | 2027 | $5,953,858,913.89              |
    | 2028 | $5,439,896,556.05              |
    | **Sum** | **$33,351,594,448.96**       |

    ---
    ### **Low FCF Growth Rate (4.64%)**
    | Year | Discounted Free Cash Flow (FCF) |
    |------|--------------------------------|
    | 2024 | $7,629,441,098.93              |
    | 2025 | $7,294,282,140.61              |
    | 2026 | $6,369,083,298.68              |
    | 2027 | $5,819,277,010.55              |
    | 2028 | $5,316,932,333.51              |
    | **Sum** | **$32,429,015,882.28**       |

    ---
    - **Average Final Year Free Cash Flow:** $5,378,414,444.78  
    - **Average Free Cash Flow Sum:** $32,890,305,165.62
    """)

st.markdown("---")
