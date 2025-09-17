# 🔧 PLC Monitor — Python + Dashboard en Tiempo Real (En Desarrollo)

Proyecto en curso: aplicación de monitoreo industrial para **PLC (Controladores Lógicos Programables)**.  
Actualmente en desarrollo con **Python**, pruebas de **Docker** y diseño inicial de la base de datos.  

---

## 🚀 Objetivo del proyecto
- 🔹 Crear un sistema que lea variables de PLC mediante protocolos industriales (ej. Modbus/TCP, OPC-UA).  
- 🔹 Mostrar la información en un **dashboard web en tiempo real**.  
- 🔹 Usar **Docker** para facilitar el despliegue en un VPS o edge device (Raspberry Pi, Orange Pi, mini-PC).  
- 🔹 Conectar a una **base de datos Postgres/Supabase** para histórico y análisis de datos.  

---

## 📌 Estado actual
- ✅ Backend inicial en Python (lectura de datos simulados).  
- ✅ Dashboard web en desarrollo (HTML/CSS/JS).  
- 🐳 **Docker** en progreso (contenedores en pruebas).  
- 🗄️ **Base de datos** en diseño (modelo de registros y alarmas).  

---

## 🧱 Tecnologías (planificadas / en pruebas)
- **Python** (FastAPI o Flask para API).  
- **Docker** (en desarrollo para contenedores de backend).  
- **Base de datos Postgres / Supabase** (en diseño).  
- **Frontend dashboard** (HTML, CSS, JS con posible framework React o Vue).  
- **Protocolos industriales**: Modbus/TCP, OPC-UA.  

---

## 🌐 Próximos pasos
- Implementar conexión con PLC real o simulado.  
- Añadir persistencia en base de datos (Postgres/Supabase).  
- Contenerizar servicios con Docker.  
- Desplegar API en VPS y UI en Vercel.  
- Crear sistema de alertas para estados críticos.  

---

💡 **Este proyecto está en progreso.**  
Demuestra mi enfoque en **automatización industrial**, **monitoreo en tiempo real** y adopción de tecnologías modernas (**Python, Docker, Supabase, Vercel**).


## 🚀 Uso

### 1. Instalar dependencias
```bash
cd api
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
