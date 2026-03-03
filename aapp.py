import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة (معالم GitHub و Fork باقية)
st.set_page_config(page_title="BDS System", layout="wide")

# 2. تهيئة مخزن البيانات لنظام الدخول واللغة
if 'user_type' not in st.session_state: 
    st.session_state.user_type = None
if 'lang' not in st.session_state:
    st.session_state.lang = 'Arabic'

# 3. إعدادات القائمة الجانبية
with st.sidebar:
    st.session_state.lang = st.radio("Language / اللغة", ["Arabic", "English"])
    if st.session_state.user_type is not None:
        st.divider()
        if st.button("تسجيل الخروج" if st.session_state.lang == "Arabic" else "Logout"):
            st.session_state.user_type = None
            st.rerun()
    st.divider()
    api_key = st.text_input("OpenAI Key", type="password")
    client = OpenAI(api_key=api_key) if api_key else None

# نصوص الواجهة (تم حذف كلمة بروفايل)
t = {
    "Arabic": {
        "title": "🛡️ نظام دعم القرار (BDS)",
        "login_h": "يرجى اختيار نوع الدخول",
        "admin_btn": "🏛️ إدارة المنظمة",
        "leader_btn": "👤 دخول القائد",
        "org_h": "🏛️ بيانات المنظمة (خاص بالإدارة)",
        "lead_h": "👤 بيانات القائد",
        "dec_h": "📝 تحليل القرار الحالي",
        "analyze": "تحليل القرار الآن",
        "save": "حفظ البيانات",
        "desc_label": "اشرح القرار الذي تود اتخاذه بكلامك العادي..."
    },
    "English": {
        "title": "🛡️ Decision Support System (BDS)",
        "login_h": "Please select login type",
        "admin_btn": "🏛️ Organization Management",
        "leader_btn": "👤 Leader Access",
        "org_h": "🏛️ Organization Data (Admin Only)",
        "lead_h": "👤 Leader Data",
        "dec_h": "📝 Current Decision Analysis",
        "analyze": "Analyze Now",
        "save": "Save Data",
        "desc_label": "Describe the decision you want to take in your own words..."
    }
}[st.session_state.lang]

# 4. منطق تسجيل الدخول
if st.session_state.user_type is None:
    st.title(t["title"])
    st.subheader(t["login_h"])
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button(t["admin_btn"]):
            st.session_state.user_type = "admin"
            st.rerun()
    with col_b:
        if st.button(t["leader_btn"]):
            st.session_state.user_type = "leader"
            st.rerun()
else:
    # --- واجهة إدارة المنظمة ---
    if st.session_state.user_type == "admin":
        st.title(t["org_h"])
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("القطاع", ["حكومي", "خاص"], key="org_sec")
            st.selectbox("حجم المنظمة", ["١٠٠ فأقل", "١٠٠ إلى ٣٥٠", "أكثر من ٣٥٠"], key="org_sz")
            st.selectbox("عمر المنظمة", ["أقل من خمس سنوات", "٥-١٥", "أكثر من ١٥"], key="org_ag")
        with col2:
            st.selectbox("تقبل الموظفين للتغيير عادة", ["بإيجابية", "أحياناً صعب", "صعب دائماً"], key="org_ch")
            st.selectbox("مدى استقلالية المنظمة في اتخاذ القرارات", ["مستقلة بالكامل", "مستقلة جزئياً", "غير مستقلة"], key="org_aut")
        
        if st.button(t["save"]):
            st.success("✅ تم حفظ بيانات المنظمة")

    # --- واجهة القائد ---
    elif st.session_state.user_type == "leader":
        st.title(t["title"])
        
        # بيانات القائد (بدون كلمة بروفايل)
        with st.expander(t["lead_h"], expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.selectbox("الأسلوب القيادي", ["توجيهي", "تشاركي", "تفويضي"], key="l_style")
                st.selectbox("عدد الموظفين تحت الإشراف المباشر", ["٥ فأقل", "٥-١٥", "١٥ فأكثر"], key="l_reports")
            with c2:
                st.selectbox("مستوى الثقة بينك وبين الفريق", ["عالي", "متوسط", "منخفض"], key="l_trust")
                st.selectbox("غالبية موظفيك", ["جدد (أقل من ٣ سنوات)", "متوسط", "قدامى (أكثر من ٧ سنوات)"], key="l_tenure")

        st.divider()
        
        # منطقة القرار
        st.subheader(t["dec_h"])
        decision_input = st.text_area(t["desc_label"], height=120)
        
        if decision_input:
            st.markdown("---")
            c3, c4 = st.columns(2)
            with c3:
                st.selectbox("قابلية القرار للتعديل", ["قابل للتعديل", "قابل جزئياً للتعديل", "غير قابل للتعديل"], key="d_flex")
                st.selectbox("متى يبدأ التنفيذ؟", ["فوري", "خلال أشهر", "تدريجي"], key="d_time")
            with c4:
                st.selectbox("مدى معرفة الموظفين بالقرار", ["سري تماماً", "يوجد تسريبات", "معلن رسمياً"], key="d_vis")
                st.text_input("ماهي فئة الموظفين المتأثرين بالقرار ؟", key="d_target")
            
            st.select_slider("ما مدى تأثر كل فئة ؟", options=["بسيط", "متوسط", "جوهري"], key="d_impact")

            if st.button(t["analyze"]):
                if not client: st.warning("Please enter API Key")
                else: st.info("جاري التحليل بناءً على البيانات المدخلة...")