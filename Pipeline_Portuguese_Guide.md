# Guía: Pipeline de Desidentificación para Portugués

## 🎯 Objetivo

Crear un pipeline de desidentificación en portugués equivalente al que usarías con **bsc-bio-ehr-es** en español.

---

## 📋 Paso a Paso: Pipeline para Portugués

### Paso 1: Elegir Modelo Base Biomédico (equivalente a bsc-bio-ehr-es)

**Opciones disponibles para Portugués:**

#### ✅ Opción 1: BioBERTpt (RECOMENDADO)

**¿Qué es?**
- Modelo BERT entrenado específicamente en textos biomédicos/clínicos en portugués
- Equivalente directo a bsc-bio-ehr-es para español

**Dónde encontrarlo:**
- **HuggingFace**: Buscar "BioBERTpt" o "BioBERT-pt"
- **GitHub**: https://github.com/HAILab-PUCPR/BioBERTpt
- **Paper**: ACL Clinical NLP 2020

**Ventajas:**
- ✅ Especializado en dominio biomédico/clínico
- ✅ Entrenado en portugués brasileño
- ✅ Mejor rendimiento que modelos generales
- ✅ Equivalente directo a bsc-bio-ehr-es

**Uso:**
```python
from transformers import AutoTokenizer, AutoModelForTokenClassification

model_name = "pucpr/BioBERTpt"  # Verificar nombre exacto en HuggingFace
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)
```

---

#### ⚠️ Opción 2: MediAlbertina

**¿Qué es?**
- Modelo médico entrenado con registros médicos electrónicos
- Específico para portugués europeo (pt-PT)

**Dónde encontrarlo:**
- **HuggingFace**: `portugueseNLP/medialbertina_pt-pt_1.5b_NER`

**Ventajas:**
- ✅ Especializado en dominio médico
- ✅ Entrenado en registros médicos reales

**Desventajas:**
- ⚠️ Portugués europeo (no brasileño)
- ⚠️ Verificar disponibilidad

**Uso:**
```python
model_name = "portugueseNLP/medialbertina_pt-pt_1.5b_NER"
```

---

#### ⚠️ Opción 3: BERTimbau (Modelo General)

**¿Qué es?**
- Modelo BERT general para portugués (no específico biomédico)
- Desarrollado por NeuralMind

**Dónde encontrarlo:**
- **HuggingFace**: `neuralmind/bert-base-portuguese-cased`
- **GitHub**: https://github.com/neuralmind-ai/portuguese-bert

**Ventajas:**
- ✅ Bien establecido y documentado
- ✅ Disponible en variantes base y large

**Desventajas:**
- ❌ NO especializado en biomédico
- ⚠️ Rendimiento inferior a BioBERTpt para tareas médicas

**Uso (si BioBERTpt no está disponible):**
```python
model_name = "neuralmind/bert-base-portuguese-cased"
# Luego hacer fine-tuning con corpus biomédico
```

---

### Paso 2: Obtener Corpus Médico en Portugués

**Opciones disponibles:**

#### ✅ Opción 1: SemClinBr

**¿Qué es?**
- Corpus clínico brasileño con 1,000 notas clínicas
- 65,117 entidades médicas anotadas
- **PERO**: NO tiene PHI labels (solo entidades médicas)

**Dónde encontrarlo:**
- Buscar "SemClinBr corpus" en papers/repositorios

**Uso:**
- ✅ Base para generar corpus sintético con PHI
- ✅ Tu pipeline sintético inserta PHI en estos textos

---

#### ✅ Opción 2: MedPT

**¿Qué es?**
- Corpus de preguntas y respuestas médicas
- 384,095 pares de interacciones paciente-médico
- Portugués brasileño

**Dónde encontrarlo:**
- **arXiv**: https://arxiv.org/abs/2511.11878

**Uso:**
- ✅ Textos médicos reales en portugués
- ✅ Base para generar corpus sintético con PHI

---

#### ⚠️ Opción 3: Corpus Generales

- **Corpus do Português**: Corpus general (no médico)
- **Corpus Lexicográfico do Português**: Corpus general

**Uso:**
- ⚠️ Menos útil (no son textos médicos)
- ✅ Podrían usarse si no hay otra opción

---

### Paso 3: Generar Corpus Sintético con PHI (TU PIPELINE)

**Este es el paso clave donde tu pipeline es crítico:**

1. **Tomar corpus médico** (SemClinBr, MedPT, o similar)
2. **Insertar PHI sintético** en portugués:
   - Nombres brasileños/portugueses: "João Silva", "Maria Santos"
   - Fechas en formato portugués: "15/03/2024", "12 de janeiro de 2023"
   - Ubicaciones: "Hospital São Paulo", "Rua das Flores, 123"
   - IDs: "CPF 123.456.789-00", "RG 12.345.678-9"
   - Teléfonos: "(11) 98765-4321"
3. **Anotar automáticamente** el PHI insertado
4. **Crear corpus con PHI labels** en formato IOB2

**Resultado:**
- Corpus de desidentificación con PHI labels en portugués
- Equivalente a MEDDOCAN/CARMEN-I pero para portugués

---

### Paso 4: Fine-tuning del Modelo para Desidentificación

**Proceso:**

1. **Cargar modelo base** (BioBERTpt o alternativa)
2. **Fine-tune con tu corpus sintético** con PHI labels
3. **Entrenar** para identificar PHI específicamente

**Código ejemplo:**
```python
from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer
from datasets import Dataset

# 1. Cargar modelo base
model_name = "pucpr/BioBERTpt"  # o la alternativa elegida
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(
    model_name,
    num_labels=len(PHI_LABELS)  # Número de etiquetas PHI
)

# 2. Preparar datos de tu corpus sintético
train_dataset = Dataset.from_dict({
    "tokens": [...],  # Tokens de tus textos
    "labels": [...]   # Labels PHI en formato IOB2
})

# 3. Fine-tuning
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    # ... otros parámetros
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

trainer.train()
```

---

## 📊 Comparación: Español vs. Portugués

| Aspecto | Español | Portugués |
|---------|---------|-----------|
| **Modelo Biomédico** | bsc-bio-ehr-es | **BioBERTpt** |
| **Modelo General** | BERT-base-spanish | BERTimbau |
| **Corpus Médico** | MEDDOCAN, CARMEN-I | SemClinBr, MedPT |
| **Corpus Desidentificación** | MEDDOCAN (con PHI) | ❌ No existe → **Tu pipeline lo crea** |
| **Estado** | ✅ Recursos disponibles | ⚠️ Necesita tu pipeline |

---

## 🎯 Recomendación Final

### Para Portugués, usa:

1. **Modelo Base:** **BioBERTpt** (equivalente a bsc-bio-ehr-es)
   - Si no está disponible: BERTimbau + fine-tuning con corpus biomédico

2. **Corpus Médico:** **SemClinBr** o **MedPT**
   - Como base para tu pipeline sintético

3. **Tu Pipeline Sintético:**
   - Inserta PHI sintético en portugués
   - Anota automáticamente
   - Crea corpus de desidentificación con PHI labels

4. **Fine-tuning:**
   - Fine-tune BioBERTpt con tu corpus sintético
   - Entrenar específicamente para desidentificación

---

## 💡 Ventajas de tu Enfoque

1. ✅ **No dependes de corpus existentes** con PHI labels (que no existen en portugués)
2. ✅ **Control total** sobre el PHI generado
3. ✅ **Escalable** - puedes generar tanto corpus como necesites
4. ✅ **Reproducible** - otros investigadores pueden usar tu pipeline
5. ✅ **Primero en portugués** - serías el primero en crear corpus de desidentificación público en portugués

---

## 📚 Referencias

- **BioBERTpt**: ACL Clinical NLP 2020
- **BERTimbau**: NeuralMind AI
- **SemClinBr**: Corpus clínico brasileño
- **MedPT**: arXiv 2024
- **MediAlbertina**: HuggingFace

---

## ✅ Checklist para Implementar

- [ ] Verificar disponibilidad de BioBERTpt en HuggingFace
- [ ] Descargar/obtener corpus médico (SemClinBr o MedPT)
- [ ] Adaptar tu pipeline sintético para portugués:
  - [ ] Generadores de nombres brasileños/portugueses
  - [ ] Formatos de fechas en portugués
  - [ ] Formatos de IDs brasileños (CPF, RG)
  - [ ] Formatos de teléfonos brasileños
  - [ ] Ubicaciones en portugués
- [ ] Generar corpus sintético con PHI labels
- [ ] Fine-tune BioBERTpt con el corpus
- [ ] Evaluar modelo de desidentificación
- [ ] Publicar corpus y modelo

---

## 🚀 Siguiente Paso

**Tu pipeline sintético es la pieza clave** que permite:
1. Crear corpus de desidentificación en portugués (que no existe)
2. Fine-tune BioBERTpt para desidentificación
3. Ser el primero en tener un modelo público de desidentificación en portugués

**¡Esto es extremadamente valioso!**




