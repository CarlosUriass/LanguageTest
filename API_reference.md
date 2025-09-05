# 📖 API Reference – LLM-Powered English Assessment

## Base URL

```
http://localhost:8000
```

---

## 🔹 `POST /evaluation/initial`

### Description

Receives the learner’s answers to an initial set of **diagnostic questions**.
The system processes responses with an **LLM-based agent**, applies **prompt-engineering + memory**, and returns the **next set of questions** (always 5 strings).

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
    }
  ]
}
```

- `user_id` (string, UUID): Unique identifier of the learner.
- `answers` (array): Answers to the **initial fixed questions**.

  - `question_id` (int): Identifier of the question.
  - `answer` (string): Free-text learner response.

---

### Response Example

```json
{
  "next_questions": [
    "What is your favorite hobby and why do you enjoy it?",
    "Describe a memorable trip you took. What did you do?",
    "What are some qualities you look for in a friend?",
    "How do you think education can be improved in your country?",
    "What are the most important skills for success in your field?"
  ]
}
```

- `next_questions` (array of strings): Always **5 dynamically generated questions**.

---

## 🔹 `POST /evaluation/final`

### Description

Finalizes the evaluation after the learner has answered both the **initial set** and the **next 5 adaptive questions**.
Returns the **estimated CEFR proficiency level (A1–C2)** and optional scores.

---

### Request Body

```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "answers": [
    {
      "question": "What is your favorite hobby and why do you enjoy it?",
      "answer": "my favorite hooby is play basketball and i enjoy it because im good on that"
    },
    {
      "question": "Describe a memorable trip you took. What did you do?",
      "answer": "i went to Guadalajara and i went to de Zoo that was nice"
    }
  ]
}
```

- `user_id` (string, UUID): Learner identifier (same session as `/initial`).
- `answers` (array): Answers to the **5 adaptive questions**.

  - `question` (string): The exact question text.
  - `answer` (string): Free-text learner response.

---

### Response Example

```json
  a2 // TODO: IMPROVE API RESPONSE
```
