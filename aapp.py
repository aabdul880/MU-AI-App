import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة وإخفاء معالم التطبيق تماماً
st.set_page_config(page_title="BDS - System", layout="wide")

# كود CSS "المنظف الشامل" لإخفاء حساب GitHub وكل الروابط
hide_all_branding = """
    <style>
    /* إخفاء القائمة العلوية والشعارات */
    header {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    
    /* إخفاء زر Fork وشعار GitHub */
    .stAppDeployButton {display: none !important;}
    #MainMenu {visibility: hidden !important;}
    
    /* إخفاء التذييل وعلامة Streamlit الحمراء/الملونة */
    footer {display: none !important;}
    #viewerBadge_container__1QS1n {display: none !important;}
    
    /* إخفاء أيقونة GitHub الجانبية التي تظهر في المتصفح */
    .viewerBadge_container__1QS1n {display: none !important;}
    
    /* تقليص المساحات البيضاء الزائدة */
    .block-container {padding-top: 1rem !important;}
    </style>
"""
st.markdown(hide_all_branding, unsafe_allow_html=True)

# --- 2. إعدادات اللغة في أعلى الصفحة ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'Arabic'

col_header1, col_header2 = st.columns([8, 2])
with col_header2:
    selected_lang = st.selectbox("🌐", ["Arabic", "English"])
    st.session_state.lang = selected_lang

# --- 3. نصوص الواجهة ---
texts = {
    "Arabic": {"title": "أداة تحليل القرارات الإدارية (BDS)", "analyze": "تحليل القرار"},
    "English": {"title": "Decision Support System (BDS)", "analyze": "Analyze Decision"}
}
t = texts[st.session_state.lang]

st.title(t["title"])

# --- 4. محتوى البروفايلات (مختصر للتجربة) ---
with st.expander("🏛️ بروفايل المنظمة" if st.session_state.lang == "Arabic" else "🏛️ Organization Profile"):
    st.write("بيانات المنظمة...")

with st.expander("👤 بروفايل القائد" if st.session_state.lang == "Arabic" else "👤 Leader Profile"):
    st.write("بيانات القائد...")

st.divider()
decision_area = st.text_area("اشرح قرارك هنا..." if st.session_state.lang == "Arabic" else "Explain your decision...")

if st.button(t["analyze"]):
    st.warning("بانتظار إضافة النظريات من ملف PDF..." if st.session_state.lang == "Arabic" else "Waiting for PDF theories...")

# مفتاح الـ API في الأسفل (اختياري)
with st.expander("⚙️ Setup"):
    api_input = st.text_input("OpenAI Key", type="password")