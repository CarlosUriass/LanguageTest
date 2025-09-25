from typing import List, Dict
from app.domain.value_objects.cefr_level import CEFRLevel
from app.domain.value_objects.scores import Scores


class LevelCalculatorService:
    """Domain service for calculating CEFR levels based on scores and feedback."""

    @staticmethod
    def calculate_overall_level(individual_levels: List[str]) -> str:
        """
        Calculate overall CEFR level from individual question levels.
        Uses a weighted approach favoring the most common level.
        """
        if not individual_levels:
            return CEFRLevel.A1.value

        # Count occurrences of each level
        level_counts = {}
        for level in individual_levels:
            if CEFRLevel.is_valid_level(level):
                level_counts[level] = level_counts.get(level, 0) + 1

        if not level_counts:
            return CEFRLevel.A1.value

        # Find the most common level
        most_common_level = max(level_counts, key=level_counts.get)
        return most_common_level

    @staticmethod
    def calculate_average_scores(scores_list: List[Scores]) -> Scores:
        """Calculate average scores from a list of individual scores."""
        if not scores_list:
            return Scores(grammar=0.0, vocabulary=0.0, fluency=0.0)

        total_grammar = sum(score.grammar for score in scores_list)
        total_vocabulary = sum(score.vocabulary for score in scores_list)
        total_fluency = sum(score.fluency for score in scores_list)
        count = len(scores_list)

        return Scores(
            grammar=round(total_grammar / count, 2),
            vocabulary=round(total_vocabulary / count, 2),
            fluency=round(total_fluency / count, 2)
        )

    @staticmethod
    def validate_level_progression(previous_level: str, current_level: str) -> bool:
        """
        Validate if level progression is reasonable.
        Returns True if progression is within one level up or down.
        """
        levels = CEFRLevel.get_all_levels()
        
        if previous_level not in levels or current_level not in levels:
            return False

        prev_index = levels.index(previous_level)
        curr_index = levels.index(current_level)
        
        # Allow progression within 1 level up or down
        return abs(curr_index - prev_index) <= 1

    @staticmethod
    def suggest_next_level_questions(current_level: str) -> str:
        """
        Suggest what level questions should be generated next.
        Usually same level or one level up for appropriate challenge.
        """
        levels = CEFRLevel.get_all_levels()
        
        if current_level not in levels:
            return CEFRLevel.A1.value

        current_index = levels.index(current_level)
        
        # If not at the highest level, suggest one level up for challenge
        if current_index < len(levels) - 1:
            return levels[current_index + 1]
        
        # If at highest level, stay at current level
        return current_level