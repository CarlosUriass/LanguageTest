# 📖 API Reference – LLM-Powered English Assessment

## Base URL

```
http://localhost:8000
```

---

## 🔹 `POST /evaluation/initial`

### Description

Receives the learner’s answers to an initial set of **diagnostic questions**.
The system processes responses with an **LLM-based agent**, applies **prompt-engineering + memory**, and returns the **next set of questions** (if any).

This endpoint is typically called at the **start of the assessment session**.

---

### Request Body

```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "answers": [
    {
      "question_id": 1,
      "answer": "The last weekend i went to dinner with friends and we take a drink after."
    },
    {
      "question_id": 2,
      "answer": "my best friend is a funny guy he is so cool"
    },
    {
      "question_id": 3,
      "answer": "when i was in the university i was working and taking classes at the same time so that was difficult but i affront the challenge"
    },
    {
      "question_id": 4,
      "answer": "the advantages of the social media is a comunication media and we see the life of others people, the disavantages of the social media is that sometimes we spend too much time in ther"
    },
    {
      "question_id": 5,
      "answer": "i want to travel to spain because my dream is go to a soccer match of my favorite club the FCB"
    },
    {
      "question_id": 6,
      "answer": "the implemetation of the IA make the university most easy and it is a way to learn easy"
    },
    {
      "question_id": 7,
      "answer": "the enterprises search for minor costs and that is what IA offer in comparition with human work"
    },
    {
      "question_id": 8,
      "answer": "i think the quote says the art is important is way of the reality"
    },
    {
      "question_id": 9,
      "answer": "it will change definitly the oportunities in mexico are different than others countrys"
    },
    {
      "question_id": 10,
      "answer": "yesterday i watch a movie which spoke about the resilency and the movie talks about a prisioner who was guilty but he was innocent and that get me thinking"
    }
  ]
}
```

- `user_id` (string, UUID): Unique identifier of the learner.
- `answers` (array): List of answers given by the user.

  - `question_id` (int): Identifier of the question.
  - `answer` (string): Free-text response.

---

### Response Example

```json
{
  "next_questions": []
}
```

- `next_questions` (array): Contains dynamically generated follow-up questions (empty if the system moves to final evaluation).

---

## 🔹 `POST /evaluation/final`

### Description

Finalizes the evaluation process and returns the **estimated English proficiency level** according to **CEFR (A1–C2)**.
This endpoint is typically called after completing the initial assessment and any adaptive questioning.

---

### Request Body

```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

---

### Response Example

```json
"b2" // !TODO: improve the API response
```

---
