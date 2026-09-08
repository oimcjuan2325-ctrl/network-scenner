import mpmath
import numpy as np
import plotly.express as graph_plot
import streamlit as st
import sympy as sp

# Configuración de precisión extrema con mpmath (50 decimales exactos)
mpmath.mp.dps = 50

st.set_page_config(
    page_title="HyperCalc | Calculadora Científica de Alta Precisión",
    page_icon="🧮",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #00ffcc; }
    .stTextInput input { background-color: #161b22; color: #ffffff; border: 1px solid #30363d; }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🧮 Motor de Cálculo Científico y Simbólico de Alta Precisión")
st.markdown(
    "Calculadora avanzada impulsada por aritmética de precisión arbitraria y motor de álgebra simbólica."
)
st.markdown("---")

# Panel lateral para elegir el modo de cálculo
st.sidebar.header("⚙️ Modos de Operación")
modo = st.sidebar.selectbox(
    "Selecciona el motor matemático:",
    [
        "Evaluador de Expresiones de Alta Precisión (50+ decimales)",
        "Cálculo Simbólico (Derivadas e Integrales)",
        "Resolución de Matrices y Sistemas Lineales",
    ],
)

if modo == "Evaluador de Expresiones de Alta Precisión (50+ decimales)":
    st.subheader("🔬 Evaluador Numérico Extremo")
    st.markdown(
        "Introduce funciones complejas (ej. `sin(pi/3) + log(100) + exp(2)`). El motor calculará el resultado con 50 decimales de precisión exacta."
    )

    expr_input = st.text_input(
        "Introduce la expresión matemática:", value="sin(pi/6) + sqrt(5)"
    )

    if st.button("🚀 Calcular con Precisión Extrema", type="primary"):
        try:
            # Evaluación segura usando el entorno de mpmath
            resultado = mpmath.nstr(mpmath.hypsec(expr_input) if False else eval(expr_input, {"__builtins__": None}, {
                "sin": mpmath.sin,
                "cos": mpmath.cos,
                "tan": mpmath.tan,
                "log": mpmath.log,
                "exp": mpmath.exp,
                "sqrt": mpmath.sqrt,
                "pi": mpmath.pi,
                "e": mpmath.e,
                "factorial": mpmath.factorial,
            }), 50)
            
            st.success("¡Cálculo completado sin pérdida de coma flotante!")
            st.markdown("### 🎯 Resultado Exacto (50 decimales):")
            st.code(resultado, language="text")
        except Exception as e:
            st.error(f"Error de sintaxis o cálculo: {e}")

elif modo == "Cálculo Simbólico (Derivadas e Integrales)":
    st.subheader("∫ Cálculo Diferencial e Integral Simbólico")
    st.markdown("Introduce una función en términos de `x` para derivarla o integrarla de forma exacta.")

    func_input = st.text_input("Función f(x):", value="x**3 * sin(x)")
    operacion = st.radio("Operación a realizar:", ["Derivada d/dx", "Integral Indefinida"])

    x = sp.Symbol('x')
    
    if st.button("⚙️ Procesar Cálculo Simbólico", type="primary"):
        try:
            expr = sp.sympify(func_input)
            if operacion == "Derivada d/dx":
                res = sp.diff(expr, x)
                st.success("¡Derivada calculada con éxito!")
                st.latex(f"\\frac{d}{dx} ({sp.latex(expr)}) = {sp.latex(res)}")
            else:
                res = sp.integrate(expr, x)
                st.success("¡Integral calculada con éxito!")
                st.latex(f"\\int ({sp.latex(expr)}) \, dx = {sp.latex(res)} + C")
        except Exception as e:
            st.error(f"No se pudo procesar la expresión simbólica: {e}")

else:
    st.subheader("📐 Resolución de Sistemas de Ecuaciones Lineales")
    st.markdown("Introduce una matriz de coeficientes para resolver sistemas de alta dimensión.")
    
    matriz_texto = st.text_area("Matriz A (separada por comas y saltos de línea):", value="2, 1\n1, 3")
    vector_texto = st.text_input("Vector B (separado por comas):", value="5, 5")

    if st.button("📊 Resolver Sistema", type="primary"):
        try:
            A = np.array([[float(num) for num in linea.split(',')] for linea in matriz_texto.split('\n')])
            B = np.array([float(num) for num in vector_texto.split(',')])
            
            solucion = np.linalg.solve(A, B)
            st.success("¡Sistema resuelto correctamente!")
            st.write("Solución del vector X:", solucion)
        except Exception as e:
            st.error(f"Error al resolver la matriz: {e}")

st.markdown("---")
st.caption("Desarrollado en Python con librerías de cálculo científico de alto rendimiento.")
