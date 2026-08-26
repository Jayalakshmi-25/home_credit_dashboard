import os

import streamlit as st

APP_MOBILE = os.getenv("HOME_CREDIT_MOBILE")
APP_OTP = os.getenv("HOME_CREDIT_OTP", "123456")


def _is_valid_mobile_number(phone_number: str) -> bool:
    cleaned = str(phone_number or "").replace(" ", "").replace("-", "")
    return (cleaned.startswith("+") or cleaned.startswith("00")) and cleaned.lstrip("+").lstrip("0").isdigit() and len(cleaned) >= 10


def _is_valid_otp(otp: str) -> bool:
    normalized_otp = str(otp or "").strip()
    return normalized_otp.isdigit() and len(normalized_otp) == 6


def current_user():
    return st.session_state.get("app_user")


def is_logged_in():
    return bool(st.session_state.get("app_authenticated"))


def login(phone_number: str, otp: str):
    normalized_phone = str(phone_number or "").strip()
    normalized_otp = str(otp or "").strip()

    if _is_valid_mobile_number(normalized_phone) and _is_valid_otp(normalized_otp):
        if APP_OTP and normalized_otp == APP_OTP:
            st.session_state["app_authenticated"] = True
            st.session_state["app_user"] = normalized_phone
            return True

        if not APP_OTP:
            st.session_state["app_authenticated"] = True
            st.session_state["app_user"] = normalized_phone
            return True

    st.session_state["app_authenticated"] = False
    st.session_state["app_user"] = None
    return False


def logout():
    st.session_state.pop("app_authenticated", None)
    st.session_state.pop("app_user", None)
    st.session_state.pop("otp_sent", None)
    st.session_state.pop("entered_phone", None)


def require_login():
    if is_logged_in():
        return True

    otp_sent = st.session_state.get("otp_sent", False)
    entered_phone = st.session_state.get("entered_phone", APP_MOBILE or "+91 98765 43210")

    st.markdown(
        """
        <style>
        .login-shell {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem 1rem;
            background: linear-gradient(180deg, #f3f3f5 0%, #f0f0f2 100%);
        }
        .login-card {
            width: min(1200px, 100%);
            display: grid;
            grid-template-columns: 1.1fr 0.9fr;
            background: rgba(18, 19, 24, 0.98);
            border: 1px solid rgba(168, 167, 178, 0.2);
            border-radius: 30px;
            overflow: hidden;
            box-shadow: 0 30px 70px rgba(15, 17, 24, 0.12);
        }
        .login-panel {
            padding: 2.2rem 2.3rem 2.8rem;
            background: linear-gradient(180deg, rgba(18, 18, 22, 1), rgba(15, 15, 18, 1));
            min-height: 440px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .login-brand-row {
            display: flex;
            align-items: center;
            gap: 1.1rem;
            margin-bottom: 2rem;
        }
        .brand-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 72px;
            height: 72px;
            border-radius: 22px;
            background: linear-gradient(135deg, #d8b8ff 0%, #a78bfa 100%);
            color: #1a1521;
            font-weight: 900;
            font-size: 2.1rem;
            box-shadow: 0 12px 25px rgba(167, 139, 250, 0.35);
        }
        .mini-tag {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 2.5rem;
            padding: 0.55rem 1.1rem;
            border-radius: 999px;
            background: rgba(168, 167, 178, 0.12);
            color: #eff0f8;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            border: 1px solid rgba(210, 206, 222, 0.14);
        }
        .login-panel h1 {
            margin: 0;
            font-size: clamp(3.3rem, 4vw, 6rem);
            line-height: 0.96;
            letter-spacing: -0.06em;
            color: #f4f1ff;
            font-weight: 800;
        }
        .login-panel p {
            margin-top: 2rem;
            margin-bottom: 0;
            max-width: 720px;
            color: #c9c0d8;
            font-size: clamp(1.15rem, 1.5vw, 1.5rem);
            line-height: 1.5;
            font-weight: 400;
        }
        .login-form-panel {
            padding: 2.2rem 2.2rem 2.3rem;
            background: rgba(12, 13, 17, 0.96);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-form-box {
            width: min(100%, 400px);
        }
        .login-form-box h3 {
            margin: 0 0 0.7rem;
            font-size: 2.1rem;
            color: #f5f3ff;
            font-weight: 700;
        }
        .login-form-box p {
            margin: 0 0 1.4rem;
            color: #bdb0d5;
            font-size: 0.98rem;
        }
        .login-form-box .stForm {
            width: 100%;
        }
        .login-form-box .stTextInput > div > div > input,
        .login-form-box .stTextInput > div > div > div,
        .login-form-box .stTextInput > div > div {
            border-radius: 14px;
            background: rgba(26, 27, 36, 0.9);
            color: #f2ebff;
            border: 1px solid rgba(166, 166, 178, 0.2);
            min-height: 52px;
        }
        .login-form-box .stButton > button {
            width: 100%;
            min-height: 50px;
            border-radius: 14px;
            border: none;
            background: linear-gradient(135deg, #8b5cf6, #a78bfa);
            color: white;
            font-weight: 700;
            letter-spacing: 0.02em;
            box-shadow: 0 14px 30px rgba(139, 92, 246, 0.28);
        }
        .otp-hint {
            margin-top: 1rem;
            padding: 0.8rem 0.9rem;
            border-radius: 12px;
            background: rgba(139, 92, 246, 0.08);
            border: 1px solid rgba(169, 138, 255, 0.2);
            color: #d8cbff;
            font-size: 0.83rem;
            line-height: 1.5;
        }
        @media (max-width: 900px) {
            .login-card {
                grid-template-columns: 1fr;
            }
            .login-panel {
                min-height: auto;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="login-shell">
            <div class="login-card">
                <div class="login-panel">
                    <div class="login-brand-row">
                        <div class="brand-badge">HC</div>
                        <div class="mini-tag">Secure Access</div>
                    </div>
                    <h1>Home Credit</h1>
                    <p>Access the Home Credit dashboard with mobile verification. Use your registered mobile number and the one-time password sent to your device.</p>
                </div>
                <div class="login-form-panel">
                    <div class="login-form-box">
                        <h3>Sign in</h3>
                        <p>Enter your mobile number to continue.</p>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        mobile_number = st.text_input("Mobile number", value=entered_phone, placeholder="+91 98765 43210")
        otp_code = st.text_input("OTP", type="password", max_chars=6, placeholder="Enter 6-digit OTP", disabled=not otp_sent)
        submitted = st.form_submit_button("Send OTP" if not otp_sent else "Verify & Login")

    st.markdown(
        """
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if submitted:
        if not otp_sent:
            if not mobile_number.strip() or not _is_valid_mobile_number(mobile_number):
                st.error("Please enter a valid mobile number with country code, for example +91 98765 43210.")
            else:
                st.session_state["entered_phone"] = mobile_number.strip()
                st.session_state["otp_sent"] = True
                st.session_state["demo_otp"] = APP_OTP
                st.success(f"OTP sent to {mobile_number.strip()}. Use the 6-digit code received on this number.")
                st.markdown(f'<div class="otp-hint">Demo OTP for this environment: <strong>{APP_OTP}</strong></div>', unsafe_allow_html=True)
                st.rerun()
            st.stop()
            return False

        if login(mobile_number, otp_code):
            st.rerun()
        else:
            st.error("Invalid OTP. Please enter the 6-digit code sent to the exact mobile number above.")
            st.markdown(f'<div class="otp-hint">Demo OTP: <strong>{APP_OTP}</strong></div>', unsafe_allow_html=True)

    st.stop()
    return False
