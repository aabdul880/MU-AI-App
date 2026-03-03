import streamlit as st
from openai import OpenAI

# إعدادات الصفحة
st.set_page_config(page_title="BDS - Decision Support", layout="wide")

# --- إعدادات اللغة ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'Arabic'

lang = st.sidebar.selectbox("Choose Language / اختر اللغة", ["Arabic", "English"])
st.session_state.lang = lang

# قاموس النصوص
texts = {
    "Arabic": {
        "title": "🛡️ أداة تحليل القرارات الإدارية (BDS)",
        "api_key": "أدخل مفتاح OpenAI API",
        "org_profile": "🏛️ بروفايل المنظمة (إدارة المنظمة)",
        "lead_profile": "👤 بروفايل القائد",
        "sector": "القطاع",
        "size": "حجم المنظمة",
        "age": "عمر المنظمة",
        "change_accept": "تقبل الموظفين للتغيير",
        "autonomy": "استقلالية القرار",
        "lead_style": "الأسلوب القيادي",
        "supervision": "عدد الموظفين تحت الإشراف",
        "trust": "مستوى الثقة",
        "tenure": "غالبية الموظفين",
        "decision_details": "📝 تفاصيل القرار الحالي",
        "decision_placeholder": "اشرح القرار الذي تود اتخاذه بكلامك العادي...",
        "flexibility": "قابلية القرار للتعديل",
        "timing": "متى يبدأ التنفيذ؟",
        "visibility": "مدى معرفة الموظفين بالقرار",
        "impacted_group": "فئة الموظفين المتأثرين",
        "impact_level": "مدى تأثر الفئة",
        "analyze_btn": "تحليل القرار بناءً على البيانات",
        "error_api": "يرجى إدخال مفتاح API أولاً.",
        "success_msg": "✅ التحليل الأكاديمي المخصص:",
        "options": {
            "sector": ["حكومي", "خاص"],
            "size": ["١٠٠ فأقل", "١٠٠ إلى ٣٥٠", "أكثر من ٣٥٠"],
            "age": ["أقل من ٥ سنوات", "٥-١٥ سنة", "أكثر من ١٥ سنة"],
            "change": ["بإيجابية", "أحياناً صعب", "صعب دائماً"],
            "autonomy": ["مستقلة بالكامل", "مستقلة جزئياً", "غير مستقلة"],
            "style": ["توجيهي", "تشاركي", "تفويضي"],
            "lead_span": ["٥ فأقل", "٥-١٥", "١٥ فأكثر"],
            "trust": ["عالي", "متوسط", "منخفض"],
            "tenure": ["جدد (أقل من ٣ سنوات)", "متوسط", "قدامى (أكثر من ٧ سنوات)"],
            "flex": ["قابل للتعديل", "قابل جزئياً", "غير قابل"],
            "timing": ["فوري", "خلال أشهر", "تدريجي"],
            "visibility": ["سري تماماً", "يوجد تسريبات", "معلن رسمياً"],
            "impact": ["بسيط", "متوسط", "جوهري"]
        }
    },
    "English": {
        "title": "🛡️ Decision Support System (BDS)",
        "api_key": "Enter OpenAI API Key",
        "org_profile": "🏛️ Organization Profile (Management)",
        "lead_profile": "👤 Leader Profile",
        "sector": "Sector",
        "size": "Organization Size",
        "age": "Organization Age",
        "change_accept": "Employee Change Acceptance",
        "autonomy": "Decision Autonomy",
        "lead_style": "Leadership Style",
        "supervision": "Number of Direct Reports",
        "trust": "Trust Level with Team",
        "tenure": "Majority of Staff Tenure",
        "decision_details": "📝 Current Decision Details",
        "decision_placeholder": "Describe the decision you want to take in your own words...",
        "flexibility": "Decision Flexibility",
        "timing": "Execution Timing",
        "visibility": "Staff Awareness Level",
        "impacted_group": "Impacted Employee Group",
        "impact_level": "Impact Intensity",
        "analyze_btn": "Analyze Decision Based on Data",
        "error_api": "Please enter the API key first.",
        "success_msg": "✅ Personalized Academic Analysis:",
        "options": {
            "sector": ["Government", "Private"],
            "size": ["100 or less", "100 to 350", "More than 350"],
            "age": ["Less than 5 years", "5-15 years", "More than 15 years"],
            "change": ["Positively", "Sometimes difficult", "Always difficult"],
            "autonomy": ["Fully independent", "Partially independent", "Not independent"],
            "style": ["Directive", "Participative", "Delegative"],
            "lead_span": ["5 or less", "5-15", "15 or more"],
            "trust": ["High", "Medium", "Low"],
            "tenure": ["New (less than 3 years)", "Intermediate", "Seniors (7+ years)"],
            "flex": ["Adjustable", "Partially Adjustable", "Non-adjustable"],
            "timing": ["Immediate", "Within months", "Gradual"],
            "visibility": ["Top Secret", "Leaked", "Officially Announced"],
            "impact": ["Low", "Medium", "High"]
        }
    }
}

t = texts[st.session_state.lang]

# إدخال مفتاح API
api_key = st.sidebar.text_input(t["api_key"], type="password")
client = OpenAI(api_key=api_key) if api_key else None

st.title(t["title"])

# --- 1. بروفايل المنظمة ---
with st.expander(t["org_profile"]):
    col1, col2 = st.columns(2)
    with col1:
        org_sector = st.selectbox(t["sector"], t["options"]["sector"])
        org_size = st.selectbox(t["size"], t["options"]["size"])
        org_age = st.selectbox(t["age"], t["options"]["age"])
    with col2:
        org_change = st.selectbox(t["change_accept"], t["options"]["change"])
        org_autonomy = st.selectbox(t["autonomy"], t["options"]["autonomy"])

# --- 2. بروفايل القائد ---
with st.expander(t["lead_profile"]):
    col3, col4 = st.columns(2)
    with col3:
        lead_style = st.selectbox(t["lead_style"], t["options"]["style"])
        lead_span = st.selectbox(t["supervision"], t["options"]["lead_span"])
    with col4:
        lead_trust = st.selectbox(t["trust"], t["options"]["trust"])
        lead_staff_tenure = st.selectbox(t["tenure"], t["options"]["tenure"])

st.divider()

# --- 3. إدخال القرار ---
st.subheader(t["decision_details"])
decision_text = st.text_area(t["decision_placeholder"])

if decision_text:
    col5, col6 = st.columns(2)
    with col5:
        dec_flex = st.selectbox(t["flexibility"], t["options"]["flex"])
        dec_timing = st.selectbox(t["timing"], t["options"]["timing"])
    with col6:
        dec_visibility = st.selectbox(t["visibility"], t["options"]["visibility"])
        target_group = st.text_input(t["impacted_group"])
    
    impact_level = st.select_slider(t["impact_level"], options=t["options"]["impact"])

    if st.button(t["analyze_btn"]):
        if not client:
            st.error(t["error_api"])
        else:
            with st.spinner("Analyzing..."):
                system_msg = f"Analyze this decision for a {st.session_state.lang} speaking leader. Context: Sector {org_sector}, Style {lead_style}, Trust {lead_trust}, Impact {impact_level}."
                
                # ملاحظة: الذكاء الاصطناعي سيرد بنفس لغة الواجهة المختارة
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": f"Decision: {decision_text}. Please provide the analysis in {st.session_state.lang}."}
                    ]
                )
                
                st.success(t["success_msg"])
                st.write(response.choices[0].message.content)