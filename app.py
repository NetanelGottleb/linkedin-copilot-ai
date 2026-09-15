import streamlit as st
import os
import json
import urllib.request
import urllib.parse

# הגדרת תצורת הדף
st.set_page_config(
    page_title="LinkedIn AI Copilot | טייס משנה חכם ללינקדין",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# שליפת מפתח ה-API
api_key = st.secrets.get("GEMINI_API_KEY", "") if hasattr(st, "secrets") else ""
if not api_key:
    api_key = os.getenv("GEMINI_API_KEY", "")

# סרגל צד - הגדרות פרופיל אישי ומפתח
with st.sidebar:
    st.markdown("<h3 style='text-align: right;'>⚙️ הגדרות ופרופיל אישי</h3>", unsafe_allow_html=True)
    if not api_key:
        api_key_input = st.text_input("מפתח Gemini API (אם לא הוגדר ב-Secrets):", type="password")
        if api_key_input:
            api_key = api_key_input
            
    st.markdown("---")
    st.markdown("<h4 style='text-align: right;'>👤 רקע מקצועי (לבסיס ההתאמה):</h4>", unsafe_allow_html=True)
    user_background = st.text_area(
        "הגדר את הכישורים והרקע שלך (משמש להתאמת משרות ופניות אישיות):",
        value="סטודנט למדעי התזונה (B.Sc.) בפקולטה לחקלאות באוניברסיטה העברית ברחובות, עם שילוב אגרו-אינפורמטיקה (פייתון, מדעי הנתונים, ביואינפורמטיקה). רקע וניסיון בהדרכת כושר ופיזיולוגיה של המאמץ, עניין במחקר מטבולי, פוד-טק ובריאות דיגיטלית.",
        height=130
    )
    st.caption("🔒 כל הנתונים נשמרים בסשן הנוכחי בלבד. שום פעולה אינה מתבצעת ללא אישורך המפורש.")

# פונקציית תקשורת מול Gemini דרך REST מובנה
def call_gemini(prompt: str, system_prompt: str, key: str = api_key) -> str:
    if not key:
        return "⚠️ נא להגדיר מפתח GEMINI_API_KEY בסרגל הצד או ב-Secrets של Streamlit להפעלת ניתוח ה-AI."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}]
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"שגיאה בתקשורת עם המודל: {e}"

# כותרת ראשית
st.markdown(
    """
    <div style="text-align: right; direction: rtl;">
        <h2 style="color: #0A66C2; margin-bottom: 2px;">💼 LinkedIn AI Copilot | טייס משנה מבוסס AI</h2>
        <p style="color: #4B5563; font-size: 1.1em;">
            איתור אנשים רלוונטיים, תגובות ערך מקצועיות, כתיבת פוסטים ואיתור משרות – <b>עם אישור ובקרה מלאים לפני כל פעולה</b>.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# טאבים לפעולות המרכזיות
tab_find, tab_comment, tab_post, tab_jobs = st.tabs([
    "🎯 איתור אנשים וחיבורים ממוקדים",
    "💬 מגיב חכם בעל ערך",
    "✍️ כתיבת פוסטים מקצועיים",
    "💼 איתור משרות ופנייה למגייס"
])

# ==========================================
# טאב 1: איתור אנשים ובקשות חיבור מותאמות אישית
# ==========================================
with tab_find:
    st.markdown("<h4 style='text-align: right;'>🎯 איתור אנשי מפתח לפי תחום וכוונת חיבור</h4>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([2, 1])
    with c1:
        target_role = st.text_input(
            "איזה אנשים תרצה לאתר?",
            value="חוקרים בתזונת ספורט ומטבוליזם או מנהלי מו\"פ בפוד-טק",
            placeholder="למשל: מנהלי גיוס בביוטק, חוקרי אגרו-אינפורמטיקה, דיאטנים קליניים..."
        )
    with c2:
        target_geo = st.selectbox("מיקום גיאוגרפי:", ["ישראל (Israel)", "גלובלי (Global)", "ארה\"ב (USA)"])

    connection_goal = st.selectbox(
        "מה מטרת החיבור העיקרית?",
        [
            "מנטורינג ולמידה מחוקרים / מובילי תחום",
            "בדיקת הזדמנויות תעסוקה ומחקר (גיוס / מעבדות)",
            "קולגות ושיתופי פעולה מקצועיים",
            "הרחבת נטוורקינג ממוקד בתעשיית המזון/בריאות"
        ]
    )

    if st.button("🔍 בנה חיפוש X-Ray ממוקד והנחיות פנייה", use_container_width=True):
        geo_filter = "Israel" if "ישראל" in target_geo else ("United States" if "ארה" in target_geo else "")
        raw_query = f"site:linkedin.com/in/ ({target_role}) {geo_filter}".strip()
        google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(raw_query)}"
        
        st.markdown("---")
        st.markdown(f"#### 🔗 1. קישור ישיר לחיפוש פרופילים מדויקים בגוגל:")
        st.link_button(f"🔎 פתח חיפוש פרופילים ב-LinkedIn ({target_role})", google_search_url)
        st.caption(f"שאילתת ה-X-Ray שהופקה: `{raw_query}`")

        # הפקת קריטריוני סינון מבוססי AI
        sys_find = f"""
        אתה מומחה נטוורקינג בכיר בלינקדין.
        המשתמש מחפש להתחבר לאנשים הבאים: {target_role} במיקום {target_geo} למטרת: {connection_goal}.
        רקע המשתמש: {user_background}.
        
        עליך לספק בקצרה ובעברית:
        1. קריטריון סינון מהיר: איך המשתמש יידע תוך 5 שניות אם האדם רלוונטי (לפי כותרת, פעילות אחרונה).
        2. זווית פנייה אותנטית: מה הנושא המשותף שסביבו נכון לפתוח בשיחה בלי להישמע ספאמי או חודרני.
        3. תבנית פתק חיבור מותאמת (עד 280 תווים!) מוכנה לשימוש.
        """
        advice = call_gemini("תן לי המלצות סינון וזווית פנייה מדויקת", sys_find)
        st.markdown(advice)

    st.markdown("---")
    st.markdown("<h5 style='text-align: right;'>✉️ ניסוח פתק חיבור מותאם אישית לפרופיל ספציפי:</h5>", unsafe_allow_html=True)
    profile_text = st.text_area(
        "הדבק כאן את הכותרת (Headline) או פסקת ה-About של האדם שמצאת:",
        placeholder="למשל: Dr. Cohen | Principal Investigator in Metabolic Health & Nutrition Research at Tel Aviv University...",
        height=100
    )
    
    if st.button("✨ נסח פתק חיבור מותאם אישית (מוגבל ל-300 תווים)", use_container_width=True):
        if not profile_text.strip():
            st.warning("נא להדביק מידע מהפרופיל של האדם.")
        else:
            sys_note = f"""
            אתה מנסח פתקי חיבור (Connection Notes) בלינקדין.
            רקע המשתמש הפונה: {user_background}.
            מטרת הפנייה: {connection_goal}.
            פרופיל הנמען: {profile_text}.
            
            דרישות ברזל:
            1. אורך: מקסימום 290 תווים כולל רווחים (מגבלת לינקדין היא 300 תווים).
            2. שפה: עברית או אנגלית לפי שפת הפרופיל של הנמען.
            3. טון: מנומס, מכבד, ספציפי ומקצועי (ללא חנופה מוגזמת, ללא נוסחי תבנית שבלוניים).
            4. ציין נקודת חיבור אמיתית בין הרקע של המשתמש לפעילות הנמען.
            """
            draft_note = call_gemini(profile_text, sys_note)
            
            # תיבת אישור ועריכה לפני שליחה
            st.markdown("#### 🛡️ שער בדיקה ואישור (Review & Confirmation):")
            st.info("בדוק את הנוסח, ערוך במידת הצורך, ורק לאחר שאישרת העתק ללינקדין:")
            approved_note = st.text_area("נוסח הפתק לאישורך ועריכתך:", value=draft_note, height=100)
            st.caption(f"מספר תווים: {len(approved_note)} מתוך 300")

# ==========================================
# טאב 2: מגיב חכם בעל ערך
# ==========================================
with tab_comment:
    st.markdown("<h4 style='text-align: right;'>💬 ניסוח תגובת ערך מקצועית לפוסט בפיד</h4>", unsafe_allow_html=True)
    post_content = st.text_area(
        "הדבק כאן את תוכן הפוסט שעליו תרצה להגיב:",
        placeholder="הדבק את הטקסט המלא של הפוסט מלינקדין...",
        height=150
    )
    
    c_style, c_lang = st.columns(2)
    with c_style:
        comment_style = st.selectbox(
            "סגנון התגובה המבוקש:",
            [
                "🔬 תגובת עומק מקצועית ומנומקת (Evidence-Based)",
                "❓ שאלה אינטליגנטית שפותחת דיון מקצועי",
                "💡 תובנה פרקטית מהניסיון המחקרי/מעשי",
                "👏 תגובת פרגון ממוקדת עם זווית ראייה אישית"
            ]
        )
    with c_lang:
        comment_lang = st.selectbox("שפת התגובה:", ["זהה לשפת הפוסט (מומלץ)", "עברית", "אנגלית"])

    if st.button("✨ נסח אפשרויות תגובה איכותיות", use_container_width=True):
        if not post_content.strip():
            st.warning("נא להדביק את תוכן הפוסט.")
        else:
            sys_comment = f"""
            אתה עוזר ניסוח תגובות מקצועי בלינקדין.
            רקע המשתמש: {user_background}.
            סגנון מבוקש: {comment_style}.
            הנחיית שפה: {comment_lang}.
            
            כללי איכות קריטיים:
            1. איסור מוחלט על תגובות בנאליות או מוזרות (כמו 'Great post!' או מלל רובוטי).
            2. התגובה חייבת להתייחס ישירות לנקודה ספציפית שהועלתה בפוסט.
            3. תן 2 אפשרויות תגובה שונות ומנוסחות היטב.
            4. כל תגובה צריכה להוסיף ערך מקצועי ולהציג את המשתמש כאיש מקצוע בר-דעת.
            """
            draft_comments = call_gemini(post_content, sys_comment)
            
            st.markdown("#### 🛡️ שער בדיקה ואישור לתגובה (Review & Confirm):")
            st.info("בדוק את האפשרויות, בחר ודייק את התגובה שהכי מייצגת אותך:")
            st.markdown(draft_comments)
            st.text_area("ערוך והעתק מכאן את התגובה המאושרת על ידך:", height=90, placeholder="הדבק כאן את הנוסח שנבחר לפני ההדבקה בלינקדין...")

# ==========================================
# טאב 3: כתיבת פוסטים מקצועיים
# ==========================================
with tab_post:
    st.markdown("<h4 style='text-align: right;'>✍️ יצירת פוסט מקצועי מבוסס ערך</h4>", unsafe_allow_html=True)
    post_topic = st.text_area(
        "מה הנושא או התובנה שתרצה לשתף?",
        placeholder="למשל: סקירת מיתוס על צריכת חלבון ותזמון סביב אימונים, או שילוב פייתון וניתוח נתונים במדעי התזונה, או סיכום של מאמר מעניין שקראת...",
        height=100
    )
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        post_format = st.selectbox(
            "מבנה הפוסט:",
            [
                "ניתוח מדעי / ניפוץ מיתוס (Evidence-Based Breakdown)",
                "תובנה אישית / לקח מתהליך לימודי ומעשי",
                "מאמר דעה מקצועי (Perspective & Future Trends)",
                "טיפ פרקטי וקצר ממוקד פעולה"
            ]
        )
    with col_p2:
        post_lang = st.selectbox("שפת הפוסט:", ["עברית", "אנגלית (English)"])

    if st.button("🚀 נסח פוסט לינקדין שלם", use_container_width=True):
        if not post_topic.strip():
            st.warning("נא להזין נושא או רעיון לפוסט.")
        else:
            sys_post = f"""
            אתה כותב פוסטים בכיר בלינקדין בתחומי המדע, התזונה, והטכנולוגיה.
            רקע הכותב: {user_background}.
            מבנה מבוקש: {post_format}.
            שפת הכתיבה: {post_lang}.
            
            מבנה פוסט מנצח:
            1. Hook: שורה ראשונה חזקה, מסקרנת ולא קליקבייטית.
            2. רווחים בין פסקאות לקריאה נוחה במסך נייד.
            3. גוף הפוסט: תובנות חדות, נתונים מבוססי ראיות, בלי מילים ריקות.
            4. שאלת סיום / Call-to-action שמעודדת דיון אינטליגנטי בתגובות.
            5. 3–5 האשטאגים ממוקדים בסוף.
            """
            draft_post = call_gemini(post_topic, sys_post)
            
            st.markdown("#### 🛡️ שער אישור ועריכת פוסט (Post Preview & Edit):")
            st.warning("שים לב: קרא את הפוסט בעיון, ודא שהעובדות והטון מדויקים עבורך לפני פרסום:")
            approved_post = st.text_area("ערוך את הפוסט המלא לאישורך:", value=draft_post, height=260)
            st.caption(f"אורך הפוסט: {len(approved_post)} תווים")

# ==========================================
# טאב 4: איתור משרות והודעה למגייס
# ==========================================
with tab_jobs:
    st.markdown("<h4 style='text-align: right;'>💼 איתור משרות מותאמות ופנייה למנהל המגייס</h4>", unsafe_allow_html=True)
    
    domain_choice = st.selectbox(
        "בחר תחום משרות רלוונטי:",
        [
            "מחקר ופיתוח בפוד-טק (FoodTech R&D / Product Development)",
            "מדעי התזונה, בריאות ותזונה קלינית (Nutrition Science / Dietetics)",
            "אגרו-אינפורמטיקה וניתוח נתונים (Bioinformatics / Agri-Data)",
            "פיזיולוגיה של המאמץ ותזונת ספורט (Sports Science / Exercise Physiology)"
        ]
    )
    
    # הפקת חיפוש ישיר במשרות לינקדין
    clean_domain_query = domain_choice.split("(")[-1].replace(")", "")
    job_search_url = f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(clean_domain_query)}&location=Israel"
    
    st.link_button(f"🔎 פתח חיפוש משרות פעילות בלינקדין עבור: {clean_domain_query}", job_search_url)
    
    st.markdown("---")
    st.markdown("<h5 style='text-align: right;'>📝 ניסוח פנייה אישית ומדויקת למנהל המגייס (Hiring Manager):</h5>", unsafe_allow_html=True)
    job_desc = st.text_area(
        "הדבק את תיאור המשרה (או דרישות התפקיד מלינקדין):",
        placeholder="הדבק כאן את ה-Job Description...",
        height=120
    )
    
    if st.button("🎯 נסח הודעת פנייה ממוקדת ומכתב מקדים קצר", use_container_width=True):
        if not job_desc.strip():
            st.warning("נא להדביק את תיאור המשרה.")
        else:
            sys_job = f"""
            אתה יועץ קריירה וגיוס בכיר.
            נתח את תיאור המשרה הבא מול הרקע של המועמד:
            רקע המועמד: {user_background}.
            תיאור המשרה: {job_desc}.
            
            הפק:
            1. ניתוח התאמה מהיר (נקודות חוזק מרכזיות של המועמד ביחס לתפקיד).
            2. הודעת פנייה אישית וישירה למגייס/למנהל המגייס בלינקדין (InMail/Message קצר, אלגנטי ולא תבניתי) שמבליט בדיוק את הערך של המועמד.
            """
            draft_job_outreach = call_gemini(job_desc, sys_job)
            
            st.markdown("#### 🛡️ שער אישור פנייה למגייס (Review & Approval):")
            st.info("בדוק את ההתאמה ואת נוסח ההודעה לפני שליחה:")
            st.markdown(draft_job_outreach)
            st.text_area("נוסח ההודעה לעריכה והעתקה ישירה:", height=100, placeholder="העתק מכאן את הנוסח המאושר...")
