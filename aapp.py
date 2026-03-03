import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة (إبقاء كل شيء كما هو بناءً على طلبك)
st.set_page_config(page_title="BDS System", layout="wide")

# 2. تهيئة الذاكرة لحفظ الحالة لضمان التعبئة لمرة واحدة
if 'org_done' not in st.session_state: st.session_state.org_done = False
if 'lead_done' not in st.session_state: st.session_state.lead_done = False

# 3. القائمة الجانبية (اللغة والـ API)
with st.sidebar:
    lang = st.radio("اللغة / Language", ["Arabic", "English"])
    st.divider()
    api_key = st.text_input("OpenAI Key", type="password")
    client = OpenAI(api_key=api_key) if api_key else None

# نصوص الواجهة المحدثة (بدون كلمة بروفايل)
t = {
    "Arabic": {
        "title": "🛡️ أداة تحليل القرارات الإدارية (BDS)",
        "org_h": "🏛️ بيانات المنظمة",
        "lead_h": "👤 بيانات القائد",
        "save": "حفظ البيانات",
        "edit": "تعديل",
        "done": "تم الحفظ بنجاح ✅",
        "dec_h": "📝 تفاصيل القرار الحالي",
        "analyze": "تحليل القرار"
    },
    "English": {
        "title": "🛡️ Decision Support System (BDS)",
        "org_h": "🏛️ Organization Data",
        "lead_h": "👤 Leader Data",
        "save": "Save Data",
        "edit": "Edit",
        "done": "Saved Successfully ✅",
        "dec_h": "📝 Current Decision Details",
        "analyze": "Analyze Decision"
    }
}[lang]

st.title(t["title"])

# --- المرحلة 1: بيانات المنظمة (إدارة المنظمة) ---
with st.expander(t["org_h"], expanded=not st.session_state.org_done):
    if st.session_state.org_done:
        st.success(t["done"])
        if st.button(t["edit"], key="edit_org"):
            st.session_state.org_done = False
            st.rerun()
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("القطاع", ["حكومي", "خاص"], key="sec")
            st.selectbox("حجم المنظمة", ["١٠٠ فأقل", "١٠٠ إلى ٣٥٠", "أكثر من ٣٥٠"], key="sz")
            st.selectbox("عمر المنظمة", ["أقل من خمس سنوات", "٥-١٥", "أكثر من ١٥"], key="ag")
        with col2:
            st.selectbox("تقبل الموظفين للتغيير عادة", ["بإيجابية", "أحياناً صعب", "صعب دائماً"], key="ch")
            st.selectbox("مدى استقلالية المنظمة في اتخاذ القرارات", ["مستقلة بالكامل", "مستقلة جزئياً", "غير مستقلة"], key="aut")
        if st.button(t["save"], key="btn_org"):
            st.session_state.org_done = True
            st.rerun()

# --- المرحلة 2: بيانات القائد ---
with st.expander(t["lead_h"], expanded=not st.session_state.lead_done):
    if st.session_state.lead_done:
        st.success(t["done"])
        if st.button(t["edit"], key="edit_lead"):
            st.session_state.lead_done = False
            st.rerun()
    else:
        col3, col4 = st.columns(2)
        with col3:
            st.selectbox("الأسلوب القيادي", ["توجيهي", "تشاركي", "تفويضي"], key="sty")
            st.selectbox("عدد الموظفين تحت الإشراف المباشر", ["٥ فأقل", "٥-١٥", "١٥ فأكثر"], key="rep")
        with col4:
            st.selectbox("مستوى الثقة بينك وبين الفريق", ["عالي", "متوسط", "منخفض"], key="tru")