from typing import List
from app.application.evaluation.dtos.initial_evaluation_dto import InitialEvaluationListDTO
from app.domain.entities.evaluation import Evaluation
from app.infrastructure.repositories.questions_repositorie_impl import QuestionRepository
from app.core.langchain_client import LangBuddyLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class EvaluationService:
    def __init__(self, llm: LangBuddyLLM, question_repo: QuestionRepository):
        self.llm = llm
        self.question_repo = question_repo

    def evaluate_answers(self, evaluation_dto: InitialEvaluationListDTO) -> dict:
        # Obtener preguntas desde la base de datos según los IDs de answers
        question_ids = [answer.question_id for answer in evaluation_dto.answers]
        questions = self.question_repo.get_questions_by_ids(question_ids)
        
        # Preparar diccionario de preguntas y respuestas
        answers_dict = {answer.question_id: answer.answer for answer in evaluation_dto.answers}
        questions_dict = {q.id: q.question for q in questions} 

        # Crear prompt de LangChain con base científica integrada
        prompt_template = PromptTemplate(
            input_variables=["answers", "questions"],
            template="""
Return ONLY valid JSON. DO NOT include any extra text.

You are an expert English language evaluator. Your analysis must be grounded in established linguistic and pedagogical principles.

---
EVALUATION FRAMEWORK AND SCIENTIFIC BASIS:
You must adhere to the following framework, which is based on the Common European Framework of Reference for Languages (CEFR) and principles of language acquisition.

1.  **Multi-component Competence Assessment:** Your evaluation of `scores` must break down proficiency into its core components, as defined by communicative competence models (Canale & Swain, 1980):
    * **Grammar (Accuracy):** The ability to use syntactic and morphological rules correctly.
    * **Vocabulary (Lexical Resource):** The range and precision of the user's lexicon.
    * **Fluency:** The ability to produce language at a natural pace with minimal hesitation, reflecting cognitive automaticity.

2.  **CEFR-Aligned Question Analysis:** The provided questions are designed to elicit responses that correspond to specific CEFR levels. You must use this understanding to estimate the `estimated_level`:
    * **A1-A2 Level Questions (e.g., 'What did you do last weekend?'):** Assess the ability to use basic tenses for familiar topics.
    * **B1 Level Questions (e.g., 'Describe a challenge you overcame'):** Assess narrative structure, use of connectors, and expression of opinions on concrete topics.
    * **B2 Level Questions (e.g., 'How has technology changed your life?'):** Assess the ability to develop clear arguments on complex/abstract topics and use a wider range of language.
    * **C1-C2 Level Questions (e.g., Discussing abstract quotes or ethical dilemmas):** Assess advanced skills like interpreting figurative language, constructing counterfactual arguments, and expressing nuanced ideas with precision.

3.  **Formative Feedback Principle (Mistakes & Suggestions):** Your feedback must facilitate learning. Based on Schmidt's "Noticing Hypothesis" (1990), you must explicitly identify `mistakes` and provide clear `suggestions` to help the user notice the gap between their output and the correct form.

4.  **Adaptive Assessment Principle (Next Questions):** The 5 new questions you generate must be targeted at the user's diagnosed overall level. This aligns with Vygotsky's "Zone of Proximal Development," ensuring the user is challenged appropriately to stimulate further learning.
---

User answers (JSON):
{{
"answers": {answers},
"questions": {questions}
}}

Instructions:
- Guided strictly by the EVALUATION FRAMEWORK above, evaluate each answer individually.
- For each answer, provide feedback with these fields:
    - question
    - answer
    - estimated_level (A1-C2): Justified by the CEFR-Aligned Question Analysis.
    - scores: {{grammar, vocabulary, fluency}}: Assessed according to the Multi-component Competence model.
    - mistakes: A list of specific errors.
    - suggestions: A list of concrete corrections or better alternatives.
- Provide an `overall level`, average `scores`, and a short `reason` that explicitly references the framework.
- Generate 5 new English `next_questions` suitable for the user's diagnosed level, following the Adaptive Assessment Principle.

Return strictly in this format:
{{
"evaluation": {{
    "level": "A1-C2",
    "scores": {{"grammar": 0.0, "vocabulary": 0.0, "fluency": 0.0}},
    "reason": "string",
    "feedback": [
    {{
        "question": "string",
        "answer": "string",
        "estimated_level": "A1-C2",
        "scores": {{"grammar": 0.0, "vocabulary": 0.0, "fluency": 0.0}},
        "mistakes": ["string"],
        "suggestions": ["string"]
    }}
    ]
}},
"next_questions": [
    "Question 1", "Question 2", "...", "Question 5"
]
}}
            """
        )

        # Instanciar LLMChain y ejecutar
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        result = chain.run({
            "answers": answers_dict,
            "questions": questions_dict
        })

        return result
