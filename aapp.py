import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة وإخفاء العلامات التجارية
st.set_page_config(page_title="BDS System", layout="wide")

hide_style = """
    <style>
    header {visibility: hidden !important;}
    footer {display: none !important;}
    #viewerBadge_container__1QS1n {display: none !important;}
    .stAppDeployButton {display: none !important;}
    /* إبقاء زر القائمة (الثلاث نقاط) ظاهراً */
    [data-testid="stToolbar"] {right: 20px !important;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 2. نظام اللغة الذكي (يظهر في القائمة الجانبية عند الضغط على الإعدادات)
with st.sidebar:
    st.markdown("### 🌐 Settings / الإعدادات")
    lang = st.radio("Choose Language / اختر اللغة", ["Arabic", "English"], index=0)
    st.session_state.lang = lang

# 3. نصوص الواجهة بناءً على الاختيار
texts = {
    "Arabic": {
        "title": "أداة تحليل القرارات الإدارية (BDS)",
        "org": "🏛️ بروفايل المنظمة",
        "leader": "👤 بروفايل القائد",
        "dec": "📝 تفاصيل القرار",
        "btn": "تحليل القرار"
    },
    "English": {
        "title": "Decision Support System (BDS)",
        "org": "🏛️ Organization Profile",
        "leader": "👤 Leader Profile",
        "dec": "📝 Decision Details",
        "btn": "Analyze Decision"
    }
}
t = texts[st.session_state.lang]

# 4. تصميم الواجهة الرئيسية
st.title(t["title"])

with st.expander(t["org"]):
    st.write("بيانات المنظمة...")

with st.expander(t["leader"]):
    st.write("بيانات القائد...")

st.divider()
st.subheader(t["dec"])
decision_text = st.text_area("..." if st.session_state.lang == "Arabic" else "Describe here...")

# مفتاح API (مخفي تحت الإعدادات في القائمة الجانبية)
with st.sidebar:
    st.divider()
    api_key = st.text_input("OpenAI Key", type="password")
    client = OpenAI(api_key=api_key) if api_key else None

if st.button(t["btn"]):
    if not client:
        st.error("Please enter API Key" if lang == "English" else "يرجى إدخال المفتاح")
    else:
        st.info("جاري التحليل..." if lang == "Arabic" else "Analyzing...")