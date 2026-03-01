# Parámetros de Generación LLM - DeepSeek

## Resumen de Parámetros Usados en el Pipeline

Este documento resume los parámetros utilizados para llamar a la API de DeepSeek durante la generación del corpus.

---

## Modelo Utilizado

**Modelo:** `deepseek-chat`  
**API Endpoint:** `https://api.deepseek.com/v1/chat/completions` (step1) o `https://api.deepseek.com/chat/completions` (step3, step4)

---

## Paso 1: Generación de Anotaciones (`step1_generate_annotations.py`)

**Propósito:** Generar valores específicos para cada etiqueta PHI (nombres, fechas, ubicaciones, IDs, etc.)

**Parámetros:**
- **Modelo:** `deepseek-chat`
- **Temperature:** `0.8` (alta para mayor diversidad en valores generados)
- **Max Tokens:** `100` (valores cortos, solo el valor de la entidad)
- **API Endpoint:** `https://api.deepseek.com/v1/chat/completions`
- **Llamadas paralelas:** Máximo 5 concurrentes (configurable con `--api-workers`)

**Código relevante:**
```python
response = requests.post(
    self.base_url,
    headers=self.headers,
    json={
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.8,
        "max_tokens": 100
    },
    timeout=30
)
```

**Justificación:** Temperature de 0.8 permite generar valores diversos para las entidades PHI, evitando repetición excesiva.

---

## Paso 3: Generación de Documentos (`step3_generate_documents.py`)

**Propósito:** Generar documentos médicos completos a partir de las anotaciones

**Parámetros:**
- **Modelo:** `deepseek-chat`
- **Temperature:** `0.7` (moderada para balance entre creatividad y coherencia)
- **Max Tokens:** `2000` (documentos completos)
- **API Endpoint:** `https://api.deepseek.com/chat/completions`
- **Llamadas concurrentes:** Máximo 5 concurrentes (configurable con `--max-concurrent`)

**Código relevante:**
```python
data = {
    "model": model,
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "max_tokens": 2000,
    "temperature": 0.7
}
```

**Justificación:** Temperature de 0.7 permite generar documentos naturales y diversos mientras mantiene coherencia médica.

---

## Paso 4: Corrección de Documentos (`step4_correct_docs.py`)

**Propósito:** Corregir documentos que no contienen todas las etiquetas requeridas

**Parámetros:**
- **Modelo:** `deepseek-chat`
- **Temperature:** `0.3` (baja para correcciones más precisas y deterministas)
- **Max Tokens:** `2000`
- **API Endpoint:** `https://api.deepseek.com/chat/completions`

**Código relevante:**
```python
data = {
    "model": model,
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "max_tokens": 2000,
    "temperature": 0.3  # Menor temperatura para correcciones más precisas
}
```

**Justificación:** Temperature de 0.3 permite correcciones más precisas y deterministas, minimizando cambios no deseados en el documento.

---

## Resumen de Parámetros por Paso

| Paso | Propósito | Temperature | Max Tokens | Justificación |
|------|-----------|-------------|------------|---------------|
| **Step 1** | Generar valores PHI | **0.8** | 100 | Alta diversidad en valores generados |
| **Step 3** | Generar documentos | **0.7** | 2000 | Balance entre creatividad y coherencia |
| **Step 4** | Corregir documentos | **0.3** | 2000 | Precisión en correcciones |

---

## Observaciones sobre Diversidad

Los parámetros de temperatura utilizados pueden explicar parcialmente los resultados de la evaluación de privacidad:

1. **Temperature 0.8 en Step 1:** Aunque es alta, la generación de valores PHI individuales puede resultar en repetición si el modelo tiene tendencias a generar valores comunes (ej: "Centro de Salud Los Álamos", "España").

2. **Temperature 0.7 en Step 3:** Moderada pero puede no ser suficiente para generar documentos completamente diversos, especialmente si los prompts son similares.

3. **Temperature 0.3 en Step 4:** Muy baja, lo que puede contribuir a la repetición de estructuras y frases en documentos corregidos.

**Recomendación para futuras generaciones:**
- Considerar aumentar temperature a 0.9-1.0 en Step 1 para mayor diversidad en valores PHI
- Considerar aumentar temperature a 0.8-0.9 en Step 3 para mayor diversidad estructural en documentos
- Mantener temperature 0.3 en Step 4 (correcciones deben ser precisas)

---

## Versión del Modelo

El código utiliza `deepseek-chat` sin especificar una versión específica. Esto significa que se utiliza la versión por defecto disponible en la API al momento de la generación.

**Nota:** Para reproducibilidad, sería recomendable documentar la versión específica del modelo utilizada o la fecha de generación del corpus.

---

## Referencias en el Código

- **Step 1:** `corpus_repo/src/pipeline/step1_generate_annotations.py` (líneas 108-117)
- **Step 3:** `corpus_repo/src/pipeline/step3_generate_documents.py` (líneas 240-250, 285-295)
- **Step 4:** `corpus_repo/src/pipeline/step4_correct_docs.py` (líneas 323-331, 358-366)

