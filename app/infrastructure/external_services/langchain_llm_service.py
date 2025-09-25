import json
from typing import Dict, Any, List
import openai

from app.application.evaluation.ports.llm_service_port import LLMServicePort
from app.core.config.settings import settings
from app.core.exceptions.evaluation_exceptions import LLMException, InvalidResponseException


class LangchainLLMService(LLMServicePort):
    """Implementation of LLM service using OpenAI directly."""

    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    async def evaluate_answers(
        self,
        questions_dict: Dict[int, str],
        answers_dict: Dict[int, str]
    ) -> Dict[str, Any]:
        """Evaluate answers using LLM and return structured feedback."""
        try:
            prompt = self._get_evaluation_prompt_template().format(
                answers=answers_dict, 
                questions=questions_dict
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            result_str = response.choices[0].message.content

            try:
                result = json.loads(result_str)
                
                # Handle nested structure from LLM response
                if "evaluation" in result and "next_questions" in result:
                    # Extract evaluation data and flatten the structure
                    evaluation_data = result["evaluation"]
                    next_questions = result["next_questions"]
                    
                    flattened_result = {
                        "level": evaluation_data["level"],
                        "scores": evaluation_data["scores"],
                        "reason": evaluation_data["reason"],
                        "feedback": evaluation_data["feedback"],
                        "next_questions": next_questions
                    }
                    return flattened_result
                elif "level" in result and "scores" in result and "feedback" in result:
                    # Already flat structure, return as is
                    return result
                else:
                    raise InvalidResponseException(f"LLM returned unexpected JSON structure. Keys found: {list(result.keys())}")
                    
            except json.JSONDecodeError as e:
                raise InvalidResponseException(f"LLM returned invalid JSON: {result_str}")

        except Exception as e:
            raise LLMException(f"Failed to evaluate answers: {str(e)}")

    async def final_evaluation(
        self,
        previous_evaluation: Dict[str, Any],
        new_answers: List[Dict[str, str]]
    ) -> Dict[str, str]:
        """Perform final evaluation and return CEFR level with reason."""
        try:
            prompt = self._get_final_evaluation_prompt_template().format(
                previous_evaluation=json.dumps(previous_evaluation, indent=2),
                new_answers_with_questions=json.dumps(new_answers, indent=2)
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            result_str = response.choices[0].message.content.strip()
            
            # Try to parse as JSON first
            try:
                result = json.loads(result_str)
                if isinstance(result, dict) and "final_level" in result:
                    return result
            except json.JSONDecodeError:
                pass
            
            # If not JSON, assume it's just the level string
            return {
                "final_level": result_str,
                "reason": "Final level determined based on comprehensive analysis"
            }

        except Exception as e:
            raise LLMException(f"Failed to perform final evaluation: {str(e)}")

    def _get_evaluation_prompt_template(self) -> str:
        """Get the prompt template for initial evaluation."""
        return """Return ONLY valid JSON. DO NOT include any extra text.
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
** Your feedback must facilitate learning. Based on Schmidt's "Noticing Hypothesis" (1990), you must explicitly identify mistakes and provide clear suggestions to help the user notice the gap between their output and the correct form. ALWAYS provide at least one mistake or suggestion, even for advanced levels (C1/C2) - focus on subtle improvements, style refinements, or advanced constructions.

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
    - mistakes: A list of specific errors (REQUIRED - even for advanced levels, identify subtle issues or areas for refinement)
    - suggestions: A list of concrete corrections or better alternatives (REQUIRED - always provide constructive feedback)
- Provide an overall level, average scores, and a short reason that explicitly references the framework.
- Generate 5 new English next_questions suitable for the user's diagnosed level, following the Adaptive Assessment Principle. 

Return strictly in this format:
{{ "level": "A1-C2", "scores": {{"grammar": 0.0, "vocabulary": 0.0, "fluency": 0.0}}, "reason": "string", "feedback": [ {{ "question": "string", "answer": "string", "estimated_level": "A1-C2", "scores": {{"grammar": 0.0, "vocabulary": 0.0, "fluency": 0.0}}, "mistakes": ["string"], "suggestions": ["string"] }} ], "next_questions": [ "Question 1", "Question 2", "...", "Question 5" ] }}"""

    def _get_final_evaluation_prompt_template(self) -> str:
        """Get the prompt template for final evaluation."""
        return """
        You are an expert English language evaluator acting as a final arbiter. Your task is to determine a definitive CEFR level and provide reasoning.

        --- SCIENTIFIC BASIS FOR FINAL JUDGMENT ---
        Your final decision must be a holistic synthesis based on the principles established in the first evaluation:
        1. CEFR Level Confirmation/Adjustment: Analyze the user's performance on these new, targeted questions.
        2. Trend Analysis (Communicative Competence): Compare performance in the second round against the first round's scores (grammar, vocabulary, fluency).

        --- CONTEXT: INITIAL EVALUATION SUMMARY ---
        {previous_evaluation}

        --- DATA: SECOND ROUND ANSWERS ---
        {new_answers_with_questions}

        --- FINAL INSTRUCTION ---
        Return your response in this EXACT JSON format:
        {{
          "final_level": "B2",
          "reason": "Detailed explanation of why this level was chosen, referencing specific evidence from both evaluations"
        }}

        Valid levels: 'A1', 'A2', 'B1', 'B2', 'C1', 'C2'.
        The reason should be comprehensive and reference specific linguistic evidence.
        """