import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة
st.set_page_config(page_title="BDS System", layout="wide")

# 2. تهيئة الذاكرة
if 'org_done' not in st.session_state: st.session_state.org_done = False
if 'lead_done' not in st.session_state: st.session_state.lead_done = False

# 3. القائمة الجانبية
with st.sidebar:
    lang = st.radio("اللغة / Language", ["Arabic", "English"])
    st.divider()
    api_key = st.text_input("OpenAI Key", type="password")
    client = OpenAI(api_key=api_key) if api_key else None

t = {
    "Arabic": {
        "title": "🛡️ أداة تحليل القرارات الإدارية (BDS)",
        "org_h": "🏛️ بيانات المنظمة",
        "lead_h": "👤 بيانات القائد",
        "save": "حفظ البيانات",
        "edit": "تعديل",
        "done": "تم الحفظ بنجاح ✅",
        "dec_h": "📝 تفاصيل القرار الحالي",
        "analyze": "تحليل القرار الآن",
        "result_h": "📊 نتيجة التحليل الأكاديمي"
    },
    "English": {
        "title": "🛡️ Decision Support System (BDS)",
        "org_h": "🏛️ Organization Data",
        "lead_h": "👤 Leader Data",
        "save": "Save Data",
        "edit": "Edit",
        "done": "Saved Successfully ✅",
        "dec_h": "📝 Current Decision Details",
        "analyze": "Analyze Now",
        "result_h": "📊 Academic Analysis Result"
    }
}[lang]

st.title(t["title"])

# --- المرحلة 1: بيانات المنظمة ---
with st.expander(t["org_h"], expanded=not st.session_state.org_done):
    if st.session_state.org_done:
        st.success(t["done"])
        if st.button(t["edit"], key="edit_org"):
            st.session_state.org_done = False
            st.rerun()
    else:
        col1, col2 = st.columns(2)
        with col1:
            sec = st.selectbox("القطاع", ["حكومي", "خاص"])
            sz = st.selectbox("حجم المنظمة", ["١٠٠ فأقل", "١٠٠ إلى ٣٥٠", "أكثر من ٣٥٠"])
            ag = st.selectbox("عمر المنظمة", ["أقل من خمس سنوات", "٥-١٥", "أكثر من ١٥"])
        with col2:
            ch = st.selectbox("تقبل الموظفين للتغيير عادة", ["بإيجابية", "أحياناً صعب", "صعب دائماً"])
            aut = st.selectbox("استقلالية اتخاذ القرار", ["مستقلة بالكامل", "مستقلة جزئياً", "غير مستقلة"])
        if st.button(t["save"], key="btn_org"):
            st.session_state.org_saved_data = f"Sector: {sec}, Size: {sz}, Age: {ag}, Change: {ch}, Autonomy: {aut}"
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
            sty = st.selectbox("الأسلوب القيادي", ["توجيهي", "تشاركي", "تفويضي"])
            rep = st.selectbox("عدد الموظفين تحت الإشراف المباشر", ["٥ فأقل", "٥-١٥", "١٥ فأكثر"])
        with col4:
            tru = st.selectbox("مستوى الثقة بينك وبين الفريق", ["عالي", "متوسط", "منخفض"])
            ten = st.selectbox("غالبية موظفيك", ["جدد (أقل من ٣ سنوات)", "متوسط", "قدامى (أكثر من ٧ سنوات)"])
        if st.button(t["save"], key="btn_lead"):
            st.session_state.lead_saved_data = f"Style: {sty}, Reports: {rep}, Trust: {tru}, Tenure: {ten}"
            st.session_state.lead_done = True
            st.rerun()

st.divider()

# --- المرحلة 3: القرار والتحليل ---
st.subheader(t["dec_h"])
decision_text = st.text_area("اشرح قرارك هنا بكلامك العادي...", height=100)

if decision_text:
    c1, c2 = st.columns(2)
    with c1:
        d_flx = st.selectbox("قابلية القرار للتعديل", ["قابل للتعديل", "قابل جزئياً", "غير قابل"])
        d_tim = st.selectbox("متى يبدأ التنفيذ؟", ["فوري", "خلال أشهر", "تدريجي"])
    with c2:
        d_vis = st.selectbox("مدى معرفة الموظفين بالقرار", ["سري تماماً", "يوجد تسريبات", "معلن رسمياً"])
        d_tar = st.text_input("ماهي فئة الموظفين المتأثرين بالقرار؟")
    
    d_imp = st.select_slider("ما مدى تأثر هذه الفئة؟", options=["بسيط", "متوسط", "جوهري"])

    if st.button(t["analyze"]):
        if not client:
            st.error("يرجى إدخال API Key من القائمة الجانبية")
        else:
            with st.spinner("جاري التحليل العلمي..."):
                # تجميع كل البيانات للذكاء الاصطناعي
                full_context = f"""
                Organization: {st.session_state.get('org_saved_data', 'N/A')}
                Leader: {st.session_state.get('lead_saved_data', 'N/A')}
                Decision: {decision_text}
                Details: Flexibility {d_flx}, Timing {d_tim}, Visibility {d_vis}, Impact {d_imp} on {d_target if 'd_target' in locals() else 'staff'}.
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": f"You are a professional management consultant. Provide a detailed academic analysis in {lang}."},
                        {"role": "user", "content": full_context}
                    ]
                )
                
                # إظهار صفحة النتائج
                st.divider()
                st.subheader(t["result_h"])
                st.write(response.choices[0].message.content)