import streamlit as st
import pandas as pd
from datetime import date
from pypdf import PdfReader


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Study Planner",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "student_name": "",
    "daily_hours": 5.0,
    "plan": [],
    "topics": [],
    "progress": {},
    "quiz_score": 0,
    "quiz_topic": "",
    "pdf_text": "",
    "pdf_name": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# FUNCTIONS
# =========================================================

def difficulty_score(difficulty):
    if difficulty == "Hard":
        return 3
    elif difficulty == "Medium":
        return 2
    return 1


def urgency_score(days):
    if days <= 3:
        return 4
    elif days <= 7:
        return 3
    elif days <= 15:
        return 2
    return 1


def priority_name(score):
    if score >= 6:
        return "HIGH"
    elif score >= 4:
        return "MEDIUM"
    return "LOW"


# =========================================================
# QUIZ QUESTION BANK
# =========================================================

QUESTIONS = [
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["function", "def", "fun", "define"],
        "answer": "def",
        "reason": "The def keyword is used to define a function in Python."
    },
    {
        "question": "Which function is used to display output?",
        "options": ["input()", "print()", "show()", "display()"],
        "answer": "print()",
        "reason": "print() displays text or values on the screen."
    },
    {
        "question": "Which symbol is used for a single-line comment?",
        "options": ["//", "#", "/*", "--"],
        "answer": "#",
        "reason": "Python uses # to create a single-line comment."
    },
    {
        "question": "Which function takes input from the user?",
        "options": ["scan()", "input()", "read()", "get()"],
        "answer": "input()",
        "reason": "input() accepts information entered by the user."
    },
    {
        "question": "Which data type stores whole numbers?",
        "options": ["float", "int", "str", "bool"],
        "answer": "int",
        "reason": "int is used to store whole numbers."
    },
    {
        "question": "Which data type stores decimal numbers?",
        "options": ["int", "float", "str", "bool"],
        "answer": "float",
        "reason": "float is used for numbers containing decimal values."
    },
    {
        "question": "Which data type stores True or False?",
        "options": ["int", "str", "bool", "float"],
        "answer": "bool",
        "reason": "bool represents True and False values."
    },
    {
        "question": "Which operator is used for exponentiation?",
        "options": ["*", "//", "**", "%"],
        "answer": "**",
        "reason": "The ** operator is used to raise a number to a power."
    },
    {
        "question": "Which keyword immediately stops a loop?",
        "options": ["stop", "break", "exit", "continue"],
        "answer": "break",
        "reason": "break immediately terminates the current loop."
    },
    {
        "question": "Which keyword skips the current loop iteration?",
        "options": ["skip", "pass", "continue", "break"],
        "answer": "continue",
        "reason": "continue skips the current iteration and moves to the next one."
    },
    {
        "question": "Which method converts text to lowercase?",
        "options": ["upper()", "lower()", "small()", "down()"],
        "answer": "lower()",
        "reason": "lower() converts characters in a string to lowercase."
    },
    {
        "question": "Which brackets are used to create a list?",
        "options": ["( )", "[ ]", "{ }", "< >"],
        "answer": "[ ]",
        "reason": "Square brackets are used to create a Python list."
    },
    {
        "question": "Which operator checks equality?",
        "options": ["=", "==", "!=", "<="],
        "answer": "==",
        "reason": "== compares two values to check whether they are equal."
    },
    {
        "question": "Which operator assigns a value to a variable?",
        "options": ["==", "=", "!=", ">="],
        "answer": "=",
        "reason": "= assigns a value to a variable."
    },
    {
        "question": "Which function returns the number of items?",
        "options": ["count()", "size()", "len()", "length()"],
        "answer": "len()",
        "reason": "len() returns the number of items in a collection."
    },
    {
        "question": "What is the result of 10 % 3?",
        "options": ["0", "1", "2", "3"],
        "answer": "1",
        "reason": "% returns the remainder. 10 divided by 3 leaves remainder 1."
    },
    {
        "question": "Which keyword is used for a condition?",
        "options": ["if", "check", "when", "condition"],
        "answer": "if",
        "reason": "if is used to execute code based on a condition."
    },
    {
        "question": "Which loop runs while a condition is True?",
        "options": ["for", "while", "if", "repeat"],
        "answer": "while",
        "reason": "A while loop runs repeatedly while its condition is True."
    },
    {
        "question": "Which collection is ordered and changeable?",
        "options": ["tuple", "list", "set", "dictionary"],
        "answer": "list",
        "reason": "A list is ordered and mutable."
    },
    {
        "question": "Which keyword is used to create a class?",
        "options": ["object", "class", "define", "struct"],
        "answer": "class",
        "reason": "The class keyword is used to define a class."
    }
]


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎓 AI Study Planner")

    st.caption("Smart Academic Management")

    st.divider()

    page = st.radio(
        "📌 Navigation",
        [
            "🏠 Dashboard",
            "📚 Study Planner",
            "📄 Topic Analyzer",
            "🧠 AI Quiz",
            "📊 Progress",
            "📅 Smart Schedule"
        ]
    )

    st.divider()

    st.info(
        "Plan → Learn → Quiz → Analyze → Improve"
    )

    st.divider()

    st.caption(
        "Built using Python + Streamlit 🐍"
    )


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.title("🎓 AI Study Planner")

    if st.session_state.student_name:
        st.subheader(
            f"Welcome, {st.session_state.student_name}! 👋"
        )
    else:
        st.subheader(
            "Your Personal Academic Assistant 🤖"
        )

    st.write(
        "Create study plans, analyze topics, "
        "take quizzes and track your exam readiness."
    )

    st.divider()

    total_subjects = len(st.session_state.plan)
    total_topics = len(st.session_state.topics)

    if st.session_state.progress:
        overall_progress = sum(
            st.session_state.progress.values()
        ) / len(st.session_state.progress)
    else:
        overall_progress = 0

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "📚 Subjects",
            total_subjects
        )

    with c2:
        st.metric(
            "📖 Topics",
            total_topics
        )

    with c3:
        st.metric(
            "📈 Preparation",
            f"{overall_progress:.0f}%"
        )

    with c4:
        st.metric(
            "🧠 Quiz Score",
            f"{st.session_state.quiz_score}%"
        )

    st.divider()

    st.header("✨ How It Works")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            ### 📚 1. Plan

            Enter subjects, difficulty,
            exam dates and available study hours.
            """
        )

    with c2:
        st.markdown(
            """
            ### 🧠 2. Test

            Add topics and take quizzes
            to check your knowledge.
            """
        )

    with c3:
        st.markdown(
            """
            ### 📊 3. Improve

            Weak topics automatically
            receive extra study time.
            """
        )

    st.divider()

    st.success(
        "💡 Tip: Regular testing is better than only reading notes."
    )


# =========================================================
# STUDY PLANNER
# =========================================================

elif page == "📚 Study Planner":

    st.title("📚 AI Study Planner")

    st.write(
        "Create a personalized daily study schedule."
    )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        name = st.text_input(
            "👤 Student Name",
            value=st.session_state.student_name
        )

    with c2:

        daily_hours = st.number_input(
            "⏰ Study Hours Per Day",
            min_value=1.0,
            max_value=24.0,
            value=st.session_state.daily_hours,
            step=0.5
        )

    st.divider()

    st.subheader("📚 Subjects")

    number = st.number_input(
        "Number of Subjects",
        min_value=1,
        max_value=10,
        value=3,
        step=1
    )

    subjects = []

    for i in range(int(number)):

        st.markdown(
            f"### Subject {i + 1}"
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            subject_name = st.text_input(
                "Subject Name",
                key=f"name_{i}",
                placeholder="Example: Python"
            )

        with c2:

            difficulty = st.selectbox(
                "Difficulty",
                ["Easy", "Medium", "Hard"],
                key=f"difficulty_{i}"
            )

        with c3:

            exam_date = st.date_input(
                "Exam Date",
                min_value=date.today(),
                key=f"exam_{i}"
            )

        subjects.append(
            {
                "name": subject_name.strip(),
                "difficulty": difficulty,
                "exam_date": exam_date
            }
        )

    st.divider()

    if st.button(
        "🚀 Generate Study Plan",
        type="primary",
        use_container_width=True
    ):

        if name.strip() == "":
            st.error("⚠️ Please enter your name.")
            st.stop()

        if any(
            subject["name"] == ""
            for subject in subjects
        ):
            st.error(
                "⚠️ Please enter all subject names."
            )
            st.stop()

        st.session_state.student_name = name
        st.session_state.daily_hours = daily_hours

        for subject in subjects:

            days_left = (
                subject["exam_date"]
                - date.today()
            ).days

            d_score = difficulty_score(
                subject["difficulty"]
            )

            u_score = urgency_score(
                days_left
            )

            score = d_score + u_score

            subject["days_left"] = days_left
            subject["score"] = score
            subject["priority"] = priority_name(score)

        total_score = sum(
            subject["score"]
            for subject in subjects
        )

        for subject in subjects:

            subject["study_hours"] = round(
                (
                    subject["score"]
                    / total_score
                ) * daily_hours,
                2
            )

        subjects.sort(
            key=lambda x: (
                -x["score"],
                x["days_left"]
            )
        )

        st.session_state.plan = subjects

        for subject in subjects:

            if subject["name"] not in st.session_state.progress:

                st.session_state.progress[
                    subject["name"]
                ] = 0

        st.success(
            "🎉 Study plan generated successfully!"
        )

    if st.session_state.plan:

        st.divider()

        st.subheader("📋 Your Study Plan")

        table = []

        for subject in st.session_state.plan:

            table.append(
                {
                    "Subject": subject["name"],
                    "Difficulty": subject["difficulty"],
                    "Exam In": f"{subject['days_left']} days",
                    "Priority": subject["priority"],
                    "Daily Hours": subject["study_hours"]
                }
            )

        df = pd.DataFrame(table)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader(
            "📊 Daily Study Distribution"
        )

        chart = pd.DataFrame(
            {
                "Subject": [
                    s["name"]
                    for s in st.session_state.plan
                ],
                "Study Hours": [
                    s["study_hours"]
                    for s in st.session_state.plan
                ]
            }
        )

        st.bar_chart(
            chart.set_index("Subject")
        )

        st.divider()

        report = pd.DataFrame(
            [
                {
                    "Student": st.session_state.student_name,
                    "Subject": s["name"],
                    "Difficulty": s["difficulty"],
                    "Exam Date": s["exam_date"],
                    "Days Left": s["days_left"],
                    "Priority": s["priority"],
                    "Daily Study Hours": s["study_hours"]
                }
                for s in st.session_state.plan
            ]
        )

        st.download_button(
            "📥 Download Study Plan",
            data=report.to_csv(index=False),
            file_name="AI_Study_Plan.csv",
            mime="text/csv",
            use_container_width=True
        )


# =========================================================
# TOPIC ANALYZER
# =========================================================

elif page == "📄 Topic Analyzer":

    st.title("📄 Topic Analyzer")

    st.write(
        "Add topics manually or upload a study PDF."
    )

    st.divider()

    st.subheader("📌 Add Topic")

    topic = st.text_input(
        "Topic Name",
        placeholder="Example: Python Loops"
    )

    if st.button("➕ Add Topic"):

        if topic.strip() == "":
            st.warning("Please enter a topic.")

        elif topic.strip() in st.session_state.topics:
            st.warning("Topic already exists.")

        else:

            st.session_state.topics.append(
                topic.strip()
            )

            st.session_state.progress[
                topic.strip()
            ] = 0

            st.success(
                f"✅ {topic.strip()} added!"
            )

    st.divider()

    st.subheader("📄 Upload Study PDF")

    uploaded_file = st.file_uploader(
        "Upload your study material",
        type=["pdf"]
    )

    if uploaded_file:

        st.success(
            f"📄 {uploaded_file.name} uploaded!"
        )

        try:

            reader = PdfReader(
                uploaded_file
            )

            text = ""

            for page_data in reader.pages:

                page_text = (
                    page_data.extract_text()
                )

                if page_text:
                    text += page_text + "\n"

            st.session_state.pdf_text = text
            st.session_state.pdf_name = uploaded_file.name

            if text.strip():

                st.success(
                    "✅ PDF text extracted successfully!"
                )

                lines = text.split("\n")

                detected_topics = []

                for line in lines:

                    clean = line.strip()

                    if len(clean) < 4:
                        continue

                    if len(clean) > 80:
                        continue

                    if (
                        clean.isupper()
                        or clean.endswith(":")
                        or clean[:2].isdigit()
                    ):

                        clean = (
                            clean
                            .replace(":", "")
                            .strip()
                        )

                        if clean not in detected_topics:

                            detected_topics.append(
                                clean
                            )

                st.divider()

                st.subheader(
                    "🔍 Detected Topics"
                )

                if detected_topics:

                    for item in detected_topics:
                        st.write(
                            f"📚 {item}"
                        )

                    if st.button(
                        "➕ Add Detected Topics"
                    ):

                        count = 0

                        for item in detected_topics:

                            if item not in st.session_state.topics:

                                st.session_state.topics.append(
                                    item
                                )

                                st.session_state.progress[
                                    item
                                ] = 0

                                count += 1

                        st.success(
                            f"✅ {count} topics added!"
                        )

                else:

                    st.warning(
                        "No clear headings found. "
                        "Add topics manually."
                    )

                with st.expander(
                    "📖 View Extracted PDF Text"
                ):

                    st.text_area(
                        "Study Material",
                        text,
                        height=300
                    )

            else:

                st.warning(
                    "⚠️ Text could not be extracted. "
                    "This may be a scanned PDF."
                )

        except Exception as e:

            st.error(
                f"❌ PDF Error: {e}"
            )

    st.divider()

    st.subheader("📚 Your Topics")

    if st.session_state.topics:

        for i, topic_name in enumerate(
            st.session_state.topics,
            start=1
        ):

            progress = st.session_state.progress.get(
                topic_name,
                0
            )

            st.write(
                f"**{i}. {topic_name}** — {progress}% prepared"
            )

    else:

        st.info(
            "No topics added yet."
        )


# =========================================================
# AI QUIZ
# =========================================================

elif page == "🧠 AI Quiz":

    st.title("🧠 AI Quiz")

    st.write(
        "Test your Python knowledge and update your preparation score."
    )

    st.divider()

    if not st.session_state.topics:

        st.warning(
            "📚 Add at least one topic first."
        )

    else:

        selected_topic = st.selectbox(
            "📌 Select Topic",
            st.session_state.topics
        )

        question_count = st.select_slider(
            "📝 Number of Questions",
            options=[10, 15, 20],
            value=10
        )

        selected_questions = QUESTIONS[
            :question_count
        ]

        st.divider()

        answers = []

        for i, q in enumerate(
            selected_questions
        ):

            st.markdown(
                f"### Q{i + 1}. {q['question']}"
            )

            answer = st.radio(
                "Choose one:",
                q["options"],
                key=f"{selected_topic}_{i}"
            )

            answers.append(answer)

            st.divider()

        if st.button(
            "🚀 Submit Quiz",
            type="primary",
            use_container_width=True
        ):

            correct = 0

            st.subheader(
                "📝 Answer Review"
            )

            for i, q in enumerate(
                selected_questions
            ):

                user_answer = answers[i]
                correct_answer = q["answer"]

                if user_answer == correct_answer:

                    correct += 1

                    st.success(
                        f"Q{i + 1}: ✅ Correct"
                    )

                else:

                    st.error(
                        f"Q{i + 1}: ❌ Wrong"
                    )

                st.write(
                    f"Your answer: **{user_answer}**"
                )

                st.write(
                    f"Correct answer: **{correct_answer}**"
                )

                st.info(
                    f"💡 Reason: {q['reason']}"
                )

                st.divider()

            total = len(selected_questions)

            wrong = total - correct

            score = round(
                (correct / total) * 100
            )

            st.session_state.quiz_score = score
            st.session_state.quiz_topic = selected_topic

            st.session_state.progress[
                selected_topic
            ] = score

            st.subheader(
                "🎯 Quiz Result"
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "✅ Correct",
                    correct
                )

            with c2:
                st.metric(
                    "❌ Wrong",
                    wrong
                )

            with c3:
                st.metric(
                    "🎯 Score",
                    f"{score}%"
                )

            st.progress(
                score / 100
            )

            if score >= 80:

                st.success(
                    "🔥 Excellent! Strong preparation."
                )

            elif score >= 50:

                st.warning(
                    "🟡 Good! Revise this topic once more."
                )

            else:

                st.error(
                    "🔴 Weak topic! More practice required."
                )


# =========================================================
# PROGRESS
# =========================================================

elif page == "📊 Progress":

    st.title("📊 Progress & Exam Readiness")

    st.write(
        "Track your preparation level."
    )

    st.divider()

    if not st.session_state.progress:

        st.info(
            "No progress available yet. Take a quiz first."
        )

    else:

        progress_data = []

        for topic_name, score in (
            st.session_state.progress.items()
        ):

            st.write(
                f"### 📚 {topic_name}"
            )

            st.progress(
                score / 100
            )

            st.write(
                f"Preparation: **{score}%**"
            )

            progress_data.append(
                {
                    "Topic": topic_name,
                    "Preparation": score
                }
            )

        df = pd.DataFrame(
            progress_data
        )

        overall = df["Preparation"].mean()

        quiz_score = st.session_state.quiz_score

        readiness = (
            overall * 0.7
            +
            quiz_score * 0.3
        )

        st.divider()

        st.subheader(
            "🏆 Overall Performance"
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "📚 Preparation",
                f"{overall:.0f}%"
            )

        with c2:
            st.metric(
                "🧠 Quiz Score",
                f"{quiz_score}%"
            )

        with c3:
            st.metric(
                "🏆 Readiness",
                f"{readiness:.0f}%"
            )

        st.progress(
            readiness / 100
        )

        if readiness >= 80:

            st.success(
                "🔥 You are highly prepared!"
            )

        elif readiness >= 60:

            st.warning(
                "💪 Good progress. Continue revision."
            )

        else:

            st.error(
                "🚨 You need more preparation."
            )

        st.divider()

        st.subheader(
            "📊 Topic Performance"
        )

        st.bar_chart(
            df.set_index("Topic")
        )


# =========================================================
# SMART SCHEDULE
# =========================================================

elif page == "📅 Smart Schedule":

    st.title("📅 Smart Schedule")

    st.write(
        "Study time increases automatically for weak topics."
    )

    st.divider()

    if not st.session_state.plan:

        st.info(
            "📚 Create a Study Plan first."
        )

    else:

        for subject in st.session_state.plan:

            name = subject["name"]

            progress = st.session_state.progress.get(
                name,
                0
            )

            base_hours = subject["study_hours"]

            if progress < 40:

                recommended = round(
                    base_hours * 1.5,
                    2
                )

                status = (
                    "🔴 Weak — Extra revision"
                )

            elif progress < 70:

                recommended = round(
                    base_hours * 1.2,
                    2
                )

                status = (
                    "🟡 Needs revision"
                )

            else:

                recommended = round(
                    base_hours,
                    2
                )

                status = (
                    "🟢 Good preparation"
                )

            st.subheader(
                f"📚 {name}"
            )

            st.write(
                f"Preparation: **{progress}%**"
            )

            st.write(
                f"Priority: **{subject['priority']}**"
            )

            st.write(
                f"Recommended Study Time: "
                f"**{recommended} hours/day**"
            )

            st.write(status)

            st.divider()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🎓 AI Study Planner | "
    "Smart Academic Management | "
    "Python + Streamlit 🐍"
)
