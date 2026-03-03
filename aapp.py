import streamlit as st
from openai import OpenAI

# إعدادات الصفحة
st.set_page_config(page_title="BDS - Decision Support", layout="wide")

# كود CSS المطور لإخفاء الهوية تماماً (العلوية والسفلية)
# قمت هنا باستهداف العناصر التي تظهر فيها كلمة Streamlit وحساب GitHub بدقة
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="stHeader"] {display: none;}
            [data-testid="stToolbar"] {display: none;}
            .stAppDeployButton {display: none;}
            #viewerBadge_container__1QS1n {display: none;}
            /* إخفاء شريط Streamlit السفلي تماماً */
            footer {display: none !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- إعدادات اللغة (نقلناها للواجهة الرئيسية لتسهيل الوصول) ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'Arabic'

# قاموس النصوص
texts = {
    "Arabic": {
        "title": "🛡️ أداة تحليل القرارات الإدارية (BDS)",
        "api_key_label": "إعدادات المطور (مفتاح API)",
        "choose_lang": "اختر اللغة",
        "org_profile": "🏛️ بروفايل المنظمة (إدارة المنظمة)",
        "lead_profile": "👤 بروفايل القائد",
        "decision_details": "📝 تفاصيل القرار الحالي",
        "analyze_btn": "تحليل القرار بناءً على البيانات",
        "options": {
            "sector": ["حكومي", "خاص"], "size": ["١٠٠ فأقل", "١٠٠ إلى ٣٥٠", "أكثر من ٣٥٠"],
            "change": ["بإيجابية", "أحياناً صعب", "صعب دائماً"], "autonomy": ["مستقلة بالكامل", "مستقلة جزئياً", "غير مستقلة"],
            "style": ["توجيهي", "تشاركي", "تفويضي"], "trust": ["عالي", "متوسط", "منخفض"],
            "impact": ["بسيط", "متوسط", "جوهري"]
        }
    },
    "English": {
        "title": "🛡️ Decision Support System (BDS)",
        "api_key_label": "Developer Settings (API Key)",
        "choose_lang": "Choose Language",
        "org_profile": "🏛️ Organization Profile",
        "lead_profile": "👤 Leader Profile",
        "decision_details": "📝 Current Decision Details",
        "analyze_btn": "Analyze Decision",
        "options": {
            "sector": ["Government", "Private"], "size": ["< 100", "100-350", "> 350"],
            "change": ["Positive", "Sometimes", "Always difficult"], "autonomy": ["Full", "Partial", "None"],
            "style": ["Directive", "Participative", "Delegative"], "trust": ["High", "Medium", "Low"],
            "impact": ["Low", "Medium", "High"]
        }
    }
}

# وضع اختيار اللغة في أعلى الصفحة بشكل أنيق بدلاً من القائمة الجانبية
col_l1, col_l2 = st.columns([8, 2])
with col_l2:
    selected_lang = st.selectbox("🌐", ["Arabic", "English"], index=0 if st.session_state.lang == "Arabic" else 1)
    st.session_state.lang = selected_lang

t = texts[st.session_state.lang]
st.title(t["title"])

# --- واجهة الإدخال ---
with st.expander(t["org_profile"]):
    c1, c2 = st.columns(2)
    with c1:
        org_sector = st.selectbox("القطاع" if st.session_state.lang == "Arabic" else "Sector", t["options"]["sector"])
    with c2:
        org_change = st.selectbox("تقبل التغيير" if st.session_state.lang == "Arabic" else "Change", t["options"]["change"])

with st.expander(t["lead_profile"]):
    c3, c4 = st.columns(2)
    with c3:
        lead_style = st.selectbox("الأسلوب" if st.session_state.lang == "Arabic" else "Style", t["options"]["style"])
    with c4:
        lead_trust = st.selectbox("الثقة" if st.session_state.lang == "Arabic" else "Trust", t["options"]["trust"])

st.divider()
st.subheader(t["decision_details"])
decision_text = st.text_area("..." if st.session_state.lang == "Arabic" else "Describe decision...")

# مفتاح الـ API مخفي في "طيّة" أسفل الصفحة
with st.expander(t["api_key_label"]):
    api_key = st.text_input("API Key", type="password")
    client = OpenAI(api_key=api_key) if api_key else None

if st.button(t["analyze_btn"]):
    if not client:
        st.error("Please enter API Key" if st.session_state.lang == "English" else "يرجى إدخال المفتاح")
    else:
        with st.spinner("Analyzing..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": f"Analyze as expert for {st.session_state.lang}."},
                          {"role": "user", "content": decision_text}]
            )
            st.success("Analysis Complete" if st.session_state.lang == "English" else "تم التحليل:")
            st.write(response.choices[0].message.content)