"""UARTのフレーム(スタートビット・データビット・ストップビット)波形図を生成する。
文字 'A' (0x41 = 0b01000001) を題材に、LSBファーストで送信される様子を描く。
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "Noto Sans JP", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

# ビット列: (ラベル, 値, 色分類)
# 'A' = 0b01000001 → LSBファーストで送信: bit0..bit7 = 1,0,0,0,0,0,1,0
bits = [
    ("IDLE", 1, "idle"),
    ("START", 0, "start"),
    ("D0\n(bit0=1)", 1, "data"),
    ("D1\n(bit1=0)", 0, "data"),
    ("D2\n(bit2=0)", 0, "data"),
    ("D3\n(bit3=0)", 0, "data"),
    ("D4\n(bit4=0)", 0, "data"),
    ("D5\n(bit5=0)", 0, "data"),
    ("D6\n(bit6=1)", 1, "data"),
    ("D7\n(bit7=0)", 0, "data"),
    ("STOP", 1, "stop"),
    ("IDLE", 1, "idle"),
]

color_map = {
    "idle": "#98a0ad",
    "start": "#b23a3a",
    "data": "#178a55",
    "stop": "#3860c6",
}

n = len(bits)
fig, ax = plt.subplots(figsize=(13, 4.2), dpi=180)

# 波形をステップで描画(1区間=1bit周期)
xs = list(range(n + 1))
ys = [b[1] for b in bits] + [bits[-1][1]]
ax.step(xs, ys, where="post", color="#1b1e25", linewidth=2.4, zorder=3)

# 各ビット区間を色分けした背景帯で示す
for i, (label, val, kind) in enumerate(bits):
    ax.axvspan(i, i + 1, color=color_map[kind], alpha=0.15, zorder=1)
    ax.text(i + 0.5, -0.38, label, ha="center", va="top", fontsize=10.5,
             color=color_map[kind], fontweight="bold")

# ビット境界の縦線
for i in range(n + 1):
    ax.axvline(i, color="#d8dde4", linewidth=1, zorder=0)

# HIGH/LOWラベル
ax.text(-0.35, 1, "High (1)", ha="right", va="center", fontsize=11, color="#586070")
ax.text(-0.35, 0, "Low (0)", ha="right", va="center", fontsize=11, color="#586070")

# 1bit周期の長さを示す矢印(STARTの区間、index=1)
ax.annotate("", xy=(2, 1.35), xytext=(1, 1.35),
            arrowprops=dict(arrowstyle="<->", color="#b9860f", linewidth=1.8))
ax.text(1.5, 1.45, "1 bit の長さ = 1 / ボーレート [秒]", ha="center", va="bottom",
        fontsize=11, color="#b9860f", fontweight="bold")

ax.set_xlim(-1.6, n + 0.3)
ax.set_ylim(-0.6, 1.75)
ax.set_yticks([])
ax.set_xticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_title("UARTの1フレーム: 文字 'A' (0x41) を送るときの波形(LSBファースト)",
             fontsize=13, fontweight="bold", color="#1b1e25", pad=18)

plt.tight_layout()
plt.savefig("01_uart_frame_waveform.png", facecolor="white")
print("saved: 01_uart_frame_waveform.png")
