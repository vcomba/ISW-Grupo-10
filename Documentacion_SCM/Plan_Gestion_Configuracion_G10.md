# Plan de Gestión de Configuración del Software (SCM)
**Asignatura:** Ingeniería de Software (4K2)  
**Grupo:** 10  

---

## 1. Estructura del Repositorio

```text
ISW-Grupo-10/
│
├── Material_Teorico/
│   ├── Programa_Asignatura/
│   ├── Presentaciones_Clases/
│   └── Material_Bibliografico/
│       ├── Ingenieria_Software/
│       ├── SCM/
│       ├── Testing_Software/
│       ├── TDD/
│       ├── Agilismo/
│       └── Lean_Kanban/
│
├── Material_Practico/
│   ├── Guias/
│   ├── Templates/
│   └── Lineamientos_Trabajos_Investigacion/
│
├── Entregas_Grupales/
│   ├── Trabajos_Practicos_Evaluables/
│   │   ├── TP_04_SCM/
│   │   ├── TP_05_SCM_Repositorio/
│   │   ├── TP_06_TDD/
│   │   ├── TP_07_SCRUM/
│   │   ├── TP_09_Testing/
│   │   ├── TP_10_KANBAN/
│   │   ├── TP_11_SCRUM_Retrospectiva/
│   │   └── TP_12_Design_Thinking/
│   └── Trabajos_Investigacion/
│       ├── TI_01_Despliegue_Producto/
│       └── TI_02_Frameworks_Lean_Agile/
│
├── Documentacion_SCM/
│   └── Plan_Gestion_Configuracion_G10.md
├── .gitignore
└── README.md

## 2. Identificación y Reglas de Nombrado de Ítems de Configuración

| Ítem de Configuración | Regla de Nombrado | Ubicación | Tipo de Ítem de Configuración |
| :--- | :--- | :--- | :--- |
| **Programa y documentación de la asignatura** | `<nombre_material>_<aaaa>.<ext>` | `/Material_Teorico/Programa_Asignatura/` | Documentación de referencia |
| **Presentación de clase** | `<nn>_<nombre_material>.<ext>` | `/Material_Teorico/Presentaciones_Clases/` | Material teórico de referencia |
| **Bibliografía** | `<autor>_<nombre_material>.<ext>` | `/Material_Teorico/Material_Bibliografico/<nombre_tema>/` | Material bibliográfico de referencia |
| **Guía** | `guia_<nombre_material>.<ext>` | `/Material_Practico/Guias/` | Material práctico de apoyo |
| **Template** | `template_<nombre_material>.<ext>` | `/Material_Practico/Templates/` | Material práctico de apoyo |
| **Lineamiento** | `lineamientos_<nombre_material>.<ext>` | `/Material_Practico/Lineamientos_Trabajos_Investigacion/` | Material práctico de apoyo |
| **Trabajo práctico** | `tp<nn>_4k2_g10_<nombre_tema>_<nombre_tipo>.<ext>` | `/Entregas_Grupales/Trabajos_Practicos_Evaluables/TP_<nn>_<nombre_tema>/` | Entregable grupal |
| **Trabajo investigación** | `ti<nn>_4k2_g10_<nombre_tema>_<nombre_tipo>.<ext>` | `/Entregas_Grupales/Trabajos_Investigacion/TI_<nn>_<nombre_tema>/` | Entregable grupal |
| **Plan SCM** | `plan_gestion_configuracion_g10.<ext>` | `/Documentacion_SCM/` | Documentación de gestión de configuración |

---

### Convenciones de variables utilizadas:
* `<aaaa>`: Año en 4 dígitos (e.g., `2026`).
* `<nn>`: Número de clase o trabajo práctico a dos dígitos (e.g., `04`, `05`, `10`).
* `<nombre_material>` / `<nombre_tema>`: Descripción temática en minúsculas y separada por guiones bajos.
* `<nombre_tipo>`: Tipo de entregable (e.g., `informe`, `presentacion`, `enunciado`).
* `<ext>`: Extensión del archivo (`.md`, `.pdf`, `.docx`, `.pptx`, etc.).