import streamlit as st
import pandas as pd

# --- 1. Настройка страницы ---
st.set_page_config(
    page_title="AI Compute Index",
    page_icon="⚡",
    layout="wide"
)

# --- CSS ХАК ДЛЯ УВЕЛИЧЕНИЯ ТАБОВ ---
# Мы внедряем стили, которые принудительно меняют размер шрифта и отступы
# у элементов, которые Streamlit использует для вкладок.
st.markdown("""
<style>
    /* Нацеливаемся на кнопки внутри контейнера табов */
    div[data-testid="stTabs"] button {
        padding-top: 1rem !important;    /* Больше отступ сверху */
        padding-bottom: 1rem !important; /* Больше отступ снизу */
    }
    /* Нацеливаемся на текст внутри кнопок */
    div[data-testid="stTabs"] button p {
        font-size: 24px !important; /* Размер шрифта (было около 16px) */
        font-weight: 700 !important; /* Жирность */
    }
</style>
""", unsafe_allow_html=True)
# ------------------------------------


# --- 2. Заголовок и легенда ---
st.title("⚡ AI Compute Price Index (Beta)")
st.markdown("""
**Objective:** Tracking real-time infrastructure economics across Hyperscalers vs. Neoclouds.
*Current Status: Snapshot Data (Jan 19, 2026). Proof-of-Concept for arbitrage analysis.*
""")

# --- 3. Подготовка данных (Data Layer) ---

# Данные для таблицы RETAIL (Spot/On-Demand)
retail_data = [
    {"Provider": "AWS", "GPU": "H100 (80GB)", "Type": "On-Demand", "Price ($/hr)": 12.32, "Region": "US East", "Availability": "Waitlist", "Source": "Hyperscaler"},
    {"Provider": "CoreWeave", "GPU": "H100 (80GB)", "Type": "On-Demand", "Price ($/hr)": 4.25, "Region": "US East", "Availability": "Limited", "Source": "Neocloud"},
    {"Provider": "Lambda", "GPU": "H100 (80GB)", "Type": "On-Demand", "Price ($/hr)": 2.49, "Region": "US West", "Availability": "Sold Out", "Source": "Neocloud"},
    {"Provider": "RunPod", "GPU": "H100 (80GB)", "Type": "Community", "Price ($/hr)": 3.69, "Region": "EU Central", "Availability": "Available", "Source": "Neocloud"},
    {"Provider": "Azure", "GPU": "A100 (80GB)", "Type": "On-Demand", "Price ($/hr)": 4.10, "Region": "US East", "Availability": "Waitlist", "Source": "Hyperscaler"},
    {"Provider": "Nebius", "GPU": "H100 (80GB)", "Type": "On-Demand", "Price ($/hr)": 4.75, "Region": "Europe", "Availability": "Available", "Source": "Neocloud"},
    # Арбитраж и Spot
    {"Provider": "AWS", "GPU": "A100 (80GB)", "Type": "Spot (Preemptible)", "Price ($/hr)": 3.85, "Region": "US East", "Availability": "Low Stock", "Source": "Hyperscaler"},
    {"Provider": "Lambda", "GPU": "A100 (80GB)", "Type": "On-Demand", "Price ($/hr)": 1.29, "Region": "US West", "Availability": "Available", "Source": "Neocloud"},
    # Inference
    {"Provider": "RunPod", "GPU": "RTX 4090 (24GB)", "Type": "Community", "Price ($/hr)": 0.74, "Region": "EU", "Availability": "Available", "Source": "Neocloud"},
    {"Provider": "Vast.ai", "GPU": "RTX 4090 (24GB)", "Type": "Community", "Price ($/hr)": 0.45, "Region": "Global", "Availability": "Available", "Source": "Marketplace"},
]
df_retail = pd.DataFrame(retail_data)

# Данные для CLUSTERS
cluster_data = [
    {"Provider": "CoreWeave", "Configuration": "HGX H100 (8x GPUs)", "Contract": "1-Year Reserved", "Price ($/hr)": 22.50, "Eff. Price per Chip": "$2.81", "Availability": "Call Sales"},
    {"Provider": "Lambda", "Configuration": "HGX H100 (8x GPUs)", "Contract": "On-Demand", "Price ($/hr)": 27.92, "Eff. Price per Chip": "$3.49", "Availability": "Waitlist"},
    {"Provider": "AWS", "Configuration": "P5.48xlarge (8x H100)", "Contract": "On-Demand", "Price ($/hr)": 98.32, "Eff. Price per Chip": "$12.29", "Availability": "Available"},
    {"Provider": "Nebius", "Configuration": "SuperPOD Slice (32x H100)", "Contract": "Reserved", "Price ($/hr)": 88.00, "Eff. Price per Chip": "$2.75", "Availability": "Available"},
]
df_clusters = pd.DataFrame(cluster_data)

# Данные SPECS
specs_data = [
    {"Chip": "NVIDIA H100 SXM", "VRAM (GB)": 80, "Memory Bandwidth (TB/s)": 3.35, "FP8 Performance (TFLOPS)": 3958, "Interconnect": "900 GB/s (NVLink)", "Best For": "LLM Training & Heavy Inference"},
    {"Chip": "NVIDIA A100 SXM", "VRAM (GB)": 80, "Memory Bandwidth (TB/s)": 2.03, "FP8 Performance (TFLOPS)": "N/A (624 FP16)", "Interconnect": "600 GB/s (NVLink)", "Best For": "Fine-tuning & Inference"},
    {"Chip": "NVIDIA RTX 4090", "VRAM (GB)": 24, "Memory Bandwidth (TB/s)": 1.00, "FP8 Performance (TFLOPS)": 660, "Interconnect": "PCIe Gen4 (Slow)", "Best For": "Dev / Small Model Inference"}
]
df_specs = pd.DataFrame(specs_data)

# Данные LLM SIZING
llm_data = [
    {"Model": "Llama-3-70B", "Min VRAM (FP16)": "140 GB", "Min VRAM (INT8)": "70 GB", "Recommended Setup": "2x A100 (80GB) or 1x H200"},
    {"Model": "Llama-3-8B", "Min VRAM (FP16)": "16 GB", "Min VRAM (INT8)": "8 GB", "Recommended Setup": "1x RTX 4090 (24GB)"},
    {"Model": "Mixtral 8x7B", "Min VRAM (FP16)": "90 GB", "Min VRAM (INT8)": "48 GB", "Recommended Setup": "2x A100 (80GB) or 4x RTX 4090"},
    {"Model": "Grok-1 (314B)", "Min VRAM (FP16)": "630 GB", "Min VRAM (INT8)": "320 GB", "Recommended Setup": "1x HGX H100 Node (8 GPUs)"},
]
df_llm = pd.DataFrame(llm_data)


# --- 4. Визуализация (Вкладки) ---
# Добавляем эмодзи прямо в названия, чтобы они стали еще заметнее
tab1, tab2, tab3, tab4 = st.tabs(["💸 RETAIL PRICING", "📦 CLUSTERS & NODES", "🛠 TECH SPECS", "🧠 LLM SIZING GUIDE"])

# --- ТАБЛИЦА 1: RETAIL ---
with tab1:
    st.subheader("Spot & On-Demand Pricing (Per Chip)")
    st.caption("Best for: Prototyping, Fine-tuning small models, Experimentation.")
    
    # Фильтры
    col1, col2 = st.columns(2)
    with col1:
        gpu_filter = st.multiselect("Select GPU", options=df_retail["GPU"].unique(), default=df_retail["GPU"].unique())
    with col2:
        provider_filter = st.multiselect("Select Provider Type", options=df_retail["Source"].unique(), default=df_retail["Source"].unique())
    
    filtered_retail = df_retail[df_retail["GPU"].isin(gpu_filter) & df_retail["Source"].isin(provider_filter)]
    
    st.dataframe(
        filtered_retail,
        column_config={"Price ($/hr)": st.column_config.NumberColumn(format="$%.2f")},
        hide_index=True,
        use_container_width=True
    )
    st.divider()
    st.info("💡 **Arbitrage Insight:** Neoclouds offer H100 compute at a **~60-70% discount** compared to major Hyperscalers.")

# --- ТАБЛИЦА 2: CLUSTERS ---
with tab2:
    st.subheader("Enterprise Node Pricing (HGX/DGX)")
    st.caption("Best for: Pre-training, Continuous Inference at Scale. Shows the discount for bulk commitment.")
    st.dataframe(df_clusters, hide_index=True, use_container_width=True)
    st.info("💡 **Insight:** Buying a reserved HGX Node on Neoclouds is ~75% cheaper than AWS On-Demand instances.")

# --- ТАБЛИЦА 3: SPECS ---
with tab3:
    st.subheader("Hardware Technical Reference")
    st.dataframe(
        df_specs,
        column_config={
            "FP8 Performance (TFLOPS)": st.column_config.TextColumn(help="Key metric for FP8 training speed (H100 killer feature)"),
            "Memory Bandwidth (TB/s)": st.column_config.NumberColumn(format="%.2f TB/s", help="Higher bandwidth = Faster token generation"),
        },
        hide_index=True,
        use_container_width=True
    )

# --- ТАБЛИЦА 4: LLM SIZING ---
with tab4:
    st.subheader("Can I run it? (LLM Inference Requirements)")
    st.caption("Mapping popular models to required hardware (FP16/INT8 precision).")
    st.dataframe(df_llm, hide_index=True, use_container_width=True)

# Footer
st.divider()
