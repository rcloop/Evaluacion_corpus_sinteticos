# Control de Etiquetas en NER: Cómo Evitar Etiquetas No Deseadas

## 🎯 Pregunta Clave

**Problema:** Si el modelo aprende todas las etiquetas del corpus, ¿cómo evitas que aprenda etiquetas que no te interesan?

**Ejemplo:**
- Quieres que identifique: PHI (PERSON, DATE, LOCATION)
- Pero el corpus también tiene: ENFERMEDAD, MEDICAMENTO
- ¿Cómo evitas que el modelo también aprenda ENFERMEDAD, MEDICAMENTO?

---

## ⚠️ Respuesta Importante

**El modelo aprende TODAS las etiquetas que están en el corpus de entrenamiento.**

**Si no quieres que aprenda ciertas etiquetas:**
- ✅ **NO las incluyas en el corpus de entrenamiento**
- ✅ **Filtra/remueve esas etiquetas antes del entrenamiento**
- ✅ **Usa un corpus que solo tenga las etiquetas que quieres**

---

## 🔍 Cómo Funciona el Aprendizaje de Etiquetas

### Proceso de Fine-tuning:

1. **Modelo lee el corpus:**
   ```
   Texto: "Juan Pérez tiene diabetes y toma aspirina"
   Etiquetas: [B-PERSON, I-PERSON, O, O, B-ENFERMEDAD, O, O, B-MEDICAMENTO]
   ```

2. **Modelo aprende TODAS las etiquetas que ve:**
   - ✅ PERSON (porque está en el corpus)
   - ✅ ENFERMEDAD (porque está en el corpus)
   - ✅ MEDICAMENTO (porque está en el corpus)

3. **Resultado:**
   - El modelo puede identificar PERSON, ENFERMEDAD, MEDICAMENTO
   - **NO puedes "desactivar" etiquetas** después del entrenamiento

---

## ✅ Soluciones: Cómo Controlar las Etiquetas

### Solución 1: Filtrar Etiquetas del Corpus (RECOMENDADO)

**Proceso:**

1. **Tienes corpus con múltiples etiquetas:**
   ```
   Texto: "Juan Pérez tiene diabetes"
   Etiquetas: [B-PERSON, I-PERSON, O, O, B-ENFERMEDAD]
   ```

2. **Filtrar para mantener solo PHI:**
   ```python
   # Pseudocódigo
   filtered_labels = []
   for label in original_labels:
       if label in ['B-PERSON', 'I-PERSON', 'B-DATE', 'I-DATE', 'B-LOCATION', 'I-LOCATION']:
           filtered_labels.append(label)
       else:
           filtered_labels.append('O')  # Marcar como "no entidad"
   ```

3. **Resultado:**
   ```
   Texto: "Juan Pérez tiene diabetes"
   Etiquetas filtradas: [B-PERSON, I-PERSON, O, O, O]
   ```

4. **Entrenar con etiquetas filtradas:**
   - Modelo solo ve: PERSON
   - Modelo NO ve: ENFERMEDAD
   - Modelo solo aprende: PERSON (y otras PHI)

---

### Solución 2: Usar Corpus Solo con Etiquetas Deseadas

**Proceso:**

1. **Crear/Seleccionar corpus que solo tenga PHI:**
   - MEDDOCAN: Solo tiene etiquetas PHI (PERSON, DATE, LOCATION, etc.)
   - NO tiene: ENFERMEDAD, MEDICAMENTO

2. **Entrenar con este corpus:**
   - Modelo solo aprende etiquetas PHI
   - NO aprende otras etiquetas (porque no están en el corpus)

**Ventaja:**
- ✅ No necesitas filtrar
- ✅ Corpus ya está "limpio"

**Desventaja:**
- ⚠️ Puede perder contexto médico útil

---

### Solución 3: Entrenamiento Multi-Tarea con Músculos Selectivos

**Proceso Avanzado:**

1. **Entrenar con todas las etiquetas:**
   - PERSON, DATE, LOCATION, ENFERMEDAD, MEDICAMENTO

2. **Durante inferencia, filtrar salidas:**
   ```python
   # Pseudocódigo
   predictions = model.predict(text)
   filtered_predictions = [p if p.startswith('PHI_') else 'O' 
                          for p in predictions]
   ```

**Limitación:**
- ⚠️ El modelo aún aprende todas las etiquetas
- ⚠️ Solo filtras en la salida, no en el aprendizaje
- ⚠️ Menos eficiente (aprende cosas que no usas)

---

## 📊 Comparación de Estrategias

| Estrategia | Ventajas | Desventajas | Recomendación |
|------------|----------|-------------|---------------|
| **Filtrar antes de entrenar** | ✅ Control total<br>✅ Modelo solo aprende lo necesario | ⚠️ Requiere procesamiento | ✅ **RECOMENDADO** |
| **Corpus solo con etiquetas deseadas** | ✅ Simple<br>✅ No requiere filtrado | ⚠️ Puede perder contexto | ✅ Buena opción |
| **Filtrar en salida** | ✅ Modelo versátil | ❌ Aprende cosas innecesarias<br>❌ Menos eficiente | ❌ No recomendado |

---

## 💡 Ejemplo Práctico: Tu Caso

### Escenario:

**Quieres:**
- Identificar PHI: PERSON, DATE, LOCATION, ID, AGE

**Tienes corpus con:**
- PHI: PERSON, DATE, LOCATION, ID, AGE
- Entidades médicas: ENFERMEDAD, MEDICAMENTO, SINTOMA

**Problema:**
- Si entrenas con todo, el modelo aprende ENFERMEDAD, MEDICAMENTO, SINTOMA también

---

### Solución: Filtrar Etiquetas

**Código Python (ejemplo):**

```python
import json

# Etiquetas PHI que quieres mantener
PHI_LABELS = ['B-PERSON', 'I-PERSON', 'B-DATE', 'I-DATE', 
              'B-LOCATION', 'I-LOCATION', 'B-ID', 'I-ID',
              'B-AGE', 'I-AGE', 'O']

def filter_labels(corpus_path, output_path):
    """
    Filtra corpus para mantener solo etiquetas PHI
    """
    with open(corpus_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    filtered_data = []
    
    for example in data:
        tokens = example['tokens']
        labels = example['labels']
        
        # Filtrar etiquetas
        filtered_labels = []
        for label in labels:
            if label in PHI_LABELS:
                filtered_labels.append(label)
            else:
                # Marcar como "no entidad" si no es PHI
                filtered_labels.append('O')
        
        filtered_data.append({
            'tokens': tokens,
            'labels': filtered_labels
        })
    
    # Guardar corpus filtrado
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)
    
    return filtered_data

# Uso
filter_labels('corpus_completo.json', 'corpus_solo_phi.json')
```

**Resultado:**
- Corpus filtrado solo tiene etiquetas PHI
- Modelo solo aprende PHI
- NO aprende ENFERMEDAD, MEDICAMENTO, SINTOMA

---

## 🎯 Estrategia Recomendada para tu Pipeline

### Opción 1: Generar Corpus Solo con PHI (MEJOR)

**Tu pipeline sintético:**
1. Genera textos médicos
2. Inserta PHI sintético
3. **Anota SOLO PHI** (PERSON, DATE, LOCATION, etc.)
4. **NO anota** entidades médicas (ENFERMEDAD, MEDICAMENTO)

**Ventaja:**
- ✅ Corpus "limpio" desde el inicio
- ✅ No necesitas filtrar
- ✅ Modelo solo aprende PHI

**Ejemplo:**
```
Texto: "El paciente Juan Pérez tiene diabetes y toma aspirina"
Etiquetas: [O, O, B-PERSON, I-PERSON, O, O, O, O, O, O]
          (Solo PERSON está etiquetado, diabetes y aspirina son O)
```

---

### Opción 2: Generar Corpus Completo y Filtrar

**Tu pipeline sintético:**
1. Genera textos médicos
2. Inserta PHI sintético
3. Anota PHI Y entidades médicas
4. **Filtra para mantener solo PHI** antes de entrenar

**Ventaja:**
- ✅ Tienes corpus completo (útil para otros propósitos)
- ✅ Puedes elegir qué etiquetas usar

**Desventaja:**
- ⚠️ Requiere paso adicional de filtrado

---

## 📋 Checklist: Control de Etiquetas

### Antes de Entrenar:

- [ ] **Definir etiquetas deseadas:**
  - PHI: PERSON, DATE, LOCATION, ID, AGE, etc.
  
- [ ] **Revisar corpus:**
  - ¿Qué etiquetas tiene el corpus?
  - ¿Hay etiquetas no deseadas?

- [ ] **Filtrar si es necesario:**
  - Remover etiquetas no deseadas
  - Marcar como 'O' (no entidad)

- [ ] **Verificar corpus filtrado:**
  - Solo contiene etiquetas deseadas
  - Formato correcto (IOB2)

### Durante el Entrenamiento:

- [ ] **Configurar modelo:**
  ```python
  num_labels = len(PHI_LABELS)  # Solo número de etiquetas PHI
  ```

- [ ] **Verificar que el modelo solo ve etiquetas PHI**

### Después del Entrenamiento:

- [ ] **Evaluar:**
  - ¿El modelo identifica solo PHI?
  - ¿Hay falsos positivos de otras entidades?

---

## 🔍 Caso Específico: bsc-bio-ehr-es + MEDDOCAN

### Situación:

**bsc-bio-ehr-es conoce:**
- MEDICAMENTO, MORFOLOGIA_TUMORAL (del entrenamiento original)

**MEDDOCAN tiene:**
- PERSON, DATE, LOCATION, ID, AGE (PHI)
- **NO tiene:** ENFERMEDAD, MEDICAMENTO (solo PHI)

**Fine-tuning con MEDDOCAN:**
- Modelo aprende: PERSON, DATE, LOCATION, ID, AGE
- Modelo **puede olvidar:** MEDICAMENTO (si no está en MEDDOCAN)
- O puede **mantener:** MEDICAMENTO (depende del fine-tuning)

**Control:**
- Si MEDDOCAN solo tiene PHI → Modelo solo aprende PHI
- Si quieres mantener MEDICAMENTO → Incluir ejemplos en el corpus

---

## 💡 Recomendación Final

### Para tu Pipeline Sintético:

**Estrategia RECOMENDADA:**

1. **Generar corpus solo con etiquetas PHI:**
   - PERSON, DATE, LOCATION, ID, AGE, etc.
   - **NO incluir:** ENFERMEDAD, MEDICAMENTO, SINTOMA

2. **Ventajas:**
   - ✅ Corpus "limpio" desde el inicio
   - ✅ Modelo solo aprende PHI
   - ✅ No necesitas filtrar
   - ✅ Más eficiente

3. **Si necesitas contexto médico:**
   - Incluir textos médicos (con enfermedades, medicamentos)
   - Pero **NO etiquetarlos** (marcar como 'O')
   - El modelo ve el contexto pero no aprende a etiquetar esas entidades

**Ejemplo:**
```
Texto: "El paciente Juan Pérez de 45 años tiene diabetes"
Etiquetas: [O, O, B-PERSON, I-PERSON, O, B-AGE, I-AGE, O, O, O]
          (Juan Pérez = PERSON, 45 años = AGE, diabetes = O)
```

**Resultado:**
- Modelo aprende: PERSON, AGE
- Modelo NO aprende: ENFERMEDAD (diabetes está marcado como O)
- Modelo ve contexto médico pero no lo etiqueta

---

## 🎯 Conclusión

### ¿Cómo evitas que el modelo aprenda etiquetas no deseadas?

**Respuesta:** 
1. ✅ **NO las incluyas en el corpus de entrenamiento**
2. ✅ **Filtra/remueve esas etiquetas antes de entrenar**
3. ✅ **Marca como 'O' (no entidad)** las entidades que no quieres etiquetar

### Para tu Pipeline:

**Mejor estrategia:**
- Generar corpus que **solo tenga etiquetas PHI**
- NO etiquetar entidades médicas (marcarlas como 'O')
- El modelo solo aprende PHI
- Mantiene contexto médico pero no lo etiqueta

**Esto te da control total sobre qué etiquetas aprende el modelo.**




