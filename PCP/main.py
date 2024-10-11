from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TERTOPCP'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://postgres:123@localhost/PCP'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Modelo de dados para o Cadastro
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
#Modelo de Dados para o estoque de Tecido
class Estoque_tecido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_tela = db.Column(db.String(100), nullable=False)
    quantidade_tela = db.Column(db.Integer, nullable=False)
    tipo_tela = db.Column(db.String(100), nullable=False)
    unidade_medida = db.Column(db.String(50), nullable=False)

    def __init__(self, nome_tela, quantidade_tela, tipo_tela, unidade_medida):
        self.nome_tela = nome_tela
        self.quantidade_tela = quantidade_tela
        self.tipo_tela = tipo_tela
        self.unidade_medida = unidade_medida
#
#Modelo de Dados para o estoque de Alças
class Estoque_alca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_alca = db.Column(db.String(255), nullable=False)
    quantidade_alca = db.Column(db.Integer, nullable=False)
    unidade_medida = db.Column(db.String(50), nullable=False)

    def __init__(self, nome_alca, quantidade_alca, unidade_medida):
        self.nome_alca = nome_alca
        self.quantidade_alca = quantidade_alca
        self.unidade_medida = unidade_medida

# Modelo de Dados para Cadastro de Pedidos
class PedidoCliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(255), nullable=False)
    produto = db.Column(db.String(255), nullable=False)
    data_emissao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_entrega = db.Column(db.DateTime, nullable=False)
    entregador = db.Column(db.String(100), nullable=False)
    emissor_pedido = db.Column(db.String(100), nullable=False)
    tamanho = db.Column(db.String(50), nullable=False)
    tela = db.Column(db.String(100), nullable=False)
    alca = db.Column(db.String(100), nullable=False)
    estampa = db.Column(db.String(255), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    quantidade_volumes = db.Column(db.Integer, nullable=False)
    observacao = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Usuario {self.usuario}>'
        

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    return render_template('cadastro.html')

@app.route('/Cadastro', methods=['POST'])
def processar_cadastro():
    usuario = request.form['usuario']
    email = request.form['email']
    senha = request.form['senha']
    confirmar_senha = request.form['confirmar_senha']
    
    if senha != confirmar_senha:
        return "As senhas não conferem! Tente novamente."
    
    senha_hash = generate_password_hash(senha)
    novo_usuario = Usuario(usuario=usuario, email=email, senha=senha_hash)



    db.session.add(novo_usuario)
    db.session.commit()

    return f"Usuário {usuario} cadastrado com sucesso!"

#Fim da parte de Cadastro

#Início da página de login

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/Login', methods=['POST'])
def processar_login():
    login_usuario = request.form['login_usuario']
    login_senha = request.form['login_senha']
    
    usuario = Usuario.query.filter_by(usuario=login_usuario).first()

    if usuario and check_password_hash(usuario.senha, login_senha):
        session['login_usuario'] = login_usuario
        return redirect(url_for('principal'))
    else:
        flash('Login Inválido', 'error')
        return render_template('login.html', login_invalido=True)
    
@app.route('/principal', methods = ['GET', 'POST'])
def principal():
    if 'login_usuario' not in session:
        return redirect(url_for('login'))
    return render_template('principal.html')

#Fim da página de Login

#Logout

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

#Página de Estoque de Tecidos

# Função para formatar a quantidade
def formatar_quantidade(quantidade):
    return f"{quantidade:,}".replace(',', '.')

@app.route('/tecido')
def tecido():
    itens = Estoque_tecido.query.all()  # Recupera todos os itens do banco de dados
    itens_formatados = []  # Inicializa uma lista para os itens formatados

    for item in itens:
        # Aplica a formatação na quantidade
        item_formatado = {
            'id': item.id,
            'nome_tela': item.nome_tela,
            'quantidade_tela': formatar_quantidade(item.quantidade_tela),
            'tipo_tela': item.tipo_tela,
            'unidade_medida': item.unidade_medida,
        }
        itens_formatados.append(item_formatado)  # Adiciona o item formatado à lista

    return render_template('Estoque_tecido.html', itens=itens_formatados)

# Adicionar item

@app.route('/add_item', methods=['POST'])
def add_item():
    nome_tela = request.form['nome_tela']
    quantidade_tela = request.form['quantidade_tela']
    tipo_tela = request.form['tipo_tela']
    unidade_medida = request.form['unidade_medida']

    
    novo_item = Estoque_tecido(nome_tela=nome_tela, quantidade_tela=quantidade_tela, tipo_tela=tipo_tela, unidade_medida=unidade_medida)
    db.session.add(novo_item)
    db.session.commit()
    
    flash('Item adicionado com sucesso!')
    return redirect(url_for('tecido'))

# Editar item

@app.route('/edit_item/<int:id>', methods=['POST'])
def edit_item(id):
    item = Estoque_tecido.query.get_or_404(id)
    
    item.nome_tela = request.form['nome_tela']
    item.quantidade_tela = request.form['quantidade_tela']
    item.tipo_tela = request.form['tipo_tela']
    item.unidade_medida = request.form['unidade_medida']
    

    db.session.commit()
    
    flash('Item atualizado com sucesso!')
    return redirect(url_for('tecido'))


# Remover item

@app.route('/delete_item/<int:id>', methods=['POST'])
def delete_item(id):
    item = Estoque_tecido.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    
    flash('Item removido com sucesso!')
    return redirect(url_for('tecido'))

#Página de Estoque de Alças

@app.route('/alca')
def alca():
    alca = Estoque_alca.query.all()
    return render_template('Estoque_alcas.html', itens=alca)

#Adicionar Alça

@app.route('/add_alca', methods=['POST'])
def add_alca():
    print(request.form)
    nome_alca = request.form['nome_alca']
    quantidade_alca = request.form['quantidade_alca']
    unidade_medida = request.form['unidade_medida']

    
    nova_alca = Estoque_alca(nome_alca=nome_alca, quantidade_alca=quantidade_alca, unidade_medida=unidade_medida)
    db.session.add(nova_alca)
    db.session.commit()
    
    flash('Item adicionado com sucesso!')
    return redirect(url_for('alca'))

#Editar Alça

@app.route('/edit_alca/<int:id>', methods=['POST'])
def edit_alca(id):
    item = Estoque_alca.query.get_or_404(id)
    
    item.nome_alca = request.form['nome_alca']
    item.quantidade_alca = request.form['quantidade_alca']
    item.unidade_medida = request.form['unidade_medida']
    
    db.session.commit()
    
    flash('Item atualizado com sucesso!')
    return redirect(url_for('alca'))

#Remover Alça

@app.route('/delete_alca/<int:id>', methods=['POST'])
def delete_alca(id):
    item = Estoque_alca.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    
    flash('Item removido com sucesso!')
    return redirect(url_for('alca'))


# Rota para processar o cadastro de pedidos
@app.route('/add_pedido', methods=['POST'])
def add_pedido():
    nome_cliente = request.form['nome_cliente']
    produto = request.form['produto']
    data_emissao = datetime.strptime(request.form['data_emissao'], '%Y-%m-%d')
    data_entrega = datetime.strptime(request.form['data_entrega'], '%Y-%m-%d')
    entregador = request.form['entregador']
    emissor_pedido = request.form['emissor_pedido']
    tamanho = request.form['tamanho']
    tela = request.form['tela']
    alca = request.form['alca']
    estampa = request.form['estampa']
    quantidade = request.form['quantidade']
    quantidade_volumes = request.form['quantidade_volumes']
    observacao = request.form['observacao']

    novo_pedido = PedidoCliente(
        nome_cliente=nome_cliente,
        produto=produto,
        data_emissao=data_emissao,
        data_entrega=data_entrega,
        entregador=entregador,
        emissor_pedido=emissor_pedido,
        tamanho=tamanho,
        tela=tela,
        alca=alca,
        estampa=estampa,
        quantidade=quantidade,
        quantidade_volumes=quantidade_volumes,
        observacao=observacao
    )

    db.session.add(novo_pedido)
    db.session.commit()
    flash('Pedido cadastrado com sucesso!')
    return redirect(url_for('Op_cadastro'))

# Rota para exibir o formulário de cadastro de pedidos
@app.route('/Op_cadastro', methods=['GET', 'POST'])
def Op_cadastro():
    return render_template('Op_cadastro.html')







if __name__ == '__main__':
    app.run(debug=True)
