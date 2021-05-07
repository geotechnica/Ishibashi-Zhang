import streamlit as st

header = st.beta_container()
description = st.beta_container()
features = st.beta_container()
plot = st.beta_container()
references = st.beta_container()

with header:
    st.title("Define and plot your soil material dynamic properities in terms of Ishibashi-Zhang")

with description:
    st.header("**Description**")

    st.markdown(">It is well known that the strain-dependent curves **G/G₀** depend mainly on soil plasticity\n in cohesive soils (Vucetic 1991)"
    " and is affected by the means of effective stress in\n cohesionless soils (Ishibashi & Zhang 1993).")


    st.latex(r'''\small\frac{G}{G_{max}} = K(\gamma)\cdot\sigma_0^{-m(\gamma)-m_0}''')

    st.markdown(">Where **K(γ)** is a decreasing function of the cyclic shear strain amplitude **γ**,\n"
            "**σ** is the mean effective confining pressure and power **m(γ)** is an increasing function of **γ**. \n"
            "**Gmax**, the maximum dynamic shear modulus is the maximum value of **G**.")

    st.latex(r'''\small m(\gamma,I_p)-m_0 = 0.272\cdot[ 1-\tanh\cdot\{\ln(\displaystyle\frac{0.000556}{\gamma})^{0.4} \})]\cdot e^{-0.0145\cdot I_p^{1.3}}''')
    st.latex(r'''\small K(\gamma,I_p) = 0.5\cdot[ 1+\tanh\cdot\{\ln(\displaystyle\frac{0.000102+n(I_p)}{\gamma})^{0.492} \})]''')

    st.latex(r'''\small
    n(I_p)=\left\{ \begin{array}{ll}
    0.0 & \textrm{for } \quad I_p = 0 \qquad\quad\text{(sandy soils)}\\
    3.37\cdot10^{-6}\cdot I_p^{1.404} & \textrm{for } \quad 0<I_p\leq15\quad\text{(low plastic soils)}\\
    7.0\cdot10^{-7}\cdot I_p^{1.976} & \textrm{for } \quad 15<I_p\leq70 \quad\text{(medium plastic soils)}\\
    2.7\cdot10^{-5}\cdot I_p^{1.115} & \textrm{for } \quad I_p>70\quad\qquad\text{(high plastic soils)}\\
    \end{array}\right.''')



with features:
    st.header("**Variable**")
    st.subheader("PI (%)")

    sel_col, disp_col = st.beta_columns(2)
    PI = sel_col.slider("Input Plasticity Index", min_value=0,max_value=200,step = 1)

    st.subheader("σm (kPa)")
    σm = int(st.text_input("Input Mean Effective Value (kPa)", 1))
    import sympy as sym
    Gmax, sst, M, K = sym.symbols("Gmax sst M K", real=True)

with plot:
    import numpy as np
    import sympy as sym
    import matplotlib.pyplot as plt


    Gmax, sst, M, K = sym.symbols("Gmax sst M K", real=True)

    def n(PI):
        if PI == 0:
            result = 0
        elif PI <= 15:
            result = (3.37 * 10 ** -6) * (PI ** 1.404)
        elif PI <= 70:
            result = (7 * 10 ** -7) * (PI ** 1.976)
        else:
            result = (2.7 * 10 ** -5) * (PI ** 1.115)
        return result

    M = 0.272 * (1 - sym.tanh(sym.ln((0.000556 / sst) ** 0.4))) * sym.exp(-0.0145 * PI ** 1.3)
    K = 0.5 * (1 + sym.tanh(sym.ln(((0.000102 + n(PI)) / sst) ** 0.492)))

    x = np.geomspace(0.000001, 0.01, 100)
    expr = K * (σm ** (M))
    y = sym.lambdify(sst, expr, "numpy")
    y = y(x)

    expr1 = (0.333 * (1 + sym.exp(-0.0145 * PI ** 1.3)) * 0.5 * (0.586 * expr ** 2 - 1.547 * expr + 1))
    D = sym.lambdify(sst, expr1, "numpy")
    D = D(x)

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.set_xlabel("Strain (%)")
    ax1.set_ylabel("Gmax/G", color="C0")
    ax2.set_ylabel('Damping Ratio', color="r")
    ax1.semilogx(x, y)
    ax2.semilogx(x, D, color="r", linestyle='dashed')
    ax1.grid(True, color='0.7', linestyle='-', which='both', axis='both')
    st.pyplot(fig)


with references:
    st.header("**Citation**")
    st.markdown("Ishibashi, I., & Zhang, X. (1993). \nUnified dynamic shear moduli and damping ratios of sand and clay.\nSoils and Foundations, 33(1), 182–191.\n(https://doi.org/10.3208/sandf1972.33.182)")


st.markdown(":arrow_forward:[Linkedin](https://www.linkedin.com/in/anilodabas/)")
st.markdown(":e-mail:[Gmail](anil.odabas@gmail.com)")
