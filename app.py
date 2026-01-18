import streamlit as st
import pandas as pd

# 1. Настройка страницы
st.set_page_config(
    page_title="AI Compute Index",
    page_icon="⚡",
    layout="wide"
)

# 2. Заголовок и легенда
st.title("⚡ AI Compute Price Index (Beta)")
st.markdown("""
**Objective:** Tracking real-time infrastructure economics across Hyperscalers vs. Neoclouds.
*Current Status: Snapshot Data (Jan 19, 2026). Proof-of-Concept for arbitrage analysis.*
""")

# 3. Хардкод данных (самый надежный способ для MVP)
# Я внес примерные данные, актуальные для рынка. 
# Вы можете поправить цены прямо здесь перед сохранением.
data = [
    {"Provider": "AWS", "GPU": "H100 (80GB)", "Type": "On-Demand", "Price ($/hr)": 12.32, "Region": "US East", "Availability": "Waitlist", "Source": "Hyperscaler"},
    {"Provider": "CoreWeave", "GPU": "H100 (80GB)", "Type": "On-Demand", "Price ($/hr)": 4.25, "Region": "US East", "Availability": "Limited", "Source": "Neocloud"},
    {"Provider": "Lambda", "GPU": "H100 (80GB)", "Type": "On-Demand", "Price ($/hr)": 2.49, "Region": "US West", "Availability": "Sold Out", "Source": "Neocloud"},
    {"Provider": "RunPod", "GPU": "H100 (80GB)", "Type": "Community", "Price ($/hr)": 3.69, "Region": "EU Central", "Availability": "Available", "Source": "Neocloud"},
    {"Provider": "Azure", "GPU": "A100 (80GB)", "Type": "On-Demand", "Price ($/hr)": 4.10, "Region": "US East", "Availability": "Waitlist", "Source": "Hyperscaler"},
    {"Provider": "Nebius", "GPU": "H100 (80GB)", "Type": "On-Demand", "Price ($/hr)": 4.75, "Region": "Europe", "Availability": "Available", "Source": "Neocloud"},
]

df = pd.DataFrame(data)

# 4. Добавляем метрику "Arbitrage" (разница с AWS)
aws_price = 12.32
df['Discount vs AWS'] = df.apply(lambda x: f"{round((1 - x['Price ($/hr)']/aws_price)*100)}%" if x['GPU'] == 'H100 (80GB)' else "-", axis=1)

# 5. Фильтры
col1, col2 = st.columns(2)
with col1:
    gpu_filter = st.multiselect("Select GPU", options=df["GPU"].unique(), default=df["GPU"].unique())
with col2:
    provider_filter = st.multiselect("Select Provider Type", options=df["Source"].unique(), default=df["Source"].unique())

# Фильтрация данных
filtered_df = df[df["GPU"].isin(gpu_filter) & df["Source"].isin(provider_filter)]

# 6. Отображение таблицы
st.dataframe(
    filtered_df,
    column_config={
        "Price ($/hr)": st.column_config.NumberColumn(format="$%.2f"),
    },
    hide_index=True,
    use_container_width=True
)

# 7. Аналитический вывод (для Хой Лама)
st.divider()
st.subheader("💡 Market Intelligence Insight")
st.info("""
**Arbitrage Opportunity:** Neoclouds currently offer H100 compute at a **~60-70% discount** compared to major Hyperscalers due to lower egress fees and bare-metal overhead. 
The main bottleneck shifts from 'Cost' to 'Availability' and 'Interconnect Speed'.
""")

st.caption("Developed by [Ваше Имя] as a prototype for infrastructure analysis.")