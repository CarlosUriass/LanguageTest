import json
from typing import List
from app.application.evaluation.dtos.final_evaluation_dto import FinalEvaluationListDTO
from app.application.evaluation.dtos.initial_evaluation_dto import InitialEvaluationListDTO
from app.domain.entities.evaluation import Evaluation
from app.infrastructure.repositories.questions_repositorie_impl import QuestionRepository
from app.infrastructure.repositories.evaluation_repository import EvaluationRepository
from app.core.langchain_client import LangBuddyLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.application.memory.services.memory_service import MemoryService
from langchain.schema import HumanMessage, AIMessage

class EvaluationService:
    def __init__(
        self,
        llm: LangBuddyLLM,
        question_repo: QuestionRepository,
        evaluation_repo: EvaluationRepository,
        memory_service_factory
    ):
        self.llm = llm
        self.question_repo = question_repo
        self.evaluation_repo = evaluation_repo
        self.memory_service_factory = memory_service_factory

    def evaluate_answers(self, evaluation_dto: InitialEvaluationListDTO) -> dict:

        # --- Crear MemoryService dinámicamente con session_id ---
        session_id = str(evaluation_dto.user_id)
        memory_service: MemoryService = self.memory_service_factory
        memory_service.set_session_id(session_id)

        # --- Obtener preguntas ---
        question_ids = [answer.question_id for answer in evaluation_dto.answers]
        questions = self.question_repo.get_questions_by_ids(question_ids)

        # --- Preparar diccionarios de preguntas y respuestas ---
        answers_dict = {answer.question_id: answer.answer for answer in evaluation_dto.answers}
        questions_dict = {q.id: q.question for q in questions}

        # --- Prompt completo ---
        prompt_template = PromptTemplate(
            input_variables=["answers", "questions"],
            template="""Return ONLY valid JSON. DO NOT include any extra text.
You are an expert English language evaluator.
Your analysis must be grounded in established linguistic and pedagogical principles.
--- EVALUATION FRAMEWORK AND SCIENTIFIC BASIS: You must adhere to the following framework, which is based on the Common European Framework of Reference for Languages (CEFR)
and principles of language acquisition.

1. **Multi-component Competence Assessment:** Your evaluation of scores must break down proficiency into its core components, as defined by communicative competence models (Canale & Swain, 1980):
* **Grammar (Accuracy):** The ability to use syntactic and morphological rules correctly. 
* **Vocabulary (Lexical Resource):** The range and precision of the user's lexicon.
* **Fluency:** The ability to produce language at a natural pace with minimal hesitation, reflecting cognitive automaticity.

2. **CEFR-Aligned Question Analysis:** The provided questions are designed to elicit responses that correspond to specific CEFR levels. You must use this understanding to estimate the estimated_level:
* **A1-A2 Level Questions (e.g., 'What did you do last weekend?'):** Assess the ability to use basic tenses for familiar topics.
* **B1 Level Questions (e.g., 'Describe a challenge you overcame'):** Assess narrative structure, use of connectors, and expression of opinions on concrete topics.
* **B2 Level Questions (e.g., 'How has technology changed your life?'):** Assess the ability to develop clear arguments on complex/abstract topics and use a wider range of language.
* **C1-C2 Level Questions (e.g., Discussing abstract quotes or ethical dilemmas):** Assess advanced skills like interpreting figurative language, constructing counterfactual arguments, and expressing nuanced ideas with precision.

3. **Formative Feedback Principle (Mistakes & Suggestions):**
** Your feedback must facilitate learning. Based on Schmidt's "Noticing Hypothesis" (1990), you must explicitly identify mistakes and provide clear suggestions to help the user notice the gap between their output and the correct form.

4. **Adaptive Assessment Principle (Next Questions):**
** The 5 new questions you generate must be targeted at the user's diagnosed overall level. This aligns with Vygotsky's "Zone of Proximal Development," ensuring the user is challenged appropriately to stimulate further learning.

--- User answers (JSON): {{ "answers": {answers}, "questions": {questions} }}

Instructions: - Guided strictly by the EVALUATION FRAMEWORK above, evaluate each answer individually.
- For each answer, provide feedback with these fields: question, answer, estimated_level, scores, mistakes, suggestions.
- Do not skip any answer. Evaluate **all provided answers**, even if there are more than 5.
- Provide an overall level, average scores, and a short reason that explicitly references the framework.
- Generate 5 new next_questions suitable for the user's diagnosed level (this is separate from the evaluation feedback).
- For each answer, provide feedback with these fields:
    - question
    - answer
    - estimated_level (A1-C2): Justified by the CEFR-Aligned Question Analysis.
    - scores: {{grammar, vocabulary, fluency}}: Assessed according to the Multi-component Competence model. 
    - mistakes: A list of specific errors.
    - suggestions: A list of concrete corrections or better alternatives.
- Provide an overall level, average scores, and a short reason that explicitly references the framework.
- Generate 5 new English next_questions suitable for the user's diagnosed level, following the Adaptive Assessment Principle. 

Return strictly in this format:
{{ "evaluation": {{ "level": "A1-C2", "scores": {{"grammar": 0.0, "vocabulary": 0.0, "fluency": 0.0}}, "reason": "string", "feedback": [ {{ "question": "string", "answer": "string", "estimated_level": "A1-C2", "scores": {{"grammar": 0.0, "vocabulary": 0.0, "fluency": 0.0}}, "mistakes": ["string"], "suggestions": ["string"] }} ] }}, "next_questions": [ "Question 1", "Question 2", "...", "Question 5" ] }}"""
        )

        # --- Ejecutar LLMChain ---
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        result_str = chain.run({"answers": answers_dict, "questions": questions_dict})

        # --- Parsear JSON ---
        try:
            result = json.loads(result_str)
        except json.JSONDecodeError:
            raise ValueError(f"LLM no devolvió un JSON válido:\n{result_str}")

        # --- Resumen de evaluación ---
        evaluation_summary = {
            "level": result["evaluation"]["level"],
            "scores": result["evaluation"]["scores"],
            "feedback": result["evaluation"]["feedback"],
            "next_questions": result.get("next_questions", [])
        }

        # --- Guardar en memoria ---
        memory_service.save_context(
        {"input": "initial_evaluation"},
        {"output": json.dumps(evaluation_summary)}
        )


        # --- Guardar feedback en DB ---
        for fb in evaluation_summary["feedback"]:
            evaluation_entity = Evaluation(
                user_id=evaluation_dto.user_id,
                question=fb.get("question", ""),
                answer=fb.get("answer", ""),
                estimated_level=fb.get("estimated_level", ""),
                grammar=fb.get("scores", {}).get("grammar", 0.0),
                vocabulary=fb.get("scores", {}).get("vocabulary", 0.0),
                fluency=fb.get("scores", {}).get("fluency", 0.0),
                mistakes=json.dumps(fb.get("mistakes", [])),
                suggestions=json.dumps(fb.get("suggestions", [])),
            )
            self.evaluation_repo.save_responses(evaluation_entity)
            
        return {"next_questions": evaluation_summary.get("next_questions", [])}
    
    def final_evaluation(self, evaluation_dto: FinalEvaluationListDTO) -> str:
        session_id = str(evaluation_dto.user_id)
        memory_service: MemoryService = self.memory_service_factory
        memory_service.set_session_id(session_id)

        # --- Cargar historial desde Redis ---
        previous_context = memory_service.load_memory_variables()
        history = previous_context.get("history", [])

        # --- Recuperar evaluación inicial ---
        last_evaluation = None
        for idx, msg in enumerate(history):
            if getattr(msg, "type", None) == "human" and getattr(msg, "content", "") == "initial_evaluation":
                # Buscar el AIMessage siguiente
                if idx + 1 < len(history) and getattr(history[idx + 1], "type", None) == "ai":
                    ai_msg = history[idx + 1]
                    ai_content_str = getattr(ai_msg, "content", "{}")
                    try:
                        last_evaluation = json.loads(ai_content_str)
                    except json.JSONDecodeError:
                        raise ValueError(f"El AIMessage no contiene JSON válido:\n{ai_content_str}")
                break

        if not last_evaluation:
            raise ValueError("No se encontró evaluación inicial para este usuario.")

        # --- Preparar nuevas respuestas con preguntas ---
        new_answers_with_questions = []
        for idx, ans in enumerate(evaluation_dto.answers):
            question_text = (
                last_evaluation.get("next_questions", [])[idx]
                if idx < len(last_evaluation.get("next_questions", []))
                else f"Question {idx+1}"
            )
            new_answers_with_questions.append({
                "question": question_text,
                "answer": ans.answer
            })

        # --- Crear prompt ---
        prompt_template = PromptTemplate(
            input_variables=["previous_evaluation", "new_answers_with_questions"],
            template="""
            You are an expert English language evaluator acting as a final arbiter. Your single task is to synthesize all available data to determine a definitive CEFR level.

            --- SCIENTIFIC BASIS FOR FINAL JUDGMENT ---
            Your final decision must be a holistic synthesis based on the principles established in the first evaluation:
            1. CEFR Level Confirmation/Adjustment: Analyze the user's performance on these new, targeted questions.
            2. Trend Analysis (Communicative Competence): Compare performance in the second round against the first round's scores (grammar, vocabulary, fluency).

            --- CONTEXT: INITIAL EVALUATION SUMMARY ---
            {previous_evaluation}

            --- DATA: SECOND ROUND ANSWERS ---
            {new_answers_with_questions}

            --- FINAL INSTRUCTION ---
            Provide ONLY the user's final, definitive CEFR level.
            Valid responses: 'A1', 'A2', 'B1', 'B2', 'C1', 'C2'.
            Example: B2
            """
            )

        # --- Inputs para el prompt ---
        prompt_inputs = {
            "previous_evaluation": json.dumps(last_evaluation, indent=2),
            "new_answers_with_questions": json.dumps(new_answers_with_questions, indent=2)
        }

        # --- Ejecutar LLMChain ---
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        result_str = chain.run(prompt_inputs).strip()

        return result_str

