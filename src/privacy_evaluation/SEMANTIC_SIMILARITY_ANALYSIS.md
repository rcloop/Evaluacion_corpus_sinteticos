# Análisis Crítico: Similitud Semántica

## Resultados Preocupantes

### Estadísticas de Similitud Semántica

- **Total de pares con similitud ≥0.85:** 100 pares
- **Similitud mínima:** 0.9880 (98.80%)
- **Similitud máxima:** 0.9965 (99.65%)
- **Similitud promedio:** 0.9904 (99.04%)
- **Todos los pares tienen similitud ≥0.95** (95%)

### Interpretación

**Esto es MUY preocupante porque:**

1. **Similitud extremadamente alta:** 99% de similitud significa que los textos son prácticamente idénticos en significado, solo con variaciones menores de palabras.

2. **Ejemplo del par más similar (99.65%):**
   - Doc1: "Paciente que acude a consulta para seguimiento de su **proceso crónico**. Refiere estabilidad clínica general sin cambios significativos en su sintomatología basal..."
   - Doc2: "Paciente que acude a consulta para seguimiento de su **patología crónica**. Refiere estabilidad clínica general sin cambios significativos en su sintomatología basal..."
   - **Diferencia:** Solo cambia "proceso crónico" por "patología crónica" - el resto es idéntico.

3. **100 pares con similitud >99%** en un corpus de 14,035 documentos significa:
   - ~0.7% de los documentos tienen un "gemelo" casi idéntico
   - Esto sugiere que el modelo está generando textos muy similares, posiblemente por:
     - **Memorización del modelo base** (DeepSeek) de textos de entrenamiento
     - **Falta de diversidad en la generación** (el modelo se "atasca" en patrones similares)
     - **Prompts muy similares** que generan textos casi idénticos

---

## Comparación con Repetición Exacta

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| **Entidades PHI repetidas (exactas)** | 1,270 | Puede ser normal en corpus sintético |
| **Pares semánticamente similares (≥0.85)** | 100 | **MUY PREOCUPANTE** - textos casi idénticos |
| **Similitud promedio** | 99.04% | **EXTREMADAMENTE ALTA** |

---

## ¿Por qué es problemático?

### 1. **Riesgo de Privacidad**

Si los textos son casi idénticos:
- Un atacante podría identificar patrones de memorización
- Si un texto contiene PHI real, su "gemelo" también podría contenerlo
- La diversidad del corpus se ve comprometida

### 2. **Calidad del Corpus**

Un corpus con 100 pares de textos casi idénticos:
- **Reduce la utilidad** para entrenamiento de modelos
- **Sugiere falta de creatividad** en la generación
- **Indica posible memorización** del modelo base

### 3. **Implicaciones para el Paper**

**Debes documentar esto explícitamente:**
- Los resultados muestran similitud semántica extremadamente alta
- Esto puede indicar memorización del modelo base (DeepSeek)
- **Limitación importante:** Sin acceso al corpus de entrenamiento de DeepSeek, no podemos distinguir entre:
  - Memorización real de datos de entrenamiento
  - Falta de diversidad en la generación sintética

---

## Posibles Causas

### 1. **Memorización del Modelo Base (DeepSeek)**
- DeepSeek podría estar "recordando" textos médicos de su corpus de entrenamiento
- Si entrenó con textos médicos españoles, podría estar generando variaciones de textos memorizados

### 2. **Falta de Diversidad en Prompts**
- Si los prompts son muy similares, el modelo generará textos similares
- Necesitamos verificar la diversidad de los prompts de generación

### 3. **Patrones de Generación Limitados**
- El modelo podría estar "atascado" en ciertos patrones de texto
- Esto sugiere que necesita más variación en la generación

---

## Recomendaciones Urgentes

### 1. **Análisis de Diversidad de Prompts**
- Verificar si los prompts de generación son muy similares
- Si es así, aumentar la diversidad de los prompts

### 2. **Análisis de los Pares Más Similares** ✅ COMPLETADO
- ✅ Revisados manualmente los 20 pares más similares
- ✅ Identificado qué los hace similares: plantillas estructurales idénticas, variaciones mínimas, PHI compartido
- 📄 Ver: `SIMILAR_PAIRS_DETAILED_ANALYSIS.md` para análisis completo

### 2.1. **Problema Real Identificado: Repetición de Entidades PHI** ⚠️
- **100 pares semánticamente similares = 0.7% del corpus** (no es el problema principal)
- **24.7% del corpus tiene "Centro de Salud Los Álamos"** (este es el problema real)
- **41% del corpus tiene al menos 3 entidades top** (falta crítica de diversidad)
- 📄 Ver: `PHI_REPETITION_ANALYSIS.md` para análisis completo

### 3. **Canary Insertion Test Real**
- Insertar canaries únicos en los **prompts** (no en textos ya generados)
- Regenerar el corpus con canaries
- Verificar si aparecen en el corpus generado

### 4. **Documentación en el Paper**
- **Ser transparente** sobre estos resultados
- Explicar que la similitud semántica extremadamente alta es una limitación
- Discutir las posibles causas y mitigaciones

---

## Conclusión

**Actualización tras análisis completo:**

### Similitud Semántica (100 pares)
- **No es el problema principal** (solo 0.7% del corpus)
- Los pares similares comparten plantillas estructurales y variaciones mínimas
- Ver `SIMILAR_PAIRS_DETAILED_ANALYSIS.md` para detalles

### Repetición de Entidades PHI ⚠️ **ESTE ES EL PROBLEMA REAL**
- **24.7% del corpus** tiene "Centro de Salud Los Álamos"
- **41% del corpus** tiene al menos 3 entidades top
- **Solo 8 fechas únicas** en 14,035 documentos
- **Solo 8 edades únicas** en 14,035 documentos

**Conclusión:** La preocupación inicial sobre similitud semántica era válida, pero el análisis revela que el **problema crítico es la falta de diversidad en entidades PHI**, no la similitud semántica de 100 pares.

**Debe documentarse explícitamente en el paper como una limitación importante.**

---

## Próximos Pasos

1. ✅ Análisis de similitud semántica completado
2. ⏳ Revisar manualmente los pares más similares
3. ⏳ Verificar diversidad de prompts
4. ⏳ Considerar regenerar con más diversidad
5. ⏳ Documentar en el paper con transparencia


