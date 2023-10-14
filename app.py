import streamlit as st
from process import process_choice,process_other, generate_image, analyze_post

# 定义问题列表
QUESTIONS = [
    "Question1: Are you usually?",
    "Question2: Among your friends, you are?",
    "Question3: In doing something that many other people do, you would rather?",
    "Question4: Do you admire the people who are?",
    "Question5: Do you more often let?",
    "Question6: Do you usually?",
    "Question7: When you go somewhere for the day, you would rather",
    "Question8: When you have a special job to do, you like to"
]

OPTIONS = {
    QUESTIONS[0]: ["A 'Good Mixer with groups of people", "Rather quiet and reserved"], # Extrovert (E) vs. Introvert (I)
    QUESTIONS[1]: ["Full of news about everybody", "One of the last to hear what is going on"], #Extrovert (E) vs. Introvert (I)
    QUESTIONS[2]: ["Invent a way of your own", "Do it in the accepted way "], #Intuition, Sensing
    QUESTIONS[3]: ["Normal-acting to never make themselves the center of attention", "Too original and individual to care whether they are the center of attention or not"],# Sensing, Intuition
    QUESTIONS[4]: ["Your heart rule your head", "Your head rule your heart"], ##  Feeling, Thinking
    QUESTIONS[5]: ["Value emotion more than logic", "Value logic more than feelings"], # Thinking, Feeling
    QUESTIONS[6]: ["Plan what you will do and when", "Just go"], # Judging, Perceiving
    QUESTIONS[7]: ["Organize it carefully before you start", "Find out what is necessary as you go along"] # Judging, Perceiving
}

def main():
    # 页面选择
    page = st.sidebar.radio("Choose Test Method", ["Questionnaire", "Post upload"])

    if page == "Questionnaire":
        questionnaire()
    elif page == "Post upload":
        post()

def questionnaire():
    custom_css = """
    <style>
        body {
            font-family: Arial, Helvetica, sans-serif;
        }
        h1 {
            font-size: 52px;
        }
        h2 {
            color: #4A90E2;
             font-size: 36px;
        }
        label[data-baseweb="radio"] div[data-testid="stMarkdownContainer"] p {
            font-size: 20px !important;
            line-height: 24px !important;
            margin-top: 5px !important;
        }
        label[data-baseweb="radio"] .st-c9 {
            margin-top: 8px !important;
        }
        .question-text {
            font-size: 30px;
            font-weight: bold;
            margin-bottom: 20px;
        }

    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    st.title("MBTI Personality Insight")
    st.markdown("""
    <p style='font-size:20px'>
        Discover deeper insights about your Myers-Briggs Type Indicator (MBTI) personality through this interactive questionnaire. 
        If the options couldn't describe you, customize your answers.
    </p>
    """, unsafe_allow_html=True)


    # 使用session_state来跟踪当前的问题索引
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0

    # 初始化两个答案字典
    if "answers_choices" not in st.session_state:
        st.session_state.answers_choices = {}
    if "answers_other" not in st.session_state:
        st.session_state.answers_other = {}

    # 显示当前问题，使用Markdown增大字体并添加额外的空间'


    cols = st.columns([4, 1])
    # 在左侧列显示问题
    current_question = QUESTIONS[st.session_state.current_question_index]
    cols[0].markdown(f'<div class="question-text">{current_question}</div>', unsafe_allow_html=True)
    
    option_a, option_b = OPTIONS[current_question]
    cols[0].markdown('<div class="custom-radio">', unsafe_allow_html=True)
    selected_option = cols[0].radio("", [option_a, option_b, "Not Listed? Enter Your Own"])
    cols[0].markdown('</div>', unsafe_allow_html=True)

    user_answer = None
    with st.container():
        st.markdown("---")
        if selected_option == "Not Listed? Enter Your Own":
        # 使用.get()方法获取值，并在键不存在时提供一个默认值
            default_value = st.session_state.answers_other.get(st.session_state.current_question_index, "")
            user_answer = st.text_input("Please write your answer:", default_value)
        else:
            user_answer = selected_option

    # 清除按钮
    if cols[1].button("Clear ALL"):
        st.session_state.current_question_index = 0
        st.session_state.answers_choices.clear()
        st.session_state.answers_other.clear()
        st.experimental_rerun()

    # 首个问题
    elif st.session_state.current_question_index == 0:
        if st.button("Next"):
            if selected_option == "Not Listed? Enter Your Own":
                st.session_state.answers_other[current_question] = user_answer
            else:
                st.session_state.answers_choices[current_question] = user_answer
            st.session_state.current_question_index += 1
            st.experimental_rerun()

    # 最后一个问题
    elif st.session_state.current_question_index == len(QUESTIONS) - 1:
        cols = st.columns([1, 1, 1])
        prev_button, _, submit_button = cols

        if prev_button.button("Prev"):
            st.session_state.current_question_index -= 1
            st.experimental_rerun()
        elif submit_button.button("Submit"):
            if selected_option == "Not Listed? Enter Your Own":
                st.session_state.answers_other[current_question] = user_answer

            else:
                st.session_state.answers_choices[current_question] = user_answer

            final0 = process_choice(st.session_state.answers_choices)
            final1 = process_other(st.session_state.answers_other)
            final = {key: final0[key]+ final1[key] for key in set(final0) | set(final1)}
            generate_image(final)
            
            

    # 中间的问题
    else:
        cols = st.columns([1, 1, 1])
        prev_button, next_button, _ = cols

        if prev_button.button("Prev"):
            st.session_state.current_question_index -= 1
            st.experimental_rerun()
        elif next_button.button("Next"):
            if selected_option == "Not Listed? Enter Your Own":
                st.session_state.answers_other[current_question] = user_answer
            else:
                st.session_state.answers_choices[current_question] = user_answer
            st.session_state.current_question_index += 1
            st.experimental_rerun()





def post():
    # 设置页面标题
    st.title("MBTI Personality Insight")
    st.markdown("""
    <p style='font-size:20px'>
        Upload posts to get insights about MBTI personality analysis. 
    </p>
    """, unsafe_allow_html=True)

    # 创建文本输入框
    user_input = st.text_area("Enter your post here:")

    # 创建提交按钮
    if st.button("Submit"):
        # 在这里调用你的文本分析函数
        final = analyze_post(user_input)  # 假设你有一个analyze_text函数来进行文本分析
        
        st.subheader("Analysis Result:")
        generate_image(final)


if __name__ == "__main__":
    main()
