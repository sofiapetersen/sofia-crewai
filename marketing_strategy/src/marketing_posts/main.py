#!/usr/bin/env python
import sys
from flask import Flask, render_template, request, jsonify
from marketing_posts.crew import MarketingPostsCrew

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  

# Rota para processar os inputs do formulário
@app.route('/run', methods=['POST'])
def run():
    customer_domain = request.form['customer_domain']
    project_description = request.form['project_description']

    inputs = {
        'customer_domain': customer_domain,
        'project_description': project_description
    }

    try:
        # Executa o CrewAI com os inputs fornecidos
        output = MarketingPostsCrew().crew().kickoff(inputs=inputs)
        
        # Retorna a resposta como JSON para ser tratada pelo frontend
        return jsonify({"success": True, "output": output})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

#  Rota para treinar os agentes 
@app.route('/train', methods=['POST'])
def train():
    customer_domain = request.form['customer_domain']
    project_description = request.form['project_description']
    n_iterations = int(request.form.get('n_iterations', 1)) 

    inputs = {
        'customer_domain': customer_domain,
        'project_description': project_description
    }

    try:
        MarketingPostsCrew().crew().train(n_iterations=n_iterations, inputs=inputs)
        return jsonify({"success": True, "message": "Training completed successfully"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
