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

Reglas de nombrado
- Programa: programa_isw_[AAAA]_v[VERSION].[EXT]
- Cronograma: cronograma_isw_[AAAA]_v[VERSION].[EXT]
- Presentación de cátedra: presentacion_catedra_isw_[AAAA]_v[VERSION].[EXT]
- Presentación de clase: presentacion_[NN]_[TEMA]_v[VERSION].[EXT]
- Bibliografía: bibliografia_[AUTOR]_[AAAA]_[TITULO]_v[VERSION].[EXT]
- Guía: guia_[TEMA]_[DESCRIPCION]_v[VERSION].[EXT]
- Template: template_[TIPO]_[TEMA]_v[VERSION].[EXT]
- Lineamiento: lineamiento_[TIPO]_[TEMA]_v[VERSION].[EXT]
- Trabajo práctico: tp_[NN]_4k2_g10_[TEMA]_[TIPO]_v[VERSION].[EXT]
- Trabajo de investigación: ti_[NN]_4k2_g10_[TEMA]_[TIPO]_v[VERSION].[EXT]
- Plan SCM: pgc_4k2_g10_v[VERSION].[EXT]
Convenciones
- [AAAA]: año de cuatro dígitos.
- [NN]: número correlativo de dos dígitos.
- [TEMA]: tema principal.
- [TIPO]: tipo de documento.
- [VERSION]: versión mayor.menor.
- [EXT]: extensión del archivo.
Los nombres se escriben en minúscula, sin tildes y utilizando _ como separador.

Líneas base
Las líneas base se crearán cuando se alcance un hito académico estable y validado.
Formato:
lb_[NN]_[HITO]
Ejemplos:
- lb_01_post_correcciones_tp04
- lb_02_ti01_finalizado
- lb_03_tp05_finalizado
Las líneas base se implementan mediante tags de Git asociados al commit correspondiente.