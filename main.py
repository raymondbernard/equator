# main.py

import configparser
from loguru import logger
from dotenv import load_dotenv
from equator_qa.charting import create_basic_charts
from equator_qa.utils import begin_benchmark, cleanup_chromadb
from equator_qa.vectordb import VectorDB_Controller
import load_images
import create_vision_json
from datetime import datetime
import sys

def validate_config(config):
    """
    Validates the presence of required sections and options in the config.ini file.
    Raises a ValueError if any required configuration is missing.
    """
    required_sections = {
        "rounds": ["answer_rounds"],
        "BENCHMARK_NAME": ["benchmark_name"],
        "evaluator_models": ["GROQ_EVALUATOR_MODEL", "OLLAMA_EVALUATOR_MODEL"],
        "execution_steps": ["EXECUTION_STEPS"],
        "student_models": ["STUDENT_OPENROUTER_MODELS", "STUDENT_GROQ_MODELS", "STUDENT_OLLAMA_MODELS"],
        "vision": ["VISION_DB"],
        "parquet": ["PARQUET"],
        "keep_vector_db": ["KEEP_VECTOR_DB"],
    }

    for section, keys in required_sections.items():
        if not config.has_section(section):
            logger.error(f"Missing required section: [{section}] in config.ini")
            raise ValueError(f"Missing required section: [{section}] in config.ini")
        for key in keys:
            if not config.has_option(section, key):
                logger.error(f"Missing required option '{key}' in section [{section}] in config.ini")
                raise ValueError(f"Missing required option '{key}' in section [{section}] in config.ini")

def main():
    """
    Main function to execute benchmarking and statistical analysis based on provided steps.

    Parameters:
        execution_steps (list, optional): A list of steps to execute. If None, defaults to a predefined list.
    """

    # Initialize the parser
    config = configparser.ConfigParser()

    # Read the INI file
    config.read("config.ini")

    # Load environment variables from the .env file to configure the application
    load_dotenv()

    # Validate the configuration
    try:
        validate_config(config)
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)

    # Capture the current date in YYYY-MM-DD format for logging and organizing results
    date_now = datetime.now().strftime("%Y-%m-%d")

    # Define the evaluator models used for benchmarking
    GROQ_EVALUATOR_MODEL = config["evaluator_models"]["GROQ_EVALUATOR_MODEL"]
    OLLAMA_EVALUATOR_MODEL = config["evaluator_models"]["OLLAMA_EVALUATOR_MODEL"]

    # Use configparser's getboolean method for boolean values
    try:
        VISION_DB = config.getboolean("vision", "VISION_DB")
        PARQUET = config.getboolean("parquet", "PARQUET")
        KEEP_VECTOR_DB = config.getboolean("keep_vector_db", "KEEP_VECTOR_DB")
    except ValueError as e:
        logger.error(f"Boolean conversion error: {e}")
        sys.exit(1)

    if not KEEP_VECTOR_DB:
        cleanup_chromadb()

    # Number of times each question will be posed to the models
    try:
        ANSWER_ROUNDS = config.getint("rounds", "answer_rounds")
    except ValueError:
        logger.error("Invalid value for 'answer_rounds'. It must be an integer.")
        sys.exit(1)

    # Identifier name for the current benchmark run
    BENCHMARK_NAME = config["BENCHMARK_NAME"]["benchmark_name"]

    if VISION_DB and PARQUET:
        load_images.main()
        create_vision_json.create_vision_benchmark_json()

    # Parse comma-separated execution steps into a list
    EXECUTION_STEPS = [step.strip() for step in config["execution_steps"]["EXECUTION_STEPS"].split(",")]

    # Parse student models
    STUDENT_OPENROUTER_MODELS = [
        model.strip() for model in config["student_models"]["STUDENT_OPENROUTER_MODELS"].split(",") if model.strip()
    ]

    STUDENT_GROQ_MODELS = [
        model.strip() for model in config["student_models"]["STUDENT_GROQ_MODELS"].split(",") if model.strip()
    ]

    STUDENT_OLLAMA_MODELS = [
        model.strip() for model in config["student_models"]["STUDENT_OLLAMA_MODELS"].split(",") if model.strip()
    ]

    # Flags to track whether certain steps have been executed
    benchmark_executed = False  # Indicates if benchmarking has been performed
    statistics_generated = False  # Indicates if statistical analysis has been performed

    # Iterate over each step provided in execution_steps to perform corresponding actions
    for step in EXECUTION_STEPS:
        if step != "generate_statistics":
            # Log the start of the benchmarking process
            logger.info("Program started successfully.")

            # Initialize the VectorDB_Controller with a parameter to determine if the vector DB should be kept
            vectordb_instance = VectorDB_Controller(keepVectorDB=KEEP_VECTOR_DB, VISION=VISION_DB)

            # Begin the benchmarking process with the specified configurations and models
            begin_benchmark(
                VISION_DB,
                EXECUTION_STEPS,  # List of execution steps
                STUDENT_OLLAMA_MODELS,  # List of Ollama student models
                STUDENT_GROQ_MODELS,  # List of GROQ student models
                STUDENT_OPENROUTER_MODELS,  # List of OpenRouter student models
                OLLAMA_EVALUATOR_MODEL,  # Ollama evaluator model
                GROQ_EVALUATOR_MODEL,  # GROQ evaluator model
                vectordb_instance,  # Instance of VectorDB_Controller
                BENCHMARK_NAME,  # Name of the benchmark
                date_now,  # Current date
                ANSWER_ROUNDS,  # Number of answer rounds
            )

            # Log the initiation of the benchmarking process
            logger.info("Starting initialization.")

            # Update the flag to indicate that benchmarking has been executed
            benchmark_executed = True

        elif step == "generate_statistics":
            # Log the start of the statistical analysis step
            logger.info("Executing generate_statistics step")

            # Generate basic statistical charts based on the execution steps and benchmarking results
            create_basic_charts(EXECUTION_STEPS, ANSWER_ROUNDS, BENCHMARK_NAME, date_now)

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

# Note:
# Do NOT run Ollama on the same machine without Docker.
# You can run Ollama on separate machines remotely with or without Docker.
# To use a remote instance, update the URL and port.
