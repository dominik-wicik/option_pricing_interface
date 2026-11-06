import streamlit as st
import numpy as np
from scipy.stats import norm


def calculate_bsm(s, k, r, q, sigma, t):

    d1 = (np.log(s/k) + (r - q + sigma**2/2)*t)/(sigma*np.sqrt(t))
    d2 = d1 - sigma*np.sqrt(t)

    nd1 = norm.cdf(d1)
    nd2 = norm.cdf(d2)

    c = s * np.exp(-q*t) * nd1 - k * np.exp(-r*t) * nd2
    p = k * np.exp(-r*t) * (1- nd2) - s * np.exp(-q*t) * (1 - nd1)

    delta_c = nd1 * np.exp(-q*t)
    delta_p = (nd1 - 1) * np.exp(-q * t)

    gamma = 1/(s*sigma*np.sqrt(2*np.pi*t))*np.exp(-0.5*(d1**2))*np.exp(-q*t)

    vega = s*np.exp(-q*t)*np.sqrt(t/(2*np.pi))*np.exp(-0.5*(d1**2))

    theta_c = -(s*sigma*np.exp(-q*t))/(2*np.sqrt(2*np.pi*t))*np.exp(-0.5*(d1**2))+q*s*np.exp(-q*t)*nd1-k*r*np.exp(-r*t)*nd2
    theta_p = -(s*sigma*np.exp(-q*t))/(2*np.sqrt(2*np.pi*t))*np.exp(-0.5*(d1**2))-q*s*np.exp(-q*t)*(1-nd1)+k*r*np.exp(-r*t)*(1-nd2)

    rho_c = k*t*np.exp(-r*t)*nd2
    rho_p = -k*t*np.exp(-r*t)*(1-nd2)

    epsilon_c = -s*t*np.exp(-q*t)*nd1
    epsilon_p = s*t*np.exp(-q*t)*(1 - nd1)

    return d1, d2, c, p, delta_c, delta_p, gamma, vega, theta_c, theta_p, rho_c, rho_p, epsilon_c, epsilon_p

st.set_page_config(page_title="Option Pricing Interface by DW", page_icon="📈")
st.set_page_config(layout="wide")
left_spacer, content_col, right_spacer = st.columns([1, 3, 1])

with left_spacer:
    
    linkedin_url = "https://www.linkedin.com/in/dominik-wicik-79271839b"
    
    st.markdown(f"""
        <div style="display: flex; align-items: center;">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" style="margin-right: 10px;">
            <a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: white; font-weight: bold; font-size: 18px;">
                Dominik Wicik
            </a>
        </div>
    """, unsafe_allow_html=True)
    
with content_col:
    
    st.title("Option Pricing Interface")
    st.write("""This dashboard is based on the Black-Scholes-Merton model.
             It was coded in Python using the Streamilt library.""")
    st.write("""The purpose of this project is to showcase my ability to code and work with financial data.
             You can find my LinkedIn profile in the top-left corner of the interface.""")
    st.markdown(f"""
                <p>
                ⚠️ DISCLAIMER: Enabling the dark mode is strictly advised for the best UI experience.
                </p>""", unsafe_allow_html=True)

    #custom tabs
    st.markdown("""
                <style>
                div[data-testid="stTabs"] button {
                flex: 1;
                }

                div[data-testid="stTabs"] button [data-testid="stMarkdownContainer"] p {
                font-size: 20px !important;
                color: white;
                }

                div[data-testid="stTabs"] button:hover {
                background-color: rgba(255, 75, 75, 0.1);
                border-radius: 5px;
                }

                div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
                    width: 49% !important;
                    background-color: #ff4b4b !important;
                }

                div[data-testid="stTabs"] [role="tablist"] {
                    display: flex;
                }

                /* Hide the glitchy red bar entirely */
                div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
                    display: none !important;
                }

                /* Style the active tab to look like a selected 'button' */
                div[data-testid="stTabs"] button[aria-selected="true"] {
                    background-color: rgba(255, 75, 75, 0.2) !important;
                    border-top: 2px solid #ff4b4b !important;
                    border-radius: 5px 5px 0px 0px !important;
                }     
                </style>
                """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Inputs & Outputs", "Formulas & Variables"])

    with tab1:
        time_mode = st.radio("Time Input Mode", ["Years (Decimal)", "Months", "Days"], horizontal=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            s = st.number_input("Asset Price ($S$)", min_value=0.01, value=100.0, step=1.0)

        with col2:
            k = st.number_input("Strike Price ($K$)", min_value=0.01, value=100.0, step=1.0)

        with col3:
            r = st.number_input("Risk-Free Rate (r)",
                        value=0.0575, 
                        step=0.01, 
                        format="%.4f")
        

        col4, col5, col6 = st.columns(3)
        with col4:
            q = st.number_input("Dividend Yield (q)", 
                        value=0.00, 
                        step=0.01, 
                        format="%.4f")
            
        with col5:
            sigma = st.number_input(r"Volatility ($\sigma$)", min_value=0.01, value=0.2, step=0.01)
            
        with col6:
            if time_mode == "Years (Decimal)":
                t = st.number_input("Time to Expiry ($T$) in Years", min_value=0.0001, value=1.0, step=0.5)
            elif time_mode == "Months":
                months = st.number_input("Time to Expiry ($T$) in Months", min_value=0.0001, value=12.0, step=1.0)
                t = months / 12
            else:
                days = st.number_input("Time to Expiry ($T$) in Days", min_value=0.0001, value=365.0, step=1.0)
                t = days / 365
        
        d1, d2, c, p, delta_c, delta_p, gamma, vega, theta_c, theta_p, rho_c, rho_p, epsilon_c, epsilon_p = calculate_bsm(s, k, r, q, sigma, t)
        
        st.markdown("---")

        #call premium and put premium values
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
                <div style="background-color:#1e2a1e; padding:20px; border-radius:10px; border-left: 5px solid #4CAF50;">
                    <p style="color:#4CAF50; margin:0; font-weight:bold;">CALL VALUE (C)</p>
                    <h2 style="margin:0;">${c:.4f}</h2>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div style="background-color:#2a1e1e; padding:20px; border-radius:10px; border-left: 5px solid #F44336;">
                    <p style="color:#F44336; margin:0; font-weight:bold;">PUT PREMIUM (P)</p>
                    <h2 style="margin:0;">${p:.4f}</h2>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        st.subheader("Greek Values")
        
        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Delta Call", f"{delta_c:.4f}")
        col1.metric("Delta Put", f"{delta_p:.4f}")

        col2.metric("Epsilon Call (per 1 pp)", f"{epsilon_c/100:.4f}", help="Multiply by 100 to get the default value.")
        col2.metric("Epsilon Put (per 1 pp)", f"{epsilon_p/100:.4f}", help="Multiply by 100 to get the default value.")
    
        col3.metric("Theta Call (per day)", f"{theta_c/365:.4f}", help="Multiply by 365 to get the default value.")
        col3.metric("Theta Put (per day)", f"{theta_p/365:.4f}", help="Multiply by 365 to get the default value.")
        
        col4.metric("Rho Call (per 1 pp)", f"{rho_c/100:.4f}", help="Multiply by 100 to get the default value.")
        col4.metric("Rho Put (per 1 pp)", f"{rho_p/100:.4f}", help="Multiply by 100 to get the default value.")

        col5.metric("Gamma", f"{gamma:.4f}")
        col5.metric("Vega (per 1 pp)", f"{vega/100:.4f}", help="Multiply by 100 to get the default value.")

    with tab2:

        #d1
        st.subheader(r"$d_1$ parameter")
        st.write(r"""is necessary to calculate call premium ($C$)
                    and put premium ($P$) later on.""")
        st.latex(r'''
        d_1 = \frac{\ln\left(\frac{S}{K}\right)+\left(r-q+\frac{\sigma^2}{2}\right)T}{\sigma\sqrt{T}}
        ''')

        st.markdown("---")

        #d2
        st.subheader(r"$d_2$ parameter")
        st.write(r"""is also required to later calculate call premium ($C$)
                    and put premium ($P$).""")
        st.latex(r'''
        d_2 = d_1 - \sigma\sqrt{T}
        ''')

        st.markdown("---")

        #call premium
        st.subheader(r"Call premium ($C$)")
        st.write("is the price of a call option.")
        st.latex(r'''
        C = S e^{-qT} N(d_1) - K e^{-rT} N(d_2)
        ''')

        st.markdown("---")

        #put premium
        st.subheader(r"Put premium ($P$)")
        st.write("is the price of a put option.")
        st.latex(r'''
        P = K e^{-rT} N(-d_2) - S e^{-qT} N(-d_1)
        ''')

        st.markdown("---")

        #delta
        st.subheader(r"Delta ($\Delta$)")
        st.write("""measures the change of option price with respect to change in the
                 underlying asset's price ($S$). Different for call and put options.""")
        st.latex(r'''
        \Delta_C = N(d_1)
        ''')
        st.latex(r'''
        \Delta_P = N(d_1) - 1
        ''')

        st.markdown("---")

        #theta
        st.subheader(r"Theta ($\Theta$)")
        st.write("""measures the change of option price with respect to change in time to expiry ($T$). 
                 Different for call and put options. By default, theta represents this change per 1 year 
                 of time to expiry change, which means that in practice it is divided by (usually) 
                 365 to get a more intuitive result.""")
        st.latex(r'''
        \Theta_C = -\frac{S\sigma}{2\sqrt{2 \pi T}} exp(\frac{-d_1^2}{2}) - K r e^{-rT} N(d_2)
        ''')
        st.latex(r'''
        \Theta_P = -\frac{S\sigma}{2\sqrt{2 \pi T}} exp(\frac{-d_1^2}{2}) + K r e^{-rT} N(-d_2)
        ''')

        st.markdown("---")
        
        #rho
        st.subheader(r"Rho ($\rho$)")
        st.write("""measures the change of option price with respect to change in the risk-free rate ($r$).
                 Different for call and put options. By default, rho represents this change per 100\%
                 of risk-free rate change, which means that in practice it is divided by 100 to get
                 a more intuitive result.""")
        st.latex(r'''
        \rho_C = K T e^{-rT} N(d_2)
        ''')
        st.latex(r'''
        \rho_P = -K T e^{-rT} N(-d_2)
        ''')

        st.markdown("---")

        #epsilon
        st.subheader(r"Epsilon or Psi ($\epsilon$ or $\psi$)")
        st.write("""measures the change of option price with respect to change in the underlying dividend
                 yield rate ($q$). Different for call and put options. By default, epsilon represents this change per 100\%
                 of dividend yield rate change, which means that in practice it is divided by 100 to get
                 a more intuitive result.""")
        st.latex(r'''
        \epsilon_C = -S T e^{-qT} N(d_1)
        ''')
        st.latex(r'''
        \epsilon_P = S T e^{-qT} N(-d_1)
        ''')

        st.markdown("---")

        #gamma
        st.subheader(r"Gamma ($\Gamma$)")
        st.write("""measures the change of delta with respect to change in the underlying asset's price ($S$).
                 Same for call and put options.""")
        st.latex(r'''
        \Gamma = \frac{1}{S \sigma \sqrt{2\pi T}}exp(\frac{-d_1^2}{2})
        ''')

        st.markdown("---")

        #vega
        st.subheader(r"Vega ($\nu$)")
        st.write("""measures the change of option price with respect to change in volatility ($\sigma$).
                 Same for call and put options. By default, vega represents this change per 100\% 
                 of volatility change, which means that in practice it is divided by 100 to get a more intuitive result.""")
        st.latex(r'''
        \nu = S \sqrt{\frac{T}{2\pi}} exp(\frac{-d_1^2}{2})
        ''')

        st.markdown("---")

        #variables
        st.write(r"$S$ - spot price of the option's underlying asset.")
        st.write(r"""$K$ - strike price/exercise price. It is the price at which the
                    underlying asset of the option can be bought (call option) or
                    sold (put option).""")
        st.write(r"""$r$ - risk-free rate. It is a theoretical rate of return on an investment
                    with no risk of financial loss. Obviously, in the real world every investment
                    comes with risk in some amount, but generally government treasury bonds
                    are considered to have "risk-free" interest rates, and thus, are used
                    in the Black-Scholes-Merton model.""")
        st.write(r"""$q$ - continuously compounded dividend yield.""")
        st.write(r"""$\sigma$ - standard deviation of the underlying asset's returns.""")
        st.write(r"""$T$ - time until expiration of the option (expressed in years). After this time
                    passes, the option holder must decide whether to exercise the option or not.""")
        st.write(r"""$N(x)$ - value of the cumulative distribution function of the standard
                    normal distribution.""")
        