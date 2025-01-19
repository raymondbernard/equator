# Importing necessary libraries and modules
from loguru import logger  # Loguru is used for enhanced logging capabilities
from dotenv import load_dotenv  # Loads environment variables from a .env file
from equator_qa.charting import create_basic_charts  # Function to generate statistical charts
from equator_qa.utils import begin_benchmark, cleanup_chromadb  # Utility functions for benchmarking and database cleanup
from datetime import datetime  # To work with date and time
from equator_qa.vectordb import VectorDB_Controller  # Controller for managing vector database operations

def main(execution_steps=None):
    """
    Main function to execute benchmarking and statistical analysis based on provided steps.
    
    Parameters:
        execution_steps (list, optional): A list of steps to execute. If None, defaults to a predefined list.
    """
    
    # Load environment variables from the .env file to configure the application
    load_dotenv()
    
    # Clean up any existing data or configurations in the vector database to ensure a fresh start
    cleanup_chromadb()

    # Define the evaluator models used for benchmarking
    GROQ_EVALUATOR_MODEL = "llama3-70b-8192"  # Model name for GROQ evaluator
    OLLAMA_EVALUATOR_MODEL = "llama3.2"  # Model name for Ollama evaluator

    # Configuration parameters for the benchmarking process
    answer_rounds = 2  # Number of times each question will be posed to the models
    benchmark_name = "Bernard"  # Identifier name for the current benchmark run
    
    # Capture the current date in YYYY-MM-DD format for logging and organizing results
    date_now = datetime.now().strftime("%Y-%m-%d")

    # If no specific execution steps are provided, use the default set of steps
    if execution_steps is None:
        execution_steps = [
            # "ollama_to_ollama_evaluate",  # Step to evaluate Ollama models against each other
            # "ollama_to_openrouter_evaluate",  # Uncomment to evaluate Ollama against OpenRouter models
            # "groq_to_ollama_evaluate",  # Uncomment to evaluate GROQ models against Ollama models
            # "groq_to_openrouter_evaluate",  # Uncomment to evaluate GROQ models against OpenRouter models
            "generate_statistics",  # Uncomment to generate and visualize statistical analysis
        ]

    # List of OpenRouter models to be used as participants in the benchmark
    student_openrouter_models = [
        # "google/learnlm-1.5-pro-experimental:free",  # Example model (commented out)
        # "liquid/lfm-40b:free",
        # "meta-llama/llama-3.2-11b-vision-instruct:free",
        "nousresearch/hermes-3-llama-3.1-405b",  # Active OpenRouter model
        # "qwen/qwen-2-7b-instruct:free",
        # "microsoft/phi-3-medium-128k-instruct:free",
    ]
    
    # List of GROQ models to be used as participants in the benchmark
    student_groq_models = [
        # "llama-3.3-70b-versatile",  # Example model (commented out)
        "llama3-70b-8192",  # Active GROQ model
    ]
    
    # List of Ollama models to be used as participants in the benchmark
    # Note: Avoid using semicolons in model names (e.g., "llama3.2:latest")
    student_ollama_models = [
        # "llama3.2",  # Example model (commented out)
        "phi3",  # Active Ollama model
        # "llama3.2",  # Another example (commented out)
    ]

    # Flags to track whether certain steps have been executed
    benchmark_executed = False  # Indicates if benchmarking has been performed
    statistics_generated = False  # Indicates if statistical analysis has been performed

    # Iterate over each step provided in execution_steps to perform corresponding actions
    for step in execution_steps:
        if "generate_statistics" not in step :
            # Log the start of the benchmarking process
            logger.info("Program started successfully.")

            # Initialize the VectorDB_Controller with a parameter to determine if the vector DB should be kept
            vectordb_instance = VectorDB_Controller(keepVectorDB=False)
            
            # Begin the benchmarking process with the specified configurations and models
            begin_benchmark(
                execution_steps,  # List of execution steps
                student_ollama_models,  # List of Ollama student models
                student_groq_models,  # List of GROQ student models
                student_openrouter_models,  # List of OpenRouter student models
                OLLAMA_EVALUATOR_MODEL,  # Ollama evaluator model
                GROQ_EVALUATOR_MODEL,  # GROQ evaluator model
                vectordb_instance,  # Instance of VectorDB_Controller
                benchmark_name,  # Name of the benchmark
                date_now,  # Current date
                answer_rounds,  # Number of answer rounds
            )
            
            # Log the initiation of the benchmarking process
            logger.info("Starting initialization.")
            
            # Update the flag to indicate that benchmarking has been executed
            benchmark_executed = True

        elif step == "generate_statistics":
            # Log the start of the statistical analysis step
            logger.info("Executing generate_statistics step")
            
            # Generate basic statistical charts based on the execution steps and benchmarking results
            create_basic_charts(execution_steps, answer_rounds, benchmark_name, date_now)
            
            # Bind the logger to a specific context ('equator=True') and log the successful generation of statistics
            logger.bind(equator=True).info("Statistics generated successfully.")
            
            # Print a confirmation message to the console
            print("-- DONE STATS --\n")
            
            # Update the flag to indicate that statistical analysis has been executed
            statistics_generated = True


    # After processing all steps, check if any recognized steps were executed
    if not benchmark_executed and not statistics_generated:
        # Log a warning indicating that no valid execution steps were provided
        logger.warning("No execution steps were provided or recognized.")

# Entry point of the script
if __name__ == "__main__":
    main()  # Invoke the main function when the script is run directly
