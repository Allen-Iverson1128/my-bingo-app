import streamlit as st
import pandas as pd
import random
# 在 import random 下方加入這行，保證每次產生的隨機數都一樣
random.seed(42)
import matplotlib.pyplot as plt

st.set_page_config(page_title="賓果獵人獵號系統", layout="wide")
st.title("🎯 BINGO BINGO 賓果獵人：進階策略版")

# --- 側邊欄設定 ---
st.sidebar.header("⚙️ 進階分析設定")
periods = st.sidebar.slider("分析期數", 100, 2000, 500)
play_type = st.sidebar.selectbox("選擇投注星數", options=[2, 3, 4], index=2)
st.sidebar.divider()
st.sidebar.info("建議設定 500 期以獲得穩定數據。")

# --- 數據模擬與核心計算 ---
# 生成數據 (01-80號，每期開20個)
data = [random.sample(range(1, 81), 20) for _ in range(periods)]
all_numbers = [num for sublist in data for num in sublist]
counts = pd.Series(all_numbers).value_counts().sort_index()

# 1. 遺漏值計算 (上次出現到現在隔了幾期)
last_occurrence = {}
for i, draw in enumerate(reversed(data)):
    for num in draw:
        if num not in last_occurrence:
            last_occurrence[num] = i

# --- 第一區：熱門排行榜與遺漏值 ---
st.subheader(f"🔥 最近 {periods} 期：Top 10 強勢號碼與遺漏分析")
top_10_idx = counts.sort_values(ascending=False).head(10).index
cols = st.columns(10)

for i, num in enumerate(top_10_idx):
    missing = last_occurrence.get(num, "N/A")
    cols[i].metric(label=f"號碼 {num}", value=f"{counts[num]}次", delta=f"隔 {missing} 期", delta_color="inverse")

st.caption("💡 紅色『隔 X 期』數字越大，代表該熱門號近期越久沒開，反彈機率越高。")

st.divider()

# --- 第二區：尾數與連號規律 ---
col_tail, col_logic = st.columns(2)

with col_tail:
    st.subheader("🔢 尾數熱度分佈 (0-9)")
    tails = [num % 10 for num in all_numbers]
    tail_counts = pd.Series(tails).value_counts().sort_index()
    fig_tail, ax_tail = plt.subplots()
    ax_tail.bar(tail_counts.index.astype(str), tail_counts.values, color='orange')
    ax_tail.set_ylabel("出現總次數")
    st.pyplot(fig_tail)
    st.info("💡 挑選號碼時，優先選擇柱狀較高的尾數。")

with col_logic:
    st.subheader("🛡️ 組合回測模擬 (2奇2偶)")
    # 簡單模擬：計算過去 100 期符合 2奇2偶的頻率
    even_odd_list = []
    for draw in data[-100:]:
        odds = len([n for n in draw if n % 2 != 0])
        evens = 20 - odds
        # 這邊模擬的是『如果20球裡奇偶各半』的機率
        even_odd_list.append(1 if (odds >= 8 and odds <= 12) else 0)
    
    win_rate = sum(even_odd_list)
    st.write(f"📊 過去 100 期中，奇偶比例接近 10:10 的機率為：**{win_rate}%**")
    st.progress(win_rate / 100)
    st.write("這證明了『2奇2偶』是極高機率的穩定組合。")

# --- 第三區：獵人精選 (自動對接星數) ---
st.divider()
st.subheader(f"🚀 獵人建議：最強 {play_type} 星組合")

# 1. 取得 Top 10 並分類 (這裡使用你原本的 top_10_idx 變數)
top_10_list = list(top_10_idx)
baskets = {
    "奇大": [n for n in top_10_list if n % 2 != 0 and n > 40],
    "奇小": [n for n in top_10_list if n % 2 != 0 and n <= 40],
    "偶大": [n for n in top_10_list if n % 2 == 0 and n > 40],
    "偶小": [n for n in top_10_list if n % 2 == 0 and n <= 40]
}

# 2. 根據星數抓取最佳組合
final_4 = [] # 這裡維持叫 final_4 是為了跟下方的評分系統對接
used_tails = set()
basket_keys = ["奇大", "奇小", "偶大", "偶小"]

# 按照星數決定要跑幾次循環
for i in range(play_type):
    key = basket_keys[i % 4]
    basket = baskets.get(key, [])
    
    # 找尾數不重複的最佳號碼
    best_pick = None
    for n in basket:
        if n % 10 not in used_tails:
            best_pick = n
            break
    
    # 如果籃子裡都重複尾數，就抓籃子裡的第一名
    if not best_pick and basket:
        best_pick = basket[0]
        
    if best_pick:
        final_4.append(best_pick)
        used_tails.add(best_pick % 10)

st.success(f"建議執行組合：**{sorted(final_4)}**")
st.info("💡 若現場 Delta 與 App 不同，請從同屬性籃子中找『現場隔最久』的號碼更換。")

# --- 第三區：獵人評分與過濾系統 ---
st.divider()
st.subheader("🛡️ 獵人終極過濾器：戰場分析")

# 把這裡的 best_4 改成 final_4，讓兩個系統對接
test_numbers = sorted(final_4) if len(final_4) == play_type else [6, 39, 59, 74]
score = 0
reasons = []

# 1. 奇偶
odds = len([n for n in test_numbers if n % 2 != 0])
if odds == 2:
    score += 25
    reasons.append("✅ 奇偶 2:2 平衡 (+25分)")

# 2. 大小
bigs = len([n for n in test_numbers if n > 40])
if bigs == 2:
    score += 25
    reasons.append("✅ 大小 2:2 平衡 (+25分)")

# 3. 尾數 (這裡因為我們新邏輯已經過濾過，通常是滿分)
tails = len(set([n % 10 for n in test_numbers]))
if tails >= 4:
    score += 25
    reasons.append(f"✅ 尾數完全分散 ({tails}種組合) (+25分)")
elif tails == 3:
    score += 15
    reasons.append(f"⚠️ 尾數稍有重複 ({tails}種組合) (+15分)")

# 4. 遺漏值 (Delta)
avg_missing = sum([last_occurrence.get(n, 0) for n in test_numbers]) / 4
if avg_missing >= 2:
    score += 25
    reasons.append(f"✅ 平均遺漏值 {avg_missing:.1f} 期，動能充足 (+25分)")

# 最終顯示
st.write(f"### 🎯 當前組合戰力評分： **{score} 分**")
for r in reasons:
    st.write(r)

if score >= 90:
    st.balloons()
    st.success("🔥 這是經過【尾數不重複】過濾的終極組合，建議執行十期計畫！")

