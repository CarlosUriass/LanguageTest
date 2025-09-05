# LLM-Powered English Level Assessment (Research-Oriented)

[![Python](https://img.shields.io/badge/python-3.10%2B-yellow)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-🚀-teal)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/LLM-OpenAI-ff69b4)](https://openai.com/)
[![Redis](https://img.shields.io/badge/Redis-memory-orange)](https://redis.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-persistent-blue)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)

This project is a **microservice** designed to evaluate a learner’s **English proficiency level** using **Large Language Models (LLMs)**.
The system integrates **prompt-engineering**, **agent-based interaction**, and **memory mechanisms** to approximate **expert human evaluation**, grounded in established theories of language acquisition and assessment.

---

## ✨ Research Motivation

Language assessment has traditionally relied on human raters and standardized tests. With the advent of LLMs, it becomes possible to automate parts of this process while remaining aligned with theoretical frameworks:

- **CEFR (Common European Framework of Reference for Languages):** Provides standardized descriptors (A1–C2) for language proficiency.
- **Canale & Swain’s Communicative Competence Model (1980):** Highlights grammar, sociolinguistic, discourse, and strategic competence.
- **Schmidt’s Noticing Hypothesis (1990):** Emphasizes conscious awareness of linguistic forms as a driver of learning.
- **Vygotsky’s Zone of Proximal Development (ZPD):** Guides adaptive questioning, where the agent acts as a “more knowledgeable other” scaffolding learner progress.

This project experiments with **LLM agents** that embody these principles in a practical, API-based environment.

---

## ✨ Key Features

- 📊 **Automated CEFR Assessment** – Estimates user proficiency levels (A1–C2) from responses.
- 🤖 **LLM-Driven Agent** – Evaluates fluency, accuracy, complexity, and communicative strategies.
- 🧠 **Conversational Memory** – Retains history for adaptive assessment aligned with ZPD principles.
- 🧩 **Research-Ready** – Configurable prompts and rubrics for experimenting with different theoretical models.
- ⚡ **FastAPI Microservice** – Exposes a clean REST API for integration with educational platforms.

---

## 🛠️ Tech Stack

- **FastAPI** – RESTful API framework
- **Python 3.10+**
- **OpenAI LLMs** – Core evaluation engine
- **Redis** – In-memory store for dialogue context
- **PostgreSQL** – Database for assessment results and learner progression
- **Docker** – Portable deployment

---

## 📚 Theoretical Foundations

- **Council of Europe (2020).** Common European Framework of Reference for Languages (CEFR).
- **Canale, M., & Swain, M. (1980).** Theoretical Bases of Communicative Approaches to Second Language Teaching and Testing.
- **Schmidt, R. (1990).** The Role of Consciousness in Second Language Learning. _Applied Linguistics_.
- **Vygotsky, L. (1978).** _Mind in Society: The Development of Higher Psychological Processes._

---

## 🌟 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI](https://openai.com/)
- [LangChain](https://www.langchain.com/)
- Researchers in **SLA (Second Language Acquisition)** and **Computational Linguistics** whose theories inspired this system.
