
import streamlit as st

st.set_page_config(page_title="von Frey 工具集", layout="wide")

# 保留 sidebar 占位，避免切页时报错
st.sidebar.empty()

st.title("🐭 von Frey 工具集平台")
st.markdown("""
欢迎使用 von Frey 工具集，本平台集成了以下两个实用工具：

1. 🔹 **SUDO 工具（简化版 von Frey）**：基于五根纤维丝的简化方法
2. 🔹 **50% 缩足阈值计算工具**：基于传统 Up-Down 方法 + k 值表进行精确计算

请点击左侧导航栏切换工具。
""")
