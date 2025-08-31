from app.domain.repositories.interfaces.question_repository_interface import QuestionRepositoryInterface

class QuestionController:
    def __init__(self, repo: QuestionRepositoryInterface):
        self.repo = repo

    def list_questions(self) -> list:
        return self.repo.list_questions()