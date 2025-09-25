# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-01-09

**Author:** Carlos Urias  
**Status:** Alpha Release  
**Priority:** High (Complete refactoring and feature implementation)

### Added

- **Clean Architecture Implementation**: Complete refactoring to hexagonal architecture with proper separation of concerns
  - Domain layer with entities, value objects, and repository interfaces
  - Application layer with use cases and DTOs
  - Infrastructure layer with external services and persistence
  - Presentation layer with API endpoints and schemas
- **Final Evaluation System**: Complete implementation of final evaluation pipeline
  - Final evaluation entities and value objects
  - Final evaluation repository with SQLAlchemy implementation
  - Final evaluation use case with comprehensive business logic
  - API endpoint for final evaluations (`POST /final-evaluation`)
- **Enhanced LLM Integration**: Robust OpenAI LLM service with improved error handling
  - Flexible JSON response parsing (handles both nested and flat formats)
  - Comprehensive prompt engineering for consistent evaluation feedback
  - Fallback mechanisms for response format variations
- **Improved Database Schema**: Enhanced database structure with proper indexing
  - Questions table with initial data seeding
  - Evaluations table with detailed scoring fields
  - Final evaluations table for comprehensive assessment results
  - Proper database comments and documentation
- **Dependency Injection**: Complete DI container implementation for loose coupling
- **Comprehensive Testing**: Full API testing with real evaluation scenarios

### Changed

- **Project Structure**: Complete reorganization following Clean Architecture principles
- **Database Migrations**: Unified migration system with single comprehensive schema file
- **API Responses**: Standardized response formats with proper error messages
- **LLM Service**: Enhanced to handle variable OpenAI response formats
- **Evaluation Logic**: Improved scoring algorithm with CEFR level assessment

### Fixed

- **JSON Parsing Issues**: Resolved LLM response parsing errors with flexible format handling
- **Import Dependencies**: Fixed all import paths after architecture refactoring
- **Database Schema**: Corrected table relationships and data types
- **Error Handling**: Comprehensive exception handling across all layers
- **Memory Leaks**: Proper session management and resource cleanup

### Removed

- **Legacy Code**: Eliminated 20+ obsolete files from previous architecture
  - Old models, repositories, controllers, and services
  - Duplicate configurations and utilities
  - Unused dependencies and imports
- **Redundant Migrations**: Consolidated multiple migration files into single schema

### Technical Debt

- **Code Quality**: Eliminated spaghetti code through proper architectural patterns
- **Maintainability**: Improved code organization and separation of concerns
- **Testability**: Enhanced testability through dependency injection and clean interfaces

### Notes

- **Major Version Bump**: Due to complete architectural refactoring and breaking changes
- **Production Ready**: Full evaluation pipeline functional with comprehensive error handling
- **API Stability**: All endpoints tested and validated with real-world scenarios
- **Database Integrity**: Proper schema with indexes and referential integrity

---

## [0.0.1] - 2025-08-30

**Author:** Carlos Urias  
**Status:** Pre-Alpha (Internal release)  
**Priority:** High (Core architecture & integrations)

### Added

- Initial project structure and build setup.
- Integration with **PostgreSQL** for persistent data storage.
- Integration with **Redis** for in-memory caching.
- Connection and setup with **OpenAI LLM** for language evaluation.
- Preliminary implementation of core functionality: user language assessment endpoint (basic, not fully complete).

### Changed

- N/A

### Fixed

- N/A

### Pending / TODO

- Complete evaluation scoring logic.
- Implement question bank management.
- Add multi-language support (Spanish, French, German, etc.).
- Integration with internal dashboard for results visualization.
- Automated testing and CI/CD pipeline setup.

### Notes

- This is the **first internal release** to validate architecture and core integrations.
- Core functionality is **preliminary**; scoring logic and evaluation flow will be refined in future versions.
- Intended for **internal testing only**.
- Future releases should include **code reviews, unit tests, and internal QA approval** before deployment.

---
