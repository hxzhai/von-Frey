import streamlit as st
import pandas as pd
import numpy as np
import os

# ----------------------------
# 页面设置
# ----------------------------
st.set_page_config(page_title="50% 缩足阈值计算", layout="wide")
st.info("👉 请点击 **左上角的 '»'** 图标展开侧边栏，填写参数后开始计算。")
st.title("🐭 Von Frey 50% 缩足阈值计算工具")

# ----------------------------
# 读取数据（使用安全路径）
# ----------------------------
try:
    # 当前 .py 脚本的目录（pages/）
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 上级目录（项目根目录）
    root_dir = os.path.dirname(current_dir)

    # 文件路径
    code_path = os.path.join(root_dir, "code_table.txt")
    k_path = os.path.join(root_dir, "k_table.txt")

    # 加载数据
    code_df = pd.read_csv(code_path, sep="\t")
    k_df = pd.read_csv(k_path, sep="\t", dtype={"测量结果": str})
except Exception as e:
    st.error(f"❌ 无法读取编号表或 k 值表，请检查文件路径是否正确。错误信息：{e}")
    st.stop()

if '克数' not in code_df.columns or '序号' not in code_df.columns:
    st.error("❌ 编号表格式不正确，必须包含 '克数'、'序号' 列。")
    st.stop()

if '测量结果' not in k_df.columns or 'k值' not in k_df.columns:
    st.error("❌ k 值表格式不正确，必须包含 '测量结果'、'k值' 列。")
    st.stop()

# ✅ 替换编号列为 log10(克重 × 10000)
code_df["编号"] = np.log10(code_df["克数"] * 10000)

# ----------------------------
# 用户输入区域 + 说明
# ----------------------------
with st.sidebar.expander("📐 方法原理与操作说明（点击展开）", expanded=False):
    st.markdown("""
### 📐 方法原理简介

本工具依据 **Dixon 提出的 Up-Down 方法**，对一系列 von Frey 刺激丝的刺激结果进行逻辑回溯，结合实验所用纤维丝的克重对数均差（δ）与匹配的经验值 k 值，计算 50% 缩足反应的刺激强度阈值。

**计算公式：**「1」  
  50% 缩足阈值（克） = 10 ^ (Xf + k × δ) / 10000

其中：
- **Xf**：最后一次测试纤维丝的克重对数（log₁₀(克重 × 10000)）
- **k**：与反应序列对应的经验系数（来源于 k 值表「2」）
- **δ**：刺激丝之间的克重对数均差（取 log₁₀(克重 × 10000) 后的均差）

---

### 🧪 Von Frey 操作说明

1. **选择测试用刺激丝：**  
   建议选取 **5～9 根克重连续、编号间距近似均匀** 的 Von Frey 刺激丝作为测试组。  
   ✅ 推荐使用奇数根纤维丝，以便选择正中间一根作为起始测试。
   
2. **固定实验动物：**  
   将小鼠放置于穿孔平台或金属网格盒中，静置适应后暴露足底。   

3. **确定起始刺激丝：**  
   测试应从所选刺激丝中 **中间克重的一根** 开始刺激（如选择了9根丝，对应克重分别为 0.04g、0.07g、0.16g、0.4g、0.6g、1.0g、1.4g、2.0g、4.0g，则从 0.6g 开始测试）。

4. **记录反应序列（0/1）：**
   - 0 表示阴性反应（无缩足）
   - 1 表示阳性反应（有缩足）
   - 每次根据反应结果选择下一根刺激丝：
     - **阳性 → 更轻的纤维丝**
     - **阴性 → 更重的纤维丝**  
   使用 0 与 1 记录每次反应，如：0010010。  
⚠️ 必须从第一次刺激开始记录反应（即第一次中间克重刺激），而不是从“反应发生翻转”之后才开始记录！

5. **终止条件：**  
   首次观察到反应结果阴阳翻转后，**继续测试 4 次**终止（即第一次0变1、或1变0后，继续测试4次，继续测试的次数**可以小于4次，不能多于4次**）。  
   **特殊情况：**  
   eg：取一系列 von Frey 纤维丝（如 0.04、0.07、0.16、0.4、0.6、1、1.4、2.0、4.0g 共 9 根）  
   ① 若从 0.6g 开始，动物连续5次出现阳性反应（即到最小克重 0.04g 动物仍出现缩足或舔足反应）或连续5次出现阴性反应（即到最大克重 4.0g 动物仍不出现缩足或舔足反应），即可直接使用 0.04g 或 4.0g 作为动物 50%缩足反应阈值；  
   ② 若已出现反应翻转，但测试到最小或最大纤维丝时不足 4 次（如 1111011，即下次测量纤维丝克重将超出设定范围），则继续使用最小或最大纤维丝按照“Up & Down”测量记录，以排除假阳性或假阴性可能；
   

6. **输入反应序列：**  
   每行输入一组完整反应序列（如 `00010101`），从最中间克重的纤维丝开始记录。

---

### 💻 工具使用方法

1.	点击左上角 「»」图标展开侧边栏
2.	在侧边栏依次设置：  
•	最小刺激丝克重  
•	最大刺激丝克重  
•	反应序列（每行一个）
3.	点击 “🚀 开始计算” 查看结果
4.	可点击下载按钮导出为 CSV 文件保存

---
参考文献：  
	「1」Chaplan SR, Bach FW, Pogrel JW, Chung JM, Yaksh TL. Quantitative assessment of tactile allodynia in the rat paw. J Neurosci Methods. 1994 Jul;53(1):55-63. doi: 10.1016/0165-0270(94)90144-9.  
	「2」Dixon WJ. Efficient analysis of experimental observations. Annu Rev Pharmacol Toxicol. 1980;20:441-62. doi: 10.1146/annurev.pa.20.040180.002301.
---
### 如需帮助请联系维护者：zhaihexin1999@163.com
    """)

st.sidebar.header("📅 参数设置")
min_weight = st.sidebar.selectbox("选择最小刺激丝克重", options=code_df["克数"].tolist())
max_weight = st.sidebar.selectbox("选择最大刺激丝克重", options=code_df["克数"].tolist())
seq_input = st.sidebar.text_area("输入反应序列（每行一条）")
start = st.sidebar.button("🚀 开始计算")

# ----------------------------
# 计算准备
# ----------------------------
sub_df = code_df[(code_df["克数"] >= min_weight) & (code_df["克数"] <= max_weight)].copy()

if sub_df.empty:
    st.error("❌ 所选克重范围无匹配，请重新选择。")
    st.stop()

min_order = sub_df["序号"].min()
max_order = sub_df["序号"].max()
n_fibers = max_order - min_order + 1
median_order = (min_order + max_order) // 2

st.markdown(f"✅ 已选 {n_fibers} 根刺激丝，中位序号为：`{median_order}`")

delta = (sub_df["编号"].max() - sub_df["编号"].min()) / (max_order - min_order)

# ----------------------------
# 主计算逻辑
# ----------------------------
if start:
    st.subheader("🔹 计算结果")

    k_df["测量结果"] = k_df["测量结果"].astype(str).str.replace(r"[\s\r\n\t]", "", regex=True)
    k_df["k值"] = pd.to_numeric(k_df["k值"], errors="coerce")

    seq_list = [line.strip() for line in seq_input.strip().splitlines() if line.strip()]
    results = []

    for idx, seq in enumerate(seq_list, start=1):
        seq_clean = ''.join(ch for ch in seq if ch in ['0', '1'])
        restored_seq = seq_clean.replace("0", "O").replace("1", "X")

        cur_order = median_order
        boundary_flag = None  # 记录是否越界
        for ch in seq_clean[:-1]:  # 推断最后刺激丝
            if ch == "0":
                cur_order += 1
            elif ch == "1":
                cur_order -= 1

            # 判断是否超出范围，若超出，则停在边界，并标记
            if cur_order > max_order:
                cur_order = max_order
                boundary_flag = "max"
            elif cur_order < min_order:
                cur_order = min_order
                boundary_flag = "min"

        # 查找实际最后刺激丝信息
        row = code_df[code_df["序号"] == cur_order]
        if row.empty:
            results.append({"序号": idx, "反应序列": seq_clean, "错误": "找不到对应序号"})
            continue

        xf = row["编号"].values[0]
        final_weight = row["克数"].values[0]

        # 判断是否需要按极值输出
        if boundary_flag == "max":
            threshold_g = max_weight  # 用最大克重阈值
            results.append({
                "序号": idx,
                "反应序列": seq_clean,
                "序列还原": restored_seq,
                "所选克重范围": f"{min_weight}g - {max_weight}g",
                "最后刺激丝克重": final_weight,
                "Xf": round(xf, 3),
                "k 值": None,
                "δ": round(delta, 4),
                "50% 缩足阈值（克）": threshold_g,
                "备注": "已超出最大克重限制"
            })
            continue
        elif boundary_flag == "min":
            threshold_g = min_weight
            results.append({
                "序号": idx,
                "反应序列": seq_clean,
                "序列还原": restored_seq,
                "所选克重范围": f"{min_weight}g - {max_weight}g",
                "最后刺激丝克重": final_weight,
                "Xf": round(xf, 3),
                "k 值": None,
                "δ": round(delta, 4),
                "50% 缩足阈值（克）": threshold_g,
                "备注": "已超出最小克重限制"
            })
            continue

        # 判断是否全0或全1，并刚好到边界
        if (seq_clean.count("0") == len(seq_clean) and cur_order == max_order) or \
           (seq_clean.count("1") == len(seq_clean) and cur_order == min_order):
            threshold_g = final_weight  # 或直接用max/min_weight
            note = "连续全阴性，输出最大阈值" if cur_order == max_order else "连续全阳性，输出最小阈值"
            results.append({
                "序号": idx,
                "反应序列": seq_clean,
                "序列还原": restored_seq,
                "所选克重范围": f"{min_weight}g - {max_weight}g",
                "最后刺激丝克重": final_weight,
                "Xf": round(xf, 3),
                "k 值": None,
                "δ": round(delta, 4),
                "50% 缩足阈值（克）": threshold_g,
                "备注": note
            })
            continue

        # 正常k值匹配与计算
        if not k_df["测量结果"].isin([seq_clean]).any():
            results.append({"序号": idx, "反应序列": seq_clean, "错误": "k 值表中未找到该序列"})
            continue

        try:
            k_val = float(k_df.loc[k_df["测量结果"] == seq_clean, "k值"].values[0])
        except:
            results.append({"序号": idx, "反应序列": seq_clean, "错误": "k 值无法转换为数值"})
            continue

        threshold_log = xf + k_val * delta
        threshold_g = 10 ** threshold_log / 10000

        results.append({
            "序号": idx,
            "反应序列": seq_clean,
            "序列还原": restored_seq,
            "所选克重范围": f"{min_weight}g - {max_weight}g",
            "最后刺激丝克重": final_weight,
            "Xf": round(xf, 3),
            "k 值": k_val,
            "δ": round(delta, 4),
            "50% 缩足阈值（克）": round(threshold_g, 4),
            "备注": ""
        })

    df_result = pd.DataFrame(results)
    st.dataframe(df_result, use_container_width=True)

    csv = df_result.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="📥 下载结果为 CSV",
        data=csv,
        file_name="VonFrey_结果.csv",
        mime="text/csv"
    )
