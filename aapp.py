import streamlit as st
from openai import OpenAI

# إعدادات الصفحة
st.set_page_config(page_title="BDS - Decision Support", layout="wide")

# كود CSS "خارق" لإخفاء كل معالم Streamlit (العلامة الملونة، الخط الأحمر، التذييل)
hide_all_streamlit_elements = """
            <style>
            /* إخفاء القائمة العلوية والخط الأحمر */
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="stHeader"] {display: none;}
            
            /* إخفاء علامة Streamlit الملونة (التاج) في أسفل اليمين */
            #viewerBadge_container__1QS1n {display: none !important;}
            .viewerBadge_container__1QS1n {display: none !important;}
            .viewerBadge_link__1S137 {display: none !important;}
            
            /* إخفاء التذييل وأي نصوص برمجية أسفل الصفحة */
            footer {display: none !important;}
            [data-testid="stStatusWidget"] {display: none !important;}
            
            /* تنظيف الحواف */
            .stAppDeployButton {display: none !important;}
            </style>
            """
st.markdown(hide_all_streamlit_elements, unsafe_allow_html=True)

# --- إعدادات اللغة ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'Arabic'

# زر اللغة في الأعلى (أنيق وبسيط)
col_l1, col_l2 = st.columns([9, 1])
with col_l2:
    selected_lang = st.selectbox("🌐", ["Arabic", "English"], index=0 if st.session_state.lang == "Arabic" else 1)
    st.session_state.lang = selected_lang

# نصوص الواجهة
texts = {
    "Arabic": {"title": "أداة تحليل القرارات الإدارية (BDS)", "btn": "تحليل القرار"},
    "English": {"title": "Decision Support System (BDS)", "btn": "Analyze"}
}
t = texts[st.session_state.lang]

st.title(t["title"])

# --- محتوى الأداة (البروفايلات) ---
with st.expander("🏛️ المنظمة" if st.session_state.lang == "Arabic" else "🏛️ Organization"):
    st.write("بيانات المنظمة هنا...")

with st.expander("👤 القائد" if st.session_state.lang == "Arabic" else "👤 Leader"):
    st.write("بيانات القائد هنا...")

st.divider()
decision_input = st.text_area("أدخل القرار هنا..." if st.session_state.lang == "Arabic" else "Enter decision...")

if st.button(t["btn"]):
    st.info("بانتظار مفتاح API والنظريات للبدء..." if st.session_state.lang == "Arabic" else "Waiting for API and theories...")