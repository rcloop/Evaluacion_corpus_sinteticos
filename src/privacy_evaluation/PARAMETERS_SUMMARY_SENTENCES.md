# Frases Resumen: Parámetros de Generación LLM

## Para Incluir en el Paper

### Opción 1: Resumen Conciso (Recomendado)

**Step 1 - Generación de Anotaciones:**
"Entity values were generated using the DeepSeek-chat model with a temperature of 0.8 and a maximum of 100 tokens per entity, configured to maximize diversity in PHI value generation."

**Step 3 - Generación de Documentos:**
"Medical documents were generated using DeepSeek-chat with a temperature of 0.7 and a maximum of 2000 tokens per document, balancing creativity and medical coherence."

**Step 4 - Corrección de Documentos:**
"Document corrections were performed using DeepSeek-chat with a temperature of 0.3 and a maximum of 2000 tokens, prioritizing precision and deterministic corrections."

---

### Opción 2: Más Detallada

**Step 1 - Generación de Anotaciones:**
"Individual PHI entity values (names, dates, locations, IDs, etc.) were generated using the DeepSeek-chat API with a temperature parameter of 0.8 to encourage diverse value generation, and a maximum token limit of 100 tokens per entity. API calls were parallelized with a maximum of 5 concurrent requests."

**Step 3 - Generación de Documentos:**
"Complete medical documents were generated from the annotations using DeepSeek-chat with a temperature of 0.7 to balance linguistic creativity with medical coherence, and a maximum token limit of 2000 tokens per document. Generation was performed asynchronously with up to 5 concurrent API calls."

**Step 4 - Corrección de Documentos:**
"Documents missing required entities were corrected using DeepSeek-chat with a lower temperature of 0.3 to ensure precise, deterministic corrections, and a maximum token limit of 2000 tokens per correction."

---

### Opción 3: En Formato de Párrafo (Para Metodología)

"The corpus generation pipeline utilized the DeepSeek-chat language model through three sequential steps. In Step 1, individual PHI entity values were generated with a temperature of 0.8 (max 100 tokens) to maximize diversity. In Step 3, complete medical documents were generated from these annotations using a temperature of 0.7 (max 2000 tokens) to balance creativity and coherence. Finally, in Step 4, documents requiring corrections were processed with a lower temperature of 0.3 (max 2000 tokens) to ensure precise modifications. All API calls were made to the DeepSeek chat completions endpoint with parallelization limited to 5 concurrent requests per step."

---

### Opción 4: Tabla con Frases (Para Apéndice o Sección de Metodología)

| Step | Purpose | Temperature | Max Tokens | Rationale |
|------|---------|-------------|------------|------------|
| **Step 1** | Generate PHI entity values | 0.8 | 100 | High temperature to maximize diversity in generated values (names, dates, locations, IDs) |
| **Step 3** | Generate complete medical documents | 0.7 | 2000 | Moderate temperature to balance linguistic creativity with medical coherence |
| **Step 4** | Correct documents missing entities | 0.3 | 2000 | Low temperature to ensure precise, deterministic corrections |

---

### Opción 5: Frases Individuales para Cada Sección

**Para la sección de Metodología (Step 1):**
"Entity value generation employed DeepSeek-chat with temperature 0.8 and a 100-token limit to encourage diverse PHI value generation across all entity types."

**Para la sección de Metodología (Step 3):**
"Document generation used DeepSeek-chat with temperature 0.7 and a 2000-token limit, configured to produce natural medical prose while maintaining coherence with the provided annotations."

**Para la sección de Metodología (Step 4):**
"Document correction utilized DeepSeek-chat with temperature 0.3 and a 2000-token limit, prioritizing precision and minimal unintended modifications."

---

### Opción 6: Frase Única Resumen (Para Abstract o Conclusiones)

"The corpus was generated using DeepSeek-chat with temperature parameters of 0.8, 0.7, and 0.3 for entity generation, document generation, and document correction steps, respectively, with token limits of 100 and 2000 tokens depending on the generation step."

---

## Recomendación

**Para la sección de Metodología del paper, recomiendo usar la Opción 3 (párrafo) o la Opción 1 (frases individuales concisas).**

La Opción 3 es mejor si quieres un párrafo fluido en la metodología.
La Opción 1 es mejor si prefieres frases separadas para cada paso.

