import streamlit as st
from openai import OpenAI

# إعدادات الواجهة
st.set_page_config(page_title="Behavioral Simulator - MU", layout="wide")
st.title("🧠 Behavioral Decision Simulator (MU)")
st.markdown("### منصة دعم القرار التنظيمي - بحث ماجستير")

# القائمة الجانبية
with st.sidebar:
    st.header("🔐 الإعدادات")
    user_key = st.text_input("أدخل مفتاح OpenAI API الخاص بك:", type="password")
    st.write("---")
    st.info("هذه الأداة مخصصة لأغراض البحث العلمي.")

# منطقة المدخلات
decision = st.text_area("صف القرار الإداري الذي ترغب في تحليله:", height=150)

if st.button("بدء التحليل السلوكي"):
    if not user_key:
        st.error("⚠️ يرجى إدخال مفتاح الـ API في القائمة الجانبية.")
    elif not decision:
        st.warning("⚠️ يرجى كتابة تفاصيل القرار أولاً.")
    else:
        try:
            client = OpenAI(api_key=user_key)
            with st.spinner('جاري تحليل الأثر السلوكي...'):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "أنت خبير في علم النفس التنظيمي والموارد البشرية. حلل القرار من منظور العدالة التنظيمية ومقاومة التغيير."},
                        {"role": "user", "content": f"حلل القرار التالي: {decision}"}
                    ]
                )
                st.success("✅ تم التحليل بنجاح!")
                st.markdown("---")
                st.markdown("#### 🔍 النتائج التحليلية:")
                st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"❌ حدث خطأ: تأكد من صحة المفتاح والرصيد. التفاصيل: {e}")

st.markdown("---")