# Physicians and artificial intelligence diverge in evaluating large language models on real clinical cases

## Abstract
While multimodal large language models (LLMs) demonstrate significant potential in healthcare applications, their clinical utility is difficult to appraise. Current evaluations of medical-assisting LLMs are often limited by sparse human expertise, narrow specialty scope, and reliance on multiple-choice benchmarks or synthetic vignettes, which can inflate performance and obscure clinical utility. We conducted a multicenter, multidisciplinary study in which more than 400 physicians—spanning seven specialties, varied experience levels, and multiple geographic settings—evaluated LLM-generated free-text responses to real, de-identified clinical cases. In a matched-control design, we also deployed an equivalent number of AI agents configured to mirror physician characteristics to examine whether automated evaluators can supplement or replace human assessment. Our results demonstrated that physician assessments exhibited substantial heterogeneity by clinical seniority and practice environment, leading to notable shifts in relative model rankings across cohorts. While AI agents delivered highly efficient, directionally aligned assessments, they did not fully capture the nuances of human clinical judgment and could not substitute for physician-centered evaluation. Instead, they promise assistive tools that can triage or pre-screen outputs to reduce human burden.

## Project Structure
```
.
├── README.md
├── configs
│   ├── API_INFO.py
│   ├── agents
│   │   ├── Junior.toml
│   │   ├── Mid.toml
│   │   └── Senior.toml
│   ├── agents_config.py
│   └── patients
│       └── template.toml
├── environment.yml
├── main.py
└── src
    ├── agent.py
    ├── constants.py
    ├── patient.py
    └── utils.py
```

## How to Run
### Environment Setup
The project runs in a Conda environment, with a basic YML file provided.
```
git clone https://github.com/payen-shi/Evaluation-Bias.git
cd Evaluation-Bias/
conda env create -f environment.yml
```

This project relies on CAMEL-AI for optimised API calling procedure. You may need to set up the CAMEL-AI environment manually if there is any issue on setup it via YML file automatically. Please refer to the official documentation of the CAMEL-AI:

https://docs.camel-ai.org/get_started/introduction

### Configuration Setup
1. Set up each patient config following the template.toml in ./configs/patients/.
2. Set up each agent type config in ./configs/agents/.
3. Update the base URLs and API keys in API_INFO.py.
4. Set the number of agents in agents_config.py.

### Run

```
# The whole project should always be run from the root directory: Evaluation-Bias/
cd Evaluation-Bias/

# Activate the conda environment
conda activate eval_env

# Run the main task, creating LLM agents to evaluate diagnostic reports with clinical records
python3 main.py
```

## Contact
CODE MAINTENANCE: 
Ziqi Yang (Email: Z.Yang21@imperial.ac.uk)

## Citation

If you use this work, please cite:
```
PLACEHOLDER FOR CITATION BIBTEX.
```

## References
Li, G., Hammoud, H. A. A. K., Itani, H., Khizbullin, D. & Ghanem, B. CAMEL: Communicative agents for “mind” exploration of large language model society. In Thirty-seventh Conference on Neural Information Processing Systems (2023).