# LLM-Powered English Level Assessment (Research-Oriented)

[![Python](https://img.shields.io/badge/python-3.10%2B-yellow)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-🚀-teal)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/LLM-OpenAI-ff69b4)](https://openai.com/)
[![Redis](https://img.shields.io/badge/Redis-memory-orange)](https://redis.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-persistent-blue)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)

A **production-ready microservice** for automated English proficiency assessment using **Large Language Models (LLMs)**, built with **Clean Architecture** principles and **Domain-Driven Design**.

---

## 🏗️ Architecture Overview

This project follows **Clean Architecture** principles with clear separation of concerns:

```
├── domain/              # Business Logic & Entities
│   ├── entities/        # Core business entities
│   ├── value_objects/   # Immutable value types
│   ├── repositories/    # Repository interfaces
│   └── services/        # Domain services
├── application/         # Use Cases & Application Logic
│   ├── use_cases/       # Business use cases
│   ├── dtos/           # Data transfer objects
│   └── ports/          # Service interfaces
├── infrastructure/     # External Dependencies
│   ├── persistence/    # Database implementations
│   └── external_services/ # Third-party services
├── presentation/       # API Layer
│   ├── api/           # REST API endpoints
│   └── schemas/       # API schemas
└── core/              # Configuration & Cross-cutting
    ├── config/        # Application settings
    ├── interfaces/    # Core interfaces
    └── exceptions/    # Custom exceptions
```

## ✨ Key Features

### 🎯 **SOLID Principles Implementation**

- **Single Responsibility**: Each class has one reason to change
- **Open/Closed**: Extensible without modification
- **Liskov Substitution**: Interfaces properly implemented
- **Interface Segregation**: Focused, cohesive interfaces
- **Dependency Inversion**: High-level modules don't depend on low-level modules

### 📊 **Assessment Capabilities**

- **CEFR Level Detection** (A1-C2) based on linguistic analysis
- **Multi-dimensional Scoring** (Grammar, Vocabulary, Fluency)
- **Adaptive Questioning** using Vygotsky's ZPD principles
- **Detailed Feedback** with mistakes and suggestions

### 🔧 **Technical Excellence**

- **Clean Architecture** with dependency inversion
- **Use Case Driven** business logic
- **Repository Pattern** for data access abstraction
- **Port/Adapter Pattern** for external service integration
- **Comprehensive Error Handling** with custom exceptions

---

## 🛠️ Technology Stack

| Layer             | Technology                       |
| ----------------- | -------------------------------- |
| **API Framework** | FastAPI with Pydantic validation |
| **Language**      | Python 3.10+ with type hints     |
| **AI/ML**         | OpenAI GPT models via LangChain  |
| **Database**      | PostgreSQL with SQLAlchemy ORM   |
| **Cache**         | Redis for session management     |
| **DI Container**  | dependency-injector              |
| **Deployment**    | Docker & Docker Compose          |

---

## 📚 API Endpoints

### Questions

- `GET /api/v1/questions/` - List all available questions

### Evaluation

- `POST /api/v1/evaluation/initial` - Initial assessment
- `POST /api/v1/evaluation/final` - Final level determination

---

## 🧪 Domain Model

### Value Objects

- **CEFRLevel**: Enumeration of language levels (A1-C2)
- **Scores**: Immutable score object with validation

### Entities

- **Question**: Assessment questions
- **Evaluation**: Assessment results and feedback

### Services

- **LevelCalculatorService**: Domain logic for level calculation
- **LLMService**: AI-powered evaluation
- **MemoryService**: Context management

---

## 🏛️ Design Patterns Used

| Pattern          | Implementation                                       | Purpose                      |
| ---------------- | ---------------------------------------------------- | ---------------------------- |
| **Repository**   | `QuestionRepository`, `EvaluationRepository`         | Data access abstraction      |
| **Use Case**     | `InitialEvaluationUseCase`, `FinalEvaluationUseCase` | Business logic orchestration |
| **Port/Adapter** | `LLMServicePort`, `MemoryServicePort`                | External service integration |
| **Value Object** | `CEFRLevel`, `Scores`                                | Immutable business values    |
| **Factory**      | Dependency injection container                       | Object creation              |
| **Strategy**     | Different LLM evaluation strategies                  | Algorithm encapsulation      |

---

## 🔍 Code Quality

- **Type Safety**: Full type annotations with mypy compatibility
- **Error Handling**: Custom exception hierarchy
- **Validation**: Pydantic models with business rule validation
- **Testing**: Unit tests for use cases and domain services
- **Documentation**: Comprehensive docstrings and API docs

---

## 📈 Scalability & Performance

- **Layered Architecture**: Easy to scale individual components
- **Caching Strategy**: Redis for session management
- **Database Optimization**: Proper indexing and query optimization
- **Async Support**: FastAPI's async capabilities
- **Containerization**: Docker for consistent deployment

---

## 🤝 Contributing

1. Follow the established architecture patterns
2. Maintain clean separation of concerns
3. Write tests for new use cases
4. Update documentation for API changes
5. Use type hints consistently

---

## 📚 Theoretical Foundations

This system implements established language assessment theories:

- **CEFR Framework**: Standardized proficiency descriptors
- **Communicative Competence Model**: Multi-dimensional assessment
- **Zone of Proximal Development**: Adaptive questioning
- **Noticing Hypothesis**: Explicit error feedback

---

## 🌟 Acknowledgements

- **Clean Architecture** by Robert C. Martin
- **Domain-Driven Design** by Eric Evans
- **CEFR Framework** by Council of Europe
- **FastAPI** framework by Sebastián Ramírez

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
