import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة وإخفاء معالم GitHub و Fork
st.set_page_config(page_title="BDS System", layout="wide")

hide_style = """
    <style>
    header {visibility: hidden !important;}
    footer {display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    #viewerBadge_container__1QS1n {display: none !important;}
    .stAppDeployButton {display: none !important;}
    [data-testid="stToolbar"] {visibility: visible !important; top: 10px !important; right: 10px !important;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 2. إعدادات اللغة في القائمة الجانبية
if 'lang' not in st.session_state:
    st.session_state.lang = 'Arabic'

with st.sidebar:
    st.session_state.lang = st.selectbox("Language / اللغة", ["Arabic", "English"])
    st.divider()
    api_key = st.text_input("OpenAI Key", type="password")
    client = OpenAI(api_key=api_key) if api_key else None

t = {
    "Arabic": {
        "title": "🛡️ نظام دعم القرار (BDS)",
        "org_h": "🏛️ بيانات المنظمة (تعبأ لمرة واحدة)",
        "lead_h": "👤 بيانات القائد (تعبأ عند التسجيل)",
        "dec_h": "📝 تحليل القرار الحالي",
        "analyze": "تحليل القرار الآن"
    },
    "English": {
        "title": "🛡️ Decision Support System (BDS)",
        "org_h": "🏛️ Organization Data (One-time)",
        "lead_h": "👤 Leader Data (Registration)",
        "dec_h": "📝 Current Decision Analysis",
        "analyze": "Analyze Now"
    }
}[st.session_state.lang]

st.title(t["title"])

# --- المرحلة الأولى: بروفايل المنظمة ---
with st.expander(t["org_h"], expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        sector = st.selectbox("القطاع" if st.session_state.lang == "Arabic" else "Sector", ["حكومي", "خاص"])
        size = st.selectbox("حجم المنظمة" if st.session_state.lang == "Arabic" else "Org Size", ["١٠٠ فأقل", "١٠٠ إلى ٣٥٠", "أكثر من ٣٥٠"])
        age = st.selectbox("عمر المنظمة" if st.session_state.lang == "Arabic" else "Org Age", ["أقل من خمس سنوات", "٥-١٥", "أكثر من ١٥"])
    with col2:
        change = st.selectbox("تقبل الموظفين للتغيير" if st.session_state.lang == "Arabic" else "Change Acceptance", ["بإيجابية", "أحياناً صعب", "صعب دائماً"])
        autonomy = st.selectbox("استقلالية القرار" if st.session_state.lang == "Arabic" else "Autonomy", ["مستقلة بالكامل", "مستقلة جزئياً", "غير مستقلة"])

# --- المرحلة الثانية: بروفايل القائد ---
with st.expander(t["lead_h"], expanded=False):
    col3, col4 = st.columns(2)
    with col3:
        style = st.selectbox("الأسلوب القيادي" if st.session_state.lang == "Arabic" else "Leadership Style", ["توجيهي", "تشاركي", "تفويضي"])
        reports = st.selectbox("عدد الموظفين تحت الإشراف" if st.session_state.lang == "Arabic" else "Direct Reports", ["٥ فأقل", "٥-١٥", "١٥ فأكثر"])
    with col4:
        trust = st.selectbox("مستوى الثقة مع الفريق" if st.session_state.lang == "Arabic" else "Trust Level", ["عالي", "متوسط", "منخفض"])
        staff_type = st.selectbox("غالبية الموظفين" if st.session_state.lang == "Arabic" else "Staff Tenure", ["جدد (أقل من ٣ سنوات)", "متوسط", "قدامى (أكثر من ٧ سنوات)"])

st.divider()

# --- المرحلة الثالثة: إدخال القرار والأسئلة المتغيرة ---
st.subheader(t["dec_h"])
decision_input = st.text_area("اكتب قرارك هنا بكلامك العادي..." if st.session_state.lang == "Arabic" else "Describe your decision...")

if decision_input:
    col5, col6 = st.columns(2)
    with col5:
        flex = st.selectbox("قابلية القرار للتعديل" if st.session_state.lang == "Arabic" else "Flexibility", ["قابل للتعديل", "قابل جزئياً", "غير قابل"])
        timing = st.selectbox("متى يبدأ التنفيذ؟" if st.session_state.lang == "Arabic" else "Timing", ["فوري", "خلال أشهر", "تدريجي"])
    with col6:
        visibility = st.selectbox("مدى معرفة الموظفين" if st.session_state.lang == "Arabic" else "Visibility", ["سري تماماً", "يوجد تسريبات", "معلن رسمياً"])
        target = st.text_input("فئة الموظفين المتأثرين" if st.session_state.lang == "Arabic" else "Impacted Group")
    
    impact_range = st.select_slider("ما مدى تأثر هذه الفئة؟" if st.session_state.lang == "Arabic" else "Impact Level", options=["بسيط", "متوسط", "جوهري"])

    if st.button(t["analyze"]):
        if not client:
            st.error("يرجى إدخال المفتاح من القائمة الجانبية")
        else:
            st.info("جاري التحليل...")