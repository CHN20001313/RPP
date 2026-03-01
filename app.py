import streamlit as st

st.set_page_config(page_title="ACS RPP Risk Calculator", layout="centered")

st.title("ACS Hemodynamic Risk Calculator")
st.markdown("Cross-Physiological RPP Risk Stratification Tool")

# ---------------------------
# 设定你论文中的真实中位数阈值（后续替换）
# ---------------------------
MEDIAN_RPP_REST = 10500
MEDIAN_RPP_PEAK = 21000
MEDIAN_HGI = 0.9
MEDIAN_RPP_MET = 4500

# ---------------------------
# 输入区域
# ---------------------------
st.header("Input Parameters")

HR_rest = st.number_input("Resting Heart Rate (bpm)", min_value=0.0, step=1.0)
SBP_rest = st.number_input("Resting SBP (mmHg)", min_value=0.0, step=1.0)

HR_peak = st.number_input("Peak Heart Rate (bpm) (optional)", min_value=0.0, step=1.0)
SBP_peak = st.number_input("Peak SBP (mmHg) (optional)", min_value=0.0, step=1.0)

MET_peak = st.number_input("Peak MET (optional)", min_value=0.0, step=0.1)
VO2_peak = st.number_input("VO2peak (mL/kg/min) (optional)", min_value=0.0, step=0.1)

# ---------------------------
# 计算按钮
# ---------------------------
if st.button("Calculate Risk Stratification"):

    if HR_rest > 0 and SBP_rest > 0:

        RPP_rest = HR_rest * SBP_rest
        st.subheader("Resting State")

        st.write(f"RPP rest: {RPP_rest:.0f}")

        if RPP_rest >= MEDIAN_RPP_REST:
            st.warning("High resting RPP → Higher residual risk")
        else:
            st.success("Low resting RPP → Lower residual risk")

        # ---------------------------
        # 如果输入峰值数据
        # ---------------------------
        if HR_peak > 0 and SBP_peak > 0:

            RPP_peak = HR_peak * SBP_peak
            HGI = (RPP_peak - RPP_rest) / RPP_rest

            st.subheader("Exercise State")

            st.write(f"RPP peak: {RPP_peak:.0f}")
            st.write(f"HGI: {HGI:.2f}")

            if HGI >= MEDIAN_HGI:
                st.success("High HGI → Favorable circulatory reserve")
            else:
                st.warning("Low HGI → Impaired hemodynamic gain")

            # ---------------------------
            # 如果输入MET
            # ---------------------------
            if MET_peak > 0:

                RPP_MET = RPP_peak / MET_peak
                st.subheader("Fitness-Adjusted Assessment")

                st.write(f"RPPpeak / METpeak: {RPP_MET:.0f}")

                if RPP_MET >= MEDIAN_RPP_MET:
                    st.warning("High workload per fitness → Higher risk")
                else:
                    st.success("Efficient workload response → Lower risk")

                # ---------------------------
                # 联合分层
                # ---------------------------
                st.subheader("Combined Risk Pattern")

                if HGI >= MEDIAN_HGI and RPP_MET < MEDIAN_RPP_MET:
                    st.success("Best Profile: High HGI + Low RPP/MET")
                elif HGI < MEDIAN_HGI and RPP_MET >= MEDIAN_RPP_MET:
                    st.error("Highest Risk Profile: Low HGI + High RPP/MET")
                else:
                    st.info("Intermediate Risk Profile")

        else:
            st.info("Enter peak HR and SBP to unlock exercise-state assessment.")

    else:
        st.error("Please enter at least resting HR and SBP.")