from flask import Flask, request, render_template, jsonify
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('db.json')  # TinyDB stores data in a JSON file

# Preguntas precargadas
predefined_questions = {
    "Hola": "¡Hola! ¿Cómo estás?",
    "Bien gracias y tu?": "Me da gusto escuchar eso, Estoy bien, gracias.",
    "De qué te gustaría hablar?": "Hablemos de lo que tú quieras."
}

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# API para manejar el chat
@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json['question']
    
    # Verificar si la pregunta coincide con las precargadas
    if user_input in predefined_questions:
        return jsonify({"response": predefined_questions[user_input]})
    
    # Buscar en la base de datos
    Question = Query()
    result = db.search(Question.question == user_input)
    
    if result:
        return jsonify({"response": result[0]['answer']})
    
    # Si no se encuentra la pregunta
    return jsonify({"response": "No tengo una respuesta para eso. ¿Cuál sería una buena respuesta?"})

# Agregar nueva respuesta a la base de datos
@app.route('/add', methods=['POST'])
def add():
    question = request.json['question']
    answer = request.json['answer']
    db.insert({'question': question, 'answer': answer})
    return jsonify({"status": "success", "message": "Nuevo conocimiento agregado."})

if __name__ == '__main__':
    app.run(debug=True)
