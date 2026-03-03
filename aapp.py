import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة والاحترافية (إخفاء Fork و GitHub)
st.set_page_config(page_title="BDS System", layout="wide")

hide_style = """
    <style>
    header {visibility: hidden !important;}
    footer {display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    .stAppDeployButton {display: none !important;}
    #viewerBadge_container__1QS1n {display: none !important;}
    /* إبقاء النقاط الثلاث فقط للوصول للإعدادات */
    [data-testid="stToolbar"] {visibility: visible !important; top: 10px !important; right: 10px !important;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 2. تهيئة الذاكرة لحفظ الحالة (Session State)
if 'org_done' not in st.session_state: st.session_state.org_done = False
if 'lead_done' not in st.session_state: st.session_state.lead_done = False

# 3. القائمة الجانبية (اللغة والـ API)
with st.sidebar:
    lang = st.radio("اللغة / Language", ["Arabic", "English"])
    st.divider()
    api_key = st.text_input("OpenAI Key", type="password")
    client = OpenAI(api_key=api_key) if api_key else None

# نصوص الواجهة بناءً على اللغة
t = {
    "Arabic": {
        "title": "🛡️ أداة تحليل القرارات الإدارية (BDS)",
        "org_h": "🏛️ بروفايل المنظمة (إدارة المنظمة)",
        "lead_h": "👤 بروفايل القائد",
        "save": "حفظ البيانات",
        "edit": "تعديل",
        "done": "تم الحفظ بنجاح ✅",
        "dec_h": "📝 تفاصيل القرار الحالي",
        "analyze": "تحليل القرار"
    },
    "English": {
        "title": "🛡️ Decision Support System (BDS)",
        "org_h": "🏛️ Organization Profile",
        "lead_h": "👤 Leader Profile",
        "save": "Save Data",
        "edit": "Edit",
        "done": "Saved Successfully ✅",
        "dec_h": "📝 Current Decision Details",
        "analyze": "Analyze Decision"
    }
}[lang]

st.title(t["title"])

# --- المرحلة 1: بروفايل المنظمة (تعبئة لمرة واحدة) ---
with st.expander(t["org_h"], expanded=not st.session_state.org_done):
    if st.session_state.org_done:
        st.info(t["done"])
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
            st.selectbox("تقبل الموظفين للتغيير", ["بإيجابية", "أحياناً صعب", "صعب دائماً"], key="ch")
            st.selectbox("استقلالية القرار", ["مستقلة بالكامل", "مستقلة جزئياً", "غير مستقلة"], key="aut")
        if st.button(t["save"], key="btn_org"):
            st.session_state.org_done = True
            st.rerun()

# --- المرحلة 2: بروفايل القائد (تعبئة لمرة واحدة) ---
with st.expander(t["lead_h"], expanded=not st.session_state.lead_done):
    if st.session_state.lead_done:
        st.info(t["done"])
        if st.button(t["edit"], key="edit_lead"):
            st.session_state.lead_done = False
            st.rerun()
    else:
        col3, col4 = st.columns(2)
        with col3:
            st.selectbox("الأسلوب القيادي", ["توجيهي", "تشاركي", "تفويضي"], key="sty")
            st.selectbox("عدد الموظفين تحت الإشراف المباشر", ["٥ فأقل", "٥-١٥", "١٥ فأكثر"], key="rep")
        with col4:
            st.selectbox("مستوى الثقة مع الفريق", ["عالي", "متوسط", "منخفض"], key="tru")
            st.selectbox("غالبية موظفيك", ["جدد (أقل من ٣ سنوات)", "متوسط", "قدامى (أكثر من ٧ سنوات)"], key="ten")
        if st.button(t["save"], key="btn_lead"):
            st.session_state.lead_done = True
            st.rerun()

st.divider()

# --- المرحلة 3: القرار الحالي (الواجهة الذكية) ---
st.subheader(t["dec_h"])
decision_text = st.text_area("اشرح قرارك هنا بكلامك العادي...", height=100)

if decision_text:
    c1, c2 = st.columns(2)
    with c1:
        st.selectbox("قابلية القرار للتعديل", ["قابل للتعديل", "قابل جزئياً", "غير قابل"], key="d_flx")
        st.selectbox("متى يبدأ التنفيذ؟", ["فوري", "خلال أشهر", "تدريجي"], key="d_tim")
    with c2:
        st.selectbox("مدى معرفة الموظفين بالقرار", ["سري تماماً", "يوجد تسريبات", "معلن رسميًا"], key="d_vis")
        st.text_input("ماهي فئة الموظفين المتأثرين بالقرار؟", key="d_tar")
    
    st.select_slider("ما مدى تأثر هذه الفئة؟", options=["بسيط", "متوسط", "جوهري"], key="d_imp")

    if st.button(t["analyze"]):
        if not client: st.error("أدخل المفتاح من القائمة الجانبية")
        else: st.info("جاري التحليل العلمي...")