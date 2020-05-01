import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  # '''
  # @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  # '''
  CORS(app, resources={r"/api/*": {"origins": "*"}})



  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,PUT,DELETE,OPTIONS')
      return response

  def paginate_questions(request, selection):
      page = request.args.get('page', 1, type=int)
      start =  (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE

      questions = [Question.format() for Question in selection]
      current_questions = questions[start:end]

      return current_questions

  # '''
  # @TODO:
  # Create an endpoint to handle GET requests
  # for all available categories.
  # '''
  @app.route('/categories')
  @cross_origin()
  def Get_All_Categories():
      try:
          categories = Category.query.order_by(Category.id).all()

          catgs = {cat.id:cat.type for cat in categories}

          if catgs is None:
              return null
      except Exception as e:
          raise


      return jsonify({
      'success': True,
      'categories': catgs
      })

      # return jsonify({
      # 'success': True,
      # 'categories': {'1' : "Science",
      # '2' : "Art",
      # '3' : "Geography",
      # '4' : "History",
      # '5' : "Entertainment",
      # '6' : "Sports"}
      #           })

  # '''
  # @TODO:
  # Create an endpoint to handle GET requests for questions,
  # including pagination (every 10 questions).
  # This endpoint should return a list of questions,
  # number of total questions, current category, categories.
  #
  # TEST: At this point, when you start the application
  # you should see questions and categories generated,
  # ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions.
  # '''
  @app.route('/questions', methods=['GET'])
  @cross_origin()
  def get_questions():
      try:
          # if method == 'GET':
          questions = Question.query.order_by(Question.id).all()
          quesn = paginate_questions(request, questions)

          categories = Category.query.order_by(Category.id).all()
          catgs = {cat.id:cat.type for cat in categories}

          currentCategory = list(set([q['category'] for q in quesn]))

          if (len(quesn) == 0):
              abort(404)
              # return jsonify({
              #     'success': False})


      except Exception as e:
          print('error in questions')
          abort(404)

      return jsonify({
          'success': True,
          'questions': quesn,
          'total_questions': len(questions),
          'current_category': currentCategory,
          'categories': catgs
      })

  # '''
  # @TODO:
  # Create an endpoint to DELETE question using a question ID.
  #
  # TEST: When you click the trash icon next to a question, the question will be removed.
  # This removal will persist in the database and when you refresh the page.
  # '''


  @app.route('/questions/<int:quesID>', methods=['DELETE'])
  @cross_origin()
  def delete_question(quesID):
      try:
          question = Question.query.filter(Question.id == quesID).one_or_none()
          if question is None:
              abort(404)
          question.delete()
      except Exception as e:
          print('In Delete Error')
          abort(422)

      return jsonify({'success' : True})

  # '''
  # @TODO:
  # Create an endpoint to POST a new question,
  # which will require the question and answer text,
  # category, and difficulty score.
  #
  # TEST: When you submit a question on the "Add" tab,
  # the form will clear and the question will appear at the end of the last page
  # of the questions list in the "List" tab.
  # '''

  @app.route('/questions', methods=['POST'])
  @cross_origin()
  def add_question():
      try:
          body = request.get_json()
          new_question = body.get('question', None)
          new_answer = body.get('answer', None)
          new_difficulty = body.get('difficulty', None)
          new_category = body.get('category', None)

          question = Question(question=new_question, answer = new_answer,
            difficulty= new_difficulty, category = new_category)
          question.insert()
      except Exception as e:
          print('In Add Question', e)
          abort(404)

      return jsonify({'success' : True})

  # '''
  # @TODO:
  # Create a POST endpoint to get questions based on a search term.
  # It should return any questions for whom the search term
  # is a substring of the question.
  #
  # TEST: Search by any phrase. The questions list will update to include
  # only question that include that string within their question.
  # Try using the word "title" to start.
  # '''

  @app.route('/searchQuestions', methods=['POST'])
  @cross_origin()
  def search_questions():
      try:
          body = request.get_json()
          searchStr = body.get('searchTerm', None)
          questions = Question.query.filter(Question.question.ilike('%{}%'.format(searchStr)))

          #print(questions)

          quesn = paginate_questions(request, questions)
      except Exception as e:
          print('Error in Search Questions')
          abort(404)

      return jsonify({
          'success': True,
          'questions': quesn,
          'total_questions': questions.count(),
          'current_category': 1
          })



  # '''
  # @TODO:
  # Create a GET endpoint to get questions based on category.
  #
  # TEST: In the "List" tab / main screen, clicking on one of the
  # categories in the left column will cause only questions of that
  # category to be shown.
  # '''

  @app.route('/categories/<int:cat_id>/questions', methods=['GET'])
  @cross_origin()
  def get_question_by_category(cat_id):
      try:
          questions = Question.query.filter(Question.category == cat_id).all()
          if len(questions) == 0:
              abort(404)
          quesn = paginate_questions(request, questions)

      except Exception as e:
          print('In Get Question by category')
          abort(422)

      return jsonify({
          'success': True,
          'questions': quesn,
          'total_questions': len(questions),
          'current_category': cat_id
          })


  # '''
  # @TODO:
  # Create a POST endpoint to get questions to play the quiz.
  # This endpoint should take category and previous question parameters
  # and return a random questions within the given category,
  # if provided, and that is not one of the previous questions.
  #
  # TEST: In the "Play" tab, after a user selects "All" or a category,
  # one question at a time is displayed, the user is allowed to answer
  # and shown whether they were correct or not.
  # '''

  @app.route('/quizzes', methods=['POST'])
  @cross_origin()
  def play_quizzes():
      # quesn = []
      try:
          # prevQuestion = request.args.get('previous_questions')
          # category = request.args.get('quiz_category')
          questions = ""
          body = request.get_json()
          prevQuestion = body.get('previous_questions', None)
          category = body.get('quiz_category', None).get('id')

          if category is None or category == 0:
              questions = Question.query.all()
          else:
              questions = Question.query.filter(Question.category == category).all()
          # print(prevQuestion)

          listQuestions = [q.format() for q in questions if q.id not in prevQuestion]
          if len(listQuestions) > 0:
              quesn = random.choice(listQuestions)
          else:
              quesn = None

          # print('previous - ', quesn)
      except Exception as e:
          print('Error in Quiz')
          abort(404)

      return jsonify({
        'success': True,
        'question': quesn
      })

  # '''
  # @TODO:
  # Create error handlers for all expected errors
  # including 404 and 422.
  # '''
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad Request'
      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource Not Found'
      }), 404

  @app.errorhandler(405)
  def not_allowed(error):
      return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method not allowed, Check URL.'
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
        'success': False,
        'error': 422,
        'message': 'Request is not processable.'
      }), 422

  @app.errorhandler(500)
  def server_error(error):
      return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal server error. Server encountered an error.'
      }), 500

  return app
