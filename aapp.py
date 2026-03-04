import streamlit as st
from openai import OpenAI

# 1. إعدادات احترافية وإخفاء Fork/GitHub
st.set_page_config(page_title="BDS System", layout="wide")

st.markdown("""
    <style>
    header {visibility: hidden !important;}
    footer {display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    .stAppDeployButton {display: none !important;}
    #viewerBadge_container__1QS1n {display: none !important;}
    </style>
""", unsafe_allow_html=True)

# 2. إعدادات اللغة والـ API مخفية
with st.sidebar:
    lang = st.radio("اللغة / Language", ["Arabic", "English"])
    api_key = st.text_input("OpenAI Key", type="password")
    client = OpenAI(api_key=api_key) if api_key else None

# 3. إنشاء التبويبات (الأقسام)
tab1, tab2, tab3 = st.tabs(["🏛️ إدارة المنظمة", "👤 بروفايل القائد", "📝 اتخاذ القرار"])

# --- القسم الأول: إدارة المنظمة (تعبئة لمرة واحدة) ---
with tab1:
    st.subheader("إعدادات المنظمة الثابتة")
    col1, col2 = st.columns(2)
    with col1:
        org_sector = st.selectbox("القطاع", ["حكومي", "خاص"], key="org_sec")
        org_size = st.selectbox("حجم المنظمة", ["١٠٠ فأقل", "١٠٠ إلى ٣٥٠", "أكثر من ٣٥٠"], key="org_sz")
        org_age = st.selectbox("عمر المنظمة", ["أقل من خمس سنوات", "٥-١٥", "أكثر من ١٥"], key="org_ag")
    with col2:
        org_change = st.selectbox("تقبل الموظفين للتغيير", ["بإيجابية", "أحياناً صعب", "صعب دائماً"], key="org_ch")
        org_autonomy = st.selectbox("استقلالية اتخاذ القرار", ["مستقلة بالكامل", "مستقلة جزئياً", "غير مستقلة"], key="org_aut")
    
    if st.button("حفظ بيانات المنظمة"):
        st.success("تم تثبيت بيانات المنظمة بنجاح ✅")

# --- القسم الثاني: بروفايل القائد (تعبئة عند التسجيل) ---
with tab2:
    st.subheader("بيانات القائد الشخصية")
    col3, col4 = st.columns(2)
    with col3:
        lead_style = st.selectbox("الأسلوب القيادي", ["توجيهي", "تشاركي", "تفويضي"], key="l_style")
        lead_reports = st.selectbox("عدد الموظفين تحت الإشراف المباشر", ["٥ فأقل", "٥-١٥", "١٥ فأكثر"], key="l_rep")
    with col4:
        lead_trust = st.selectbox("مستوى الثقة مع الفريق", ["عالي", "متوسط", "منخفض"], key="l_trust")
        lead_tenure = st.selectbox("غالبية موظفيك", ["جدد (أقل من ٣ سنوات)", "متوسط", "قدامى (أكثر من ٧ سنوات)"], key="l_ten")

    if st.button("حفظ بروفايل القائد"):
        st.success("تم تسجيل بروفايل القائد بنجاح ✅")

# --- القسم الثالث: منطقة القرار (التفاعل اليومي) ---
with tab3:
    st.subheader("تحليل القرار الحالي")
    decision_text = st.text_area("اشرح قرارك هنا بكلامك العادي...", height=150)
    
    if decision_text:
        st.divider()
        st.markdown("#### أسئلة إضافية حول هذا القرار:")
        c1, c2 = st.columns(2)
        with c1:
            dec_flex = st.selectbox("قابلية القرار للتعديل", ["قابل للتعديل", "قابل جزئياً", "غير قابل"])
            dec_time = st.selectbox("متى يبدأ التنفيذ؟", ["فوري", "خلال أشهر", "تدريجي"])
        with c2:
            dec_vis = st.selectbox("مدى معرفة الموظفين بالقرار", ["سري تماماً", "يوجد تسريبات", "معلن رسمياً"])
            dec_target = st.text_input("ماهي فئة الموظفين المتأثرين؟")
        
        dec_impact = st.select_slider("ما مدى تأثر هذه الفئة؟", options=["بسيط", "متوسط", "جوهري"])

        if st.button("بدء التحليل الذكي"):
            if not client: st.warning("يرجى إدخال API Key من القائمة الجانبية")
            else: st.info("جاري معالجة القرار بناءً على كافة البروفايلات المسجلة...")