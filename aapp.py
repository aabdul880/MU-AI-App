import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة
st.set_page_config(page_title="BDS System", layout="wide")

# كود CSS "المنظف الشامل" لإخفاء أيقونة الحساب وكل معالم النظام
hide_all_branding = """
    <style>
    /* إخفاء القائمة العلوية والخط الأحمر */
    header {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    
    /* إخفاء شعار GitHub والتاج الأحمر الصغير وأي أيقونات عائمة */
    .stAppDeployButton {display: none !important;}
    #MainMenu {visibility: hidden !important;}
    footer {display: none !important;}
    #viewerBadge_container__1QS1n {display: none !important;}
    
    /* استهداف أيقونة الحساب الدائرية (Avatar) التي تظهر في الزاوية */
    img[src*="githubusercontent"], .st-emotion-cache-1v0mbdj, .st-emotion-cache-zq5wmm {
        display: none !important;
    }

    /* إخفاء أي أزرار أو روابط تظهر أسفل الشاشة */
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    
    /* تقليص الفراغ العلوي */
    .block-container {padding-top: 0rem !important;}
    </style>
"""
st.markdown(hide_all_branding, unsafe_allow_html=True)

# --- 2. الواجهة ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'Arabic'

col_header = st.columns([8, 2])
with col_header[1]:
    selected_lang = st.selectbox("🌐", ["Arabic", "English"])
    st.session_state.lang = selected_lang

texts = {
    "Arabic": {"title": "أداة تحليل القرارات الإدارية (BDS)", "btn": "تحليل القرار"},
    "English": {"title": "Decision Support System (BDS)", "btn": "Analyze"}
}
t = texts[st.session_state.lang]

st.title(t["title"])

# --- بقية أقراص الإدخال ---
with st.expander("🏛️" if st.session_state.lang == "Arabic" else "🏛️ Organization"):
    st.write("البيانات...")

st.divider()
decision_input = st.text_area("اشرح القرار..." if st.session_state.lang == "Arabic" else "Explain decision...")

# مفتاح الـ API للتحليل
with st.expander("⚙️ Setup"):
    api_key = st.text_input("OpenAI Key", type="password")
    client = OpenAI(api_key=api_key) if api_key else None

if st.button(t["btn"]):
    if not client: st.error("Enter Key")
    else: st.info("Analyzing...")