-- =============================================================================
-- LanguageTest Database Schema
-- =============================================================================
-- Script para crear todas las tablas necesarias en la base de datos LanguageTest
-- Ejecutar en PostgreSQL
-- Versión: 2.0
-- Fecha: 2025-09-25

-- =============================================================================
-- TABLA: questions
-- =============================================================================
-- Almacena las preguntas disponibles para las evaluaciones
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Índices para tabla questions
CREATE INDEX IF NOT EXISTS idx_questions_created_at ON questions(created_at);

-- Comentarios para documentación
COMMENT ON TABLE questions IS 'Almacena las preguntas disponibles para las evaluaciones de inglés';
COMMENT ON COLUMN questions.question IS 'Texto de la pregunta';

-- =============================================================================
-- TABLA: evaluations
-- =============================================================================
-- Almacena los resultados de las evaluaciones iniciales de los usuarios
CREATE TABLE IF NOT EXISTS evaluations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    estimated_level VARCHAR(10) NOT NULL,
    grammar FLOAT NOT NULL,
    vocabulary FLOAT NOT NULL,
    fluency FLOAT NOT NULL,
    mistakes TEXT NOT NULL,  -- JSON string
    suggestions TEXT NOT NULL,  -- JSON string
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para tabla evaluations
CREATE INDEX IF NOT EXISTS idx_evaluations_user_id ON evaluations(user_id);
CREATE INDEX IF NOT EXISTS idx_evaluations_level ON evaluations(estimated_level);
CREATE INDEX IF NOT EXISTS idx_evaluations_created_at ON evaluations(created_at);

-- Comentarios para documentación
COMMENT ON TABLE evaluations IS 'Almacena los resultados detallados de las evaluaciones iniciales';
COMMENT ON COLUMN evaluations.user_id IS 'ID del usuario que realizó la evaluación';
COMMENT ON COLUMN evaluations.question IS 'Pregunta que se le hizo al usuario';
COMMENT ON COLUMN evaluations.answer IS 'Respuesta proporcionada por el usuario';
COMMENT ON COLUMN evaluations.estimated_level IS 'Nivel CEFR estimado para esta respuesta (A1-C2)';
COMMENT ON COLUMN evaluations.grammar IS 'Puntuación de gramática (0.0-10.0)';
COMMENT ON COLUMN evaluations.vocabulary IS 'Puntuación de vocabulario (0.0-10.0)';
COMMENT ON COLUMN evaluations.fluency IS 'Puntuación de fluidez (0.0-10.0)';
COMMENT ON COLUMN evaluations.mistakes IS 'Lista de errores identificados (JSON)';
COMMENT ON COLUMN evaluations.suggestions IS 'Lista de sugerencias de mejora (JSON)';

-- =============================================================================
-- TABLA: final_evaluations
-- =============================================================================
-- Almacena los resultados de las evaluaciones finales de los usuarios
CREATE TABLE IF NOT EXISTS final_evaluations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    initial_level VARCHAR(10),
    final_level VARCHAR(10) NOT NULL,
    reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Índices para tabla final_evaluations
CREATE INDEX IF NOT EXISTS idx_final_evaluations_user_id ON final_evaluations(user_id);
CREATE INDEX IF NOT EXISTS idx_final_evaluations_created_at ON final_evaluations(created_at);
CREATE INDEX IF NOT EXISTS idx_final_evaluations_final_level ON final_evaluations(final_level);

-- Comentarios para documentación
COMMENT ON TABLE final_evaluations IS 'Almacena los resultados de las evaluaciones finales de los usuarios';
COMMENT ON COLUMN final_evaluations.user_id IS 'ID del usuario que realizó la evaluación';
COMMENT ON COLUMN final_evaluations.initial_level IS 'Nivel determinado en la evaluación inicial';
COMMENT ON COLUMN final_evaluations.final_level IS 'Nivel final determinado por el LLM';
COMMENT ON COLUMN final_evaluations.reason IS 'Explicación del LLM para el nivel final asignado';

-- =============================================================================
-- DATOS INICIALES
-- =============================================================================
-- Insertar preguntas básicas si no existen
INSERT INTO questions (question) VALUES 
    ('What did you do last weekend?'),
    ('Describe your best friend.'),
    ('Tell me about a time you faced a challenge and how you overcame it.'),
    ('What are the advantages and disadvantages of social media?'),
    ('If you could travel anywhere in the world, where would you go and why?'),
    ('How has technology changed your life in the last ten years?'),
    ('To what extent do you think automation and AI will affect the future of employment?'),
    ('"Art is not a mirror to reflect reality, but a hammer with which to shape it." What does this quote mean to you?'),
    ('If you had been born in a different country, how would your life have been different?'),
    ('Discuss an ethical dilemma you''ve read about or seen in a film and explain your position on it.')
ON CONFLICT DO NOTHING;

-- =============================================================================
-- VERIFICACIÓN
-- =============================================================================
-- Verificar que todas las tablas existen
SELECT 
    table_name,
    table_type
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('questions', 'evaluations', 'final_evaluations')
ORDER BY table_name;

-- Mostrar conteo de registros
SELECT 
    'questions' as table_name, 
    COUNT(*) as record_count 
FROM questions
UNION ALL
SELECT 
    'evaluations' as table_name, 
    COUNT(*) as record_count 
FROM evaluations
UNION ALL
SELECT 
    'final_evaluations' as table_name, 
    COUNT(*) as record_count 
FROM final_evaluations;