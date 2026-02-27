import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="賓果數據分析大師", layout="wide")
st.title("🎱 BINGO BINGO 賓果賓果數據分析")

# --- 側邊欄設定 ---
st.sidebar.header("⚙️ 模擬參數")
periods = st.sidebar.slider("分析期數", 100, 2000, 500)
pick_num = st.sidebar.selectbox("你想玩幾星？", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# 生成賓果模擬數據 (01-80號，每期開20個)
data = [random.sample(range(1, 81), 20) for _ in range(periods)]
all_numbers = [num for sublist in data for num in sublist]
counts = pd.Series(all_numbers).value_counts().sort_index()

# --- 1. 熱門號碼 Top 10 ---
st.subheader(f"🔥 最近 {periods} 期：最常出現號碼排行榜")
top_10 = counts.sort_values(ascending=False).head(10)
cols = st.columns(10)
for i, (num, count) in enumerate(top_10.items()):
cols[i].metric(label=f"號碼 {num}", value=f"{count}次")

# --- 2. 數據分析圖表 ---
st.divider()
col_left, col_right = st.columns(2)

with col_left:
st.subheader("📊 01-80 出現頻率")
fig, ax = plt.subplots()
ax.bar(counts.index, counts.values, color='skyblue')
ax.set_xlabel("號碼")
ax.set_ylabel("次數")
st.pyplot(fig)

with col_right:
st.subheader("⚖️ 奇偶 & 大小分析")
# 簡單分析最後一期的奇偶
last_draw = data[-1]
odds = len([n for n in last_draw if n % 2 != 0])
evens = 20 - odds
bigs = len([n for n in last_draw if n > 40])
smalls = 20 - bigs

st.write(f"最新一期狀態：")
st.write(f"• 奇偶數：{odds} 奇 / {evens} 偶")
st.write(f"• 大小號：{bigs} 大 / {smalls} 小")
st.info("通常賓果 20 個號碼中，奇偶與大小會趨近於 10:10。")

# --- 3. 系統推薦 ---
st.divider()
hot_nums = list(top_10.index[:pick_num])
st.success(f"💡 根據數據熱度，建議您的 {pick_num} 星推薦組合為：**{sorted(hot_nums)}**")
