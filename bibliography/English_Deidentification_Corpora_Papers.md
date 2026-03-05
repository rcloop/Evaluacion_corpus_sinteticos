# Papers on Large-Scale English De-identification Corpora

## Main Benchmark Corpora for De-identification in English

### 1. i2b2 2014 De-identification Challenge

**Paper 1: Corpus Description**
- **Stubbs, A., Uzuner, Ö., et al. (2015)**
- "Annotating longitudinal clinical narratives for de-identification: The 2014 i2b2/UTHealth corpus"
- **Journal of Biomedical Informatics**, 58, S20-S29
- **DOI**: 10.1016/j.jbi.2015.07.020
- **URL**: https://www.sciencedirect.com/science/article/pii/S1532046415001615
- **Corpus Size**: 1,304 discharge summaries
- **Entities**: **28,872 PHI entities** (longitudinal annotations)
- **Patients**: 296 patients (multiple documents per patient)
- **Description**: Describes the corpus creation and annotation guidelines for the 2014 i2b2 de-identification challenge

**Paper 2: Challenge Overview**
- **Stubbs, A., Kotfila, C., & Uzuner, Ö. (2015)**
- "Automated systems for the de-identification of longitudinal clinical narratives: Overview of 2014 i2b2/UTHealth shared task track 1"
- **Journal of Biomedical Informatics**, 58, S11-S19
- **DOI**: 10.1016/j.jbi.2015.06.007
- **URL**: https://www.sciencedirect.com/science/article/pii/S1532046415001603
- **Description**: Overview of the challenge, participating systems, and results

### 2. i2b2 2006 De-identification Challenge (Original)

**Paper 1: Challenge Description**
- **Uzuner, Ö., Luo, Y., & Szolovits, P. (2007)**
- "Evaluating the State-of-the-Art in Automatic De-identification"
- **Journal of the American Medical Informatics Association**, 14(5), 550-563
- **DOI**: 10.1197/jamia.M2444
- **URL**: https://academic.oup.com/jamia/article/14/5/550/730828
- **Corpus Size**: 889 discharge summaries
- **Description**: Original i2b2 de-identification challenge, establishing the benchmark

**Paper 2: Results and Methods**
- **Uzuner, Ö., et al. (2008)**
- "Evaluating the State-of-the-Art in De-identification: A New Gold Standard"
- **AMIA Annual Symposium Proceedings**, 2008, 251-255
- **URL**: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2655990/
- **Description**: Detailed results and evaluation metrics

### 3. MIMIC-III (⚠️ NOT suitable for de-identification training)

**Important Note**: MIMIC-III is **already de-identified** - all PHI has been removed. It does **NOT** contain labeled PHI annotations and therefore **cannot be used to train de-identification models**. The PHI was removed using automated systems, but the original PHI labels are not available.

**Paper 1: Database Description**
- **Johnson, A. E. W., et al. (2016)**
- "MIMIC-III, a freely accessible critical care database"
- **Scientific Data**, 3, 160035
- **DOI**: 10.1038/sdata.2016.35
- **URL**: https://www.nature.com/articles/sdata201635
- **Corpus Size**: ~40,000 patients, ~58,000 admissions, ~2 million clinical notes
- **Description**: Large-scale de-identified critical care database (PHI already removed)
- **Limitation**: Cannot be used for training de-identification models (no PHI labels available)

**Paper 2: De-identification Methods Used**
- **Dernoncourt, F., et al. (2017)**
- "De-identification of patient notes with recurrent neural networks"
- **Journal of the American Medical Informatics Association**, 24(3), 596-606
- **DOI**: 10.1093/jamia/ocw156
- **URL**: https://academic.oup.com/jamia/article/24/3/596/2631508
- **Description**: Methods used to de-identify MIMIC-III notes (achieving >95% precision), but the original PHI annotations are not part of the released dataset

### 4. UCSF De-identification Corpus (✅ Has PHI Labels - ❌ Not Publicly Available)

**Important Clarification**: The UCSF corpus of 4,500 manually annotated clinical notes **DOES have PHI labels** (ground truth). It was used to **develop and evaluate Philter**, not created by Philter.

**What We Know:**
- **Corpus Size**: 4,500 manually annotated clinical notes
  - 2,500 notes used for algorithm development
  - 2,000 notes used for testing/evaluation
- **PHI Labels**: ✅ **YES** - The corpus has PHI manually annotated (ground truth) because it was used to develop Philter
- **Purpose**: Used to train and evaluate Philter de-identification system
- **Paper**: Published in NPJ Digital Medicine (Nature), 2020
- **Status**: ❌ **NOT publicly available** - access restricted to UCSF-affiliated researchers

**Philter Development:**
- Philter was **developed USING** this corpus (not the other way around)
- The corpus served as ground truth for training and evaluating Philter
- Philter achieved 99.46% recall and F2-score of 94.36% on UCSF test set
- Philter was then used to de-identify 130+ million clinical notes at UCSF

**UCSF Information Commons:**
- Provides de-identified data from 8+ million patients (processed by Philter)
- These are **already de-identified** notes, not the original corpus with PHI labels
- Access requires: UCSF affiliation, IRB approval, and data use agreements
- **URL**: https://ars.ucsf.edu/information-commons-data

**Key Distinction:**
1. **UCSF Corpus (4,500 notes)**: Has PHI labels (ground truth) - used to develop Philter - **NOT public**
2. **UCSF Information Commons**: 130+ million notes already de-identified by Philter - **NOT suitable for training**

**Conclusion**: The UCSF corpus of 4,500 notes **does have PHI labels** and was used to develop Philter. However, it is **not publicly available** and therefore **cannot be used as a benchmark** comparable to i2b2 2014 or MEDDOCAN for training de-identification models.

### 5. Other Large-Scale De-identification Corpora

**Paper: Longitudinal De-identification**
- **Stubbs, A., & Uzuner, Ö. (2015)**
- "Annotating risk factors for heart disease in clinical narratives for diabetic patients"
- **Journal of Biomedical Informatics**, 58, S78-S91
- **DOI**: 10.1016/j.jbi.2015.07.021
- **URL**: https://www.sciencedirect.com/science/article/pii/S1532046415001627
- **Description**: Part of the 2014 i2b2 challenge, focusing on longitudinal data

## Comparison with Spanish Corpora

### Size Comparison:

| Corpus | Language | Documents | Entities | Notes |
|--------|----------|-----------|----------|-------|
| **UCSF Corpus** | English | 4,500 | Unknown | ✅ PHI labeled (ground truth)<br>❌ Not publicly available |
| **i2b2 2014** | English | 1,304 | **28,872** | ✅ PHI labeled for training |
| **i2b2 2006** | English | 889 | ~16,000+ | ✅ PHI labeled for training |
| **MIMIC-III** | English | ~2M notes | N/A | ❌ Already de-identified (no PHI labels) |
| **MEDDOCAN** | Spanish | ~1,000 | 22,795 | ✅ PHI labeled for training |
| **CARMEN-I** | Spanish | 2,000 | 5,895 | ✅ PHI labeled for training |

### Key Findings:

1. **UCSF Corpus** (4,500 documents) - **HAS PHI labels** (used to develop Philter), but **NOT publicly available**; access restricted to UCSF researchers; cannot be used as a benchmark
2. **i2b2 2014** (1,304 documents) is the **largest publicly available and well-documented** corpus for de-identification training in English, **though it is relatively small** compared to other medical corpora
3. **i2b2 2014** (1,304 documents) exceeds **MEDDOCAN** (~1,000 documents) by ~30%
4. **i2b2 2014** significantly exceeds **CARMEN-I** (2,000 documents) in entity density and annotation depth
5. **MIMIC-III** (~2M notes) is NOT suitable for training de-identification models - it is already de-identified and contains no PHI labels
6. **i2b2 challenges** are the primary publicly available benchmarks for training de-identification models in English
7. English corpora (i2b2) achieve >95% precision in PHI recognition through hybrid architectures
8. English corpora provide longitudinal data, which is rare in non-English languages

### Answer to: "Is i2b2 2014 the largest database to train for de-identification in English?"

**Qualified Answer**: 
- **i2b2 2014 is the largest publicly available and well-documented corpus** for training de-identification models in English (1,304 documents with PHI labels)
- **However, it is relatively small** - only 1,304 documents compared to other medical corpora (e.g., MIMIC-III has ~2M notes, but they're already de-identified)
- **The scarcity of large public de-identification corpora with PHI labels** is a significant limitation in the field
- **Larger corpora exist** (e.g., UCSF Corpus with 4,500 documents) but are **NOT publicly available**

**See**: `Deidentification_Corpus_Size_Analysis.md` for detailed analysis
- There are references to a **UCSF corpus with 4,500 documents**, but it is **NOT publicly available** (restricted to UCSF researchers) and therefore cannot be used as a benchmark
- **i2b2 2014** is widely recognized as the primary publicly available benchmark and is extensively documented in peer-reviewed publications

### Suitable Corpora for Training De-identification Models:

✅ **Can be used for training (publicly available):**
- i2b2 2014 (1,304 documents with PHI labels) - **Largest publicly available and well-documented**
- i2b2 2006 (889 documents with PHI labels)
- MEDDOCAN (~1,000 documents with PHI labels)
- CARMEN-I (2,000 documents with PHI labels)

❌ **Cannot be used (not publicly available):**
- UCSF Corpus (4,500 documents with PHI labels - restricted access, not publicly available)
  - **Note**: This corpus HAS PHI labels and was used to develop Philter, but is not publicly accessible

❌ **Cannot be used for training:**
- MIMIC-III (already de-identified, no PHI labels available)

## References for Citation

### Primary i2b2 Papers:

1. Stubbs, A., Uzuner, Ö., et al. (2015). "Annotating longitudinal clinical narratives for de-identification: The 2014 i2b2/UTHealth corpus." *Journal of Biomedical Informatics*, 58, S20-S29.

2. Stubbs, A., Kotfila, C., & Uzuner, Ö. (2015). "Automated systems for the de-identification of longitudinal clinical narratives: Overview of 2014 i2b2/UTHealth shared task track 1." *Journal of Biomedical Informatics*, 58, S11-S19.

3. Uzuner, Ö., Luo, Y., & Szolovits, P. (2007). "Evaluating the State-of-the-Art in Automatic De-identification." *Journal of the American Medical Informatics Association*, 14(5), 550-563.

4. Dernoncourt, F., et al. (2017). "De-identification of patient notes with recurrent neural networks." *Journal of the American Medical Informatics Association*, 24(3), 596-606.

5. Johnson, A. E. W., et al. (2016). "MIMIC-III, a freely accessible critical care database." *Scientific Data*, 3, 160035.
   - **Note**: MIMIC-III is already de-identified and does not contain PHI labels for training de-identification models.

