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

2.  **Setup Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    pip install -r requirements.txt

3. **Install Ollama and Model:**
    ```bash
    cd LLM_Orchestration
    chmod +x install_ollama.sh
    ./install_ollama.sh
    ./setup_ollama_model.sh  # Place Gemma 3 27B GGUF file first

## 📊 Dataset Access

The final **Kurdish Multi-Domain Corpus (KMDC)** is publicly available on Hugging Face:

👉 [Download KMDC Dataset Here](https://huggingface.co/datasets/shkomq/Kurdish-Multi-Domain-Corpus-KMDC)

## 🧪 Quick Start

    # Start Ollama server
    cd LLM_Orchestration
    python3 run_server_bg_first.py
    
    # Generate multi-domain dataset
    python3 run_generator_bg_first.py
    
    # Clean and process data
    cd ../Data_Engineering
    python3 dataset_cleaner.py input.json output.json
    
    # Translate categories
    cd ../Translation_Pipeline
    python3 advanced_translator.py
    
    # Analyze results
    cd ../Analysis_Tools
    python3 analyze_categories.py final_corpus.json
    
    # Stop all processes
    cd ../LLM_Orchestration
    ./pkill_ollama.sh

## 📋 Covered Domains

| Domain (English) | Domain (Kurdish) |
|------------------|------------------|
| Politics | سیاسەت |
| Economy | ئابوری |
| Health | تەندروستی |
| Culture & Arts | کەلتور و هونەر |
| Science | زانست |
| Sports | وەرزش |
| Religion | دین |
| Law & Justice | یاسا |
| Education | پەروەردە |
| History | مێژوو |
| Environment | ژینگە |
| Media | میدیا |

## ⚙️ Configuration
Model Parameters (Modelfile)
    PARAMETER temperature 0.7
    PARAMETER top_p 0.9
    PARAMETER top_k 40
    PARAMETER repeat_penalty 1.1
    PARAMETER num_ctx 8192

Environment Variables
    export OLLAMA_HOST="0.0.0.0:11434"
    export OLLAMA_HOME="/mnt/storage1/shko/ollama"
    export CUDA_VISIBLE_DEVICES="0,1"

## 📈 Performance

| Operation | Scale | Time |
|-----------|-------|------|
| Model loading | 27B params | ~15 sec |
| Q&A generation | 1,000 prompts | ~3 min |
| Dataset cleaning | 100,000 records | ~5 sec |
| Category translation | 500 categories | ~2 min |

## 🤝 Acknowledgments

This research was supported by the **College of Intelligence and Computing, Tianjin University, China**. Special thanks to the contributors and colleagues who assisted in the acquisition and curation of multi-domain Kurdish language resources.

## ✍️ Citation

If you use this pipeline or the KMDC dataset in your research, please cite:

```bibtex
@article{kmdc_v1_2026,
  title={Kurdish Multi-Domain Corpus (KMDC) V1},
  author={Shko Muhammed Qader and Zheng Wang},
  year={2026},
  publisher={github},
  howpublished={\url{https://github.com/shkomq/Kurdish_Multi_Domain_Corpus_KMDC_Pipeline/}}
}

## 📄 License

Academic Research Use Only
