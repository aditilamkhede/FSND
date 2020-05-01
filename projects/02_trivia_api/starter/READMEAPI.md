# TRIVIA

Trivia App is built to create bonding experience for its employees and students.
Thus app was created to hold trivia on a regular basis and play the game.

This application allows you to add new questions, get list of all questions.
List of questions by category and search questions.

## Getting Started

This application uses react in the frontend and python as backend programming
language. We have created a REST API TRIVIA which is implemented using Flask
Cors.

## Pre-requisites

Python3, pip and node should be installed on local machine.

### Backend

From the backend folder run requirements.txt.

pip install -r requirements.txt

#### Database Setup
Restore a database using the trivia.psql file provided.
From the backend folder in terminal run:

psql trivia < trivia.psql

To run the application, execute:

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

### Frontend

From the frontend folder, run the following commands:

npm install
npm start
Open http://localhost:3000 to view the application in the browser.

### Testing
To run the tests navigate to backend folder and run the following commands:

dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py

If you are running the commands first time, exclude dropdb command.

All tests are included in the test_flaskr.py and should be maintained as updates
are made to the application.

## API Reference

### Getting Started

    - Base URL: Currently application runs locally. Application is hosted at
    http://127.0.0.1:5000.
    - Authentication: Current version of the application does not require authentication or API keys.

### Error Handling

  Errors are returned as json objects:
    {
      'success': False,
      'error': 422,
      'message': 'Request is not processable.'
    }

  Application returns following error codes:

  - 200 - OK(success)

  - 400 - Bad Request

  - 404 - Resource Not Found

  - 405 - Method not allowed

  - 422 - Not processable

  - 500 - Internal Server Error

### End Points

#### GET /categories

    1. Returns a list of categories and success value

    Sample
      curl http://127.0.0.1:5000/categories

      {
        "categories": {
          "1": "Science",
          "2": "Art",
          "3": "Geography",
          "4": "History",
          "5": "Entertainment",
          "6": "Sports"
        },
        "success": true
    }

#### GET /questions

    1. Returns a list of questions, success value, total questions, categories.
    2. Results are also paginated.

##### Sample:
      curl http://127.0.0.1:5000/questions

      {
        "categories": {
          "1": "Science",
          "2": "Art",
          "3": "Geography",
          "4": "History",
          "5": "Entertainment",
          "6": "Sports"
        },
        "current_category": [
          1,
          2,
          4
        ],
        "questions": [
          {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
          },
          {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
          },
          {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
          },
          {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
          },
          {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
          },
          {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
          },
          {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
          },
          {
            "answer": "Marie Curie",
            "category": 1,
            "difficulty": 1,
            "id": 24,
            "question": "First Female to win 2 Nobel Prizes"
          },
          {
            "answer": "Ada Lovelace",
            "category": 1,
            "difficulty": 5,
            "id": 25,
            "question": "Female Mathematician who is considered first female computer programmer"
          },
          {
            "answer": "Indira Gandhi",
            "category": 4,
            "difficulty": 3,
            "id": 31,
            "question": "Who is India'a First Female Prime Minister"
          }
        ],
        "success": true,
        "total_questions": 20
      }

#### DELETE /question/{question_id}

      1. Deletes a question of the given id.
      2. Returns the success value.

##### Sample
        curl http://127.0.0.1:5000/questions/10

        {
          "success": true
        }

#### POST /questions

      1. Adds a new question to the questions list.
      2. Returns a success value.

##### Sample
        curl -d '{"question": "Who is the first female Indian Pilot?",
          "answer": "Sarla Thakral","difficulty": "4","category": "4"}'
          -H "Content-Type: application/json"
          -X POST http://127.0.0.1:5000/questions

        {
          "success": true
        }

#### POST /categories/{categorie_id}/questions

      1. Returns a list of questions for selected category, success value,
        current category and total questions.

##### Sample
        curl http://127.0.0.1:5000/categories/4/questions

        {
        "current_category": 4,
        "questions": [
          {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
          },
          {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
          },
          {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
          },
          {
            "answer": "Indira Gandhi",
            "category": 4,
            "difficulty": 3,
            "id": 31,
            "question": "Who is India'a First Female Prime Minister"
          },
          {
            "answer": "Sarla Thakral",
            "category": 4,
            "difficulty": 4,
            "id": 33,
            "question": "Who is the first female Indian Pilot?"
          },
          {
            "answer": "Sarla Thakral",
            "category": 4,
            "difficulty": 4,
            "id": 34,
            "question": "Who is the first female Indian Pilot?"
          },
          {
            "answer": "Sarla Thakral",
            "category": 4,
            "difficulty": 4,
            "id": 35,
            "question": "Who is the first female Indian Pilot?"
          }
        ],
        "success": true,
        "total_questions": 7
        }

#### POST /searchQuestions

      1. Returns a list of questions based on a search term, total questions,
        current category and a success value.

##### Sample
        curl -d '{"searchTerm":"fem"}' -H "Content-Type: application/json"
          -X POST http://127.0.0.1:5000/searchQuestions

          {
          "current_category": 1,
          "questions": [
            {
              "answer": "Marie Curie",
              "category": 1,
              "difficulty": 1,
              "id": 24,
              "question": "First Female to win 2 Nobel Prizes"
            },
            {
              "answer": "Ada Lovelace",
              "category": 1,
              "difficulty": 5,
              "id": 25,
              "question": "Female Mathematician who is considered first female computer programmer"
            },
            {
              "answer": "Indira Gandhi",
              "category": 4,
              "difficulty": 3,
              "id": 31,
              "question": "Who is India'a First Female Prime Minister"
            },
            {
              "answer": "Sarla Thakral",
              "category": 4,
              "difficulty": 4,
              "id": 33,
              "question": "Who is the first female Indian Pilot?"
            }
            ],
            "success": true,
            "total_questions": 6
          }

#### POST /quizzes

      1. Returns a random question based on selected category, excludeing
        previous questions and also returns a success value.

##### Sample
        curl -d '{"previous_questions":["18"],"quiz_category":{"id":"2"}}'
          -H "Content-Type: application/json"
          -X POST http://127.0.0.1:5000/quizzes

          {
            "question": {
              "answer": "One",
              "category": 2,
              "difficulty": 4,
              "id": 18,
              "question": "How many paintings did Van Gogh sell in his lifetime?"
            },
            "success": true
          }
