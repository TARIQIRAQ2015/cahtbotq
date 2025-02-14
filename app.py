import streamlit as st
import openai
from datetime import datetime

# تهيئة الصفحة
st.set_page_config(
    page_title="روبوت المحادثة الذكي",
    page_icon="🤖",
    layout="centered"
)

# تعيين مفتاح API الخاص بـ OpenAI
openai.api_key = "YOUR-OPENAI-API-KEY"

# تصميم CSS مخصص
st.markdown("""
<style>
.stTextInput {
    padding: 10px;
}
.stButton>button {
    width: 100%;
    border-radius: 5px;
    height: 50px;
    margin-top: 10px;
}
.chat-message {
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    display: flex;
}
.chat-message.user {
    background-color: #2b313e;
}
.chat-message.assistant {
    background-color: #475063;
}
</style>
""", unsafe_allow_html=True)

# عنوان التطبيق
st.title("🤖 روبوت المحادثة الذكي")

# تهيئة محفوظات المحادثة في session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# مربع إدخال الرسالة
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # إنشاء رد الروبوت
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        assistant_response = response.choices[0].message.content
        
        # إضافة رد الروبوت
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
            
    except Exception as e:
        st.error(f"حدث خطأ: {str(e)}")

# زر لمسح المحادثة
if st.button("مسح المحادثة"):
    st.session_state.messages = []
    st.experimental_rerun()
