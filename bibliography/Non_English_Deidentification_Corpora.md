# Corpus Públicos de Desidentificación con PHI Labels en Idiomas No-Inglés

## ⚠️ Situación Crítica: Escasez de Corpus Públicos con PHI Labels

**Hallazgo Principal**: **NO existen corpus públicos específicos de desidentificación con PHI labels en alemán o francés** comparables a i2b2 o MEDDOCAN.

---

## 🇩🇪 Alemán (German)

### ❌ NO hay corpus público de desidentificación con PHI labels

**Corpus Médicos Disponibles (pero SIN PHI labels para desidentificación):**

| Corpus | Documentos | Tipo de Anotación | ¿PHI Labels? | Notas |
|--------|------------|-------------------|--------------|-------|
| **BRONCO** | 200 discharge summaries | NER médico (enfermedades, historias clínicas) | ❌ **NO** | Anotado para NER médico general, NO para desidentificación |
| **Mantra GSC (German)** | 250 documentos | Conceptos biomédicos (UMLS) | ❌ **NO** | Anotado para reconocimiento de conceptos, NO PHI |
| **The German Commons** | 154.56 mil millones tokens | Textos generales en alemán | ❌ **NO** | No es corpus médico ni tiene PHI labels |

**Conclusión para Alemán:**
- ❌ **NO existe corpus público de desidentificación con PHI labels**
- ⚠️ Los corpus disponibles son para NER médico general, NO para desidentificación
- 📊 El corpus más grande (BRONCO) tiene solo 200 documentos y NO tiene PHI labels

---

## 🇫🇷 Francés (French)

### ❌ **CONFIRMADO: NO existe corpus público de desidentificación con PHI labels**

**Búsqueda Exhaustiva Realizada:**
- ✅ Búsqueda en papers académicos
- ✅ Búsqueda en repositorios (HAL, arXiv, etc.)
- ✅ Búsqueda de challenges/competitions
- ✅ Búsqueda de corpus médicos franceses

**Resultado:** **NO se encontró ningún corpus público de desidentificación con PHI labels en francés.**

**Corpus Médicos Disponibles (pero SIN PHI labels para desidentificación):**

| Corpus | Documentos | Tipo de Anotación | ¿PHI Labels? | Notas |
|--------|------------|-------------------|--------------|-------|
| **FRASIMED** | 2,051 casos sintéticos | Conceptos médicos vinculados | ❌ **NO** | Casos **sintéticos**, anotado para conceptos médicos, NO PHI |
| **Quaero French Medical** | 103,056 palabras | 10 categorías UMLS | ❌ **NO** | Anotado para entidades médicas, NO PHI |
| **E3C (French subset)** | Parte de corpus multilingüe | Enfermedades, relaciones | ❌ **NO** | Anotado para conceptos médicos, NO PHI |
| **Mantra GSC (French)** | 250 documentos | Conceptos biomédicos (UMLS) | ❌ **NO** | Anotado para reconocimiento de conceptos, NO PHI |

**Conclusión para Francés:**
- ❌ **NO existe corpus público de desidentificación con PHI labels**
- ⚠️ FRASIMED es el más grande (2,051 casos) pero son **sintéticos** y NO tienen PHI labels
- 📊 Los corpus disponibles son para NER médico general, NO para desidentificación
- 🚨 **Situación crítica confirmada**: Si quisieras entrenar un modelo de desidentificación en francés, **NO existe un corpus público disponible**

---

## 🇪🇸 Español (Spanish) - Para Comparación

### ✅ SÍ hay corpus públicos de desidentificación con PHI labels

| Corpus | Documentos | PHI Entities | Estado |
|--------|------------|--------------|--------|
| **MEDDOCAN** | ~1,000 | 22,795 | ✅ Público con PHI labels |
| **CARMEN-I** | 2,000 | 5,895 | ✅ Público con PHI labels |

**Español es el único idioma no-inglés con corpus públicos de desidentificación con PHI labels.**

---

## 📊 Comparación: Corpus Públicos con PHI Labels para Desidentificación

| Idioma | Corpus Más Grande | Documentos | PHI Entities | Estado |
|--------|-------------------|------------|--------------|--------|
| **Inglés** | i2b2 2014 | 1,304 | 28,872 | ✅ Público |
| **Español** | CARMEN-I | 2,000 | 5,895 | ✅ Público |
| **Español** | MEDDOCAN | ~1,000 | 22,795 | ✅ Público |
| **Francés** | ❌ **NO EXISTE** | - | - | ❌ No disponible |
| **Alemán** | ❌ **NO EXISTE** | - | - | ❌ No disponible |
| **Portugués** | SemClinBr | 1,000 | 65,117* | ⚠️ Entidades médicas, NO PHI |
| **Rumano** | MoNERo | ~500 | 23,188* | ⚠️ Entidades biomédicas, NO PHI |

*Nota: SemClinBr y MoNERo tienen entidades médicas pero NO están específicamente anotados para PHI/desidentificación.

---

## 🔍 Distinción Importante: NER Médico vs. Desidentificación

### ❌ NO son lo mismo:

**NER Médico General:**
- Anota: Enfermedades, medicamentos, síntomas, procedimientos
- Propósito: Extracción de información médica
- Ejemplos: BRONCO, FRASIMED, Quaero, Mantra GSC

**Desidentificación (PHI Labels):**
- Anota: Nombres, fechas, ubicaciones, IDs, edades, etc. (información identificable)
- Propósito: Proteger privacidad del paciente
- Ejemplos: i2b2, MEDDOCAN, CARMEN-I

**⚠️ Un corpus puede tener NER médico pero NO tener PHI labels para desidentificación.**

---

## 🎯 Conclusión General

### Para Alemán:
- ❌ **NO existe corpus público de desidentificación con PHI labels**
- El corpus más grande (BRONCO) tiene solo 200 documentos y NO tiene PHI labels
- **Situación crítica**: No hay recursos públicos para entrenar modelos de desidentificación en alemán

### Para Francés:
- ❌ **NO existe corpus público de desidentificación con PHI labels**
- FRASIMED (2,051 casos sintéticos) NO tiene PHI labels
- **Situación crítica**: No hay recursos públicos para entrenar modelos de desidentificación en francés

### Comparación con Otros Idiomas:
- **Inglés**: i2b2 2014 (1,304 docs, 28,872 PHI entities) ✅
- **Español**: CARMEN-I (2,000 docs, 5,895 PHI entities) ✅
- **Español**: MEDDOCAN (~1,000 docs, 22,795 PHI entities) ✅
- **Francés**: ❌ No disponible
- **Alemán**: ❌ No disponible

---

## 💡 Implicaciones

La **ausencia total de corpus públicos de desidentificación con PHI labels en alemán y francés** justifica:

1. **Desarrollo de pipelines sintéticos** (como el proyecto del usuario)
2. **Transfer learning** desde inglés/español
3. **Cross-lingual approaches**
4. **Generación de datos sintéticos** con PHI labels

---

## 📚 Referencias

- **BRONCO**: Corpus alemán de 200 resúmenes de alta - NER médico, NO PHI
- **FRASIMED**: 2,051 casos sintéticos en francés - Conceptos médicos, NO PHI
- **MEDDOCAN**: ~1,000 casos en español - ✅ PHI labels para desidentificación
- **CARMEN-I**: 2,000 documentos en español - ✅ PHI labels para desidentificación
- **i2b2 2014**: 1,304 documentos en inglés - ✅ PHI labels para desidentificación

