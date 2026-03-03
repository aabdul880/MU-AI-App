import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="BDS System", layout="wide")

# كود CSS "الاحترافي" لمسح Fork و GitHub وإبقاء الثلاث نقاط
hide_elements = """
    <style>
    /* إخفاء شريط العنوان بالكامل بما فيه Fork و GitHub */
    header {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    
    /* إخفاء التذييل وعلامة Streamlit */
    footer {display: none !important;}
    #viewerBadge_container__1QS1n {display: none !important;}
    .stAppDeployButton {display: none !important;}

    /* إظهار زر القائمة (الثلاث نقاط) فقط في مكان أنيق */
    [data-testid="stToolbar"] {
        visibility: visible !important;
        top: 10px !important;
        right: 10px !important;
    }
    
    /* تنظيف الواجهة من أي حواف زائدة */
    .block-container {padding-top: 2rem !important;}
    </style>
"""
st.markdown(hide_elements, unsafe_allow_html=True)

# --- 2. نظام الإعدادات واللغة (داخل السايدبار الذي يفتح من القائمة) ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'Arabic'

with st.sidebar:
    st.markdown("### ⚙️ Settings / الإعدادات")
    lang_choice = st.radio("Language / اللغة", ["Arabic", "English"], 
                           index=0 if st.session_state.lang == 'Arabic' else 1)
    st.session_state.lang = lang_choice
    
    st.divider()
    # مكان إدخال المفتاح بعيداً عن أعين المستخدم الرئيسي
    api_key = st.text_input("OpenAI Key", type="password")
    client = OpenAI(api_key=api_key) if api_key else None

# --- 3. نصوص التطبيق المترجمة ---
texts = {
    "Arabic": {
        "title": "🛡️ أداة تحليل القرارات الإدارية (BDS)",
        "org": "🏛️ بروفايل المنظمة (إدارة المنظمة)",
        "lead": "👤 بروفايل القائد",
        "desc": "📝 تفاصيل القرار الحالي",
        "btn": "تحليل القرار بناءً على البيانات",
        "placeholder": "اشرح القرار هنا بكلامك العادي..."
    },
    "English": {
        "title": "🛡️ Decision Support System (BDS)",
        "org": "🏛️ Organization Profile",
        "lead": "👤 Leader Profile",
        "desc": "📝 Decision Details",
        "btn": "Analyze Decision",
        "placeholder": "Describe your decision here..."
    }
}
t = texts[st.session_state.lang]

# --- 4. تصميم الواجهة الرئيسية ---
st.title(t["title"])

with st.expander(t["org"]):
    st.info("سيتم ربط هذه البيانات بالنظريات لاحقاً" if st.session_state.lang == 'Arabic' else "Data will be linked to theories later")

with st.expander(t["lead"]):
    st.info("بيانات القائد" if st.session_state.lang == 'Arabic' else "Leader Data")

st.divider()
st.subheader(t["desc"])
decision_text = st.text_area(t["placeholder"], height=150)

if st.button(t["btn"]):
    if not client:
        st.error("يرجى إدخال مفتاح API من قائمة الإعدادات" if st.session_state.lang == 'Arabic' else "Please enter API Key from Settings")
    else:
        st.success("جاري التحليل العلمي..." if st.session_state.lang == 'Arabic' else "Scientific analysis in progress...")