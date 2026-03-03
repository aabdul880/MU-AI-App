import streamlit as st
from openai import OpenAI

# إعدادات الصفحة وإخفاء معالم التطبيق لضمان الخصوصية
st.set_page_config(page_title="BDS - Decision Support", layout="wide")

# كود احترافي لإخفاء الهوية (حساب GitHub، القوائم، والتذييل)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stAppDeployButton {display:none;}
            [data-testid="stHeader"] {display:none;}
            [data-testid="stToolbar"] {display:none;}
            [data-testid="stDecoration"] {display:none;}
            [data-testid="stStatusWidget"] {display:none;}
            #viewerBadge_container__1QS1n {display:none;}
            .st-emotion-cache-zq5wmm {display:none;}
            .st-emotion-cache-15zrgzn {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- إعدادات اللغة ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'Arabic'

# شريط جانبي بسيط لإعدادات اللغة والـ API
with st.sidebar:
    lang = st.selectbox("Choose Language / اختر اللغة", ["Arabic", "English"])
    st.session_state.lang = lang
    
    # القاموس داخل السايدبار ليبقى المنظر الرئيسي نظيفاً
    texts = {
        "Arabic": {
            "title": "🛡️ أداة تحليل القرارات الإدارية (BDS)",
            "api_key": "أدخل مفتاح OpenAI API",
            "org_profile": "🏛️ بروفايل المنظمة (إدارة المنظمة)",
            "lead_profile": "👤 بروفايل القائد",
            "decision_details": "📝 تفاصيل القرار الحالي",
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
            "org_profile": "🏛️ Organization Profile",
            "lead_profile": "👤 Leader Profile",
            "decision_details": "📝 Current Decision Details",
            "analyze_btn": "Analyze Decision",
            "error_api": "Please enter the API key.",
            "success_msg": "✅ Analysis:",
            "options": {
                "sector": ["Government", "Private"],
                "size": ["100 or less", "100 to 350", "More than 350"],
                "age": ["< 5 years", "5-15 years", "> 15 years"],
                "change": ["Positively", "Sometimes difficult", "Always difficult"],
                "autonomy": ["Full", "Partial", "None"],
                "style": ["Directive", "Participative", "Delegative"],
                "lead_span": ["< 5", "5-15", "> 15"],
                "trust": ["High", "Medium", "Low"],
                "tenure": ["New", "Intermediate", "Senior"],
                "flex": ["Adjustable", "Partial", "Non-adjustable"],
                "timing": ["Immediate", "Months", "Gradual"],
                "visibility": ["Secret", "Leaked", "Announced"],
                "impact": ["Low", "Medium", "High"]
            }
        }
    }
    t = texts[st.session_state.lang]
    api_key = st.text_input(t["api_key"], type="password")
    client = OpenAI(api_key=api_key) if api_key else None

# --- الواجهة الرئيسية ---
st.title(t["title"])

with st.expander(t["org_profile"]):
    col1, col2 = st.columns(2)
    with col1:
        org_sector = st.selectbox("القطاع" if st.session_state.lang == "Arabic" else "Sector", t["options"]["sector"])
        org_size = st.selectbox("الحجم" if st.session_state.lang == "Arabic" else "Size", t["options"]["size"])
    with col2:
        org_change = st.selectbox("تقبل التغيير" if st.session_state.lang == "Arabic" else "Change", t["options"]["change"])
        org_autonomy = st.selectbox("الاستقلالية" if st.session_state.lang == "Arabic" else "Autonomy", t["options"]["autonomy"])

with st.expander(t["lead_profile"]):
    col3, col4 = st.columns(2)
    with col3:
        lead_style = st.selectbox("الأسلوب" if st.session_state.lang == "Arabic" else "Style", t["options"]["style"])
    with col4:
        lead_trust = st.selectbox("الثقة" if st.session_state.lang == "Arabic" else "Trust", t["options"]["trust"])

st.divider()

st.subheader(t["decision_details"])
decision_text = st.text_area("..." if st.session_state.lang == "Arabic" else "Describe decision...")

if st.button(t["analyze_btn"]):
    if not client:
        st.error(t["error_api"])
    else:
        with st.spinner("Analyzing..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": f"Analyze as expert for {st.session_state.lang}."},
                          {"role": "user", "content": decision_text}]
            )
            st.success(t["success_msg"])
            st.write(response.choices[0].message.content)