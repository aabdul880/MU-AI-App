# ابحث عن جزء التحليل في كودك واستبدله بهذا الجزء الذكي:

if st.button(t["analyze"]):
    if not client: 
        st.warning("يرجى إدخال مفتاح API")
    else:
        # 1. إضافة دائرة الانتظار الاحترافية
        with st.spinner("🧠 جاري الربط بين بيانات المنظمة ونظريات القيادة... انتظر قليلاً"):
            try:
                # 2. استخدام موديل mini للسرعة الهائلة
                response = client.chat.completions.create(
                    model="gpt-4o-mini", 
                    messages=[
                        {"role": "system", "content": f"أنت خبير إداري تحلل القرارات بناءً على سياق المنظمة {st.session_state.org_sec} وأسلوب القائد."},
                        {"role": "user", "content": f"حلل هذا القرار: {decision_input}"}
                    ]
                )
                
                # 3. إظهار النتيجة بشكل أنيق
                st.success("✅ تم الانتهاء من التحليل")
                st.markdown("---")
                st.write(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"حدث خطأ: {e}")