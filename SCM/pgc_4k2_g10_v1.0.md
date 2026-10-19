# Plan de Gestión de Configuración del Software (SCM)

**Asignatura:** Ingeniería y Calidad de Software (4K2)  
**Grupo:** 10

## Estructura del repositorio

```
ISW-Grupo-10/
├── Documentacion_Academica/
│   ├── programa_isw_[AAAA]_v[VERSION].[EXT]
│   ├── cronograma_isw_[AAAA]_v[VERSION].[EXT]
│   ├── presentacion_catedra_isw_[AAAA]_v[VERSION].[EXT]
│   └── Material_Apoyo/
│       └── apoyo_[TEMA]_[DESCRIPCION]_v[VERSION].[EXT]
│
├── Material_Teorico/
│   ├── Presentaciones/
│   │   └── presentacion_[NN]_[TEMA]_v[VERSION].[EXT]
│   └── Bibliografia/
│       └── [TEMA]/
│           └── bibliografia_[AUTOR]_[AAAA]_[TITULO]_v[VERSION].[EXT]
│
├── Material_Practico/
│   ├── Guias/
│   │   └── guia_[TEMA]_[DESCRIPCION]_v[VERSION].[EXT]
│   ├── Templates/
│   │   └── template_[TIPO]_[TEMA]_v[VERSION].[EXT]
│   └── Lineamientos/
│       └── lineamiento_[TIPO]_[TEMA]_v[VERSION].[EXT]
│
├── Entregas_Grupales/
│   ├── Trabajos_Practicos/
│   │   └── TP_[NN]/
│   │       └── tp_[NN]_4k2_g10_[TEMA]_[TIPO]_v[VERSION].[EXT]
│   └── Trabajos_Investigacion/
│       └── TI_[NN]/
│           └── ti_[NN]_4k2_g10_[TEMA]_[TIPO]_v[VERSION].[EXT]
│
└── SCM/
    └── pgc_4k2_g10_v[VERSION].[EXT]
```

README.md y .gitignore son archivos de soporte y no se consideran IC.

## Reglas de nombrado

| IC | Regla | Ejemplo |
|---|---|---|
| Programa | `programa_isw_[AAAA]_v[VERSION].[EXT]` | `programa_isw_2026_v1.0.pdf` |
| Cronograma | `cronograma_isw_[AAAA]_v[VERSION].[EXT]` | `cronograma_isw_2026_v1.1.pdf` |
| Presentación de cátedra | `presentacion_catedra_isw_[AAAA]_v[VERSION].[EXT]` | `presentacion_catedra_isw_2026_v1.0.pdf` |
| Material de apoyo | `apoyo_[TEMA]_[DESCRIPCION]_v[VERSION].[EXT]` | `apoyo_evaluaciones_material_parciales_v1.0.pdf` |
| Presentación de clase | `presentacion_[NN]_[TEMA]_v[VERSION].[EXT]` | `presentacion_05_scm_v1.0.pdf` |
| Bibliografía | `bibliografia_[AUTOR]_[AAAA]_[TITULO]_v[VERSION].[EXT]` | `bibliografia_sommerville_2011_ingenieria_de_software_v1.0.pdf` |
| Guía | `guia_[TEMA]_[DESCRIPCION]_v[VERSION].[EXT]` | `guia_scm_consigna_tp04_v1.0.pdf` |
| Template | `template_[TIPO]_[TEMA]_v[VERSION].[EXT]` | `template_caso_prueba_testing_software_v1.0.xlsx` |
| Lineamiento | `lineamiento_[TIPO]_[TEMA]_v[VERSION].[EXT]` | `lineamiento_poster_investigacion_v1.0.pdf` |
| Trabajo práctico | `tp_[NN]_4k2_g10_[TEMA]_[TIPO]_v[VERSION].[EXT]` | `tp_04_4k2_g10_scm_informe_v1.0.pdf` |
| Trabajo de investigación | `ti_[NN]_4k2_g10_[TEMA]_[TIPO]_v[VERSION].[EXT]` | `ti_01_4k2_g10_design_thinking_poster_v1.0.pdf` |
| Plan SCM | `pgc_4k2_g10_v[VERSION].[EXT]` | `pgc_4k2_g10_v1.0.pdf` |

Los nombres de archivo se escriben en minúscula, sin tildes ni caracteres especiales, con `_` como separador. Todos los IC llevan versión.

## Convenciones

- **[AAAA]:** año de cuatro dígitos (2026).
- **[NN]:** número de dos dígitos con cero a la izquierda. Según la regla: número de presentación según el cronograma, número de TP, número correlativo de TI o número correlativo de línea base.
- **[TEMA]:** tema principal (scm, testing_software, design_thinking).
- **[TIPO]:** tipo de documento (informe, poster, presentacion, caso_prueba).
- **[DESCRIPCION]:** descripción breve cuando el tema no alcanza (material_parciales).
- **[AUTOR]:** apellido del autor principal (sommerville).
- **[TITULO]:** título abreviado (ingenieria_de_software).
- **[VERSION]:** mayor.menor. Todo IC entra como 1.0; el mayor sube ante cambios significativos y el menor ante cambios menores.
- **[EXT]:** extensión en minúscula, sin el punto (pdf, docx).
- **[HITO]:** evento que origina una línea base. El entregable se escribe sin guion bajo (tp04, ti01).

## Líneas base

Se crea una línea base al alcanzar alguno de estos hitos:

- Finalización y validación de cada trabajo práctico evaluable.
- Finalización y validación de cada trabajo de investigación grupal.
- Cierre de la cursada.

Un entregable está **validado** cuando cumple las reglas de este plan, fue revisado y aprobado por el grupo y fue entregado a la cátedra. Si la cátedra hace observaciones, la línea base se crea después de incorporar las correcciones (`post_correcciones_[entregable]`).

Cada línea base abarca todos los IC del repositorio en el commit etiquetado. Se implementa con un tag anotado de Git, que no se modifica ni se elimina una vez creado.

Formato: `lb_[NN]_[HITO]`

- `lb_01_post_correcciones_tp04`
- `lb_02_ti01_finalizado`
- `lb_03_tp05_finalizado`
- `lb_[NN]_cierre_cursada`