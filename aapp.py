import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="BDS System", layout="wide")

# 2. إعدادات اللغة في القائمة الجانبية
if 'lang' not in st.session_state:
    st.session_state.lang = 'Arabic'

with st.sidebar:
    st.session_state.lang = st.radio("Language / اللغة", ["Arabic", "English"])
    st.divider()
    api_key = st.text_input("OpenAI Key", type="password")
    client = OpenAI(api_key=api_key) if api_key else None

# نصوص الواجهة بناءً على اللغة المختارة
t = {
    "Arabic": {
        "title": "🛡️ نظام دعم القرار (BDS)",
        "tab_org": "🏛️ إدارة المنظمة",
        "tab_dec": "📝 اتخاذ القرار",
        "org_h": "بيانات المنظمة (تعبأ لمرة واحدة)",
        "dec_h": "تحليل القرار الحالي",
        "analyze": "تحليل القرار الآن"
    },
    "English": {
        "title": "🛡️ Decision Support System (BDS)",
        "tab_org": "🏛️ Organization Management",
        "tab_dec": "📝 Decision Making",
        "org_h": "Organization Data (One-time setup)",
        "dec_h": "Current Decision Analysis",
        "analyze": "Analyze Now"
    }
}[st.session_state.lang]

st.title(t["title"])

# 3. تقسيم الواجهة إلى تبويبات (بدون شاشة دخول)
tab1, tab2 = st.tabs([t["tab_org"], t["tab_dec"]])

# --- التبويب الأول: إدارة المنظمة ---
with tab1:
    st.subheader(t["org_h"])
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("القطاع" if st.session_state.lang == "Arabic" else "Sector", ["حكومي", "خاص"], key="org_sec")
        st.selectbox("حجم المنظمة" if st.session_state.lang == "Arabic" else "Org Size", ["١٠٠ فأقل", "١٠٠ إلى ٣٥٠", "أكثر من ٣٥٠"], key="org_sz")
        st.selectbox("عمر المنظمة" if st.session_state.lang == "Arabic" else "Org Age", ["أقل من خمس سنوات", "٥-١٥", "أكثر من ١٥"], key="org_ag")
    with col2:
        st.selectbox("تقبل الموظفين للتغيير" if st.session_state.lang == "Arabic" else "Change Acceptance", ["بإيجابية", "أحياناً صعب", "صعب دائماً"], key="org_ch")
        st.selectbox("استقلالية اتخاذ القرار" if st.session_state.lang == "Arabic" else "Decision Autonomy", ["مستقلة بالكامل", "مستقلة جزئياً", "غير مستقلة"], key="org_aut")
    
    if st.button("حفظ البيانات" if st.session_state.lang == "Arabic" else "Save Data"):
        st.success("تم الحفظ ✅")

# --- التبويب الثاني: اتخاذ القرار (مباشرة للقائد) ---
with tab2:
    st.subheader(t["dec_h"])
    decision_input = st.text_area("اشرح قرارك هنا بكلامك العادي..." if st.session_state.lang == "Arabic" else "Describe your decision here...", height=150)
    
    if decision_input:
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("قابلية القرار للتعديل" if st.session_state.lang == "Arabic" else "Flexibility", ["قابل للتعديل", "قابل جزئياً", "غير قابل"], key="d_flex")
            st.selectbox("متى يبدأ التنفيذ؟" if st.session_state.lang == "Arabic" else "Timing", ["فوري", "خلال أشهر", "تدريجي"], key="d_time")
        with c2:
            st.selectbox("مدى معرفة الموظفين بالقرار" if st.session_state.lang == "Arabic" else "Visibility", ["سري تماماً", "يوجد تسريبات", "معلن رسمياً"], key="d_vis")
            st.text_input("ماهي فئة الموظفين المتأثرين بالقرار ؟" if st.session_state.lang == "Arabic" else "Impacted Group", key="d_target")
        
        st.select_slider("ما مدى تأثر كل فئة ؟" if st.session_state.lang == "Arabic" else "Impact Level", options=["بسيط", "متوسط", "جوهري"], key="d_impact")

        if st.button(t["analyze"]):
            if not client: st.warning("Please enter API Key in sidebar")
            else: st.info("جاري التحليل...")