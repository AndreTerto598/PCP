from flask import Flask, render_template, redirect, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TERTOPCP'


@app.route('/cadastro', methods=['GET'])
def cadastro():
    return render_template('cadastro.html')

@app.route('/Cadastro', methods=['POST'])
def processar_cadastro():
    usuario = request.form['usuario']
    email = request.form['email']
    senha = request.form['senha']
    confirmar_senha = request.form['confirmar_senha']
    print(usuario)
    print(senha)
    if senha != confirmar_senha:
        return "As senhas não conferem! Tente novamente."
    return f"Usuário {usuario} cadastrado com sucesso!"
    
    




if __name__ == '__main__':
    app.run(debug=True)
