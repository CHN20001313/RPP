import streamlit as st

st.set_page_config(page_title="ACS RPP Risk Calculator", layout="wide")

st.title("ACS Hemodynamic Risk Calculator")
st.markdown("Cross-Physiological RPP Risk Stratification Tool")

# ===========================
# 真实中位数阈值（替换为论文数据）
# ===========================
MEDIAN_RPP_REST = 10500
MEDIAN_RPP_PEAK = 21000
MEDIAN_HGI = 0.9
MEDIAN_RPP_MET = 4500

# ===========================
# 左侧输入区域
# ===========================
st.sidebar.header("Input Parameters")

HR_rest = st.sidebar.number_input("Resting Heart Rate (bpm)", min_value=0.0, step=1.0)
SBP_rest = st.sidebar.number_input("Resting SBP (mmHg)", min_value=0.0, step=1.0)

st.sidebar.markdown("---")
st.sidebar.subheader("Exercise Data")

HR_peak = st.sidebar.number_input("Peak Heart Rate (bpm)", min_value=0.0, step=1.0)
SBP_peak = st.sidebar.number_input("Peak SBP (mmHg)", min_value=0.0, step=1.0)

st.sidebar.markdown("---")
st.sidebar.subheader("Fitness Data (Choose One)")

MET_peak = st.sidebar.number_input("Peak MET", min_value=0.0, step=0.1)
VO2_peak = st.sidebar.number_input("VO2peak (mL/kg/min)", min_value=0.0, step=0.1)

calculate = st.sidebar.button("Calculate Risk Stratification")

# ===========================
# 右侧结果区域
# ===========================
if calculate:

    # ---------------------------
    # 基础输入检查
    # ---------------------------
    if HR_rest <= 0 or SBP_rest <= 0:
        st.error("Please enter resting HR and SBP.")
        st.stop()

    # ---------------------------
    # MET 与 VO2 逻辑检查
    # ---------------------------
    if MET_peak > 0 and VO2_peak > 0:
        st.error("Please enter either METpeak or VO2peak, not both.")
        st.stop()

    if VO2_peak > 0:
        MET_peak = VO2_peak / 3.5
        st.info(f"VO₂peak converted to METpeak: {MET_peak:.2f}")

    # ===========================
    # 静息状态
    # ===========================
    RPP_rest = HR_rest * SBP_rest

    st.header("Resting State Assessment")
    st.metric("RPP rest", f"{RPP_rest:.0f}")

    if RPP_rest >= MEDIAN_RPP_REST:
        st.warning("High resting RPP → Higher residual risk")
    else:
        st.success("Low resting RPP → Lower residual risk")

    # ===========================
    # 运动状态
    # ===========================
    if HR_peak > 0 and SBP_peak > 0:

        RPP_peak = HR_peak * SBP_peak
        HGI = (RPP_peak - RPP_rest) / RPP_rest

        st.header("Exercise State Assessment")

        col1, col2 = st.columns(2)
        col1.metric("RPP peak", f"{RPP_peak:.0f}")
        col2.metric("Hemodynamic Gain Index (HGI)", f"{HGI:.2f}")

        if HGI >= MEDIAN_HGI:
            st.success("High HGI → Favorable circulatory reserve")
        else:
            st.warning("Low HGI → Impaired hemodynamic gain")

        # ===========================
        # 体能校正分析
        # ===========================
        if MET_peak > 0:

            RPP_MET = RPP_peak / MET_peak

            st.header("Fitness-Adjusted Assessment")
            st.metric("RPPpeak / METpeak", f"{RPP_MET:.0f}")

            if RPP_MET >= MEDIAN_RPP_MET:
                st.warning("High workload per fitness → Higher risk")
            else:
                st.success("Efficient workload response → Lower risk")

            # ===========================
            # 联合风险模式
            # ===========================
            st.header("Combined Risk Pattern")

            if HGI >= MEDIAN_HGI and RPP_MET < MEDIAN_RPP_MET:
                st.success("Best Profile: High HGI + Low RPP/MET")
            elif HGI < MEDIAN_HGI and RPP_MET >= MEDIAN_RPP_MET:
                st.error("Highest Risk Profile: Low HGI + High RPP/MET")
            else:
                st.info("Intermediate Risk Profile")

        else:
            st.info("Enter METpeak or VO₂peak to unlock fitness-adjusted analysis.")

    else:
        st.info("Enter peak HR and SBP to unlock exercise-state assessment.")