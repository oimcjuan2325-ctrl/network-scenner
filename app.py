import mpmath
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import sympy as sp

# Configuración de precisión
mpmath.mp.dps = 30

st.set_page_config(
    page_title="HyperCalc | Consola Científica Avanzada",
    page_icon="🧮",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #00ffcc; }
    .stTextInput input, .stTextArea textarea { 
        background-color: #161b22; 
        color: #00ffcc; 
        border: 1px solid #30363d; 
        font-family: monospace;
        font-size: 1.1rem;
    }
    div.stButton > button {
        background-color: #21262d;
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 6px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #30363d;
        color: #00ffcc;
        border-color: #00ffcc;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🧮 Consola Científica de Precisión & Motor Simbólico")
st.markdown(
    "Sistema de cálculo avanzado con teclado de símbolos matemáticos y representación en plano cartesiano interactivo."
)
st.markdown("---")

# Modo de operación principal
modo = st.sidebar.selectbox(
    "Modo de Operación:",
    [
        "Cálculo Simbólico, Derivadas/Integrales y Plano Cartesiano",
        "Evaluador Numérico de Alta Precisión (30+ decimales)",
        "Resolución de Matrices y Sistemas Lineales",
    ],
)

if modo == "Cálculo Simbólico, Derivadas/Integrales y Plano Cartesiano":
    st.subheader("∫ Motor Simbólico y Visualización Gráfica")
    st.markdown(
        "Introduce una función en términos de `x`. Puedes usar el teclado de símbolos para ayudarte."
    )

    # Estado de sesión para conservar la función si se pulsa un botón de símbolo
    if "expr_val" not in st.session_state:
        st.session_state.expr_val = "x**3 - 3*x"

    # --- TECLADO VIRTUAL DE SÍMBOLOS MATEMÁTICOS ---
    st.markdown("**⌨️ Teclado de Símbolos Rápidos:**")
    c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11 = st.columns(11)

    # Nota: Streamlit recarga al pulsar un botón, usamos callbacks o actualizamos session_state
    def add_symbol(sym):
        st.session_state.expr_val += sym

    if c1.button("x"):
        add_symbol("x")
    if c2.button("+"):
        add_symbol("+")
    if c3.button("-"):
        add_symbol("-")
    if c4.button("*"):
        add_symbol("*")
    if c5.button("/"):
        add_symbol("/")
    if c6.button("^"):
        add_symbol("**")
    if c7.button("sin("):
        add_symbol("sin(x)")
    if c8.button("cos("):
        add_symbol("cos(x)")
    if c9.button("log("):
        add_symbol("log(x)")
    if c10.button("exp("):
        add_symbol("exp(x)")
    if c11.button("Clear"):
        st.session_state.expr_val = ""

    # Cuadro de entrada conectado al state
    func_input = st.text_input("Función f(x):", key="expr_val")

    operacion = st.radio(
        "Operación analítica:",
        ["Derivada d/dx", "Integral Indefinida", "Solo Graficar Función"],
        horizontal=True,
    )

    x = sp.Symbol("x")

    if st.button("🚀 Procesar Análisis y Plano Cartesiano", type="primary"):
        try:
            expr = sp.sympify(func_input)

            # Mostrar resultado analítico según la opción
            st.markdown("---")
            st.subheader("📊 Resultados Analíticos")

            resultado_calculo = expr
            if operacion == "Derivada d/dx":
                resultado_calculo = sp.diff(expr, x)
                st.latex(
                    f"\\frac{{d}}{{dx}} \\left( {sp.latex(expr)} \\right) = {sp.latex(resultado_calculo)}"
                )
            elif operacion == "Integral Indefinida":
                resultado_calculo = sp.integrate(expr, x)
                st.latex(
                    f"\\int \\left( {sp.latex(expr)} \\right) \\, dx = {sp.latex(resultado_calculo)} + C"
                )
            else:
                st.latex(f"f(x) = {sp.latex(expr)}")

            # --- PLANO CARTESIANO INTERACTIVO ---
            st.markdown("---")
            st.subheader("📈 Plano Cartesiano (Gráfica Interactiva)")

            # Convertir la expresión de SymPy a una función numérica utilizable en NumPy
            f_lambdified = sp.lambdify(x, expr, modules=["numpy"])

            # Rango del eje X para el plano cartesiano
            x_vals = np.linspace(-10, 10, 400)
            try:
                y_vals = f_lambdified(x_vals)

                # Crear gráfica con Plotly (Plano cartesiano profesional)
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=x_vals,
                        y=y_vals,
                        mode="lines",
                        name=f"f(x) = {func_input}",
                        line=dict(color="#00ffcc", width=3),
                    )
                )

                # Configurar ejes estilo plano cartesiano (con líneas de referencia en 0)
                fig.update_layout(
                    title="Representación en el Plano Cartesiano 2D",
                    xaxis_title="Eje X",
                    yaxis_title="Eje Y",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="#161b22",
                    font_color="white",
                    xaxis=dict(
                        zeroline=True,
                        zerolinewidth=2,
                        zerolinecolor="gray",
                        gridcolor="#30363d",
                    ),
                    yaxis=dict(
                        zeroline=True,
                        zerolinewidth=2,
                        zerolinecolor="gray",
                        gridcolor="#30363d",
                    ),
                )

                st.plotly_chart(fig, use_container_width=True)

            except Exception as plot_err:
                st.warning(
                    f"No se pudo renderizar la gráfica para este rango: {plot_err}"
                )

        except Exception as e:
            st.error(f"Error de sintaxis matemática: {e}")

elif modo == "Evaluador Numérico de Alta Precisión (30+ decimales)":
    st.subheader("🔬 Evaluador Numérico Extremo")
    expr_num = st.text_input(
        "Introduce expresión:", value="sin(pi/6) + sqrt(10)"
    )
    if st.button("Calcular con 30 decimales", type="primary"):
        try:
            res = mpmath.nstr(
                eval(
                    expr_num,
                    {"__builtins__": None},
                    {
                        "sin": mpmath.sin,
                        "cos": mpmath.cos,
                        "tan": mpmath.tan,
                        "log": mpmath.log,
                        "exp": mpmath.exp,
                        "sqrt": mpmath.sqrt,
                        "pi": mpmath.pi,
                        "e": mpmath.e,
                    },
                ),
                30,
            )
            st.success("Resultado de alta precisión:")
            st.code(res, language="text")
        except Exception as e:
            st.error(f"Error: {e}")

else:
    st.subheader("📐 Resolución de Sistemas Lineales")
    matriz_txt = st.text_area("Matriz A (ej: 2,1 / 1,3):", value="2, 1\n1, 3")
    vector_txt = st.text_input("Vector B (ej: 5,5):", value="5, 5")
    if st.button("Resolver Sistema", type="primary"):
        try:
            A = np.array(
                [[float(n) for n in l.split(",")] for l in matriz_txt.split("\n")]
            )
            B = np.array([float(n) for n in vector_txt.split(",")])
            sol = np.linalg.solve(A, B)
            st.success("Solución del sistema:")
            st.write(sol)
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption(
    "Motor de cálculo simbólico y visualización matemática impulsado por Python."
)
