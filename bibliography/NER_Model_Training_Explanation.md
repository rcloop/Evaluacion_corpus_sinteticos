# Cómo Funcionan los Modelos NER: Etiquetas y Entrenamiento

## 🎯 Preguntas Clave

1. ¿Tienes que decirle a un NER qué etiquetas identificar?
2. ¿Lo aprende directamente de los corpus anotados?
3. ¿Puede generar etiquetas nuevas?

---

## 📚 Respuesta Corta

**Respuesta:** 
- ✅ **SÍ, lo aprende de los corpus anotados**
- ⚠️ **Las etiquetas deben estar en el corpus de entrenamiento**
- ✅ **SÍ puede aprender nuevas etiquetas** con fine-tuning en corpus con esas etiquetas

---

## 🔍 Cómo Funciona un Modelo NER

### 1. Preentrenamiento (Base del Modelo)

**Ejemplo: bsc-bio-ehr-es**

**Proceso:**
1. **Preentrenamiento en lenguaje general:**
   - Aprende representaciones de palabras en contexto
   - Entiende estructura del lenguaje
   - NO aprende etiquetas específicas aún

2. **Preentrenamiento en dominio biomédico:**
   - Aprende terminología médica
   - Entiende contexto clínico
   - Aún NO aprende etiquetas específicas

**En este punto:**
- ✅ Entiende el lenguaje y contexto
- ❌ NO sabe qué etiquetas identificar específicamente

---

### 2. Fine-tuning para NER (Aprende Etiquetas)

**Ejemplo: bsc-bio-ehr-es fine-tuneado en PharmaCoNER**

**Proceso:**
1. **Corpus anotado con etiquetas:**
   ```
   Texto: "El paciente toma aspirina"
   Etiquetas: [O, O, O, O, MEDICAMENTO, O]
   ```

2. **El modelo aprende:**
   - Qué palabras corresponden a qué etiquetas
   - Patrones contextuales para cada etiqueta
   - Cómo identificar cada tipo de entidad

3. **Resultado:**
   - El modelo puede identificar las etiquetas que vio en el corpus
   - NO puede identificar etiquetas que no vio

**Etiquetas aprendidas en bsc-bio-ehr-es:**
- MEDICAMENTO (de PharmaCoNER)
- MORFOLOGIA_TUMORAL (de CANTEMIST)
- VARIABLE_CLINICA (de ICTUSnet)
- **NO aprendió:** PHI labels (nombres, fechas, etc.)

---

## 🎯 ¿Tienes que Decirle las Etiquetas?

### Respuesta: ⚠️ **Depende del enfoque**

### Opción 1: Fine-tuning Estándar (Más Común)

**Proceso:**
1. **Preparas corpus con etiquetas:**
   ```
   Texto: "Juan Pérez nació el 15/03/1980"
   Etiquetas: [B-PERSON, I-PERSON, O, O, B-DATE, I-DATE, I-DATE]
   ```

2. **El modelo aprende automáticamente:**
   - Qué etiquetas existen (PERSON, DATE, etc.)
   - Cómo identificarlas
   - Patrones para cada etiqueta

3. **NO tienes que "decirle" explícitamente:**
   - El modelo infiere las etiquetas del corpus
   - Aprende todas las etiquetas que aparecen en los datos

**Ejemplo con MEDDOCAN:**
- Corpus tiene etiquetas: PERSON, DATE, LOCATION, ID, etc.
- Modelo aprende automáticamente estas etiquetas
- Puede identificar estas etiquetas después del fine-tuning

---

### Opción 2: Few-Shot / Zero-Shot (Menos Común)

**Proceso:**
1. **Le das ejemplos de etiquetas:**
   ```
   "Identifica: PERSON, DATE, LOCATION"
   Ejemplo: "Juan Pérez nació el 15/03/1980 en Madrid"
   ```

2. **El modelo intenta identificar:**
   - Basándose en ejemplos
   - Sin entrenamiento explícito

**Limitación:**
- ⚠️ Rendimiento mucho menor
- ⚠️ Requiere modelos muy grandes (GPT-4, etc.)
- ⚠️ No es el enfoque estándar para NER

---

## 📊 ¿Puede Generar Etiquetas Nuevas?

### Respuesta: ✅ **SÍ, con fine-tuning**

### Cómo Agregar Nuevas Etiquetas:

**Escenario:** bsc-bio-ehr-es solo sabe MEDICAMENTO, pero quieres que identifique PHI.

**Proceso:**

1. **Preparar corpus con nuevas etiquetas:**
   ```
   Texto: "Paciente Juan Pérez, fecha 15/03/1980"
   Etiquetas: [O, B-PERSON, I-PERSON, O, B-DATE, I-DATE, I-DATE]
   ```

2. **Fine-tuning con nuevo corpus:**
   - El modelo aprende las nuevas etiquetas (PERSON, DATE)
   - Mantiene conocimiento de etiquetas anteriores (MEDICAMENTO)
   - Puede identificar ambas

3. **Resultado:**
   - ✅ Identifica MEDICAMENTO (del entrenamiento original)
   - ✅ Identifica PERSON, DATE (del nuevo fine-tuning)

---

## 🔄 Proceso Completo: De bsc-bio-ehr-es a Desidentificación

### Paso 1: Modelo Base (bsc-bio-ehr-es)

**Etiquetas que conoce:**
- MEDICAMENTO
- MORFOLOGIA_TUMORAL
- VARIABLE_CLINICA

**NO conoce:**
- ❌ PERSON (nombre de paciente)
- ❌ DATE (fecha como PHI)
- ❌ LOCATION (ubicación como PHI)

---

### Paso 2: Fine-tuning con MEDDOCAN

**Corpus MEDDOCAN tiene etiquetas:**
- PERSON
- DATE
- LOCATION
- ID
- AGE
- etc.

**Proceso de fine-tuning:**
1. Toma bsc-bio-ehr-es como base
2. Entrena con textos de MEDDOCAN y sus etiquetas PHI
3. El modelo aprende:
   - ✅ Nuevas etiquetas: PERSON, DATE, LOCATION, etc.
   - ✅ Mantiene: MEDICAMENTO (si está en el corpus)

**Resultado:**
- Modelo puede identificar PHI (nuevas etiquetas)
- También puede identificar entidades médicas (si están en el corpus)

---

## 📋 Formato de Entrenamiento

### Formato IOB2 (Estándar para NER):

```
Texto: "Juan Pérez nació el 15/03/1980 en Madrid"

Etiquetas IOB2:
Juan     B-PERSON
Pérez    I-PERSON
nació    O
el       O
15       B-DATE
/        I-DATE
03       I-DATE
/        I-DATE
1980     I-DATE
en       O
Madrid   B-LOCATION
```

**El modelo aprende:**
- B-PERSON: Inicio de nombre de persona
- I-PERSON: Continuación de nombre de persona
- B-DATE: Inicio de fecha
- I-DATE: Continuación de fecha
- B-LOCATION: Inicio de ubicación
- O: No es entidad

**NO tienes que "decirle" qué es PERSON o DATE:**
- El modelo aprende automáticamente de las etiquetas en el corpus
- Infiere que B-PERSON significa "inicio de persona"
- Aprende patrones para identificar PERSON

---

## 🎯 Respuestas Directas a tus Preguntas

### 1. ¿Tienes que decirle qué etiquetas identificar?

**Respuesta:** ⚠️ **No directamente, pero sí indirectamente**

**Cómo:**
- ✅ Preparas corpus con las etiquetas que quieres
- ✅ El modelo aprende automáticamente qué etiquetas existen
- ❌ NO le "dices" explícitamente "identifica PERSON, DATE, etc."
- ✅ El modelo infiere las etiquetas del corpus

**Ejemplo:**
- Si tu corpus tiene etiquetas: [PERSON, DATE, LOCATION]
- El modelo aprende automáticamente estas 3 etiquetas
- NO necesitas configurar manualmente "busca estas etiquetas"

---

### 2. ¿Lo aprende directamente de los corpus anotados?

**Respuesta:** ✅ **SÍ, exactamente**

**Proceso:**
1. Corpus anotado → Modelo ve texto + etiquetas
2. Modelo aprende patrones: "cuando veo 'Juan Pérez' en contexto X, es PERSON"
3. Modelo generaliza: "puedo identificar PERSON en nuevos textos"

**El modelo NO tiene conocimiento previo de etiquetas:**
- Aprende TODO de los corpus anotados
- Si una etiqueta no está en el corpus, no la aprende
- Si una etiqueta está en el corpus, la aprende automáticamente

---

### 3. ¿Puede generar etiquetas nuevas?

**Respuesta:** ✅ **SÍ, con fine-tuning en corpus con nuevas etiquetas**

**Proceso:**
1. **Modelo base** (bsc-bio-ehr-es) conoce: MEDICAMENTO
2. **Fine-tuning** con corpus que tiene: PERSON, DATE
3. **Resultado:** Modelo conoce: MEDICAMENTO, PERSON, DATE

**Limitaciones:**
- ⚠️ Necesitas corpus anotado con las nuevas etiquetas
- ⚠️ El modelo solo aprende etiquetas que ve en el corpus
- ⚠️ No puede "inventar" etiquetas sin datos

**Tu pipeline sintético:**
- ✅ Genera corpus con etiquetas PHI (PERSON, DATE, etc.)
- ✅ Permite fine-tuning para aprender estas nuevas etiquetas
- ✅ Crea modelo que identifica PHI (nuevas etiquetas)

---

## 💡 Ejemplo Práctico: Tu Caso

### Situación Actual:

**bsc-bio-ehr-es sin fine-tuning:**
- Conoce: MEDICAMENTO, MORFOLOGIA_TUMORAL
- NO conoce explícitamente: PERSON, DATE, LOCATION
- **PERO** identifica ~70% de PHI (por patrones estructurales)

**¿Por qué identifica 70% sin conocer las etiquetas?**
- Reconoce patrones estructurales (fechas, nombres)
- NO está "entrenado" para etiquetarlos como PHI
- Es más "adivinación inteligente" que identificación precisa

---

### Con Fine-tuning (MEDDOCAN o tu pipeline):

**Proceso:**
1. Corpus con etiquetas PHI: PERSON, DATE, LOCATION, etc.
2. Fine-tuning: Modelo aprende estas etiquetas explícitamente
3. Resultado: Modelo identifica PHI con etiquetas correctas

**Mejora:**
- 70% (sin etiquetas) → 90%+ (con etiquetas aprendidas)
- Identificación precisa con etiquetas correctas
- Menos falsos positivos/negativos

---

## 📊 Comparación: Sin vs. Con Etiquetas Explícitas

### Sin Etiquetas en Corpus (solo preentrenamiento):

| Aspecto | Rendimiento |
|---------|-------------|
| Identificación de PHI | ~70% (patrones estructurales) |
| Etiquetas correctas | ⚠️ No etiqueta explícitamente |
| Precisión | Media (muchos falsos positivos) |
| Recall | Media (muchos falsos negativos) |

**Problema:**
- Identifica "algo" pero no sabe qué etiqueta ponerle
- No distingue bien entre tipos de PHI

---

### Con Etiquetas en Corpus (fine-tuning):

| Aspecto | Rendimiento |
|---------|-------------|
| Identificación de PHI | ~90%+ (aprendizaje explícito) |
| Etiquetas correctas | ✅ Etiqueta explícitamente (PERSON, DATE, etc.) |
| Precisión | Alta (menos falsos positivos) |
| Recall | Alta (menos falsos negativos) |

**Ventaja:**
- Identifica PHI Y sabe qué tipo es (PERSON, DATE, etc.)
- Distingue bien entre tipos de PHI
- Etiquetado preciso y estructurado

---

## 🎯 Conclusión

### Respuestas Finales:

1. **¿Tienes que decirle qué etiquetas identificar?**
   - ❌ NO directamente
   - ✅ SÍ indirectamente (preparando corpus con esas etiquetas)
   - ✅ El modelo aprende automáticamente qué etiquetas existen

2. **¿Lo aprende directamente de los corpus anotados?**
   - ✅ **SÍ, completamente**
   - ✅ Todo el conocimiento de etiquetas viene del corpus
   - ✅ Sin corpus anotado, no aprende etiquetas nuevas

3. **¿Puede generar etiquetas nuevas?**
   - ✅ **SÍ, con fine-tuning en corpus con nuevas etiquetas**
   - ✅ Puede aprender PERSON, DATE, etc. aunque no las conocía antes
   - ⚠️ Necesita corpus anotado con esas etiquetas

4. **¿Cómo evitas que aprenda etiquetas no deseadas?**
   - ✅ **NO las incluyas en el corpus de entrenamiento**
   - ✅ **Filtra/remueve esas etiquetas antes de entrenar**
   - ✅ **Marca como 'O' (no entidad)** las entidades que no quieres etiquetar
   - Ver `NER_Label_Control_Filtering.md` para detalles completos

### Para tu Proyecto:

**Tu pipeline sintético:**
1. ✅ Genera corpus con etiquetas PHI (PERSON, DATE, LOCATION, etc.)
2. ✅ Permite fine-tuning de bsc-bio-ehr-es con estas etiquetas
3. ✅ El modelo aprende estas nuevas etiquetas automáticamente
4. ✅ Mejora del 70% (sin etiquetas) → 90%+ (con etiquetas aprendidas)

**Esto es exactamente lo que necesitas para crear modelos de desidentificación en nuevos idiomas.**

