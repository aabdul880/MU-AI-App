import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة الأساسية (GitHub و Fork ستظهر بشكل طبيعي)
st.set_page_config(page_title="BDS System", layout="wide")

# 2. تهيئة مخزن البيانات لنظام الدخول واللغة
if 'user_type' not in st.session_state: 
    st.session_state.user_type = None
if 'lang' not in st.session_state:
    st.session_state.lang = 'Arabic'

# 3. إعدادات القائمة الجانبية (اللغة و المفتاح)
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

# نصوص الواجهة بناءً على اللغة
t = {
    "Arabic": {
        "title": "🛡️ نظام دعم القرار (BDS)",
        "login_h": "يرجى اختيار نوع الدخول",
        "admin_btn": "🏛️ دخول إدارة المنظمة",
        "leader_btn": "👤 دخول القائد",
        "org_h": "🏛️ إعدادات المنظمة (خاص بالإدارة)",
        "dec_h": "📝 تحليل القرار الحالي",
        "analyze": "تحليل القرار الآن",
        "save": "حفظ البيانات"
    },
    "English": {
        "title": "🛡️ Decision Support System (BDS)",
        "login_h": "Please select login type",
        "admin_btn": "🏛️ Admin Login",
        "leader_btn": "👤 Leader Login",
        "org_h": "🏛️ Organization Settings (Admin Only)",
        "dec_h": "📝 Current Decision Analysis",
        "analyze": "Analyze Now",
        "save": "Save Data"
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
            st.selectbox("القطاع" if st.session_state.lang == "Arabic" else "Sector", ["حكومي", "خاص"], key="org_sec")
            st.selectbox("حجم المنظمة" if st.session_state.lang == "Arabic" else "Size", ["١٠٠ فأقل", "١٠٠ إلى ٣٥٠", "أكثر من ٣٥٠"], key="org_sz")
            st.selectbox("عمر المنظمة" if st.session_state.lang == "Arabic" else "Age", ["أقل من خمس سنوات", "٥-١٥", "أكثر من ١٥"], key="org_ag")
        with col2:
            st.selectbox("تقبل الموظفين للتغيير" if st.session_state.lang == "Arabic" else "Change", ["بإيجابية", "أحياناً صعب", "صعب دائماً"], key="org_ch")
            st.selectbox("استقلالية القرار" if st.session_state.lang == "Arabic" else "Autonomy", ["مستقلة بالكامل", "مستقلة جزئياً", "غير مستقلة"], key="org_aut")
        
        if st.button(t["save"]):
            st.success("✅")

    # --- واجهة القائد (مباشرة للقرار بدون بروفايل) ---
    elif st.session_state.user_type == "leader":
        st.title(t["title"])
        st.subheader(t["dec_h"])
        
        decision_input = st.text_area("اشرح قرارك هنا بكلامك العادي..." if st.session_state.lang == "Arabic" else "Describe your decision...", height=150)
        
        if decision_input:
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.selectbox("قابلية القرار للتعديل" if st.session_state.lang == "Arabic" else "Flexibility", ["قابل للتعديل", "قابل جزئياً", "غير قابل"], key="d_flex")
                st.selectbox("متى يبدأ التنفيذ؟" if st.session_state.lang == "Arabic" else "Timing", ["فوري", "خلال أشهر", "تدريجي"], key="d_time")
            with c2:
                st.selectbox("مدى معرفة الموظفين" if st.session_state.lang == "Arabic" else "Visibility", ["سري تماماً", "يوجد تسريبات", "معلن رسمياً"], key="d_vis")
                st.text_input("ماهي فئة الموظفين المتأثرين بالقرار ؟" if st.session_state.lang == "Arabic" else "Impacted Group", key="d_target")
            
            st.select_slider("ما مدى تأثر كل فئة ؟" if st.session_state.lang == "Arabic" else "Impact Level", options=["بسيط", "متوسط", "جوهري"], key="d_impact")

            if st.button(t["analyze"]):
                if not client: st.warning("Please enter API Key")
                else: st.info("Analyzing...")