# Análisis: Repetición de Entidades PHI en el Corpus

## Resumen Ejecutivo

**Problema identificado:** Aunque no hay un triple específico de 3 entidades que aparezca exactamente en el 25% del corpus, existe un **problema crítico de falta de diversidad** en las entidades PHI generadas:

- **41% de los documentos** (5,760 de 14,035) tienen al menos 3 de las 10 entidades más repetidas
- **20.9% de los documentos** (2,934) tienen al menos 4 de las top entidades
- **8% de los documentos** (1,127) tienen al menos 5 de las top entidades

**Entidades individuales extremadamente repetidas:**
- "Centro de Salud Los Álamos": **24.7%** del corpus (3,463 documentos)
- "España": **24.2%** del corpus (3,392 documentos)
- "1234 BCD": **23.8%** del corpus (3,339 documentos)
- "12 de julio de 2023": **23.8%** del corpus (3,338 documentos)
- "+34 91 876 54 32": **23.3%** del corpus (3,265 documentos)

---

## Análisis Detallado

### 1. Entidades Individuales Más Repetidas

| Ranking | Entidad | Documentos | Porcentaje del Corpus |
|---------|---------|------------|----------------------|
| 1 | "Centro de Salud Los Álamos" | 3,463 | **24.7%** |
| 2 | "España" | 3,392 | **24.2%** |
| 3 | "1234 BCD" | 3,339 | **23.8%** |
| 4 | "12 de julio de 2023" | 3,338 | **23.8%** |
| 5 | "+34 91 876 54 32" | 3,265 | **23.3%** |
| 6 | "Grado en Medicina" | 3,254 | **23.2%** |
| 7 | "HC-2024-789012" | 3,154 | **22.5%** |
| 8 | "Comunidad Valenciana" | 3,154 | **22.5%** |
| 9 | "Laura Méndez Iglesias" | 3,049 | **21.7%** |
| 10 | "Avenida de la Constitución 12" | 2,872 | **20.5%** |

**Observación crítica:** Cada una de estas entidades aparece en aproximadamente **1 de cada 4-5 documentos**, lo que indica una falta extrema de diversidad en la generación.

### 2. Co-ocurrencia de Entidades Top

**Triple más común:**
- "1234 BCD" + "Centro de Salud Los Álamos" + "España"
- Aparece en: **263 documentos (1.9% del corpus)**

**Aunque este triple específico solo aparece en el 1.9% del corpus, el problema real es diferente:**

### 3. Documentos con Múltiples Entidades Top

| Número de Entidades Top | Documentos | Porcentaje del Corpus |
|------------------------|------------|----------------------|
| **≥3 entidades top** | **5,760** | **41.0%** |
| **≥4 entidades top** | **2,934** | **20.9%** |
| **≥5 entidades top** | **1,127** | **8.0%** |

**Interpretación:**
- Casi la mitad del corpus (41%) contiene al menos 3 de las 10 entidades más repetidas
- Esto significa que hay una **concentración masiva** de las mismas entidades en una gran proporción del corpus
- No es que un triple específico aparezca en el 25%, sino que **muchos documentos comparten múltiples entidades de un conjunto muy limitado**

### 4. Diversidad de Entidades por Tipo

| Tipo PHI | Valores Únicos | Interpretación |
|----------|----------------|----------------|
| **Person** | 125 | Baja diversidad (560 entidades repetidas) |
| **ID** | 673 | Diversidad moderada (543 entidades repetidas) |
| **Date** | **8** | **MUY BAJA DIVERSIDAD** (35 entidades repetidas) |
| **Location** | 74 | Baja diversidad (59 entidades repetidas) |
| **Phone** | 68 | Baja diversidad (52 entidades repetidas) |
| **Email** | 26 | Baja diversidad (21 entidades repetidas) |
| **Age** | **8** | **MUY BAJA DIVERSIDAD** |

**Problemas críticos:**
- **Solo 8 fechas únicas** en todo el corpus de 14,035 documentos
- **Solo 8 edades únicas** en todo el corpus
- Esto explica por qué "12 de julio de 2023" aparece en el 23.8% del corpus

---

## Implicaciones

### 1. **Falta de Diversidad en Generación**

El modelo está generando un conjunto muy limitado de valores PHI:
- Reutiliza las mismas ubicaciones, nombres, IDs, fechas, etc.
- No está creando suficiente variación en los valores sintéticos

### 2. **Riesgo de Re-identificación**

Si estas entidades aparecen en el 20-25% del corpus:
- Un atacante podría usar estas entidades como "fingerprints" para identificar documentos
- La combinación de múltiples entidades top aumenta el riesgo de re-identificación

### 3. **Memorización vs. Falta de Diversidad**

**No podemos distinguir definitivamente entre:**
- Memorización del corpus de entrenamiento de DeepSeek
- Falta de diversidad en la generación sintética

**Pero el patrón es claro:**
- Las mismas entidades aparecen en una proporción masiva del corpus
- Esto sugiere que el modelo está "atascado" en un conjunto limitado de valores

### 4. **Utilidad del Corpus para NER**

**Problema para entrenamiento de modelos NER:**
- Si el 24% del corpus tiene "Centro de Salud Los Álamos", el modelo puede sobre-aprender este patrón
- La falta de diversidad reduce la capacidad del corpus para generalizar

---

## Comparación con Similitud Semántica

**100 pares semánticamente similares (99%+ similitud):**
- Representan solo **0.7%** del corpus (100 pares de 14,035 documentos)
- **No es el problema principal**

**Repetición de entidades PHI:**
- **24.7% del corpus** tiene "Centro de Salud Los Álamos"
- **41% del corpus** tiene al menos 3 entidades top
- **Este es el problema real**

**Conclusión:** La preocupación del usuario es correcta. El problema no es la similitud semántica (100 pares), sino la **repetición masiva de entidades PHI** en una gran proporción del corpus.

---

## Recomendaciones

### 1. **Aumentar Diversidad en Generación**
- Implementar un sistema de "pool" de valores PHI más diverso
- Asegurar que cada valor PHI aparezca en menos del 5% del corpus
- Generar más variación en fechas, ubicaciones, nombres, IDs

### 2. **Filtrado de Documentos**
- Considerar filtrar documentos que contengan más de 2-3 entidades top
- Mantener solo una muestra representativa de documentos con entidades repetidas

### 3. **Análisis de Prompts**
- Verificar si los prompts de generación están limitando la diversidad
- Aumentar la variación en los ejemplos y templates

### 4. **Documentación Transparente**
- Documentar esta limitación en el paper
- Explicar que la repetición de entidades es un problema de diversidad, no necesariamente memorización
- Recomendar mejoras futuras para aumentar la diversidad

---

## Conclusión

**El problema real no es:**
- ❌ 100 pares semánticamente similares (0.7% del corpus)

**El problema real es:**
- ✅ **24.7% del corpus** tiene "Centro de Salud Los Álamos"
- ✅ **41% del corpus** tiene al menos 3 entidades top
- ✅ **Solo 8 fechas únicas** en 14,035 documentos
- ✅ **Solo 8 edades únicas** en 14,035 documentos

**Esto indica una falta crítica de diversidad en la generación de valores PHI, que es más preocupante que la similitud semántica de 100 pares de documentos.**

