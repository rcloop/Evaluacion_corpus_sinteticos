# Análisis Detallado: Memorization Detection

## Resumen Ejecutivo

**Total de entidades PHI únicas repetidas: 1,270**

El análisis de memorization detection revela patrones significativos de repetición de entidades PHI en el corpus generado. Esto puede indicar:
1. **Memorización del modelo base** (DeepSeek) de datos de entrenamiento
2. **Patrones de generación sintética** (reutilización de valores limitados)
3. **Ejemplos hardcodeados en el pipeline de generación**

---

## Desglose por Categoría PHI

| Categoría | Entidades Únicas Repetidas | Interpretación |
|-----------|----------------------------|----------------|
| **Person** | 560 | Nombres de pacientes y personal sanitario |
| **ID** | 543 | Identificadores, números de historia clínica, códigos |
| **Location** | 59 | Ubicaciones geográficas, centros de salud |
| **Date** | 35 | Fechas específicas |
| **Phone** | 52 | Números de teléfono |
| **Email** | 21 | Direcciones de correo electrónico |

---

## Top 10 Entidades Más Repetidas

### 1. **"Centro de Salud Los Álamos"** (Location)
- **3,463 ocurrencias** en múltiples documentos
- Aparece en ~24.7% de los 14,035 documentos
- **Análisis**: Nombre de centro sanitario muy repetido

### 2. **"España"** (Location)
- **3,392 ocurrencias**
- Aparece en ~24.2% de los documentos
- **Análisis**: País de referencia común

### 3. **"1234 BCD"** (ID)
- **3,339 ocurrencias**
- **Análisis**: Identificador de vehículo sanitario muy repetido

### 4. **"12 de julio de 2023"** (Date)
- **3,338 ocurrencias**
- **Análisis**: Fecha específica extremadamente repetida

### 5. **"Salud Los Álamos"** (Person/Location - posible error de etiquetado)
- **3,459 ocurrencias**
- **Análisis**: Variante del nombre del centro sanitario

### 6. **"789012"** (ID)
- **3,315 ocurrencias**
- Parte de números de historia clínica (HC-2024-789012)
- **Análisis**: Patrón numérico muy repetido

### 7. **"Comunidad Valenciana"** (Location)
- **3,154 ocurrencias** (person) + **3,154 ocurrencias** (location)
- **Análisis**: Región geográfica muy repetida

### 8. **"HC-2024-789012"** (ID)
- **3,154 ocurrencias**
- **Análisis**: Número de historia clínica específico muy repetido

### 9. **"Laura Méndez Iglesias"** (Person)
- **3,049 ocurrencias**
- Aparece en ~21.7% de los documentos
- **Análisis**: Nombre de paciente extremadamente repetido

### 10. **"+34 91 876 54 32"** (Phone)
- **3,265 ocurrencias**
- **Análisis**: Número de teléfono muy repetido

---

## Análisis de Causas Potenciales

### 1. **Ejemplos en el Pipeline de Generación**

**Hallazgo**: En `step1_generate_annotations.py` se encontraron valores hardcodeados:
- `"Dra. Elena Rodríguez Martínez"` (y variantes)
- `"123456789"` (y variantes de números de beneficiario)

**Impacto**: Si estos valores aparecen frecuentemente en las anotaciones generadas, el modelo los repetirá en los documentos.

### 2. **Patrones de Generación Sintética**

**Observación**: Algunas entidades como "1234 BCD", "789012", "HC-2024-789012" sugieren:
- Uso de un conjunto limitado de valores sintéticos
- Posible generación determinística o pseudoaleatoria con semillas limitadas

### 3. **Memorización del Modelo Base (DeepSeek)**

**Hipótesis**: Si "Laura Méndez Iglesias" aparece 3,049 veces sin estar explícitamente en los prompts:
- Podría ser memorización del corpus de entrenamiento de DeepSeek
- O podría estar presente en ejemplos del prompt que no hemos identificado

**Evidencia a favor**:
- Nombres españoles comunes ("Laura", "Méndez", "Iglesias") podrían estar en el corpus de entrenamiento
- El modelo podría estar "completando" patrones conocidos

**Evidencia en contra**:
- Si fuera memorización pura, esperaríamos ver más variación
- La repetición sistemática sugiere más bien un patrón de generación

---

## Interpretación de Resultados

### ¿Es Normal esta Repetición?

**Para un corpus sintético de 14,035 documentos:**

1. **Repetición de valores sintéticos**: ✅ **ESPERADO**
   - Si el pipeline genera un conjunto limitado de nombres/IDs sintéticos
   - Es normal que se reutilicen en múltiples documentos
   - **Ejemplo**: Si solo generas 100 nombres diferentes, cada uno aparecerá ~140 veces en promedio

2. **Repetición extrema de valores específicos**: ⚠️ **REQUIERE INVESTIGACIÓN**
   - "Laura Méndez Iglesias" en 3,049 documentos (21.7%) es muy alto
   - "12 de julio de 2023" en 3,338 documentos (23.8%) es sospechoso
   - **Posibles causas**:
     - Ejemplos hardcodeados en prompts
     - Semillas de generación limitadas
     - Memorización del modelo base

### Nivel de Riesgo: **CRÍTICO**

**Razones**:
1. **1,270 entidades PHI únicas repetidas** es un número significativo
2. **Algunas entidades aparecen en >20% de los documentos**
3. **Sin acceso al corpus de entrenamiento de DeepSeek**, no podemos distinguir entre:
   - Memorización real del modelo base
   - Patrones de generación sintética esperados

---

## Recomendaciones

### 1. **Verificar Prompts y Ejemplos**
- Revisar si "Laura Méndez Iglesias", "Los Álamos", "1234 BCD" aparecen en:
  - Prompts de generación
  - Ejemplos en el código
  - Plantillas de documentos

### 2. **Análisis de Diversidad**
- Calcular la diversidad de entidades PHI generadas
- Comparar con la diversidad esperada para un corpus sintético

### 3. **Canary Insertion Test Real**
- Insertar canaries únicos en los **prompts** (no en textos ya generados)
- Regenerar el corpus con canaries
- Verificar si aparecen en el corpus generado

### 4. **Comparación con Corpus de Entrenamiento**
- Si es posible, verificar si estas entidades aparecen en:
  - Corpus de entrenamiento de DeepSeek
  - Corpus médico español público (MEDDOCAN, etc.)

---

## Conclusión

Los resultados muestran **repetición significativa de entidades PHI**, pero la interpretación es **ambigua**:

- **Si es generación sintética controlada**: La repetición es esperada y no necesariamente problemática
- **Si es memorización del modelo base**: Representa un riesgo de privacidad real

**Sin acceso a los prompts completos y al corpus de entrenamiento de DeepSeek, no podemos determinar definitivamente la causa.**

**Recomendación**: Documentar esta limitación en el paper y realizar análisis adicionales (canary insertion real, análisis de diversidad) para aclarar la naturaleza de estas repeticiones.


