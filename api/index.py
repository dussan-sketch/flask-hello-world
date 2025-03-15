from flask import Flask, request, jsonify, render_template, send_from_directory
import random
import os

app = Flask(__name__)

# Respuestas brainrot predefinidas
respuestas_brainrot = [
    "no tengo neuronas suficientes para eso",
    "bro, eso es literalmente un npc moment",
    "estás pidiendo demasiado para mi cpu",
    "mi cerebro acaba de crashear 💀",
    "mi neurona está en modo overclock",
    "literalmente perdí una neurona solo por leer eso",
    "demasiadas palabras, necesito un resumen en emojis",
    "esa pregunta activó un pantallazo azul en mi mente 🖥️💥",
    "no procesé ni una sola palabra, bro",
    "mi cerebro se apagó por inactividad",
    "eso es un glitch en la matrix",
    "bro, no hay suficientes megabytes en mi cabeza para eso",
    "se me cayó el sistema operativo cerebral",
    "reboot necesario, memoria llena",
    "tengo menos lógica que un algoritmo mal programado",
    "acabo de perder una actualización de inteligencia",
    "error 404: respuesta no encontrada",
    "el buffering mental está en 99%...",
    "eso me sonó a un código encriptado",
    "mis neuronas están corriendo en 1 FPS",
    "estoy en modo ahorro de energía cerebral",
    "acabas de mandar mi cerebro al servidor de espera",
    "necesito una actualización de RAM para entender eso",
    "eso no está en mi base de datos",
    "mi sistema de pensamiento está en mantenimiento",
    "mi cerebro está descargando la respuesta, espera...",
    "me saliste con un virus de información",
    "demasiadas palabras, pásamelo en TikTok",
    "me dejaste en modo avión",
    "eso no está en mi firmware",
    "mi capacidad de procesamiento es insuficiente",
    "no tengo señal de pensamientos ahora mismo",
    "necesito un procesador más potente para entender esto",
    "mis neuronas crashearon y no quieren reiniciar",
    "respondo en 24-48 horas, mi sistema es lento",
    "mi almacenamiento de ideas está lleno",
]

# Diccionario de traducción brainrot
traducciones = {
    "hola": ["👋 SALUDOS, SER DE LUZ", "¿QUIÉN DESPERTÓ AL NPC?", "INTERFAZ HUMANA DETECTADA 🤖"],
    "voy": ["ME MUEVO A VELOCIDAD CUÁNTICA 🚀", "realizo un speedrun IRL 🏃‍♂️💨"],
    "venir": ["MODO TELETRANSPORTE EN PROGRESO ⚡", "DESPLAZAMIENTO INTERDIMENSIONAL 📍"],
    "comprar": ["HAGO TRANSACCIONES FINANCIERAS 💰", "sigma grindset activated 📈"],
    "vender": ["TRANSFERENCIA DE ACTIVOS 🔄", "COMERCIO DE ALTA VELOCIDAD 🚀"],
    "hambre": ["METABOLISMO HACIENDO SPEEDRUN 💀", "EL BUFFER DE CALORÍAS ESTÁ EN 0% ⚠️"],
    "sed": ["¡NECESITO HIDRATACIÓN! 🚰", "CRISIS DE AGUA INMINENTE 💦"],
    "comer": ["METIENDO COMBUSTIBLE AL MOTOR 🍔🚀", "NUTRIENTES OPTIMIZADOS 🧪"],
    "dormir": ["ENTRANDO EN HIBERNACIÓN 💤", "APAGANDO SISTEMA OPERATIVO XP 🔥"],
    "despierto": ["BOOTEO COMPLETADO ✅", "CARGANDO CONCIENCIA 🧠"],
    "cansado": ["BATERÍA AL 1% ⚡", "MODO AHORRO DE ENERGÍA ACTIVADO 💤"],
    "calor": ["BING CHILLING MODE OFF 🔥", "ME DERRITO COMO UN PINGÜINO EN EL DESIERTO 🌞"],
    "frío": ["PINGÜINO ACTIVADO 🐧", "CONECTANDO AL SERVIDOR DE ANTÁRTIDA ❄️"],
    "amigo": ["ALIADO EN LA SIMULACIÓN 🤝", "SOCIO ESTRATÉGICO EN EL MULTIVERSO 💼"],
    "enemigo": ["OBJETIVO HOSTIL DETECTADO ⚠️", "NPC HOSTIL EN EL RADAR 🛑"],
    "trabajar": ["MODO GRINDSET ACTIVADO 📈", "PROCESO DE EXPLOTACIÓN LABORAL EN CURSO 💼"],
    "dinero": ["PAPELES VERDES 📄💵", "CASHFLOW INTENSIFIES 💰"],
    "rico": ["BILL GATES MOMENT 🏦", "ELON MODE ACTIVADO 🚀"],
    "pobre": ["FONDOS INSUFICIENTES ❌", "LA CUENTA ESTÁ MÁS VACÍA QUE MI CEREBRO 💀"],
    "deuda": ["NIVEL DE CRÉDITO: 💀", "SALDO NEGATIVO ACTIVADO 🚨"],
    "internet": ["CONECTADO AL MAINFRAME 🌐", "LA MATRIX ME HABLA 📡"],
    "wifi": ["SEÑAL INESTABLE 📶", "CONECTANDO CON EL MULTIVERSO 🌐"],
    "computador": ["CENTRO DE PROCESAMIENTO INTELIGENTE 💻", "EL ORÁCULO DIGITAL 🔮"],
    "celular": ["EXTENSIÓN CIBERNÉTICA 📱", "SIMULADOR DE VIDA SOCIAL 📡"],
    "baño": ["RECALIBRANDO SISTEMA HIDRÁULICO 🚿", "ELIMINANDO CACHÉ CORPORAL 🛁"],
    "bañar": ["PROCESO DE PURIFICACIÓN ACTIVADO 🚿", "MODO LIMPIEZA ULTRASONIDO 🫧"],
    "música": ["VIBRACIONES ULTRADIMENSIONALES 🎵", "SINTONIZANDO RADIO GALÁCTICA 📻"],
    "cantar": ["MODO CONCIERTO EN EL BAÑO ACTIVADO 🎤", "SINTONÍA DE FRECUENCIAS SONORAS 🎶"],
    "tele": ["PORTAL DE LAVADO DE CEREBRO 📺", "DISTRACCIÓN CORPORATIVA 4K 📡"],
    "carro": ["MÁQUINA DE LOCOMOCIÓN 🔥", "MODO FAST & FURIOUS ACTIVADO 🏎️"],
    "fútbol": ["SIMULACIÓN DE PATADAS ⚽", "TORNEO DE PATADAS INTERDIMENSIONALES 🔥"],
    "zapatos": ["PROTECCIÓN PARA EL PROCESADOR HUMANO 👟", "SOPORTE PARA LA INTERFAZ DE MOVIMIENTO 🦵"],
    "correr": ["MODO VELOCISTA ACTIVADO 🏃", "SPEEDRUN IRL EN PROGRESO 🚀"],
    "volar": ["GRAVEDAD DESACTIVADA ✈️", "ACTIVANDO MODO SUPERMAN 🦸‍♂️"],
    "estudiar": ["PROCESANDO INFORMACIÓN 📚", "AUMENTANDO RAM INTELECTUAL 🧠"],
    "leer": ["DESCIFRANDO JEROGLÍFICOS 📖", "PROCESANDO TEXTO EN ALTA RESOLUCIÓN 🔎"],
    "escribir": ["DIGITANDO A 300 PALABRAS POR MINUTO ⌨️", "DESCARGANDO IDEAS AL FORMATO 2D 📝"],
}


# Lista de imágenes brainrot
imagenes_brainrot = [
    "brainrot11.jpg",
    "brainrot2.jpg",
    "brainrpt3.jpeg",
    "brainrot4.webp",
    "brainrot5.jpg"
]

# Lista de audios aleatorios
audios = ["11.m4a", "12.m4a", "13.m4a", "14.m4a", "15.m4a", "16.m4a"]

def perder_neuronas():
    """Responde preguntas con brainrot y distorsión."""
    respuesta = random.choice(respuestas_brainrot)
    return respuesta.upper() if random.random() < 0.5 else "".join(
        letra if random.random() > 0.2 else random.choice("aeiou") for letra in respuesta
    )

def traducir_a_brainrot(frase):
    """Reemplaza palabras normales por términos brainrot."""
    palabras = frase.lower().split()
    return " ".join([random.choice(traducciones[p]) if p in traducciones else p for p in palabras])

@app.route('/')
def home():
    audio_fondo = random.choice(audios)  # Selección aleatoria del audio de fondo
    return render_template('index.html', audio_fondo=audio_fondo)

@app.route('/convertir', methods=['POST'])
def convertir():
    """Maneja la conversión según el modo elegido."""
    data = request.form
    frase = data.get("frase", "").strip()
    modo = data.get("modo", "1")

    if not frase:
        return jsonify({"error": "No se ingresó una frase"}), 400

    resultado = perder_neuronas() if modo == "1" else traducir_a_brainrot(frase) if modo == "2" else None
    if resultado is None:
        return jsonify({"error": "Mod inválido"}), 400

    imagen = random.choice(imagenes_brainrot)
    audio = random.choice(audios)

    return jsonify({"respuesta": resultado, "imagen": f"/static/{imagen}", "audio": f"/static/audio/{audio}"})

if __name__ == '__main__':
    app.run(debug=True, port=3123)