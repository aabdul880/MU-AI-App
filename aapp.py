import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة وإخفاء العناصر غير المرغوبة
st.set_page_config(page_title="BDS System", layout="wide")

hide_elements = """
    <style>
    header {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    footer {display: none !important;}
    #viewerBadge_container__1QS1n {display: none !important;}
    .stAppDeployButton {display: none !important;}
    [data-testid="stToolbar"] {
        visibility: visible !important;
        top: 10px !important;
        right: 10px !important;
    }
    .block-container {padding-top: 2rem !important;}
    </style>
"""
st.markdown(hide_elements, unsafe_allow_html=True)

# 2. نظام اللغة والإعدادات (داخل السايدبار)
if 'lang' not in st.session_state:
    st.session_state.lang = 'Arabic'

with st.sidebar:
    st.markdown("### ⚙️ Settings / الإعدادات")
    lang_choice = st.radio("Language / اللغة", ["Arabic", "English"], 
                           index=0 if st.session_state.lang == 'Arabic' else 1)
    st.session_state.lang = lang_choice
    st.divider()
    api_key = st.text_input("OpenAI Key", type="password")
    client = OpenAI(api_key=api_key) if api_key else None

# 3. نصوص التطبيق
texts = {
    "Arabic": {
        "title": "🛡️ أداة تحليل القرارات الإدارية (BDS)",
        "org": "🏛️ بروفايل المنظمة",
        "lead": "👤 بروفايل القائد",
        "desc": "📝 تفاصيل القرار الحالي",
        "btn": "تحليل القرار",
        "style": "الأسلوب القيادي",
        "trust": "مستوى الثقة مع الفريق",
        "sector": "القطاع",
        "size": "حجم المنظمة"
    },
    "English": {
        "title": "🛡️ Decision Support System (BDS)",
        "org": "🏛️ Organization Profile",
        "lead": "👤 Leader Profile",
        "desc": "📝 Decision Details",
        "btn": "Analyze Decision",
        "style": "Leadership Style",
        "trust": "Trust Level",
        "sector": "Sector",
        "size": "Org Size"
    }
}
t = texts[st.session_state.lang]

# 4. الواجهة الرئيسية (هنا تظهر البيانات)
st.title(t["title"])

# بروفايل المنظمة
with st.expander(t["org"]):
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox(t["sector"], ["حكومي", "خاص"] if st.session_state.lang == 'Arabic' else ["Government", "Private"])
    with col2:
        st.selectbox(t["size"], ["صغير", "متوسط", "كبير"] if st.session_state.lang == 'Arabic' else ["Small", "Medium", "Large"])

# بروفايل القائد (الآن ستظهر البيانات هنا)
with st.expander(t["lead"]):
    col3, col4 = st.columns(2)
    with col3:
        st.selectbox(t["style"], ["توجيهي", "تشاركي", "تفويضي"] if st.session_state.lang == 'Arabic' else ["Directive", "Participative", "Delegative"])
    with col4:
        st.select_slider(t["trust"], options=["منخفض", "متوسط", "عالي"] if st.session_state.lang == 'Arabic' else ["Low", "Medium", "High"])

st.divider()
st.subheader(t["desc"])
decision_text = st.text_area("..." if st.session_state.lang == 'Arabic' else "Describe decision...")

if st.button(t["btn"]):
    if not client:
        st.error("أدخل المفتاح من الإعدادات")
    else:
        st.info("جاري المعالجة...")