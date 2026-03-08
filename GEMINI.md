# Project Context: Agentic RAG Log Triage System
## Core Objective:

    - We are building a production-ready, automated debugging agent designed for high-throughput environments (like semiconductor testing or complex network infrastructure). The goal is to completely eliminate manual log scrolling. The system ingests raw system failure logs, standardizes them, cross-references the errors against official documentation, and generates a verifiable, actionable fix report.

# Architectural Scope
    - The pipeline is strictly divided into three distinct operations.

## Knowledge Base Ingestion: 
    - We process official technical manuals into text chunks and store them locally in a Chroma vector database. This establishes a ground truth and prevents the LLM from hallucinating fixes.

## Log Parsing via Drain3: 
  - We abandon regular expressions. We pipe raw text logs through the drain3 library to automatically extract the static log template and isolate the dynamic error variables (like specific hex codes, timestamps, or IP addresses).

# Agentic Synthesis: 
    The agent queries the Chroma database using the clean, static drain3 template to retrieve the exact documentation matching the error. It then feeds those official docs and the isolated dynamic variables to the LLM to output a clean Markdown report detailing the root cause and the required fix.

# Operational Boundaries

- The system must remain domain-agnostic. It should function identicality whether fed standard Linux syslogs or proprietary semiconductor test output.

- All generated reports must be deterministic and easily verifiable by a human engineer referencing the original source manual.

- The local Python environment acts as the central router. It hands data between the local file system, the Chroma database, and the Gemini CLI.

# Additional Guidelines:
  - This project is inspired by [Medical Assistant RAG](Project_5_MedicalAssistant_Full_Code_NLP_RAG_ChinmayRozekar_CLEANED.ipynb) jupyter notebook
  - The aim of this project is to implement a solution something like this but for production quality software.
  - We will not use any jupyter nb
  - we will most likely need to set up a .venv for this project
  - we also need a .gitignore for such a large chromadb
  - we are not using Ollama as described in the jupyter nb, everything is being run locally on the machine. but we will use Gemini CLI 
  - We should be using most of the libraries mentioned in the jupyter nb along with Drain3 library
  - At the end / completion of this project , we aim to ship an executable binary file that takes user input on the terminal with flags (options) 
  - The tool should have a help menu as well.
  
# My system Information:
      Model Name: MacBook Pro
      Model Identifier: Mac16,1
      Chip: Apple M4
      Memory: 16 GB
      Serial Number (system): K41N9KG47P
ProductName:            macOS
ProductVersion:         15.6
BuildVersion:           24G84