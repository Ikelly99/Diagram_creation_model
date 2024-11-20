# Diagram Creation Model

This project implements a Python-based model that uses **LangChain** and the **diagrams** package to generate and analyze visual diagrams from natural language descriptions and images. The model interprets user input, provides detailed explanations, and generates diagrams based on the provided input. The project is packaged in a Docker container for easy deployment.

## Features

- **Architecture Creation:** Users provide a natural language description, and the model generates an architecture diagram based on the input.
- **Architecture Analysis:** Users upload an image along with a natural language description, and the model analyzes the diagram, explaining its components and verifying its structure.
- **NLP-Driven Diagram Generation:** Converts human language input into architecture visualizations using the diagrams package.
- **Diagram Explanation:** Offers detailed, human-readable explanations of the generated or analyzed architecture.
- **Streamlit Frontend:** A web interface built with Streamlit to interact with the model, upload images, and view generated diagrams.
- **Security Filtering:** Implements regex-based input validation to detect and block malicious inputs.
- **Dockerized Solution:** Packages everything into a Docker container for consistent and scalable deployment.

## How It Works

### Architecture Creation

1. **Input:**
   - Users enter a natural language description of the desired architecture (e.g., cloud services, infrastructure).
   
2. **Processing:**
   - The model parses the input and generates a corresponding architecture diagram.

3. **Output:**
   - A diagram is displayed along with an explanation of the components and relationships.

### Architecture Analysis

1. **Input:**
   - Users upload an image of an architecture diagram and provide a description for analysis.
   
2. **Processing:**
   - The model analyzes the uploaded diagram, checks its components, and verifies the accuracy against the description.

3. **Output:**
   - A detailed explanation of the diagram is provided, along with insights on its viability and any advantages/disadvantages.

## Setup

### Requirements

- Python 3.8+
- Docker
- Dependencies listed in `requirements.txt`

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Diagram_creation_model
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```bash
   OPENAI_API_KEY=<your_openai_api_key>
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t diagram-creation-model .
   ```
2. Run the Docker container:
   ```bash
   docker run -p 8501:8501 diagram-creation-model
   ```
3. Access the app in your browser at `http://localhost:8501`.

## Project Structure

- **app.py:** Main entry point for the Streamlit app.
- **class_model_diagram.py:** Functions for generating and analyzing architecture diagrams.
- **diagram_image_generation_test.py:** Logic for converting text descriptions into diagrams.
- **input_validator.py:** Validates user input to ensure safe and accurate processing.
- **image_analysis.py:** Analyzes uploaded images to verify and explain diagram structures.
- **utils.py:** Provides helper functions, including input filtering and utility tasks.
- **Dockerfile:** Defines the Docker setup for the application.

## Contributors

@Rudolphcljc Rodolfo Carlos Lagunas Jardines
@fermoregom Fernando Moreno Gomez
@Ikelly99 Isaac Kelly Ramirez
