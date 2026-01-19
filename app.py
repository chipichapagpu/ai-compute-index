import streamlit as st
import pandas as pd
import io
import altair as alt

# --- 1. Page Config ---
st.set_page_config(
    page_title="AI Compute Intelligence Platform",
    page_icon="✨",
    layout="wide"
)

# --- CSS: Minimalist & Stylish Styling ---
st.markdown("""
<style>
    /* Основной фон приложения */
    .stApp {
        background-color: #ffffff;
    }
    
    /* 1. УДАЛЯЕМ СТАНДАРТНУЮ ГИПЕРССЫЛОЧНУЮ ПОДСВЕТКУ */
    div[data-testid="stTabs"] [data-baseweb="tab-highlight-transformer"] {
        display: none !important;
    }
    
    /* Убираем стандартную нижнюю границу списка табов */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        border-bottom: 1px solid #f0f2f6 !important;
        gap: 24px;
    }

    /* 2. СТИЛИЗАЦИЯ КНОПОК ТАБОВ */
    div[data-testid="stTabs"] button {
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
        border-bottom: 2px solid transparent !important; 
        
        color: #64748b !important; /* Нейтральный серый цвет текста для всех табов */
        padding: 8px 4px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease;
        font-size: 16px !important;
    }
    
    /* Эффект при наведении */
    div[data-testid="stTabs"] button:hover {
        color: #1a2b3c !important;
        background-color: transparent !important;
    }

    /* 3. СТИЛЬ АКТИВНОЙ КНОПКИ (КРАСНАЯ ЛИНИЯ) */
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #1a2b3c !important; /* Темный текст вместо голубого */
        background-color: transparent !important;
        border-bottom: 2px solid #ff4b4b !important; /* Красная полоска */
    }

    /* Фикс цвета текста внутри активной кнопки для разных версий Streamlit */
    div[data-testid="stTabs"] button[aria-selected="true"] p {
        color: #1a2b3c !important; /* Темный текст вместо голубого */
        font-weight: 600 !important;
    }
    
    /* USP Box */
    .usp-box {
        background: #ffffff;
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 30px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    }
    .usp-box h1 {
        color: #050f1a;
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    /* Таблицы без внутренней прокрутки */
    div[data-testid="stDataFrame"] > div {
        max-height: none !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 40px;
        color: #64748b;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. Data Loading ---

# Local Data
hardware_csv = """Hardware,Manufacturer,Type,Release date,PetaFLOPS (FP-16),PetaFLOPS (FP-8),Memory (GB),Memory bandwidth (TB/s),Power Consumption (Watts),Foundry
Amazon Trainium3,Amazon AWS,GPU,2025-12-02,2520,2520,155,4.9,700,TSMC
Google TPU v7 Ironwood,Google,TPU,2025-11-06,2500,4610,192,7.37,960,TSMC
Huawei Ascend 920,Huawei,NPU,2025-10-01,2500,0,144,4,0,SMIC
NVIDIA GB300 (Blackwell Ultra),NVIDIA,GPU,2025-08-22,2310,5000,288,8,1400,TSMC
NVIDIA B300 (Blackwell Ultra),NVIDIA,GPU,2025-08-22,2310,4500,270,7.7,1100,TSMC
AMD Instinct MI355X,AMD,GPU,2025-06-12,2250,4600,288,8,1400,TSMC
AMD Instinct MI350X,AMD,GPU,2025-06-12,2250,4600,288,8,1000,TSMC
NVIDIA GB200,NVIDIA,GPU,2025-02-15,1750,5000,186,8,1200,TSMC
Amazon Trainium2,Amazon AWS,GPU,2024-12-03,1680,1300,96,2.9,500,TSMC
NVIDIA H200 SXM,NVIDIA,GPU,2024-11-18,1310,1980,141,4.8,700,TSMC
NVIDIA B100,NVIDIA,GPU,2024-11-15,1310,3500,192,8,700,TSMC
NVIDIA B200,NVIDIA,GPU,2024-11-15,1020,4500,180,7.7,1000,TSMC
Huawei Ascend 910C,Huawei,GPU,2024-10-15,990,0,128,3.2,700,SMIC
AMD Instinct MI325X,AMD,GPU,2024-10-10,990,0,256,6,1000,TSMC
Intel Habana Gaudi3,Intel,Other,2024-09-24,990,1680,128,3.7,900,TSMC
Maia 100 (M100),Microsoft,GPU,2024-08-27,989,0,0,0,500,TSMC
Google TPU v6e Trillium,Google,TPU,2024-05-14,989,918,32,1.64,380,TSMC
NVIDIA H100 NVL,NVIDIA,GPU,2024-03-14,918,0,94,3.9,400,TSMC
MTT S4000,Moore Threads,GPU,2023-12-19,900,0,48,0.7,450,SMIC
Google TPU v5p,Google,TPU,2023-12-06,800,0,95,2.7,540,TSMC
AMD Instinct MI300X,AMD,GPU,2023-12-06,800,0,192,5.3,750,TSMC
AMD Radeon Instinct MI308X,AMD,GPU,2023-12-06,756,0,192,5.3,750,TSMC
NVIDIA HGX H20,NVIDIA,GPU,2023-11-09,667,0,96,4,400,TSMC
NVIDIA GH200,NVIDIA,GPU,2023-08-08,362,0,0,4.9,700,TSMC
NVIDIA H800 SXM5,NVIDIA,GPU,2023-03-21,312,0,80,3.36,700,TSMC
NVIDIA GH100,NVIDIA,GPU,2023-03-21,312,0,0,3.07,700,TSMC
"""

dc_csv = """Rank,Owner,Location,State,Hardware,Chip Count (Est),Current AI Power (MW),Max Planned Power (MW),Comments
1,Google,Columbus,OH,TPU (Multi-gen),200000,500,1000,Uses multi-datacenter training.
2,Google,Omaha,NE,TPU (Latest),200000,500,1000,Dispersed campus connected by fiber.
3,Meta,Columbus,OH,Mixed / GPU,0,500,0,Hybrid site using standard buildings.
4,AWS,New Carlisle,IN,Trainium 2,500000,420,2000,Project Rainier scale.
5,Microsoft,Atlanta,GA,Nvidia GB200,150000,350,700,"Fairwater" type campus.
6,xAI,Memphis,TN,Nvidia GB200,110000,400,1000,Colossus 2; rapid construction.
7,Microsoft,Mt. Pleasant,WI,Nvidia GB200,150000,350,2000,Massive expansion plans.
8,AWS,Canton,MS,Trainium 2,200000,300,1000,Located next to fulfillment center.
9,OpenAI,Abilene,TX,Nvidia GB200,100000,200,0,Project Stargate ready by 2026.
10,xAI,Memphis,TN,Hopper / Blackwell,230000,300,300,Colossus 1 factory conversion.
"""

scale_csv = """Platform,Chip / Accelerator,Release Date / Status,Interconnect Technology,Single Domain Scale (Chips),Interconnect Bandwidth (GB/s),HBM Memory (GB)
Google,TPU v7 (Ironwood),2026 (Est),ICI,9216,1200,192
NVIDIA,GB300 (Blackwell Ultra),2025 (Late),NVLink 5,72,1800,288
AWS,Trainium2,2024 (Dec),NeuronLink v2,64,1000,96
Google,TPU v6e (Trillium),2024 (Late),ICI,256,800,32
NVIDIA,GB200 (Blackwell),2024 (Mar),NVLink 5,72,1800,192
Google,TPU v5p,2024 (Feb),ICI,8960,1200,95
AMD,MI300X,2023 (Dec),Infinity Fabric,8,896,192
NVIDIA,GH200 (Grace Hopper),2023 (May),NVLink,576,900,144
NVIDIA,H100 (SuperPOD),2022 (Sep),NVLink 4,256,900,80
Google,TPU v4,2021 (May),ICI,4096,275,32
"""

# Parsing
df_hw = pd.read_csv(io.StringIO(hardware_csv))
df_dc = pd.read_csv(io.StringIO(dc_csv))
df_scale = pd.read_csv(io.StringIO(scale_csv))

# Google Sheets Data
sheet_id = "1mIR77MY66RspGRMRh8oHXGX9oUjFFqspjlAPCdC6qO4"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

@st.cache_data(ttl=600)
def load_gsheet(url):
    return pd.read_csv(url)

try:
    df_clouds = load_gsheet(sheet_url)
except:
    df_clouds = pd.DataFrame()

# --- 3. UI Content ---
st.markdown("""
<div class="usp-box">
    <h1>AI Compute Intelligence Platform</h1>
    <p style='color: #475569; font-size: 1.15rem; max-width: 900px; line-height: 1.6;'>
        Strategic intelligence on high-performance silicon, infrastructure bottlenecks, and cluster scalability. 
        Synthesizing raw technical specifications into actionable insights for the next era of compute.
    </p>
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
tabs = st.tabs([
    "Hardware Comparison", 
    "Global Infrastructure", 
    "Cluster Scalability", 
    "Blackwell vs TPU Analysis"
])

# --- TAB 1: Hardware Comparison ---
with tabs[0]:
    st.subheader("Compute Performance Leaderboard")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Max HBM Capacity", "288 GB")
    m2.metric("Max Bandwidth", "8.0 TB/s")
    m3.metric("Peak FP8 Compute", "5000 TFLOPS")
    m4.metric("Chips Indexed", "26")
    st.divider()

    st.subheader("🔍 Compare Mode")
    selected_chips = st.multiselect(
        "Select up to 3 chips for side-by-side comparison:", 
        options=df_hw["Hardware"].unique(),
        max_selections=3
    )
    
    if selected_chips:
        comparison_df = df_hw[df_hw["Hardware"].isin(selected_chips)].set_index("Hardware").T
        st.dataframe(comparison_df, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("Full Hardware Index")
    selected_mf = st.multiselect("Filter Manufacturer", options=df_hw["Manufacturer"].unique(), default=df_hw["Manufacturer"].unique())
    f_hw = df_hw[df_hw["Manufacturer"].isin(selected_mf)]
    
    hw_height = (len(f_hw) + 1) * 35 + 10
    st.dataframe(f_hw, use_container_width=True, hide_index=True, height=hw_height)

# --- TAB 2: Global Infrastructure ---
with tabs[1]:
    st.subheader("Mega-Scale AI Campus Distribution")
    st.dataframe(df_dc, use_container_width=True, hide_index=True, height=420)

# --- TAB 3: Cluster Scalability ---
with tabs[2]:
    st.subheader("Single Domain Scalability Metrics")
    df_scale_sorted = df_scale.sort_values("Single Domain Scale (Chips)", ascending=True)
    scale_chart = alt.Chart(df_scale_sorted).mark_bar(color='#0061ff', size=40).encode(
        x=alt.X('Chip / Accelerator:N', sort=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Single Domain Scale (Chips):Q', title="Max Chips in Domain"),
        tooltip=['Chip / Accelerator', 'Single Domain Scale (Chips)']
    ).properties(height=450)
    st.altair_chart(scale_chart, use_container_width=True)
    
    scale_height = (len(df_scale) + 1) * 35 + 10
    st.dataframe(df_scale, use_container_width=True, hide_index=True, height=scale_height)

# --- TAB 4: Blackwell vs TPU Analysis ---
with tabs[3]:
    st.subheader("Strategic Comparison: NVIDIA vs Google")
    if not df_clouds.empty:
        cloud_height = (len(df_clouds) + 1) * 35 + 10
        st.dataframe(df_clouds, use_container_width=True, hide_index=True, height=cloud_height)
    else:
        st.error("Live data stream unavailable.")

# --- 4. Footer ---
st.markdown('<div class="footer">AI Compute Intelligence Platform | Latest Update: Jan 19, 2026</div>', unsafe_allow_html=True)
