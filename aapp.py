import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة (بدون أكواد إخفاء CSS)
st.set_page_config(page_title="BDS System", layout="wide")

# 2. تهيئة مخزن البيانات لنظام الدخول
if 'user_type' not in st.session_state: 
    st.session_state.user_type = None

# 3. واجهة تسجيل الدخول
if st.session_state.user_type is None:
    st.title("🛡️ نظام دعم القرار (BDS)")
    st.subheader("يرجى اختيار نوع الدخول")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🏛️ دخول إدارة المنظمة"):
            st.session_state.user_type = "admin"
            st.rerun()
    with col_b:
        if st.button("👤 دخول القائد"):
            st.session_state.user_type = "leader"
            st.rerun()
else:
    # زر خروج للعودة للقائمة الرئيسية يظهر في الجانب
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.user_type = None
        st.rerun()

    # القائمة الجانبية لإعدادات الـ API
    with st.sidebar:
        st.divider()
        api_key = st.text_input("OpenAI Key", type="password")
        client = OpenAI(api_key=api_key) if api_key else None

    # --- واجهة إدارة المنظمة (تظهر فقط عند دخول المنظمة) ---
    if st.session_state.user_type == "admin":
        st.title("🏛️ إعدادات المنظمة (خاص بالإدارة)")
        st.info("البيانات هنا تعبأ لمرة واحدة من قبل الإدارة.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("القطاع", ["حكومي", "خاص"], key="org_sector")
            st.selectbox("حجم المنظمة", ["١٠٠ فأقل", "١٠٠ إلى ٣٥٠", "أكثر من ٣٥٠"], key="org_size")
            st.selectbox("عمر المنظمة", ["أقل من خمس سنوات", "٥-١٥", "أكثر من ١٥"], key="org_age")
        with col2:
            st.selectbox("تقبل الموظفين للتغيير", ["بإيجابية", "أحياناً صعب", "صعب دائماً"], key="org_change")
            st.selectbox("استقلالية اتخاذ القرار", ["مستقلة بالكامل", "مستقلة جزئياً", "غير مستقلة"], key="org_autonomy")
        
        if st.button("حفظ بيانات المنظمة"):
            st.success("تم الحفظ بنجاح ✅")

    # --- واجهة القائد (تظهر فقط عند دخول القائد) ---
    elif st.session_state.user_type == "leader":
        st.title("👤 لوحة تحكم القائد")
        
        # بروفايل القائد (خاص بالقائد فقط)
        with st.expander("👤 بروفايل القائد (تعبأ عند التسجيل)", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.selectbox("الأسلوب القيادي", ["توجيهي", "تشاركي", "تفويضي"], key="l_style")
                st.selectbox("عدد الموظفين تحت الإشراف", ["٥ فأقل", "٥-١٥", "١٥ فأكثر"], key="l_reports")
            with c2:
                st.selectbox("مستوى الثقة مع الفريق", ["عالي", "متوسط", "منخفض"], key="l_trust")
                st.selectbox("غالبية موظفيك", ["جدد (أقل من ٣ سنوات)", "متوسط", "قدامى (أكثر من ٧ سنوات)"], key="l_tenure")

        st.divider()
        
        # منطقة القرار
        st.subheader("📝 اتخاذ قرار جديد")
        decision_input = st.text_area("اشرح قرارك هنا بكلامك العادي...", height=100)
        
        if decision_input:
            st.markdown("##### تفاصيل القرار:")
            c3, c4 = st.columns(2)
            with c3:
                st.selectbox("قابلية القرار للتعديل", ["قابل للتعديل", "قابل جزئياً", "غير قابل"], key="d_flex")
                st.selectbox("متى يبدأ التنفيذ؟", ["فوري", "خلال أشهر", "تدريجي"], key="d_time")
            with c4:
                st.selectbox("مدى معرفة الموظفين", ["سري تماماً", "يوجد تسريبات", "معلن رسمياً"], key="d_vis")
                st.text_input("فئة الموظفين المتأثرين بالقرار ؟", key="d_target")
            
            st.select_slider("ما مدى تأثر كل فئة ؟", options=["بسيط", "متوسط", "جوهري"], key="d_impact")

            if st.button("تحليل القرار"):
                if not client: st.warning("يرجى إدخال API Key")
                else: st.info("يتم التحليل الآن...")