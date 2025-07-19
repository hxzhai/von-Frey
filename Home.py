import streamlit as st

st.set_page_config(page_title="von Frey 工具集", layout="wide")

with st.sidebar:
    st.info("🧪 请选择左侧页面进入不同工具模块。")

st.title("👋 欢迎使用 von Frey 工具集")
st.markdown("""
本项目包含两个常用 von Frey 行为学计算工具：

1. **50% 缩足阈值计算工具**（基于 Up-Down 方法）
2. **SUDO 工具（简化版 von Frey）**（基于固定五根纤维丝组合）

👉 请从左侧选择功能页面开始使用。
""")
