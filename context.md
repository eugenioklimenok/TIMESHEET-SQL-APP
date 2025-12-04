# CONTEXT.md – Lineamientos oficiales del proyecto TIMESHEET-SQL-APP

Este documento define **cómo deben trabajar Codex Web, Codex VS Code y cualquier agente IA** sobre este proyecto. Es un **manual técnico permanente** que asegura continuidad, coherencia y seguridad al alternar entre entornos.

> **Este archivo es parte central del proyecto.**  
> Todo agente IA debe cargarlo y seguirlo EXACTAMENTE.

---

# 1. Objetivo del proyecto
TIMESHEET-SQL-APP es una API backend basada en **FastAPI + SQLModel + PostgreSQL**.  
El objetivo es construir un MVP sólido que permita:
- gestión de usuarios
- gestión de cuentas/organizaciones
- gestión de proyectos
- administración de timesheets
- validaciones robustas
- arquitectura escalable
- control estricto mediante Roadmap

---

# 2. Fuente única de verdad
El proyecto tiene **dos fuentes oficiales de contexto**:

## **2.1. Código fuente del repositorio**  
El estado real del proyecto SIEMPRE es el que está en GitHub (o local cuando se usa VS Code).

## **2.2. `Roadmap.md`**  
Es la **única guía para la ejecución de tareas**.  
Define:
- fases
- tareas
- estado de cada una
- dependencias
- objetivos de calidad

**El agente debe seguir EXCLUSIVAMENTE este roadmap.**
No inventar tareas nuevas.  
No modificar tareas fuera de orden.

---

# 3. Reglas para el agente IA
Cualquier agente (Web o VS Code) debe trabajar bajo este protocolo.

## **3.1. Etapas obligatorias para cada tarea**
Toda acción sobre el proyecto debe realizarse en 3 etapas separadas:

### **ETAPA 1 – ANÁLISIS (solo lectura)**
El agente debe:
- leer el código relevante
- leer `Roadmap.md`
- leer `CONTEXT.md`
- NO modificar archivos
- NO hacer commits

### **ETAPA 2 – PLAN DETALLADO (sin modificar archivos)**
El agente debe:
- explicar qué hará
- enumerar los archivos que va tocar
- justificar cada modificación
- pedir confirmación explícita

### **ETAPA 3 – EJECUCIÓN (modificar archivos)**
Solo si el usuario escribe:

```
APROBAR EJECUCIÓN TAREA X
```

El agente podrá:
- modificar archivos
- actualizar `Roadmap.md` solo en la tarea asignada
- mostrar diffs completos

**Prohibido:**
- tocar fases futuras
- modificar tareas anteriores
- correr API o tests
- conectarse a bases de datos o redes externas

---

# 4. Comandos oficiales del proyecto
Estos comandos controlan al agente IA.

## **4.1. Comandos de control**
```
SOLO ANALISIS
SOLO PLAN
APROBAR EJECUCIÓN TAREA X
DETENER EJECUCIÓN
REINICIAR TAREA X
```

## **4.2. Flujos Web ↔ VS Code**
**VS Code → Web:**
- hacer commit y push
- en Codex Web: cargar Roadmap + Context + repo

**Web → VS Code:**
- hacer merge/pull request
- en VS Code: hacer pull

Los agentes NO comparten “historial de chat”.  
La sincronización SIEMPRE es por medio del repositorio y estos archivos.

---

# 5. Convenciones técnicas del proyecto

## **5.1. Identificadores**
El proyecto usa:
- `id` = UUID interno, no editable
- `code` = identificador legible por el usuario, único

Para:
- usuarios
- cuentas
- proyectos

## **5.2. Unicidad y validaciones**
Debe existir:
- unicidad en base de datos
- validación de duplicados en CRUD
- respuestas coherentes en routers

## **5.3. Estructura del código**
```
/app
  /models
  /schemas
  /crud
  /routers
  /services (a desarrollar en Fase 1 – Tarea 3)
```

## **5.4. Roadmap como contrato**
El roadmap es incremental.
No se puede:
- adelantar tareas futuras
- reordenar fases
- modificar tareas completadas

---

# 6. Normas para actualizaciones del Roadmap
Al completar una tarea, el agente debe:
- marcarla como COMPLETADA
- agregar un resumen técnico breve
- NO modificar otras tareas
- NO alterar fases no relacionadas

---

# 7. Normas para commits
El mensaje debe ser generado por IA cuando se solicite:

Formato recomendado (Conventional Commits):
```
feat(faseX-tareaY): descripción general

- puntos destacados
- decisiones técnicas claves
- impacto en modelos/schemas/crud
```

El agente **no debe crear commits automáticamente**.  
Solo modificar archivos; el usuario controla los commits.

---

# 8. Límite estricto del agente
El agente NO puede:
- ejecutar API
- abrir conexiones a PostgreSQL
- correr migraciones reales
- ejecutar código Python
- modificar archivos fuera del proyecto
- inventar fases o tareas
- alterar seguridad (JWT) antes de tiempo

---

# 9. Cómo iniciar cualquier sesión en Codex Web
El usuario debe iniciar con:

```
Codex, cargá Roadmap.md y CONTEXT.md del repositorio:
[URL del repo]
Usá estos archivos como guía oficial del proyecto.
Seguimos por la fase/tarea indicada.
```

Esto permite que Codex Web entienda el estado REAL del proyecto sin depender del historial del chat.

---

# 10. Estado actual del proyecto (actualizar manualmente si cambia)
- Fase 1 – Tarea 1 → COMPLETADA
- Fase 1 – Tarea 2 → COMPLETADA
- Próximo paso: **Fase 1 – Tarea 3** (Servicios y separación de lógica)

---

# FIN DEL CONTEXT.md
Este archivo debe mantenerse actualizado.  
Es parte crítica de la arquitectura del proyecto y del flujo de trabajo entre entornos.

