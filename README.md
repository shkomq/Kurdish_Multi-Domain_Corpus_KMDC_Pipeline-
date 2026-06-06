# Kurdish Multi-Domain Corpus (KMDC) Pipeline

Official implementation of the **KMDC Pipeline**, as presented in our research conducted at the **College of Intelligence and Computing, Tianjin University**.

This repository provides a modular, high-throughput suite designed to transform non-searchable Kurdish (Sorani) multi-domain literature into a structured, scientific-grade dataset spanning **12+ domains** including politics, economy, health, culture, science, sports, religion, law, education, history, environment, and media.

---

## 🚀 Key Features
* **Multi-Domain Extraction:** High-fidelity text acquisition from OCR-challenging scripts across diverse subject areas using advanced LLM techniques.
* **High-Throughput Inference:** Optimized **Ollama + Gemma 3 27B** configuration specifically tuned for **dual NVIDIA RTX 4090 D** GPUs.
* **Structured Output:** Automated transformation of raw multi-domain text into standardized JSON with full metadata and category labels.
* **Cross-Lingual Alignment:** Hybrid Kurdish→English category translation combining offline mapping, rule extraction, and Google Translate API.
* **Performance:** Achieves robust classification across 12+ domains with automated category normalization and deduplication.

## 📁 Repository Structure
The pipeline consists of **4 modular components** (Python + Shell scripts):

* `Data_Engineering/`: Corpus cleaning, merging, deduplication, and number normalization (7 scripts).
* `Translation_Pipeline/`: Kurdish→English category mapping with hybrid translation strategy (5 scripts).
* `Analysis_Tools/`: Corpus metrics, category distribution, and inspection utilities (4 scripts).
* `LLM_Orchestration/`: Ollama server management, model registration, and dataset generation (11 scripts).

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/shkomq/Kurdish-Multi-Domain-Corpus-KMDC-Pipeline.git
    cd Kurdish-Multi-Domain-Corpus-KMDC-Pipeline
