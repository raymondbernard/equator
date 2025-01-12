from loguru import logger  # Logging utility for enhanced logging capabilities
from dotenv import load_dotenv  # Utility to load environment variables from a .env file

from equator_qa.charting import create_basic_charts  # Function to create visual representations of data
from equator_qa.utils import (
    begin_benchmark,  # Function to initialize and run benchmarks
    cleanup_chromadb,  # Function to clean up the database before execution
)
from datetime import datetime  # Used to generate the current date and time
from equator_qa.vectordb import VectorDB_Controller  # Class to manage vector database operations

# Load environment variables from the .env file
load_dotenv()

# Configure logging: Logs will be written to 'vectordb.log' with a specific format and INFO level
logger.add("vectordb.log", format="{time} {level} {message}", filter="", level="INFO")

# Main execution block
if __name__ == "__main__":
    # Cleanup any existing data in the vector database to ensure a fresh start
    cleanup_chromadb()

    # Model names for the evaluator
    GROQ_EVALUATOR_MODEL = "llama3-70b-8192"
    OLLAMA_EVALUATOR_MODEL = "llama3.2"
  
    # Number of times each question will be asked to the models
    answer_rounds = 2

    # Name of the benchmark being executed
    benchmark_name = "Bernard"

    # The date used for naming directories and ensuring data consistency
    # If the folder structure does not match `date_now`, either rename the folder
    # or hardcode this value to ensure analytics align correctly.
    date_now = datetime.now().strftime("%Y-%m-%d")

    # List of steps to execute; comment/uncomment to toggle specific tasks
    execution_steps = [
        # "ollama_to_groq_evaluate",  # Evaluate Ollama models against GROQ models
        # "ollama_to_openrouter_evaluate",  # Evaluate Ollama models against OpenRouter models
        # "groq_to_ollama_evaluate",  # Evaluate GROQ models against Ollama models
        # "groq_to_openrouter_evaluate",  # Evaluate GROQ models against OpenRouter models
        "generate_statistics",  # Generate and visualize statistical analysis
    ]

    # List of OpenRouter models to be used as students in the benchmark
    student_openrouter_models = [
        # Examples of commented-out models for potential use
        # "google/learnlm-1.5-pro-experimental:free",
        # "liquid/lfm-40b:free",
        # "meta-llama/llama-3.2-11b-vision-instruct:free",
        "nousresearch/hermes-3-llama-3.1-405b",  # Active model
        # "qwen/qwen-2-7b-instruct:free",
        # "microsoft/phi-3-medium-128k-instruct:free",
    ]
    
    # List of GROQ models to be used as students in the benchmark
    student_groq_models = [
        # "llama-3.3-70b-versatile",
        "llama3-70b-8192",  # Active model
    ]

    # List of Ollama models to be used as students in the benchmark
    # Avoid using semicolons in model names (e.g., "llama3.2:latest")
    student_ollama_models = [
        "llama3.2",  # Active model
    ]

    # If "generate_statistics" is not in execution_steps, begin benchmarking
    if "generate_statistics" not in execution_steps:
        # Create an instance of the VectorDB_Controller
        vectordb_instance = VectorDB_Controller(keepVectorDB=False)
        # Start the benchmark with specified configurations
        begin_benchmark(
            execution_steps,
            student_ollama_models,
            student_groq_models,
            student_openrouter_models,
            OLLAMA_EVALUATOR_MODEL,
            GROQ_EVALUATOR_MODEL,
            vectordb_instance,
            benchmark_name,
            date_now,
            answer_rounds,
        )

    # If "generate_statistics" is in execution_steps, create statistical charts
    if "generate_statistics" in execution_steps:
        create_basic_charts(execution_steps, answer_rounds, benchmark_name, date_now)
        print("-- DONE STATS --\n")
