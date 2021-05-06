import streamlit as st

header = st.beta_container()
description = st.beta_container()
features = st.beta_container()
plot = st.beta_container()
references = st.beta_container()

with header:
    st.title("Define and Plot Your Soil Material Dynamic Properities in terms of Ishibashi-Zhang")


with description:
    st.title("Description")
    st.text(" It is well known that the strain-dependent curves")
    st.latex(r'''\frac{G}{G_0}''')
    st.text("depend mainly on soil plasticity\n in cohesive soils (Vucetic1991)"
            " and is affected by the means of effective stress in\n cohesionless soils (Ishibashi & Zhang 1993).")
    st.latex(r'''x^2 = \frac{n^2+n}{10}''')

with features:
    st.title("Variable")
    st.header("PI (%)")

    sel_col, disp_col = st.beta_columns(2)
    PI = sel_col.slider("Input Plasticity Index", min_value=0,max_value=200,step = 1)

    st.header("σm (kPa)")
    σm = int(st.text_input("Input Mean Effective Value (kPa)", 1))
    import sympy as sym
    Gmax, sst, M, K = sym.symbols("Gmax sst M K", real=True)

with plot:
    import numpy as np
    import sympy as sym
    import matplotlib.pyplot as plt
    st.header("Plot")

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
    st.title("References")
    st.text("Ishibashi, I., & Zhang, X. (1993). \nUnified dynamic shear moduli and damping ratios of sand and clay.\nSoils and Foundations, 33(1), 182–191.\nhttps://doi.org/10.3208/sandf1972.33.182")




