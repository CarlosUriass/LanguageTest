# Instrucciones para probar la API LanguageTest

## 🚀 Cómo probar los endpoints

### 1. Iniciar el servidor

```bash
# En una terminal, activa el virtual environment y ejecuta:
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### 2. Probar con el script de Python (Recomendado)

```bash
# En otra terminal:
python test_endpoints.py
```

### 3. Probar con curl

```bash
# Ejecutar el script de curl:
./test_curl.sh
```

### 4. Probar endpoints individuales

#### Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

#### Listar Preguntas

```bash
curl -X GET "http://localhost:8000/api/v1/questions/"
```

#### Evaluación Inicial

```bash
curl -X POST "http://localhost:8000/api/v1/evaluation/initial" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 123,
    "answers": [
      {
        "question_id": 1,
        "answer": "I like to read books and watch movies in my free time."
      },
      {
        "question_id": 2,
        "answer": "My name is Carlos and I study computer science."
      }
    ]
  }'
```

#### Evaluación Final

```bash
curl -X POST "http://localhost:8000/api/v1/evaluation/final" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 123,
    "answers": [
      {"answer": "Technology has transformed how we communicate."},
      {"answer": "Learning languages opens many opportunities."}
    ]
  }'
```

### 5. Ver documentación interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 6. Ejemplos de respuestas esperadas

#### Health Check Response:

```json
{
  "status": "healthy",
  "service": "Language Test API"
}
```

#### List Questions Response:

```json
{
  "questions": [
    { "id": 1, "question": "What did you do last weekend?" },
    { "id": 2, "question": "Tell me about yourself." }
  ]
}
```

#### Initial Evaluation Response:

```json
{
  "level": "B1",
  "scores": {"grammar": 7.5, "vocabulary": 8.0, "fluency": 7.0},
  "reason": "Based on overall performance...",
  "feedback": [...],
  "next_questions": [...]
}
```

#### Final Evaluation Response:

```json
{
  "final_level": "B1"
}
```

### 7. Solución de problemas comunes

#### Error de conexión:

- Verificar que el servidor esté ejecutándose en el puerto 8000
- Revisar que no haya otros procesos usando el puerto

#### Error de base de datos:

- Verificar que PostgreSQL esté ejecutándose
- Revisar las variables de entorno en el archivo .env

#### Error de Redis:

- Verificar que Redis esté ejecutándose
- Revisar la configuración de Redis en .env

#### Error de OpenAI:

- Verificar que OPENAI_API_KEY esté configurada correctamente
- Revisar que tengas créditos disponibles en tu cuenta de OpenAI
