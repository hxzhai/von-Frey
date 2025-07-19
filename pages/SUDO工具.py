
import streamlit as st
import pandas as pd

# 加载修正后的 von Frey 对照表
@st.cache_data
def load_data():
    df = pd.read_csv("von_frey_thresholds_corrected.csv", dtype={"Binary_Pattern": str})
    return df

df = load_data()
df["Binary_Pattern"] = df["Binary_Pattern"].astype(str)

st.title("von Frey 阈值查询工具")

st.markdown("""
#### 使用说明：  
一种简化的up-down方法（SUDO），用于使用冯·弗雷丝测量啮齿动物的机械伤害刺激  
本工具是基于 von Frey 行为测试中常用的五根纤维丝（**0.16 g、0.4 g、0.6 g、1.0 g、2.0 g**）的反应组合规律所构建的阈值换算表。  
其结果基于对这些特定力度纤维丝的递进测试设计，**不适用于其他力度**（注意以上五根纤维丝中间跳过了1.4g的纤维丝）。  
⚠️ 请勿混用，以确保换算结果的科学性和可解释性。
**记录反应序列（0/1）：**  
    测试时从最小克数 **0.16g开始起测**     
   - 0 表示阴性反应（无缩足）
   - 1 表示阳性反应（有缩足）
   - 每次根据反应结果选择下一根刺激丝：
     - **阳性 → 更轻的纤维丝**
     - **阴性 → 更重的纤维丝**  
     
共 **测量6次** ，若 **连续出现4次阳性（1111），或5次阴性（00000）** ，即停止测量
     
参考文献：Bonin RP, Bories C, De Koninck Y. A simplified up-down method (SUDO) for measuring mechanical nociception in rodents using von Frey filaments. Mol Pain. 2014 Apr 16;10:26. doi: 10.1186/1744-8069-10-26. 
""")
st.markdown("由 0 表示阴性，1 表示阳性，例如输入序列 **000010**），可单个或多个查询。")

input_text = st.text_area("请输入序列（每行一个）")

if st.button("查询阈值"):
    if input_text.strip() == "":
        st.warning("请输入至少一个序列")
    else:
        query_list = [line.strip() for line in input_text.splitlines() if line.strip()]
        result_df = pd.DataFrame(query_list, columns=["Binary_Pattern"])
        merged_df = result_df.merge(df, on="Binary_Pattern", how="left", sort=False)

        # 添加序号 & 显示中文列名
        merged_df_display = merged_df.copy()
        merged_df_display.rename(columns={"Binary_Pattern": "输入序列"}, inplace=True)
        merged_df_display.insert(0, "序号", range(1, len(merged_df_display) + 1))
        merged_df_display.rename(columns={"Binary_Pattern": "输入序列"}, inplace=True)

        # 添加“反应序列”列（输入序列的 O/X 转换）
        merged_df_display["反应序列"] = merged_df_display["输入序列"].apply(
            lambda x: x.replace("0", "O").replace("1", "X")
        )

        # 将“反应序列”列移到“输入序列”右边
        cols = list(merged_df_display.columns)
        if "反应序列" in cols and "输入序列" in cols:
            cols.insert(cols.index("输入序列") + 1, cols.pop(cols.index("反应序列")))
            merged_df_display = merged_df_display[cols]

        st.write("查询结果如下：")
        st.dataframe(merged_df_display, use_container_width=True)
        csv = merged_df.to_csv(index=False).encode('utf-8')
        st.download_button("下载结果 CSV", csv, "von_frey_results.csv", "text/csv")
