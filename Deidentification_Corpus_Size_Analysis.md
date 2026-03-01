# Análisis del Tamaño de Corpus de Desidentificación en Inglés

## ⚠️ Observación Importante

**i2b2 2014 es relativamente pequeño** (1,304 documentos) comparado con otros corpus médicos. Sin embargo, sigue siendo el **corpus público más grande con PHI labels** para entrenar modelos de desidentificación.

## 📊 Comparación de Corpus Públicos con PHI Labels

| Corpus | Documentos | Entidades PHI | Estado | Notas |
|--------|------------|---------------|--------|-------|
| **i2b2 2014** | **1,304** | **28,872** | ✅ Público | **Más grande PÚBLICO con PHI labels** |
| **i2b2 2006** | 889 | ~16,000+ | ✅ Público | Más pequeño que 2014 |
| **UCSF Corpus** | 4,500 | Desconocido | ❌ **NO público** | Más grande pero acceso restringido |

## 🔍 ¿Por qué es tan pequeño?

### El Problema Fundamental

**Para entrenar modelos de desidentificación necesitas:**
- ✅ Documentos con **PHI labels** (ground truth)
- ✅ PHI **anotada manualmente** o verificada
- ✅ Acceso **público** para investigación

**La mayoría de corpus grandes:**
- ❌ Ya están **desidentificados** (sin PHI labels)
- ❌ No tienen **ground truth** para entrenar
- ❌ No son **públicos** (acceso restringido)

### Ejemplos de Corpus Grandes (pero NO útiles para entrenar desidentificación)

| Corpus | Tamaño | ¿Tiene PHI Labels? | ¿Útil para Entrenar? |
|--------|--------|---------------------|----------------------|
| **MIMIC-III** | ~2M notas | ❌ NO (ya desidentificado) | ❌ NO |
| **CheXpert Plus** | 36M tokens | ❓ Probablemente ya desidentificado | ❓ Verificar |
| **MedDialog** | 700M tokens | ❌ Probablemente ya desidentificado | ❌ NO |

## 📈 Comparación con Corpus No-Inglés

| Idioma | Corpus | Documentos | Entidades | Estado |
|--------|--------|------------|-----------|--------|
| **Inglés** | i2b2 2014 | 1,304 | 28,872 | ✅ Público |
| **Español** | MEDDOCAN | ~1,000 | 22,795 | ✅ Público |
| **Español** | CARMEN-I | 2,000 | 5,895 | ✅ Público |
| **Portugués** | SemClinBr | 1,000 | 65,117 | ✅ Público |

**Observación**: Aunque i2b2 2014 es pequeño, es **comparable o mayor** que muchos corpus no-inglés en términos de documentos.

## 🎯 Conclusión

### i2b2 2014 es:
- ✅ El **corpus público más grande** con PHI labels para desidentificación en inglés
- ⚠️ **Relativamente pequeño** (1,304 documentos) comparado con otros corpus médicos
- ✅ **Bien documentado** y ampliamente usado como benchmark
- ✅ **Longitudinal** (296 pacientes con múltiples documentos)

### La Escasez de Corpus Grandes con PHI Labels

**Razones:**
1. **Privacidad**: Los datos clínicos con PHI son altamente sensibles
2. **Regulaciones**: HIPAA y otras regulaciones limitan el acceso
3. **Costo**: Anotar PHI manualmente es costoso y requiere expertos
4. **Riesgo**: Publicar datos con PHI reales es riesgoso

### Corpus Más Grandes (pero NO públicos)

- **UCSF Corpus**: 4,500 documentos con PHI labels - **NO público** (acceso restringido)
- Otros corpus institucionales: Probablemente existen pero no son públicos

## 📚 Referencias

- **i2b2 2014**: Stubbs et al. (2015) - 1,304 documentos, 28,872 PHI entities
- **i2b2 2006**: Uzuner et al. (2007) - 889 documentos
- **UCSF Corpus**: NPJ Digital Medicine (2020) - 4,500 documentos (NO público)

## 💡 Implicaciones para la Investigación

La **escasez de corpus grandes con PHI labels** es una limitación fundamental en el campo de desidentificación clínica. Esto justifica:

1. **Desarrollo de pipelines sintéticos** (como el proyecto del usuario)
2. **Técnicas de data augmentation**
3. **Transfer learning** desde corpus pequeños
4. **Semi-supervised learning**




