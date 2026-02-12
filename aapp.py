import streamlit as st
from openai import OpenAI

# إعدادات الصفحة والاسم الجديد
st.set_page_config(page_title="Behavioral Decision Simulator (BDS)", layout="wide")

# العنوان الرئيسي
st.title("🧠 Behavioral Decision Simulator (BDS)")
st.markdown("##### منصة تحليل القرارات الإدارية بناءً على المتغيرات السلوكية")
st.write("---")

# القائمة الجانبية (بيانات ثابتة + الإعدادات)
with st.sidebar:
    st.header("🔐 إعدادات النظام")
    user_key = st.text_input("أدخل مفتاح OpenAI API:", type="password")
    
    st.write("---")
    st.header("🏢 بيانات المنظمة الثابتة")
    org_name = st.text_input("اسم المنظمة (اختياري):", placeholder="مثلاً: وزارة... / شركة...")
    org_type = st.selectbox("نوع القطاع:", ["حكومي", "خاص", "غير ربحي"])
    org_size = st.selectbox("حجم القوى العاملة:", ["صغير (أقل من 50)", "متوسط (50-500)", "كبير (أكثر من 500)"])
    org_culture = st.selectbox("نوع الثقافة التنظيمية:", ["رسمية/هرمية", "مرنة/تشاركية", "تركز على الإنجاز"])
    
    st.info("هذه البيانات تُستخدم لضبط دقة التحليل السلوكي.")

# منطقة المدخلات للقرار المراد تحليله
st.markdown("#### 📝 تفاصيل القرار التنظيمي")
decision_title = st.text_input("عنوان القرار:", placeholder="مثلاً: تطبيق العمل عن بُعد")
decision_desc = st.text_area("وصف القرار الإداري وسياقه:", height=150)

# زر التحليل
if st.button("بدء محاكاة الأثر السلوكي"):
    if not user_key:
        st.error("⚠️ يرجى تزويد النظام بمفتاح الـ API من القائمة الجانبية.")
    elif not decision_desc:
        st.warning("⚠️ يرجى وصف القرار المراد تحليله.")
    else:
        try:
            client = OpenAI(api_key=user_key)
            with st.spinner('جاري تشغيل محاكاة BDS...'):
                prompt = f"""
                تحليل قرار لـ {org_name} (قطاع {org_type}، حجم {org_size}، ثقافة {org_culture}).
                القرار: {decision_title} - {decision_desc}
                
                المطلوب: تحليل سلوكي معمق يشمل:
                1. الأثر على الرضا الوظيفي والولاء.
                2. توقعات مقاومة التغيير وطرق علاجها.
                3. تحليل العدالة التنظيمية المتوقعة للقرار.
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "أنت خبير في السلوك التنظيمي (BDS Specialist)."},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.success("✅ اكتملت عملية المحاكاة بنجاح")
                st.markdown("### 🔍 نتائج تحليل BDS:")
                st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"❌ حدث خطأ في الاتصال: {e}")

st.write("---")
st.caption("Behavioral Decision Simulator (BDS) - Master's Research Project")
