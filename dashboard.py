import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os


# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="OSINT // STRAIT OF HORMUZ", layout="wide", initial_sidebar_state="collapsed")

# --- OSINT CSS STYLING ---
st.markdown("""
<style>
    /* Force medium-dark OSINT aesthetic */
    .stApp {
        background-color: #0f172a;
        font-family: "Courier New", Courier, monospace;
    }
    
    /* FIX: Force text colors to be bright and visible, without breaking dropdowns */
    p, label {
        color: #e2e8f0 !important;
    }
    
    /* FIX: Ensure Dropdown Selectbox Items are Readable (Dark text on Light dropdown) */
    [data-baseweb="popover"] span, [data-baseweb="popover"] div, ul[role="listbox"] li {
        color: #0f172a !important;
    }
    
    /* FIX: Make the Metric values (e.g. "50 SHIPS/DAY") bright white */
    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }
    /* FIX: Make the Metric labels (e.g. "PRE-CRISIS THROUGHPUT") visible */
    [data-testid="stMetricLabel"] > div > div > p {
        color: #94a3b8 !important;
        font-family: "Courier New", Courier, monospace !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: "Courier New", Courier, monospace !important;
        color: #f8fafc !important;
    }
    
    /* Custom divider */
    hr {
        border-color: #334155 !important;
    }
    
    /* ====== MOBILE RESPONSIVE ====== */
    @media (max-width: 768px) {
        /* Scale down the giant title */
        .stApp h1 {
            font-size: 1.4rem !important;
            letter-spacing: 0px !important;
        }
        .stApp h4 {
            font-size: 0.9rem !important;
        }
        
        /* Situation report box */
        .stApp div[style*='border-left: 4px solid #f59e0b'] {
            font-size: 0.95rem !important;
            padding: 12px !important;
        }
        
        /* Force Streamlit columns to stack vertically */
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
        
        /* Metric cards: make text smaller */
        [data-testid="stMetricValue"] {
            font-size: 1.4rem !important;
        }
        [data-testid="stMetricLabel"] > div > div > p {
            font-size: 0.7rem !important;
        }
        
        /* Simulation result cards */
        .stApp div[style*='min-height: 130px'] {
            min-height: 100px !important;
        }
        .stApp div[style*='min-height: 130px'] h2 {
            font-size: 1.6rem !important;
        }
        .stApp div[style*='min-height: 130px'] h5 {
            font-size: 0.8rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    # Utilizing a dynamic absolute path so it works locally and on the cloud seamlessly
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "Hormuz_Data_2026.csv")
    
    if not os.path.exists(file_path):
        st.error(f"[ERROR] Cannot connect to database target: {file_path}")
        st.stop()
        
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    
    daily = df.groupby('date').size().reset_index(name='transit_count')
    full_dates = pd.date_range(start=daily['date'].min(), end=daily['date'].max(), freq='D')
    daily = daily.set_index('date').reindex(full_dates, fill_value=0).reset_index()
    daily.rename(columns={'index': 'date'}, inplace=True)
    
    return df, daily

df, daily = load_data()

event_dates = {
    'Israel Strikes': pd.to_datetime('2026-02-10'),
    'US Strikes': pd.to_datetime('2026-02-28'),
    'Total Blockade': pd.to_datetime('2026-03-15'),
    'Ceasefire': pd.to_datetime('2026-03-28'),
}

# --- HEADER: THE OSINT HOOK ---
st.markdown("<h1 style='text-align: left; font-size: 2.8rem; color: #10b981; letter-spacing: 2px;'>INTELLIGENCE BRIEF: OPERATION CHOKEPOINT</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: left; color: #94a3b8; font-weight: 300;'>TARGET SET: INDIAN MACROECONOMICS & MIDDLE-CLASS STABILITY</h4>", unsafe_allow_html=True)

st.markdown("""
<div style='background-color: #1e293b; border-left: 4px solid #f59e0b; padding: 20px; border-radius: 2px; font-size: 1.15rem; line-height: 1.7; margin-top: 15px;'>
<b style='color: #f8fafc;'>SITUATION REPORT:</b> <span style='color: #cbd5e1;'>India imports ~85% of its crude oil, with massive volumes transiting the Strait of Hormuz. 
When operations at this chokepoint cease, the impact is not confined to the global elite. The supply shock travels immediately into the Indian heartland. Freight costs spike 300% due to African routing, devastating MSME exports, while crude deficits trigger fuel rationing and runaway inflation on FMCG (fast-moving consumer goods) and grocery items.</span>
</div>
""", unsafe_allow_html=True)

# --- IMPACT METRICS ---
st.markdown("<br><h5 style='color: #64748b; letter-spacing: 1px;'>[1] LOGISTICS SEVERANCE TELEMETRY</h5>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

col1.metric("PRE-CRISIS THROUGHPUT", "50 SHIPS/DAY")
col2.metric("AIRSTRIKE SUPPRESSION", "4 SHIPS/DAY", "-92% CRITICAL", delta_color="inverse")
col3.metric("MILITARY BLOCKADE", "1 SHIP/DAY", "-97% HALT", delta_color="inverse")
col4.metric("INDIAN SUPPLY AT RISK", "~2.5M BPD", "CRITICAL SHOCK", delta_color="inverse")

st.markdown("<hr>", unsafe_allow_html=True)

# --- SECTION I: TIMELINE ---
st.markdown("### [2] TEMPORAL ANALYSIS: SUPPLY CHAIN COLLAPSE")

fig_timeline = px.bar(daily, x='date', y='transit_count', 
                     labels={'transit_count': 'Vessels (Daily)', 'date': 'Timeline'},
                     color_discrete_sequence=['#3b82f6'])

colors = ['#f59e0b', '#dc2626', '#991b1b', '#10b981']
for (name, date), color in zip(event_dates.items(), colors):
    fig_timeline.add_vline(x=date, line_dash="dash", line_color=color, line_width=2)
    fig_timeline.add_annotation(x=date, y=55, text=f"<b>{name}</b>", showarrow=False, bgcolor=color, font=dict(color="#ffffff"))

fig_timeline.update_layout(template='plotly_dark', margin=dict(l=0, r=0, t=40, b=0), plot_bgcolor="#0f172a", paper_bgcolor="#0f172a")
fig_timeline.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
fig_timeline.update_xaxes(showgrid=False)
st.plotly_chart(fig_timeline, use_container_width=True)

# --- SECTION II: THE DOMINO EFFECT ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### [3] SECTORAL TRAFFIC DEFICIT")

cargo_types = df['cargo_type'].value_counts().head(8).index.tolist()
selected_cargo = st.selectbox("> FILTER TARGET CARGO VECTOR:", ["All Cargo Types"] + cargo_types)

if selected_cargo == "All Cargo Types":
    cargo_df = daily
else:
    c_df = df[df['cargo_type'] == selected_cargo].groupby('date').size().reset_index(name='transit_count')
    cargo_df = c_df.set_index('date').reindex(pd.date_range(start=daily['date'].min(), end=daily['date'].max(), freq='D'), fill_value=0).reset_index()
    cargo_df.rename(columns={'index': 'date'}, inplace=True)

fig_cargo = px.area(cargo_df, x='date', y='transit_count', color_discrete_sequence=['#ef4444'])
fig_cargo.update_layout(template='plotly_dark', height=350, plot_bgcolor="#0f172a", paper_bgcolor="#0f172a", margin=dict(l=0, r=0, t=20, b=0))
fig_cargo.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
st.plotly_chart(fig_cargo, use_container_width=True)

# --- SECTION III: THE CONSUMER SHOCK (SIMULATION) ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### [4] HOUSEHOLD ECONOMIC CASUALTY SHOCK MODEL")

col_sim1, col_sim2 = st.columns([1, 2])

with col_sim1:
    st.markdown("<span style='color: #f59e0b; font-size: 1rem;'>⚠️ <b>ACTIVATE SIMULATION PARAMETERS</b></span>", unsafe_allow_html=True)
    st.markdown("<span style='color: #94a3b8; font-size: 0.9rem;'>India Strategic Petroleum Reserves (ISPR) contain roughly 10-12 days of emergency supply. The slider measures the systemic breakage of the Indian middle-class if the blockade holds beyond reserve depletion.</span>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    blockade_days = st.slider("> INPUT CONFLICT DURATION (DAYS):", 0, 180, 45, step=5)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='color: #ef4444; border-left: 3px solid #ef4444; padding-left: 10px;'>FORECAST: DAY {blockade_days} OF BLOCKADE</h5>", unsafe_allow_html=True)

with col_sim2:
    # --- INDIAN ECONOMICS MODEL ---
    # Petrol Base: 96 INR/Liter. 
    base_petrol = 96.0
    petrol_price = base_petrol + (blockade_days * 0.25) + (12 if blockade_days >= 20 else 0) + (22 if blockade_days >= 60 else 0)
    
    # CPI Inflation (Food & Grocery): Base ~5.0%
    base_cpi = 5.0
    cpi_inflation = base_cpi + ((blockade_days / 30) * 1.5)
    
    # MSME & Manufacturing Job Losses:
    job_losses = 0 if blockade_days < 40 else (blockade_days - 35) * 125000 
    
    m1, m2, m3 = st.columns(3)
    
    m1.markdown(f"""
    <div style='background-color: #1e293b; padding: 15px; border-radius: 4px; text-align: center; border: 1px solid #334155; min-height: 130px; display: flex; flex-direction: column; justify-content: center;'>
    <h5 style='margin:0; color: #cbd5e1; font-size: 0.9rem;'>PETROL AT PUMP (₹/L)</h5>
    <h2 style='margin:10px 0; font-size: 2.2rem; color: #ef4444;'>₹{petrol_price:.1f}</h2>
    <p style='margin:0; font-size: 0.8rem; color: #64748b;'>Baseline: ₹96.0</p>
    </div>
    """, unsafe_allow_html=True)

    m2.markdown(f"""
    <div style='background-color: #1e293b; padding: 15px; border-radius: 4px; text-align: center; border: 1px solid #334155; min-height: 130px; display: flex; flex-direction: column; justify-content: center;'>
    <h5 style='margin:0; color: #cbd5e1; font-size: 0.9rem;'>FMCG / FOOD INFLATION</h5>
    <h2 style='margin:10px 0; font-size: 2.2rem; color: #f59e0b;'>{cpi_inflation:.1f}%</h2>
    <p style='margin:0; font-size: 0.8rem; color: #64748b;'>Pre-crisis: 5.0%</p>
    </div>
    """, unsafe_allow_html=True)
    
    if job_losses == 0:
        job_text = "SAFE"
        job_color = "#10b981"
    else:
        job_text = f"{job_losses / 1000000:.1f}M LOST"
        job_color = "#ef4444"
        
    m3.markdown(f"""
    <div style='background-color: #1e293b; padding: 15px; border-radius: 4px; text-align: center; border: 1px solid #334155; min-height: 130px; display: flex; flex-direction: column; justify-content: center;'>
    <h5 style='margin:0; color: #cbd5e1; font-size: 0.9rem;'>MSME SECTOR JOBS</h5>
    <h2 style='margin:10px 0; font-size: 2.2rem; color: {job_color};'>{job_text}</h2>
    <p style='margin:0; font-size: 0.8rem; color: #64748b;'>Textile & Tech Exports</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Trajectory chart
    days_arr = np.arange(0, 185, 5)
    pain_df = pd.DataFrame({'Days Closed': days_arr})
    pain_df['Petrol Price (INR)'] = base_petrol + (pain_df['Days Closed'] * 0.25) + np.where(pain_df['Days Closed'] >= 20, 12, 0) + np.where(pain_df['Days Closed'] >= 60, 22, 0)
    
    fig_econ = px.line(pain_df, x='Days Closed', y='Petrol Price (INR)', title="PETROL SHOCK TRAJECTORY (ISPR DEPLETION)")
    fig_econ.update_traces(line=dict(color="#ef4444", width=3))
    
    # Tracker marker
    fig_econ.add_vline(x=blockade_days, line_dash='dash', line_color='#3b82f6', annotation_text=f"Selected: Day {blockade_days}")
    
    # Zone markers
    fig_econ.add_vrect(x0=20, x1=60, fillcolor="#f59e0b", opacity=0.05, layer="below", line_width=0, annotation_text="Strategic Reserves Low", annotation_position="top left", annotation_font_color="#f59e0b")
    fig_econ.add_vrect(x0=60, x1=180, fillcolor="#ef4444", opacity=0.1, layer="below", line_width=0, annotation_text="Global Supply Starvation", annotation_position="top left", annotation_font_color="#ef4444")
    
    fig_econ.update_layout(template='plotly_dark', height=320, plot_bgcolor="#0f172a", paper_bgcolor="#0f172a", margin=dict(l=0, r=0, t=40, b=0))
    fig_econ.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
    
    st.plotly_chart(fig_econ, use_container_width=True)

st.markdown("<br><hr><p style='text-align: center; color: #475569; font-size: 0.8rem; font-family: monospace;'>END OF REPORT.</p>", unsafe_allow_html=True)
