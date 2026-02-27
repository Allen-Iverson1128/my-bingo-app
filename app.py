import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
from collections import Counter

st.set_page_config(page_title="三星彩分析大師", layout="wide")
st.title("🎰 三星彩數據分析與回測")

# 側邊欄設定
st.sidebar.header("⚙️ 設定")
total_periods = st.sidebar.slider("總期數", 500, 5000, 1000)
test_size = st.sidebar.slider("回測期數", 50, 500, 100)

# 生成模擬數據
data = [tuple(random.randint(0, 9) for _ in range(3)) for _ in range(total_periods)]
df = pd.DataFrame(data, columns=['百位', '十位', '個位'])

# 統計圖表
col1, col2 = st.columns(2)
with col1:
st.subheader("📊 數字頻率")
pos = st.selectbox("選擇位置", ['百位', '十位', '個位'])
st.bar_chart(df[pos].value_counts())

with col2:
st.subheader("📈 和值分佈")
sums = df.sum(axis=1)
fig, ax = plt.subplots()
ax.hist(sums, bins=28, color='gold', edgecolor='black')
st.pyplot(fig)

# 回測邏輯
st.divider()
st.subheader("🧪 策略回測報告")
train_df = df.iloc[:-test_size]
test_df = df.iloc[-test_size:]
rec = (train_df['百位'].mode()[0], train_df['十位'].mode()[0], train_df['個位'].mode()[0])

hits = 0
for row in test_df.itertuples(index=False):
if tuple(row) == rec:
hits += 1

st.write(f"💡 推薦組合：{rec}")
st.metric("中獎次數", f"{hits} 次")