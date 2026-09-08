import socket
from datetime import datetime
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="CyberScan | Network & Port Analyzer",
    page_icon="🛡️",
    layout="wide",
)

# Estilo visual moderno (Dark/Cyberpunk touch)
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
    }
    h1 {
        color: #00ffcc;
    }
    .stMetric {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🛡️ Network & Port Security Analyzer")
st.markdown(
    "Herramienta avanzada de auditoría y reconocimiento de infraestructura de red."
)

# Sidebar para controles
st.sidebar.header("⚙️ Parámetros de Escaneo")
target_input = st.sidebar.text_input(
    "Objetivo (IP o Dominio)",
    value="scanme.nmap.org",
    help="Introduce un dominio o IP válida para analizar.",
)

# Selección de puertos comunes a escanear
port_options = {
    "Rápidos (Web & Básicos: 21, 22, 80, 443, 8080)": [
        21,
        22,
        23,
        25,
        53,
        80,
        110,
        443,
        445,
        3306,
        8080,
    ],
    "Ampliados (Top 20 comunes)": [
        21,
        22,
        23,
        25,
        53,
        80,
        110,
        135,
        139,
        443,
        445,
        993,
        995,
        1433,
        3306,
        3389,
        5432,
        8080,
        8443,
        27017,
    ],
}

selected_profile = st.sidebar.selectbox(
    "Perfil de Puertos", options=list(port_options.keys())
)
ports_to_scan = port_options[selected_profile]

scan_button = st.sidebar.button("🚀 Iniciar Escaneo de Seguridad", type="primary")

# Función para escanear puertos vía sockets de Python
def scan_ports(target, ports):
    open_ports = []
    closed_ports = 0
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        return None, "No se pudo resolver el host. Comprueba la IP o dominio."

    with st.spinner(
        f"Analizando {target} ({target_ip}) en {len(ports)} puertos..."
    ):
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.8)  # Timeout rápido
            result = s.connect_ex((target_ip, port))
            if result == 0:
                open_ports.append(port)
            else:
                closed_ports += 1
            s.close()

    return {
        "ip": target_ip,
        "open": open_ports,
        "closed": closed_ports,
        "total": len(ports),
    }, None


# Función para comprobar cabeceras HTTP de seguridad
def check_http_headers(target):
    # Asegurar formato URL
    url = (
        target
        if target.startswith("http")
        else f"https://{target.strip()}"
    )
    headers_info = {}
    try:
        response = requests.get(url, timeout=3)
        # Cabeceras clave de seguridad web
        security_headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Server",
        ]
        for header in security_headers:
            headers_info[header] = response.headers.get(
                header, "No configurado ❌"
            )
        return headers_info, None
    except Exception as e:
        return None, f"No se pudo realizar la auditoría HTTP (¿Puerto 80/443 cerrados o bloqueados?): {e}"


if scan_button:
    st.markdown("---")
    st.subheader(f"📊 Resultados del Análisis para: `{target_input}`")

    # Ejecutar escaneo de puertos
    scan_results, error = scan_ports(target_input, ports_to_scan)

    if error:
        st.error(error)
    else:
        # Métricas principales
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="IP Resuelta", value=scan_results["ip"]
            )
        with col2:
            st.metric(
                label="Puertos Abiertos Detectados",
                value=len(scan_results["open"]),
            )
        with col3:
            st.metric(
                label="Puertos Seguros/Cerrados",
                value=scan_results["closed"],
            )

        # Visualización gráfica de los puertos con Plotly
        st.markdown("### 📈 Distribución del Estado de Puertos")
        status_data = pd.DataFrame(
            {
                "Estado": ["Abiertos", "Cerrados/Filtrados"],
                "Cantidad": [
                    len(scan_results["open"]),
                    scan_results["closed"],
                ],
            }
        )

        fig = px.pie(
            status_data,
            names="Estado",
            values="Cantidad",
            hole=0.4,
            color="Estado",
            color_discrete_map={
                "Abiertos": "#ff4b4b",
                "Cerrados/Filtrados": "#00ffcc",
            },
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Detalle de puertos abiertos
        st.markdown("### 🔍 Detalle de Servicios Activos")
        if scan_results["open"]:
            # Diccionario común de servicios por puerto
            common_services = {
                21: "FTP (File Transfer)",
                22: "SSH (Secure Shell)",
                23: "Telnet (Inseguro)",
                25: "SMTP (Correo)",
                53: "DNS (Domain Name System)",
                80: "HTTP (Web sin cifrar)",
                110: "POP3",
                135: "RPC",
                139: "NetBIOS",
                443: "HTTPS (Web Segura SSL)",
                445: "Microsoft-DS (SMB)",
                1433: "SQL Server",
                3306: "MySQL Database",
                3389: "RDP (Escritorio Remoto)",
                5432: "PostgreSQL",
                8080: "HTTP Proxy / Alt Web",
                8443: "HTTPS Alt",
            }

            port_data = []
            for p in scan_results["open"]:
                service_name = common_services.get(
                    p, "Servicio Desconocido / Personalizado"
                )
                port_data.append(
                    {
                        "Puerto": p,
                        "Protocolo": "TCP",
                        "Servicio Asociado": service_name,
                        "Estado": "⚠️ Abierto",
                    }
                )

            st.dataframe(pd.DataFrame(port_data), use_container_width=True)
        else:
            st.success(
                "¡Excelente! No se han detectado puertos abiertos en el rango seleccionado."
            )

        # Auditoría de Cabeceras HTTP (Extra técnico que flipará al profesor)
        st.markdown("---")
        st.subheader("🌐 Auditoría de Cabeceras HTTP de Seguridad")
        headers_result, h_error = check_http_headers(target_input)

        if h_error:
            st.info(h_error)
        else:
            h_df = pd.DataFrame(
                list(headers_result.items()),
                columns=["Cabecera de Seguridad", "Estado / Valor"],
            )
            st.table(h_df)

    st.markdown("---")
    st.caption(
        f"Análisis completado a las {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Creado con Streamlit & Python."
    )
else:
    st.info(
        "👈 Introduce un objetivo en la barra lateral y haz clic en **'Iniciar Escaneo de Seguridad'** para comenzar."
    )
