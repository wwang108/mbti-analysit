import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
from interact_with_llm import Agent
import json
import numpy as np


agent = Agent()
QUESTION_ANSWER_MAP = {
    "Question1: Are you usually?": {
        "A 'Good Mixer with groups of people": "Extrovert",
        "Rather quiet and reserved": "Introvert"
    },
    "Question2: Among your friends, you are?": {
        "Full of news about everybody": "Extrovert",
        "One of the last to hear what is going on": "Introvert"
    },
    "Question3: In doing something that many other people do, you would rather?": {
        "Invent a way of your own": "Intuition",
        "Do it in the accepted way": "Sensing"
    },
    "Question4: Do you admire the people who are?": {
        "Normal-acting to never make themselves the center of attention": "Sensing",
        "Too original and individual to care whether they are the center of attention or not": "Intuition"
    },
    "Question5: Do you more often let?": {
        "Your heart rule your head": "Feeling",
        "Your head rule your heart": "Thinking"
    },
    "Question6: Do you usually?": {
        "Value emotion more than logic": "Feeling",
        "Value logic more than feelings": "Thinking"
    },
    "Question7: When you go somewhere for the day, you would rather": {
        "Plan what you will do and when": "Judging",
        "Just go": "Perceiving"
    },
    "Question8: When you have a special job to do, you like to": {
        "Organize it carefully before you start": "Judging",
        "Find out what is necessary as you go along": "Perceiving"
    }
}
final = {"E_I": 0, "S_N":0, "T_F":0, "J_P":0 }
personality_map = {"Extrovert":("E_I", 0), "Introvert":("E_I", 50),
                   "Sensing":("S_N", 0), "Intuition":("S_N", 50),
                    "Thinking":("T_F", 0), "Feeling":("T_F", 50),
                    "Judging":("J_P", 0), "Perceiving":("J_P", 50)}
def process_choice(dic):
    final = {"J_P":0 ,"T_F":0,  "S_N":0, "E_I": 0 }
    for k, v in dic.items():
        pair = personality_map[QUESTION_ANSWER_MAP[k][v]]
        final[pair[0]] += pair[1]
    return final


def process_other(other):
    agent = Agent()
    result = {}
    for k,v in other.items():
        pair = agent.send_msg({k:v})
        result[pair[0]] = pair[1]
    final = {"J_P":0 ,"T_F":0,  "S_N":0, "E_I": 0 }
    for k,v in result.items():
        pair = personality_map[k]
        try:
            final[pair[0]] += 0.5 * int(v)
        except:
            final[pair[0]] += 25
    return final
    
def analyze_post(post):
    agent = Agent()

    result = agent.send_post(post)
    print(result)
    try:
        data = json.loads(result)
        final = {"J_P":0 ,"T_F":0,  "S_N":0, "E_I": 0 }
        final['E_I'] = 100 - data["Extrovert-Introvert"]["score"]
        final['S_N'] = 100 - data["Sensing-Intuition"]["score"]
        final["T_F"] = 100 - data["Thinking-Feeling"]["score"]
        final["J_P"] = 100 - data["Judging-Perceiving"]["score"]
    except:
        final = {}
    return final
    


def generate_image(final):
    if final == {}:
        st.write("I have no idea about it. Please provide more information")
        return
    # 初始化画布和坐标轴
    fig, ax = plt.subplots(figsize=(6, 6))

    # 设置渐变颜色
    colors = [
        ['#FF6347', '#FFD700'],
        ['#00FA9A', '#32CD32'],
        ['#6495ED', '#4682B4'],
        ['#DDA0DD', '#8A2BE2']
    ]

    # 创建一个大的图像数组
    img = np.zeros((100, 100, 3), dtype=np.uint8)

    sorted_keys = ["E_I", "S_N", "T_F", "J_P"]
    personality= ""
    for k in sorted_keys:
        v = final[k]
        if v < 50:
            personality += k[0]
        else:
            personality += k[2]
    for idx, k in enumerate(sorted_keys):
        v = final[k]
        if idx == 0:  # 左上
            img[int(50*(1-v/100)):50, :50] = np.array([int(colors[idx][0][i:i+2], 16) for i in (1, 3, 5)])
            img[:int(50*(1-v/100)), :50] = np.array([int(colors[idx][1][i:i+2], 16) for i in (1, 3, 5)])
        elif idx == 1:  # 右上
            img[int(50*(1-v/100)):50, 50:] = np.array([int(colors[idx][0][i:i+2], 16) for i in (1, 3, 5)])
            img[:int(50*(1-v/100)), 50:] = np.array([int(colors[idx][1][i:i+2], 16) for i in (1, 3, 5)])
        elif idx == 2:  # 左下
            img[50+int(50*(1-v/100)):, :50] = np.array([int(colors[idx][0][i:i+2], 16) for i in (1, 3, 5)])
            img[50:int(50*(1-v/100))+50, :50] = np.array([int(colors[idx][1][i:i+2], 16) for i in (1, 3, 5)])
        else:  # 右下
            img[50+int(50*(1-v/100)):, 50:] = np.array([int(colors[idx][0][i:i+2], 16) for i in (1, 3, 5)])
            img[50:int(50*(1-v/100))+50, 50:] = np.array([int(colors[idx][1][i:i+2], 16) for i in (1, 3, 5)])
    ax.set_title(f'Your MBTI persopnality may be {personality}', fontsize=16)
    ax.imshow(img)
    ax.axis('off')  # 不显示坐标轴

    # 在每个部分中添加文本
    for idx, k in enumerate(sorted_keys):
        v = final[k]
        if idx == 0:
            ax.text(25, 25, f"{k[0]} {100-v:.0f}%\n{k[2]} {v:.0f}%", ha='center', va='center', color='black', fontsize=12)
        elif idx == 1:
            ax.text(75, 25, f"{k[0]} {100-v:.0f}%\n{k[2]} {v:.0f}%", ha='center', va='center', color='black', fontsize=12)
        elif idx == 2:
            ax.text(25, 75, f"{k[0]} {100-v:.0f}%\n{k[2]} {v:.0f}%", ha='center', va='center', color='black', fontsize=12)
        else:
            ax.text(75, 75, f"{k[0]} {100-v:.0f}%\n{k[2]} {v:.0f}%", ha='center', va='center', color='black', fontsize=12)

    # 使用st.pyplot显示图表
    st.pyplot(fig)





# def generate_image(final):
    
    
#     # 初始化列表来保存标签和值
#     labels = []
#     values_l = []
#     values_r = []

#     sorted_keys = ["J_P","T_F","S_N", "E_I"]
#     # 遍历字典，更新标签和值列表
#     for k in sorted_keys:
#         v = final[k]
#         labels.append(k)
#         values_l.append(100-v)
#         values_r.append(v)

#     personality = ''

#     for k in sorted_keys:
#         v = final[k]
#         if v < 50:
#             personality += k[0]
#         else:
#             personality += k[2]
#     personality = personality[::-1]
#     fig, ax = plt.subplots(figsize=(10,6))

#     # 使用Seaborn的更漂亮的默认样式
#     sns.set(style="whitegrid")

#     # 为每个键绘制两个条形图，一个为E/S/T/J值，另一个为I/N/F/P值
#     width = 0.4
#     ind = range(len(labels))
#     p1 = ax.barh(ind, values_l, width, color=sns.color_palette("coolwarm", 4)[2], label='E/S/T/J')
#     p2 = ax.barh(ind, values_r, width, left=values_l, color=sns.color_palette("coolwarm", 4)[0], label='I/N/F/P')

#     # 设置标签和标题
#     ax.set_yticks(ind)
#     ax.set_yticklabels([label[0] for label in labels])
#     ax.set_xticks([0, 50, 100])
#     ax.set_xlabel('Percentage', fontsize=14)
#     ax.set_title(f'Your MBTI persopnality may be {personality}', fontsize=16)
#     ax.legend(loc = 'upper right', bbox_to_anchor=(1.15, 1.15))
#     # 显示右侧的'I/N/F/P'标签
#     for i, label in enumerate(labels):
#         ax.text(105, i, label[2], ha='center', va='center', color='black', fontsize=12)
#     # 使用st.pyplot显示图表
#     st.pyplot(fig)

