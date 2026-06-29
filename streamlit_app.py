import streamlit as st
import pickle
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SpamShield AI",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("spam_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ---------------- CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(
        135deg,
        #f4faf5,
        #edf6ef,
        #e7f2ea
    );
}

#MainMenu, footer, header {
    visibility: hidden;
}

/* Main Container */
.main .block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

/* Hero Card */
.hero-card {
    background: white;
    border-radius: 35px;
    padding: 45px;
    text-align: center;
    box-shadow: 0px 12px 30px rgba(0,0,0,0.08);
    margin-bottom: 30px;
}

/* Title */
.hero-title {
    font-size: 65px;
    font-weight: 800;
    color: #153c34;
}

/* Subtitle */
.hero-subtitle {
    font-size: 24px;
    color: #5c7b72;
}

/* Text Area */
textarea {
    border-radius: 20px !important;
    border: 2px solid #d9e8df !important;
    background: white !important;
    font-size: 18px !important;
}

/* Button */
div.stButton > button:first-child {
    background: linear-gradient(
        90deg,
        #1c6d5e,
        #69c3a4
    );
    color: white;
    border: none;
    border-radius: 18px;
    height: 60px;
    width: 100%;
    font-size: 22px;
    font-weight: bold;
}

div.stButton > button:first-child:hover {
    background: linear-gradient(
        90deg,
        #17594d,
        #59b493
    );
    color: white;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: white;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0px 5px 18px rgba(0,0,0,0.08);
}

.footer {
    text-align:center;
    color:#54786d;
    margin-top:40px;
    font-size:16px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class='hero-card'>

<h1 class='hero-title'>
🛡️ SpamShield AI
</h1>

<p class='hero-subtitle'>
Intelligent Email & SMS Security Assistant
</p>

</div>
""", unsafe_allow_html=True)

# ---------------- INPUT ----------------
message = st.text_area(
    "✉️ Enter your message",
    placeholder="Type your email or SMS here...",
    height=180
)

# ---------------- WORD LISTS ----------------
spam_words = [
    "win","won","prize","lottery","free","click",
    "offer","money","urgent","claim","gift",
    "congratulations","cash","limited","reward"
]

bank_words = [
    "bank","account","otp","kyc","credit","debit"
]

job_words = [
    "job","hiring","salary","interview","earn"
]

romance_words = [
    "love","dear","relationship","dating"
]

delivery_words = [
    "parcel","delivery","courier","shipment"
]

# ---------------- PREDICTION ----------------
if st.button("🛡️ Analyze Message"):

    if message.strip() == "":
        st.warning("Please enter a message.")

    else:

        transformed = vectorizer.transform([message])

        prediction = model.predict(transformed)[0]

        probability = np.max(
            model.predict_proba(transformed)
        ) * 100

        message_lower = message.lower()

        suspicious = []

        for word in spam_words:
            if word in message_lower:
                suspicious.append(word)

        tips = []

        if "click" in message_lower:
            tips.append(
                "Do not click unknown links."
            )

        if "otp" in message_lower:
            tips.append(
                "Never share your OTP."
            )

        if "bank" in message_lower:
            tips.append(
                "Verify bank messages before responding."
            )

        if prediction == 1:
            tips.append(
                "Avoid sharing personal information."
            )

        category = "General Spam"

        if any(word in message_lower for word in bank_words):
            category = "💳 Banking Scam"

        elif any(word in message_lower for word in job_words):
            category = "💼 Job Scam"

        elif any(word in message_lower for word in romance_words):
            category = "💕 Romance Scam"

        elif any(word in message_lower for word in delivery_words):
            category = "📦 Delivery Scam"

        elif "lottery" in message_lower or "prize" in message_lower:
            category = "🎁 Lottery Scam"

        score = 10

        score -= len(suspicious)

        if "http" in message_lower:
            score -= 2

        if "!" in message:
            score -= 1

        score = max(score, 1)

        # ---------------- RESULT ----------------
        if prediction == 1:
            st.error("🚫 SPAM DETECTED")
        else:
            st.success("✅ SAFE MESSAGE")

        # ---------------- DASHBOARD ----------------
        st.markdown("## 📊 Analysis Dashboard")

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Spam Probability",
                f"{probability:.2f}%"
            )

        with c2:
            st.metric(
                "Security Score",
                f"{score}/10"
            )

        st.progress(int(probability))

        st.markdown("---")

        c1, c2 = st.columns(2)

        with c1:
            st.subheader("🔍 Suspicious Words")

            if suspicious:
                for word in suspicious:
                    st.write("•", word)
            else:
                st.write(
                    "No suspicious words found."
                )

        with c2:
            st.subheader("🎯 Scam Category")
            st.info(category)

        st.markdown("---")

        st.subheader("🛡️ Safety Tips")

        if tips:
            for tip in tips:
                st.write("✅", tip)
        else:
            st.write(
                "No immediate security concerns detected."
            )

        st.markdown("---")

        st.subheader("📈 Message Insights")

        i1, i2, i3, i4 = st.columns(4)

        i1.metric(
            "Length",
            len(message)
        )

        i2.metric(
            "!",
            message.count("!")
        )

        i3.metric(
            "Links",
            message.count("http")
        )

        i4.metric(
            "Suspicious",
            len(suspicious)
        )

# ---------------- FOOTER ----------------
st.markdown("""
<div class='footer'>
Built with ❤️ using Python, Scikit-Learn & Streamlit
</div>
""", unsafe_allow_html=True)