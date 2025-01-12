
# EQUATOR Evaluator Framework 

## Overview

The **EQUATOR Evaluator** is a robust framework designed to systematically evaluate the factual accuracy and reasoning capabilities of large language models (LLMs). Unlike traditional evaluation methods, which often prioritize fluency over accuracy, this tool employs a **deterministic scoring system** that ensures precise and unbiased assessment of LLM-generated responses.

This repository implements the methodology described in the research paper "EQUATOR: A Deterministic Framework for
Evaluating LLM Reasoning with Open-EndedQuestions. # v1.0.0-beta"(Bernard et al., 2024). By leveraging vector databases and smaller, locally hosted LLMs, the LLM Evaluator bridges the gap between scalability and accuracy in automated assessments.

Study paper: 
[ArVix Study](https://arxiv.org/abs/2501.00257)


![Equator Framework](EQUATOR-Framework.png "EQUATOR: A Deterministic Framework for Evaluating LLM Reasoning")

---


Youtube Videos:

## Demo Video

[Short explainer video](https://www.youtube.com/watch?v=ryTRe18UHXE)

[Deep Dive Podcast video](https://www.youtube.com/watch?v=FVVAPXlRvPg)



## Key Features

1. **Deterministic Scoring**: Assigns binary scores (100% or 0%) based solely on factual correctness.
2. **Vector Database Integration**: Embeds open-ended questions and human-evaluated answers for semantic matching.
3. **Automated Evaluation**: Uses smaller LLMs to provide scalable and efficient assessments.
4. **Bias Mitigation**: Eliminates scoring biases related to linguistic fluency or persuasion.
5. **Cost Efficiency**: Optimizes token usage, significantly reducing operational costs for evaluation.

---

## Why LLM Evaluator?

Traditional methods, like multiple-choice or human evaluation, fail to capture the nuanced reasoning and factual accuracy required in high-stakes domains such as medicine or law. The LLM Evaluator:

- Focuses on **factual correctness** over linguistic style.
- Reduces reliance on human evaluators by automating the grading process.
- Provides insights into where LLMs fall short, enabling targeted improvements in model training.

---

## Methodology

### 1. Deterministic Scoring Framework
The scoring framework evaluates LLM-generated answers against a vector database of human-evaluated responses. It follows these steps:
1. **Embed Inputs**: Convert questions and answers into vector embeddings using models like `all-minilm`.
2. **Retrieve Closest Match**: Identify the most semantically similar answer key using cosine similarity.
3. **Binary Scoring**: Assign 100% if the student’s answer matches the answer key; otherwise, 0%.

### 2. Vector Database
The vector database, implemented with ChromaDB, stores embeddings of open-ended questions and their corresponding answer keys. This database serves as the single source of truth for evaluations.

### 3. Evaluator LLM
A smaller LLM (e.g., LLaMA 3.2B) acts as the evaluator, ensuring strict adherence to the scoring criteria while reducing computational overhead.

---
## Details of features

We classify LLMS as evaluators and students 
Eluator LLMS evaluate the "student models " in the case the STOA models found on OpenRouter (276Below is an updated “Evaluator vs. Student” matrix that includes **Groq → Ollama** support as well.

---

## Evaluator vs. Student Matrix

* Values are approximations:
  - OpenRouter has **293 models** from OpenAI, etc.
  - Groq has **14 models**.
  - Ollama has **34925 models** = **148 families** and **270 sizes**.

| **Evaluator LLM**  | **Student LLM**        | **Support Status**       |
|---------------------|------------------------|--------------------------|
| **Ollama (local)**  | OpenRouter            | **Currently supported**  |
| **Ollama (local)**  | Groq                  | **Currently supported**  |
| **Ollama (local)**  | Ollama (local)        | **Currently supported**  |
| **Groq**            | OpenRouter            | **Currently supported**  |
| **Groq**            | Ollama (local)        | **Currently supported**  |
| **Groq**            | Groq                  | **Next release**         |
| **OpenRouter**      | OpenRouter            | **Next release**         |

To determine the **possible amount of testing** from a combinatorial perspective based on your current support for Evaluator and Student LLMs, we'll break down the calculations step-by-step.

---

## **1. Understanding the Components**

### **Evaluator LLMs:**
- **Ollama (Local):** 34,925 models
- **Groq:** 14 models

### **Student LLMs:**
- **OpenRouter:** 293 models
- **Groq:** 14 models
- **Ollama (Local):** 34,925 models

**Total Evaluator Models:** 34,925 (Ollama) + 14 (Groq) = **34,939 Evaluators**

**Total Student Models:** 293 (OpenRouter) + 14 (Groq) + 34,925 (Ollama) = **35,232 Students**

---

## **2. Supported Evaluator-Student Combinations**

**currently supported** combinations are:

1. **Ollama (Evaluator) → OpenRouter (Student)**
2. **Ollama (Evaluator) → Groq (Student)**
3. **Ollama (Evaluator) → Ollama (Student)**
4. **Groq (Evaluator) → OpenRouter (Student)**
5. **Groq (Evaluator) → Ollama (Student)**

### **Unsupported (Next Release):**
6. **Groq (Evaluator) → Groq (Student)**
7. **OpenRouter (Evaluator) → OpenRouter (Student)**

---

## Calculating the Number of Combinations**

### * Current Support**

1. **Ollama Evaluator Combinations:**
   - **With OpenRouter Students:**  
     34,925 Evaluators × 293 Students = **10,232,275 combinations**
   
   - **With Groq Students:**  
     34,925 Evaluators × 14 Students = **488,950 combinations**
   
   - **With Ollama Students:**  
     34,925 Evaluators × 34,925 Students = **1,219,755,625 combinations**
   
   **Subtotal for Ollama Evaluators:**  
   10,232,275 + 488,950 + 1,219,755,625 = **1,230,476,850 combinations**

2. **Groq Evaluator Combinations:**
   - **With OpenRouter Students:**  
     14 Evaluators × 293 Students = **4,102 combinations**
   
   - **With Ollama Students:**  
     14 Evaluators × 34,925 Students = **488,950 combinations**
   
   **Subtotal for Groq Evaluators:**  
   4,102 + 488,950 = **493,052 combinations**

**Total Current Combinations:**  
1,230,476,850 (Ollama) + 493,052 (Groq) = **1,230,969,902 combinations**

### **B. Future Support (Next Release)**

1. **Groq Evaluator → Groq Student:**  
   14 Evaluators × 14 Students = **196 combinations**

2. **OpenRouter Evaluator → OpenRouter Student:**  
   293 Evaluators × 293 Students = **85,849 combinations**

**Total Future Combinations:**  
196 + 85,849 = **86,045 combinations**

---

## **4. Grand Total of Possible Evaluator-Student Combinations**

- **Currently Supported:** ~**1,230,970,000 combinations**
- **With Next Release:** ~**1,231,056,000 combinations**

*Note:* These figures are **approximate** due to rounding in intermediate steps.

---

## **5. Summary**

- **Total Supported Combinations (Current):**  
  **~1.23 Billion Evaluator-Student Pairs**

- **Additional Combinations (Next Release):**  
  **~86,045 Evaluator-Student Pairs**

---

## **6. Implications for Testing**

With **over 1.23 billion** possible Evaluator-Student pairs currently supported, comprehensive testing would involve an extensive and potentially resource-intensive process. Here's how you might approach it:

### **A. Prioritization Strategies:**
1. **Model Importance:** Focus on evaluating high-impact or frequently used models first.
2. **Diversity:** Ensure a diverse range of model families and sizes are tested to cover different capabilities and use cases.
3. **Incremental Testing:** Start with a subset of combinations and gradually expand.

### **B. Automation and Parallelization:**
- Utilize automated testing frameworks to handle large-scale evaluations.
- Leverage parallel processing to distribute the workload across multiple machines or instances.

### **C. Sampling Techniques:**
- Instead of exhaustively testing all combinations, use statistical sampling methods to select representative pairs for evaluation.

### **D. Continuous Integration:**
- Implement continuous testing pipelines that automatically evaluate new combinations as models are added or updated.

---

## **7. Recommendations**

Given the sheer volume of possible combinations, it's crucial to implement a **strategic testing plan**:

1. **Define Testing Objectives:** Clearly outline what you aim to achieve with each test (e.g., performance benchmarks, compatibility checks).
2. **Allocate Resources:** Ensure you have the necessary computational resources to handle large-scale testing.
3. **Monitor and Iterate:** Continuously monitor testing outcomes and refine your strategies based on findings and evolving requirements.

By adopting a structured and prioritized approach, you can effectively manage the extensive testing landscape and ensure robust evaluation of your LLM combinations.

### Key Points

1. **Evaluator LLMs (the “grader”)**  
   - **Ollama** (local).  
   - **Groq**.  
   - *More evaluators planned for future releases.*

2. **Student LLMs (the “respondent”)**  
   - **OpenRouter** (276+ models: OpenAI, Anthropic, etc.).  
   - **Groq**.  
   - **Ollama** (local).  
   - *More students planned for future releases.*

3. **Current Highlights**  
   - **Ollama** can evaluate answers from OpenRouter, Groq, or Ollama itself.  
   - **Groq** can evaluate answers from OpenRouter, Groq, **or Ollama**.  
   - Ongoing development will expand these capabilities even further.  

Use this chart as a quick reference for which LLM can serve as the **evaluator** versus which can serve as the **student**.  We will be testing an OpenRouter to OpenRouter impelmation in our next release.  
Below is an updated “Evaluator vs. Student” matrix that includes **Groq → Ollama** support as well.

---
## **Installation**

1. **Clone the repository**
    ```bash
    git clone https://github.com/raymondbernard/equator.git
    cd equator
    ```
2. **Download Ollama and resister at groq.com and openrouter.ai**
   1. download  Ollama at https://ollama.com and install 
   2. register and retrieve at Groq to get your api key  - https://console.groq.com/keys
   3. register and retrieve your api key at openrouter https://openrouter.ai/


3. **Set Up the Environment**
   - Rename `copy-to.env` to `.env` in your working directory.
   - Add the necessary API keys to the `.env` file.
   - Example:
     ```plaintext
     OPENROUTER_KEY="sk-xxx"
     GROQ_API_KEY="gsk_xxx"
     ```

4. **Optional: Set Up a Virtual Environment**
   It is recommended to use a virtual environment to avoid conflicts with other Python packages.

   #### On **Windows**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install equator
   deactivate
   ```

   #### On **Linux/MacOS**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install equator
   deactivate
   ```

5. **Install our requirements**
   ```bash
   pip install -r requirements.txt
   ```

 6. **Open the main.py file.** 
    1. Look at the comments in the file for directions on how to configure your test runs. It's straight forward.  


### Configuration

- **Execution Steps**: Define the steps to execute in the `execution_steps` list.  Please run the application with just do one execution_step at a time and comment out the other steps. In a future release we will enable a bit more automation.  
* Note the steps will use different models as evaluators and students.  
   ie.   ollama_to_groq_evaluate = ollama is the evaluator and groq is the student. 
   Here’s a clearer and easier-to-follow version of your instructions with improved formatting and structure:

---

## **IMPORTANT INSTRUCTIONS**

### **Step-by-Step Execution**

To ensure everything runs smoothly, **please execute the program one step at a time!** Follow these guidelines:

1. **Toggle Steps by Adding/Removing Comments**  
   Modify the `execution_steps` list by uncommenting **one line at a time**.  
   After running the program, re-comment the executed step if needed and proceed to the next.

### **Example Execution Process**

Here’s the structure of your `execution_steps` list:

```python
execution_steps = [
    # "ollama_to_groq_evaluate",  # Uncomment one line at a time, then run the program.
    # "ollama_to_openrouter_evaluate",  # Currently working.
    # "groq_to_ollama_evaluate",  # Currently working.
    # "groq_to_openrouter_evaluate",  # Currently working.
    "generate_statistics",  # Always run last, after completing all evaluations.
]
```

### **How to Execute**:
1. Choose **one step** to execute by removing the `#` at the beginning of the corresponding line.
2. Run the program.
3. After the step completes, **comment the step again** by re-adding the `#` if you plan to run additional steps.
4. Move to the next step and repeat.

---

### **Order of Execution**

1. Uncomment `"ollama_to_groq_evaluate"` and run.
2. Uncomment `"ollama_to_openrouter_evaluate"` and run.
3. Uncomment `"groq_to_ollama_evaluate"` and run.
4. Uncomment `"groq_to_openrouter_evaluate"` and run.
5. Finally, ensure only `"generate_statistics"` is uncommented and run to compile results.

---

### **Tips for Success**
- **One line at a time:** Never leave multiple steps uncommented.
- **Save progress:** If something goes wrong, re-check the list and verify only one line is uncommented.
- **Final step:** Always finish with `"generate_statistics"` to summarize your results.

---

This format highlights the importance of running one step at a time and makes the process easy to follow.
- **Models**: Specify the models to benchmark in the respective lists.
    ```python
    student_openrouter_models = [
        "nousresearch/hermes-3-llama-3.1-405b",
    ]
    
    student_groq_models = [
        "llama3-70b-8192",
    ]

    student_ollama_models = [
        "llama3.2",
    ]
    ```

- **Benchmark Settings**: Adjust benchmarking parameters such as evaluator models, benchmark name, and answer rounds.
    ```python
    GROQ_EVALUATOR_MODEL = "llama3-70b-8192"
    OLLAMA_EVALUATOR_MODEL = "llama3.2"
    benchmark_name = "Bernard"
    answer_rounds = 2
    ```

### Logging

Logs are saved to `vectordb.log` with INFO level by default.


## Usage

### Running the Program

1. **In your Python Environment**
2. 
   ```bash
   >py -m main   
   ```

### Viewing Results
We create a directory named after the corresponding date to organize the benchmarks. Within this directory, you will find a collection of charts and CSV files containing statistics and token analytics.

Results, including scores and explanations, are saved in the specified output directory as JSON files. Each entry includes:
- Question
- Model-generated answer
- Evaluator response for the score
- Score

---
## Example Dataset

The repository includes two datasets to test the reasoning capabilities of LLMs:

1. **Default Dataset**: 
   - The file `linguistic_benchmark.json` contains open-ended questions across various categories, such as puzzles, spatial reasoning, and logic. This smaller dataset is ideal for quick tests or debugging. You are welcome to add more questions to the dataset or customize them for your domain. 

We do have a QA `linguistic_benchmark.json with over 1000+ .  However, we will create a website which will pusblish our resutls using this dataset. 
---

**Why We Keep Our Dataset Private**

   Our research examines the performance of large language models (LLMs) across state-of-the-art (SOTA) benchmarks, and we aim to maintain statistically significant evaluation results. If we were to release our full dataset publicly, there is a risk that future models could be trained or fine-tuned on our test items, which would compromise the fairness and meaningfulness of our benchmark. By keeping these data private, we ensure that our comparisons remain valid and our results accurately reflect model performance under unbiased test conditions. 
   
  
   Although our primary focus is maintaining a statistically significant and unbiased dataset for testing AI performance in QA reasoning and logic, we understand that different industries—such as law, medicine, or finance—have unique needs. Our linguistic_benchmark.json file can be extended to include domain-specific prompts and example responses. This approach allows you to evaluate how well AI models perform in your specialized context without compromising the integrity of our core benchmarking methodology. By adding your own questions, you can preserve our standardized evaluation framework while tailoring the tests to your field’s specific challenges.  We aim to maintain a current benchmark results for our EQUATOR at equator.github.io 

   

## Contributions

### Authors
- Raymond Bernard (Independent Researcher)
- Shaina Raza, Ph.D. (Vector Institute)
- Subhabrata Das, PhD (JP Morgan Chase)
- Raul Murugan (Columbia University)

---

## Future Work

- Expand the vector database to include more diverse datasets.
- Optimize the embedding and retrieval process for larger-scale deployments.
- Investigate additional scoring criteria for complex reasoning tasks.

---
- *Acknowledgment*: We extend our gratitude to James Huckle for inspiring our work.  
- We have incorporated elements from [https://github.com/autogenai/easy-problems-that-llms-get-wrong](https://github.com/autogenai/easy-problems-that-llms-get-wrong).  
- Our approach advances the field by simplifying the benchmarking process through our capability to score open-ended questions effectively.  
- Rather than benchmarking multiple models across disparate APIs, we leverage OpenRouter.ai's unified API, using the OpenAI SDK, which provides access to over 270 models for comprehensive benchmarking.  
  
- ## Citation
If you use this framework in your research, please cite:

```
@article {bernard2024equator,
  title        = {{EQUATOR: A Deterministic Framework for Evaluating LLM Reasoning with Open-Ended Questions. \# v1.0.0-beta}},
  author       = {Bernard, Raymond and Raza, Shaina and Das, Subhabrata and Murugan, Rahul},
  year         = {2024},
  eprint       = {2501.00257},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL},
  note         = {MSC classes: 68T20; ACM classes: I.2.7; I.2.6; H.3.3},
  howpublished = {arXiv preprint arXiv:2501.00257 [cs.CL]},
  doi          = {10.48550/arXiv.2501.00257},
}

```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.

---

*Generated with ❤️ by Equator QA Team*