# app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# ----------------------------------------
# Configuración de la página
# ----------------------------------------
st.set_page_config(
    page_title="Informe Scouting – José Daniel Layon Morito",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------
# CSS inline para estilo FIFA avanzado y botones
# ----------------------------------------
st.markdown("""
<style>
/* Contenedor general de la card */
.fifa-card {
    display: flex;
    max-width: 900px;
    margin: 40px auto;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    font-family: 'Helvetica Neue', Arial, sans-serif;
}
/* Lado izquierdo: degradado, foto, overall, posición */
.fifa-card__left {
    position: relative;
    width: 280px;
    background: linear-gradient(135deg, #1f4e78 0%, #133b5c 100%);
    color: #fff;
    text-align: center;
    padding: 20px 0;
}
.fifa-card__left img.photo {
    width: 160px; height: 160px;
    object-fit: cover;
    border-radius: 50%;
    border: 4px solid #fff;
}
.fifa-card__left .overall {
    position: absolute; top: 20px; left: 20px;
    font-size: 60px; font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}
.fifa-card__left .position {
    position: absolute; bottom: 20px; left: 50%;
    transform: translateX(-50%);
    font-size: 18px; text-transform: uppercase;
    letter-spacing: 2px; background: rgba(0,0,0,0.3);
    padding: 4px 12px; border-radius: 12px;
}
/* Lado derecho: datos, escudo, líneas, vídeos */
.fifa-card__right {
    flex: 1; background: #f4f4f4; padding: 32px 40px;
    position: relative;
}
.fifa-card__right img.team-badge {
    position: absolute; top: 32px; right: 32px;
    width: 80px; height: 80px; object-fit: contain;
}
.fifa-card__right h2 { margin: 0 0 8px; font-size: 32px; color: #333; }
.fifa-card__right h4 { margin: 4px 0 16px; font-size: 16px; color: #666; }
.fifa-card__right .info { display: flex; gap: 24px; margin-bottom: 24px; }
.fifa-card__right .info .label {
    font-size: 12px; text-transform: uppercase; color: #888; margin-bottom: 4px;
}
.fifa-card__right .info .value {
    font-size: 20px; color: #333; font-weight: bold;
}
.fifa-card__right .videos { margin-top: 24px; }
.fifa-card__right .videos li { margin-bottom: 6px; }
.fifa-card__right .videos a {
    color: #1f4e78; text-decoration: none;
}
.fifa-card__right .videos a:hover { text-decoration: underline; }
/* Botones más atractivos */
.stButton>button {
    background-color: #1f4e78; color: white;
    padding: 0.6em 1.2em; border-radius: 8px; font-size: 1rem;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------
# Datos del jugador
# ----------------------------------------
jugador = {
    "nombre": "José Daniel Layon Morito",
    "equipo": "CD Estepona",
    "categoria": "3ª Andaluza Cadete Grupo II",
    "valoracion": 3,                # de 1 a 5
    "posicion": "ED / EI",         # Extremo Derecho / izquierdo
    "foto_url": "https://i.imgur.com/24D328z.jpg",
    "escudo_url": "https://cdn.resfu.com/img_data/equipos/19064.png?size=120x&lossy=1",
    "videos": [
        "https://youtu.be/MYWt92AlwxM",
        "https://www.youtube.com/watch?v=L8jEzb29Du8",
        "https://youtu.be/IXqVLvHs-MU",
        "https://youtu.be/RZFe9J05mR4",
        "https://youtu.be/AeSPCk62nmo"
    ],
    "radar": {"Ritmo":7, "Físico":7, "Defensa":5, "Regate":8, "Pase":7, "Tiro":7},
    "partidos": [
        {
            "titulo": "⚽ UD San Pedro vs CD Estepona",
            "rival": "UD San Pedro",
            "resultado": "0 – 2",
            "rol": "Extremo derecho / izquierdo",
            "valoracion": 3,
            "informe": {
                "comentario": "Partido complicado; ingresó a los 15’ y desbordó con peligro.",
                "actuacion": {
                    "sistema_juego": "4-4-2",
                    "rol": "Extremo derecho",
                    "desempeno": "Gran desborde y centros medidos; bajón tras 60’.",
                    "participacion": "Activo 75 minutos.",
                    "liderazgo": "Debería alzar la voz en el grupo."
                }
            }
        },
        {
            "titulo": "⚽ CD Atlético Marbelli vs CD Estepona",
            "rival": "CD Atlético Marbelli",
            "resultado": "1 – 8",
            "rol": "Extremo / Extremo izquierdo",
            "valoracion": 5,
            "informe": {
                "comentario": "Exhibición ofensiva: 2 goles y 1 asistencia.",
                "actuacion": {
                    "sistema_juego": "4-3-3 ofensivo",
                    "rol": "Interior derecho",
                    "desempeno": "Desequilibrio constante, pases de gol precisos.",
                    "participacion": "Protagonista total.",
                    "liderazgo": "Tomó responsabilidades en momentos clave."
                }
            }
        },
        {
            "titulo": "⚽ Marbella CF vs CD Estepona",
            "rival": "Marbella CF",
            "resultado": "3 – 2",
            "rol": "Extremo derecho",
            "valoracion": 4,
            "informe": {
                "comentario": "Dos incursiones letales y entendimiento táctico.",
                "actuacion": {
                    "sistema_juego": "4-3-3",
                    "rol": "Extremo derecho",
                    "desempeno": "Dominó banda y generó superioridad.",
                    "participacion": "100% del tiempo.",
                    "liderazgo": "Impuso carácter tras empate."
                }
            }
        },
        {
            "titulo": "⚽ Estación de Cártama vs CD Estepona",
            "rival": "Estación de Cártama",
            "resultado": "1 – 2",
            "rol": "Extremo derecho",
            "valoracion": 3,
            # 
        }
    ]
}

# ----------------------------------------
# Sidebar de navegación
# ----------------------------------------
secciones = [
    "Datos Generales",
    "Resumen de Partidos",
    "Perfil & Liderazgo",
    "Análisis Técnico",
    "Análisis Táctico",
    "Análisis Físico",
    "Conclusiones"
]
choice = st.sidebar.radio("🎯 Sección", secciones)

# ----------------------------------------
# 1. Datos Generales
# ----------------------------------------
if choice == "Datos Generales":
    st.markdown(f"""
    <div class="fifa-card">
      <div class="fifa-card__left">
        <div class="overall">15</div></br></br>
        <img class="photo" src="{jugador['foto_url']}" alt="Foto jugador"/>
        <div class="position">{jugador['posicion']}</div>
      </div>
      <div class="fifa-card__right">
        <img class="team-badge" src="{jugador['escudo_url']}" alt="Escudo equipo"/>
        <h2>{jugador['nombre']}</h2>
        <h4>{jugador['equipo']} ― {jugador['categoria']}</h4>
        <div class="info">
          <div><div class="label">Valoración</div><div class="value">{'⭐'*jugador['valoracion']} ({jugador['valoracion']}/5)</div></div>
          <div><div class="label">Posición</div><div class="value">{jugador['posicion']}</div></div>
        </div>
        <hr style="border:none; border-top:1px solid #ddd; margin:0 0 16px;">
        <h4>📹 Vídeos de Análisis</h4>
        <ul class="videos">
          {''.join(f'<li><a href="{u}" target="_blank">{u}</a></li>' for u in jugador['videos'])}
        </ul>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------
# 2. Resumen de Partidos
# ----------------------------------------
elif choice == "Resumen de Partidos":
    st.title("📊 Resumen de Partidos")
    df = pd.DataFrame([
        {
            "Partido": p["titulo"],
            "Resultado": p["resultado"],
            "Rol principal": p["rol"],
            "Valoración": f"{p['valoracion']}/5"
        }
        for p in jugador["partidos"]
    ])
    st.dataframe(df, use_container_width=True)

# ----------------------------------------
# 3. Perfil & Liderazgo
# ----------------------------------------
elif choice == "Perfil & Liderazgo":
    st.title("🧠 Perfil & Liderazgo")
    st.markdown("""
- **🔭 Visión y Posicionamiento**  
  - Estira la defensa rival ganando metros en banda y abre pasillos interiores con movimientos de ruptura.  
  - Lee las líneas de pase y utiliza su cuerpo para cerrar carriles de circulación, forzando al oponente a jugar hacia zonas congestionadas.  
  - En fase defensiva, se repliega con criterio, cubriendo la espalda del lateral y cerrando espacios entre líneas.

- **🚀 Iniciación de Juego**  
  - Domina el timing de recepción para recibir espalda a la defensa y girarse con un control orientado.  
  - Combina conducción en conducción en velocidad media con pases al primer toque de máxima eficacia.  
  - Rompe la primera línea de presión con envíos filtrados o conducciones directas hacia la zona de creación.

- **📣 Comunicación y Mando**  
  - Debe elevar su voz para coordinar coberturas, avisar de desmarques y ordenar salidas en bloque alto. Cuando llevan un resultado adverso se le nota nervioso y suele salirse del partido.  
  - Una comunicación más constante reforzará la cohesión del equipo y evitará despistes en fases críticas.

- **🔄 Versatilidad Táctica**  
  - **Extremo puro:** Explota la línea de cal, busca desbordes en carrera y centra buscando principalmente primer palo o punto de penalti.  
  - **Extremo a pierna cambiada:** Juega a veces a pierna cambiada en el extremo izquierdo donde enera superioridad numérica y ejecuta disparos lejanos buscando sorprender y siempre terminando jugadas.  
  - Su polivalencia le permite adaptarse a otos sistemas donde pensamos que puede jugar tambien como mediapunta o incluso de falso 9.

- **💡 Liderazgo en el Terreno de Juego**   
  - Lidera con sacrificio en el trabajo sin balón: corre, presiona y recupera balones que marcan el pulso del encuentro.  
  - Debe potenciar su rol de líder positivo, animando a los compañeros en caídas y celebrando colectivamente los éxitos.
    """)


# ----------------------------------------
# 4. Análisis Técnico
# ----------------------------------------
elif choice == "Análisis Técnico":
    st.title("⚙️ Análisis Técnico")
    st.markdown("""
#### ⚡ Manejo de Balón & Desborde  
- **1vs1 Rotundo:** Ejecuta cambios de orientación y amortigua el balón con el pie fuerte, protegiendo el cuero como un auténtico ‘pegamento’ en banda.  
- **Conducción Dinámica:** Salidas en carrera con balón al pie que desarman la presión rival, alternando toques cortos y arrancadas explosivas.  

#### 🎯 Pases & Asistencia  
- **Visión de Pases Interiores:** Auna capacidad de pase corto como largo y sabe buscar esos centros o espacios vacios donde puede entrar un compañero para aprovechar ese espacio y generar peligro.  
- **Asistencia:** Cuando juega de extremo derecho en la mayor parte de ocasiones su jugada mas repetida es entrada hasta linea de fondo a veces conduciendo o bien tras recibir balon largo y esa conduccion por linea de fondo termina con un "pase de la muerte" que nada mas tiene que ser empujgado por su compañero.  
- **Una marcha mas:** Tiene capacidad para tener mas ritmo y ese ritmo le hará no perder oportunidades. A veces balones que parecen que se va a hacer con el, no llega o si llega tras control tiene una perdida. Eso puede ser fruto de falta de determinación y confianza.

#### 🎵 Regate & Cambio de Ritmo  
- **Sorpresa en el Arranque:** Despliega un cambio de ritmo vertiginoso al primer toque, ‘rompiendo’ al defensor con arrancadas en vertical. Tiene habilidad en el 1vs1.
- **Ritmo Intermitente:** Sabe dosificar la velocidad, alternando sprint y pausa para descolocar líneas defensivas. Puede ser mas protagonista si quiere. 

#### 🔧 Primer Pase  
- **Primer Toque Letal:** Despliega un primer pase orientado hacia el espacio con peso y dirección precisos, abriendo líneas de pase y facilitando el diseño de ataques combinativos.

#### 
    """)

    # Radar chart
    cats = list(jugador["radar"].keys())
    vals = list(jugador["radar"].values())
    angles = np.linspace(0, 2*np.pi, len(cats), endpoint=False).tolist()
    vals += vals[:1]; angles += angles[:1]
    fig, ax = plt.subplots(figsize=(5,5), subplot_kw=dict(polar=True))
    ax.plot(angles, vals, linewidth=2)
    ax.fill(angles, vals, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), cats)
    ax.set_ylim(0,10)
    st.pyplot(fig)

# ----------------------------------------
# 5. Análisis Táctico
# ----------------------------------------
elif choice == "Análisis Táctico":
    st.title("🗺️ Análisis Táctico")
    st.markdown("""
**Sistemas predominantes**  
- 4-4-2 tradicional con amplitud de banda. Buscando llegadas a linea de fondo y centros.
- Variante 4-3-3 para potenciar carriles interiores y en este caso aprovechar espacios por dentro y buscar lanzamientos.

**Funciones clave**  
- **Extremo Derecho:** Genera superioridad y centros al área.  
- **Extremo izquierdo:** Incursión central y creación de espacios. Busca lanzamiento desde ese perfil por dentro.

**Áreas de mejora**  
- Mayor agresividad en presión alta. Mayor capacidad fisica para aguantar "embistes" del rival. Le hacen muchas faltas, casi todas lo son pero debe de intentar aguantar esas embestidas a veces. Esta en una edad para trabajar ese aspecto.  
- Concentración. No salirse del partido, pese a resultados encontrar. Denotamos que a medida que el partido avanza y si tiene resultado en contra baja mucho el rendimiento por estar "ausente" y el equipo lo nota.
    """)
    st.markdown("### Mapa de Posición Principal")
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#aabb97', line_color='white')
    fig, ax = pitch.draw(figsize=(8,6))
    # Ubicación aproximada en banda derecha
    ax.scatter(100, 72, s=300, color='#1f4e78', edgecolors='white', linewidth=2)
    ax.scatter(90, 20, s=300, color='#1f4e78', edgecolors='white', linewidth=2)
    ax.text(100, 78, "José Daniel", ha='center', color='white', weight='bold')
    ax.text(90, 25, "José Daniel", ha='center', color='white', weight='bold')
    st.pyplot(fig)

# ----------------------------------------
# 6. Análisis Físico
# ----------------------------------------
elif choice == "Análisis Físico":
    st.title("💪 Análisis Físico")
    st.markdown("""
- **🔋 Resistencia Aeróbica:**  
  Exhibe un fondo físico muy sólido durante los primeros 60–70 minutos, manteniendo intensidad en la presión y cobertura de línea. No obstante, en los últimos 15 minutos se aprecia un descenso en la capacidad de reenganche y ritmo de ayudas, especialmente tras esfuerzos intensos. 

- **⚡ Velocidad & Aceleración:**  
  Demuestra explosividad sobresaliente en arrancadas cortas de 5–15 m, ganando metros con facilidad en carrera en línea recta. Además, su aceleración sostenida en distancias medias (20–30 m) le permite incorporarse al ataque y cerrar espacios en contragolpes.

- **🔨 Fuerza & Duelo Corporal:**  
  Con una complexión atlética, muestra buen centro de gravedad para proteger balón en el cuerpo a cuerpo. Sin embargo, en duelos de contacto prolongado tiende a ceder terreno.

- **🤸‍♂️ Agilidad & Equilibrio:**  
  Sobresale en cambios de orientación y regates en espacios cortos, manteniendo una base sólida y rápida recuperación post-finta. Su capacidad para girarse bajo presión y retomar la verticalidad destaca;

- **⚙️ Respuesta Anaeróbica:**  
  Su capacidad para encadenar esfuerzos de alta intensidad es notable, aunque la acumulación de metros en el tramo final penaliza un poco su punch defensivo. 


- **🏃‍♂️ Participación Física en Juego:**  
  Su implicación en la presión alta y repliegues es evidente, recorriendo zonas amplias de la banda. Para maximizar su rendimiento, podría reforzar su intensidad de sprint tras pérdida y su presencia en zonas de rechace, convirtiéndose en un pulmón ofensivo y defensivo durante los 90 minutos.
    """)


# ----------------------------------------
# 7. Conclusiones
# ----------------------------------------
elif choice == "Conclusiones":
    st.title("✅ Conclusiones & Recomendaciones")
    st.markdown("""
**Fortalezas**  
- Desborde 1vs1 , asosiciaciones con delantero o enlace es de lo mas destacado. Palpamos buen golpeo de balon pero nos ha faltado ver más en ese aspecto.  
- Cambio de ritmo, velocidad "eléctrico" y visión de pase. Anticipa jugadas. Tiene buen manejo de balón y técnicamente es un jugador destacado en su categoria. 

**Áreas de mejora**  
1. Pases largos y jugar mas buscando porteria rival. Tiene llegada al area y tiene que hacer mas goles.  
2. Mejorar el aspecto táctico y emocional. 
3. Nos gustaria ver el rendimiento de José Daniel en categorias de Cadete más relevantes. 


    """)



