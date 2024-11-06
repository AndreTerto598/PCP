
#-------------------------------------------------------------------------------------------------
from flask_login import logout_user
from flask import Flask, render_template, redirect, request, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, update
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_migrate import Migrate
from datetime import datetime
import json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from datetime import datetime
import math
from sqlalchemy import or_
from sqlalchemy import extract
#-------------------------------------------------------------------------------------------------


#Config-------------------------------------------------------------------------------------------
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.sacacho.com.br'  # Altere para seu servidor SMTP
app.config['MAIL_PORT'] = 587  # Porta para TLS
app.config['MAIL_USERNAME'] = 'adm2@sacacho.com.br'
app.config['MAIL_PASSWORD'] = 'Sacacho@947'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
app.config['SECRET_KEY'] = 'TERTOPCP'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://postgres:123@localhost/PCP'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#-------------------------------------------------------------------------------------------------


# Configurar o LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#-------------------------------------------------------------------------------------------------


#Função para enviar mensagem ---------------------------------------------------------------------
def send_notification_email(message):
    msg = Message('Notificação de Pedido',
                  sender='adm2@sacacho.com.br',
                  recipients=['adm2@sacacho.com.br'])
    msg.body = message
    mail.send(msg)

#-------------------------------------------------------------------------------------------------


#Modelo de dados para o Cadastro------------------------------------------------------------------
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(255), nullable=False)

def __repr__(self):
        return f'<Usuario {self.usuario}>'

#-------------------------------------------------------------------------------------------------

#Modelo de Dados para o estoque de Tecido---------------------------------------------------------
class Estoque_tecido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_tela = db.Column(db.String(100), nullable=False)
    quantidade_tela = db.Column(db.Float, nullable=False)
    tipo_tela = db.Column(db.String(100), nullable=False)
    unidade_medida = db.Column(db.String(50), nullable=False)
    gramatura = db.Column(db.Float, nullable=True)

    def __init__(self, nome_tela, quantidade_tela, tipo_tela, unidade_medida, gramatura):
        self.nome_tela = nome_tela
        self.quantidade_tela = quantidade_tela
        self.tipo_tela = tipo_tela
        self.unidade_medida = unidade_medida
        self.gramatura = gramatura

#-------------------------------------------------------------------------------------------------


#User ID -----------------------------------------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
#-------------------------------------------------------------------------------------------------

# Função para obter a quantidade de um tecido pelo nome-------------------------------------------
def get_quantidade_tecido(nome_tela):
    tecido = Estoque_tecido.query.filter_by(nome_tela=nome_tela).first()
    if tecido:
        return tecido.quantidade_tela  # Retorna a quantidade encontrada
    return 0  # Retorna 0 se o tecido não for encontrado

app.jinja_env.globals['get_quantidade_tecido'] = get_quantidade_tecido

#-------------------------------------------------------------------------------------------------

#Função para obter a quantidade de alças pelo nome------------------------------------------------
def get_quantidade_alca(nome_alca):
    alca = Estoque_alca.query.filter_by(nome_alca=nome_alca).first()
    if alca:
        return alca.quantidade_alca #Retorna a quantidade encontrada
    return 0 #Retorna 0 se a alça não for encontrada
app.jinja_env.globals['get_quantidade_alca'] = get_quantidade_alca

#-------------------------------------------------------------------------------------------------

#Modelo de Dados para o estoque de Alças----------------------------------------------------------
class Estoque_alca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_alca = db.Column(db.String(255), nullable=False)
    quantidade_alca = db.Column(db.Float, nullable=False)
    unidade_medida = db.Column(db.String(50), nullable=False)

    def __init__(self, nome_alca, quantidade_alca, unidade_medida):
        self.nome_alca = nome_alca
        self.quantidade_alca = quantidade_alca
        self.unidade_medida = unidade_medida

#-------------------------------------------------------------------------------------------------

# Modelo de Dados para Cadastro de Pedidos--------------------------------------------------------
class PedidoCliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(255), nullable=False)
    tipo_produto = db.Column(db.String(255), nullable=True)
    produto = db.Column(db.String(255), nullable=False)
    data_emissao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_entrega = db.Column(db.DateTime, nullable=False)
    entregador = db.Column(db.String(100), nullable=False)
    emissor_pedido = db.Column(db.String(100), nullable=False)
    tamanho_altura = db.Column(db.String(50), nullable=True)
    tamanho_largura = db.Column(db.String(50), nullable=True)
    tela = db.Column(db.String(100), nullable=True)
    alca = db.Column(db.String(100), nullable=True)
    medida_alca = db.Column(db.Float, nullable=True)
    estampa = db.Column(db.String(255), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    quantidade_volumes = db.Column(db.Integer, nullable=False)
    observacao = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='andamento')
    ficha_id = db.Column(db.Integer, db.ForeignKey('ficha_tecnica.id'))  # Aqui você pode usar o ID da ficha
    ficha = db.relationship('FichaTecnica', backref='pedidos')
    operador = db.Column(db.String(100))

    def __repr__(self):
        return f'<PedidoCliente {self.nome_cliente}>'
    
#-------------------------------------------------------------------------------------------------
    
# Modelo de Dados para Ficha Técnica--------------------------------------------------------------
class FichaTecnica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    insumos = db.Column(db.Text, nullable=False)  # Pode ser uma string ou lista de insumos
    custo_producao = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<FichaTecnica {self.descricao}>'
    
#-------------------------------------------------------------------------------------------------

    
#Rota de Cadastro --------------------------------------------------------------------------------
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

#-------------------------------------------------------------------------------------------------

#Rota de login -----------------------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

from flask_login import login_user

@app.route('/Login', methods=['POST'])
def processar_login():
    login_usuario = request.form['login_usuario']
    login_senha = request.form['login_senha']
    
    usuario = Usuario.query.filter_by(usuario=login_usuario).first()

    if usuario and check_password_hash(usuario.senha, login_senha):
        login_user(usuario)  # Autentica o usuário
        return redirect(url_for('principal'))
    else:
        flash('Login Inválido', 'error')
        return render_template('login.html', login_invalido=True)
    
#-------------------------------------------------------------------------------------------------


#Rota da Página Principal ------------------------------------------------------------------------
@app.route('/principal', methods=['GET', 'POST'])
@login_required
def principal():
    total_sacos = db.session.query(db.func.sum(PedidoCliente.quantidade)).filter_by(tipo_produto='saco').scalar() or 0
    total_sacolas = db.session.query(db.func.sum(PedidoCliente.quantidade)).filter_by(tipo_produto='sacola').scalar() or 0
    total_bigbags = db.session.query(db.func.sum(PedidoCliente.quantidade)).filter_by(tipo_produto='big bag').scalar()or 0
    pedidos_em_andamento = PedidoCliente.query.filter_by(status='andamento').count()
    pedidos_finalizados = PedidoCliente.query.filter_by(status='finalizado').count()
    total_pedidos = pedidos_em_andamento + pedidos_finalizados

    # Quantidade por mês para cada tipo de pedido
    def get_quantidade_por_mes(tipo_produto):
        return db.session.query(
            extract('month', PedidoCliente.data_emissao).label('mes'),
            db.func.sum(PedidoCliente.quantidade).label('quantidade')
        ).filter_by(tipo_produto=tipo_produto).group_by('mes').order_by('mes').all()

    sacos_por_mes = get_quantidade_por_mes('saco')
    sacolas_por_mes = get_quantidade_por_mes('sacola')
    bigbags_por_mes = get_quantidade_por_mes('big bag')

    # Preparar dados para o gráfico
    meses = list(range(1, 13))  # Meses de 1 a 12
    sacos_data = [next((q for m, q in sacos_por_mes if m == mes), 0) for mes in meses]
    sacolas_data = [next((q for m, q in sacolas_por_mes if m == mes), 0) for mes in meses]
    bigbags_data = [next((q for m, q in bigbags_por_mes if m == mes), 0) for mes in meses]
    
    
    print(f'Total de Pedidos: {total_pedidos}, Pedidos em Andamento: {pedidos_em_andamento}, Pedidos Finalizados: {pedidos_finalizados}')
    print("Sacos Data:", sacos_data)
    print("Sacolas Data:", sacolas_data)
    print("Big Bags Data:", bigbags_data)
    return render_template('principal.html',total_bigbags=total_bigbags,total_sacos=total_sacos, total_sacolas=total_sacolas, 
                           sacos_data=sacos_data,sacolas_data=sacolas_data,bigbags_data=bigbags_data,
                           pedidos_em_andamento=pedidos_em_andamento, 
                           pedidos_finalizados=pedidos_finalizados, 
                           total_pedidos=total_pedidos)

#-------------------------------------------------------------------------------------------------


#Logout ------------------------------------------------------------------------------------------

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#-------------------------------------------------------------------------------------------------

#Página de Estoque de Tecidos --------------------------------------------------------------------

# Função para formatar a quantidade
@app.template_filter('formatar_quantidade')
def formatar_quantidade(quantidade):
    try:
        quantidade = float(quantidade)  # Convertendo para float se necessário
        return f"{quantidade:,.2f}".replace('.', '#').replace(',', '.').replace('#', ',')
    except (ValueError, TypeError):
        return "0,00"  # Valor padrão em caso de erro

@app.route('/tecido')
def tecido():
    itens = Estoque_tecido.query.all()
    itens_formatados = []

    for item in itens:
        item_formatado = {
            'id': item.id,
            'nome_tela': item.nome_tela,
            'quantidade_tela': item.quantidade_tela,  
            'quantidade_tela_formatada': formatar_quantidade(item.quantidade_tela),  # Exibição formatada
            'tipo_tela': item.tipo_tela,
            'unidade_medida': item.unidade_medida,
            'gramatura': formatar_quantidade(item.gramatura)
        }
        itens_formatados.append(item_formatado)

    return render_template('Estoque_tecido.html' , itens=itens_formatados)

# Adicionar item

@app.route('/add_item', methods=['POST'])
def add_item():
    nome_tela = request.form['nome_tela']
    quantidade_tela = request.form['quantidade_tela'].replace(',', '.')  # Substituir vírgula por ponto
    tipo_tela = request.form['tipo_tela']
    unidade_medida = request.form['unidade_medida']
    gramatura = request.form['gramatura'].replace(',', '.')
    
    # Converter quantidade para float
    try:
        quantidade_tela, gramatura = float(quantidade_tela, gramatura)
    except ValueError:
        flash('Por favor, insira uma quantidade válida.')
        return redirect(url_for('tecido'))
    
    novo_item = Estoque_tecido(nome_tela=nome_tela, quantidade_tela=quantidade_tela, tipo_tela=tipo_tela, unidade_medida=unidade_medida,gramatura=gramatura)
    db.session.add(novo_item)
    db.session.commit()
    
    flash('Item adicionado com sucesso!')
    return redirect(url_for('tecido'))

# Editar item

@app.route('/edit_item/<int:id>', methods=['POST'])
def edit_item(id):
    item = Estoque_tecido.query.get_or_404(id)
    
    item.nome_tela = request.form['nome_tela']
    quantidade_tela = request.form['quantidade_tela'].replace(',', '.')  # Substituir vírgula por ponto
    item.tipo_tela = request.form['tipo_tela']
    item.unidade_medida = request.form['unidade_medida']
    gramatura = request.form['gramatura'].replace(',', '.')

    # Converter quantidade para float
    try:
        item.quantidade_tela = float(quantidade_tela)
    except ValueError:
        flash('Por favor, insira uma quantidade válida.')
        return redirect(url_for('tecido'))
    try:
        item.gramatura = float(gramatura)
    except ValueError:
        flash('Por favor, insira uma quantidade válida.')
        return redirect(url_for('tecido'))
    
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


#-------------------------------------------------------------------------------------------------

#Página de Estoque de Alças ----------------------------------------------------------------------

@app.template_filter('formatar_quantidade_alca')
def formatar_quantidade_alca(quantidade):
    try:
        quantidade = float(quantidade)  # Convertendo para float se necessário
        return f"{quantidade:,.0f}".replace(',', '.')  # Exibe a quantidade com separador de milhar
    except (ValueError, TypeError):
        return "0"
    
#Rota para formatar a quantidade de alças

@app.template_filter('formatar_quantidade_alca')
def formatar_quantidade_alca(quantidade):
    try:
        quantidade = float(quantidade)  # Convertendo para float se necessário
        # Exibe a quantidade com separador de milhar (.) e duas casas decimais (,)
        return f"{quantidade:,.2f}".replace('.', '#').replace(',', '.').replace('#', ',')
    except (ValueError, TypeError):
        return "0,00"  # Valor padrão em caso de erro


#Rota de alças

@app.route('/alca')
def alca():
    alcas = Estoque_alca.query.all()
    itens_formatados = []

    for item in alcas:
        item_formatado = {
            'id': item.id,
            'nome_alca': item.nome_alca,
            'quantidade_alca': item.quantidade_alca,  # Mantenha o valor original aqui
            'quantidade_alca_formatada': formatar_quantidade_alca(item.quantidade_alca),  # Exibição formatada
            'unidade_medida': item.unidade_medida,
        }
        itens_formatados.append(item_formatado)

    return render_template('Estoque_alcas.html', itens=itens_formatados)

#Adicionar Alça

@app.route('/add_alca', methods=['POST'])
def add_alca():
    nome_alca = request.form['nome_alca']
    quantidade_alca = request.form['quantidade_alca']
    unidade_medida = request.form['unidade_medida']

    nova_alca = Estoque_alca(nome_alca=nome_alca, quantidade_alca=quantidade_alca, unidade_medida=unidade_medida)
    db.session.add(nova_alca)
    db.session.commit()
    
    flash('Alça adicionada com sucesso!')
    return redirect(url_for('alca'))

#Editar Alça

@app.route('/edit_alca/<int:id>', methods=['POST'])
def edit_alca(id):
    item = Estoque_alca.query.get_or_404(id)
    
    item.nome_alca = request.form['nome_alca']
    item.quantidade_alca = request.form['quantidade_alca']  
    item.unidade_medida = request.form['unidade_medida']
    
    db.session.commit()
    
    flash('Alça atualizada com sucesso!')
    return redirect(url_for('alca'))

#Remover Alça

@app.route('/delete_alca/<int:id>', methods=['POST'])
def delete_alca(id):
    item = Estoque_alca.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    
    flash('Alça removida com sucesso!')
    return redirect(url_for('alca'))

#-------------------------------------------------------------------------------------------------


#Bloco de Cadastro de OP -------------------------------------------------------------------------

#Rota para pesquisar telas
@app.route('/search_telas', methods=['GET'])
def search_telas():
    query = request.args.get('q', '')  # Termo de busca fornecido pelo usuário
    telas = Estoque_tecido.query.filter(Estoque_tecido.nome_tela.ilike(f'%{query}%')).all()  # Busca telas que contenham o termo
    telas_list = [{'nome_tela': tela.nome_tela} for tela in telas]
    return jsonify(telas_list)  # Retorna os dados em formato JSON

#Rota para pesquisar Alças
@app.route('/search_alcas', methods=['GET'])
def search_alcas():
    query = request.args.get('q', '')  # Termo de busca fornecido pelo usuário
    alcas = Estoque_alca.query.filter(Estoque_alca.nome_alca.ilike(f'%{query}%')).all()  # Busca telas que contenham o termo
    alcas_list = [{'nome_alca': alca.nome_alca} for alca in alcas]
    return jsonify(alcas_list)  # Retorna os dados em formato JSON

#Rota para pesquisar Fichas
@app.route('/search_fichas', methods=['GET'])
def search_fichas():
    query = request.args.get('q', '')  # Termo de busca fornecido pelo usuário
    fichas = FichaTecnica.query.filter(FichaTecnica.descricao.ilike(f'%{query}%')).all()  # Busca telas que contenham o termo
    fichas_list = [{'descricao': fichas.descricao} for fichas in fichas]
    return jsonify(fichas_list)  # Retorna os dados em formato JSON

@app.route('/add_pedido', methods=['POST'])
def add_pedido():
    # Capturando os dados do formulário
    nome_tela = request.form.get('tela')
    print(f'Tela: {nome_tela}')

    # Verificar se a Tela existe
    tela = Estoque_tecido.query.filter_by(nome_tela=nome_tela).first()
    if not tela:
        flash('Tela não encontrada.')
        return redirect(url_for('Op_cadastro'))

    # Tornar a verificação de Alça opcional para Sacos
    tipo_produto = request.form.get('tipo_produto', '').lower()  # Ignorar maiúsculas e minúsculas
    alca = None
    if tipo_produto == 'sacola':  # Apenas verificar alça se não for 'Saco'
        nome_alca = request.form.get('alca')
        alca = Estoque_alca.query.filter_by(nome_alca=nome_alca).first()
        if not alca:
            flash('Alça não encontrada.')
            return redirect(url_for('Op_cadastro'))

    nome_cliente = request.form['nome_cliente']
    produto = request.form['produto']
    data_emissao = datetime.strptime(request.form['data_emissao'], '%Y-%m-%d').strftime('%d/%m/%Y')
    data_entrega= datetime.strptime(request.form['data_emissao'], '%Y-%m-%d').strftime('%d/%m/%Y')
    entregador = request.form['entregador']
    emissor_pedido = request.form['emissor_pedido']
    tamanho_altura = request.form['tamanho_altura']
    tamanho_largura = request.form['tamanho_largura']

    # Convertendo a medida da alça de vírgula para ponto, se necessário
    medida_alca = request.form['medida_alca'].replace(',', '.')  # Substitui a vírgula por ponto
    medida_alca = float(medida_alca) if medida_alca else None  # Converte para float

    estampa = request.form['estampa']
    quantidade = request.form['quantidade']
    quantidade_volumes = request.form['quantidade_volumes']
    observacao = request.form['observacao']
    status = request.form.get('status')

    novo_pedido = PedidoCliente(
        nome_cliente=nome_cliente,
        tipo_produto=tipo_produto,
        produto=produto,
        data_emissao=data_emissao,
        data_entrega=data_entrega,
        entregador=entregador,
        emissor_pedido=emissor_pedido,
        tamanho_altura=tamanho_altura,
        tamanho_largura=tamanho_largura,
        tela=nome_tela,  # Usar o valor da tela do formulário
        alca=alca.nome_alca if alca else None,  # Ajustado para ser None se alça não existir
        medida_alca=medida_alca,
        estampa=estampa,
        quantidade=quantidade,
        quantidade_volumes=quantidade_volumes,
        observacao=observacao,
        status=status
    )
    
    
    db.session.add(novo_pedido)
    db.session.commit()
    send_notification_email('Atenção! Um novo pedido cadastrado!')
    flash('Pedido cadastrado com sucesso!')
    return redirect(url_for('Op_andamento'))


# Rota para Cadastro de Big Bags
@app.route('/add_bigbag', methods=['POST'])
def add_bigbag():
    descricao_ficha = request.form.get('ficha')  # Obtém a descrição da ficha
    print(f'Ficha: {descricao_ficha}')

    # Verificar se a Ficha existe
    ficha = FichaTecnica.query.filter_by(descricao=descricao_ficha).first()  # Busca a ficha pela descrição
    if not ficha:
        flash('Ficha não encontrada.')
        return redirect(url_for('Op_cadastro'))
    

    # Obtendo os dados do formulário de Big Bags
    nome_cliente = request.form.get('nome_cliente')
    tipo_produto = request.form.get('tipo_produto', '').lower()  # Ignorar maiúsculas e minúsculas
    produto = request.form.get('produto')
    data_emissao = datetime.strptime(request.form.get('data_emissao'), '%Y-%m-%d')
    data_entrega = datetime.strptime(request.form.get('data_entrega'), '%Y-%m-%d')
    entregador = request.form.get('entregador')
    emissor_pedido = request.form.get('emissor_pedido')
    estampa = request.form.get('estampa')
    quantidade = int(request.form.get('quantidade'))  # Quantidade de Big Bags
    quantidade_volumes = request.form.get('quantidade_volumes')
    observacao = request.form.get('observacao')
    status = request.form.get('status')

    # Criar o objeto do pedido
    novo_pedido_bigbag = PedidoCliente(
        nome_cliente=nome_cliente,
        tipo_produto=tipo_produto,
        produto=produto,
        data_emissao=data_emissao,
        data_entrega=data_entrega,
        entregador=entregador,
        emissor_pedido=emissor_pedido,
        estampa=estampa,
        quantidade=quantidade,
        quantidade_volumes=quantidade_volumes,
        observacao=observacao,
        status=status,
        ficha_id=ficha.id  # ID da ficha técnica selecionada
    )
    
    
    # Adicionar o pedido ao banco de dados
    db.session.add(novo_pedido_bigbag)
    db.session.commit()
    send_notification_email('Atenção! Um novo pedido cadastrado!')
    # Exibir mensagem de sucesso
    flash('Pedido de Big Bags cadastrado com sucesso e baixa de estoque realizada!')
    return redirect(url_for('Op_andamento'))

# Rota para exibir o formulário de cadastro de pedidos
@app.route('/Op_cadastro', methods=['GET', 'POST'])
def Op_cadastro():
    fichas_tecnicas = FichaTecnica.query.all()
    telas = Estoque_tecido.query.all()
    print(f'Telas encontradas: {[tela.nome_tela for tela in telas]}') 
    return render_template('Op_cadastro.html', fichas_tecnicas=fichas_tecnicas, telas=telas)


#-------------------------------------------------------------------------------------------------

#Rota para exibir os pedidos em andamento --------------------------------------------------------
@app.route('/Op_andamento')
def Op_andamento():
    pedidos = PedidoCliente.query.filter_by(status='andamento').all()
    return render_template('Op_andamento.html', pedidos=pedidos)

#Rota para editar pedidos
@app.route('/editar_pedido/<int:id>', methods=['GET', 'POST'])
def editar_pedido(id):
    pedido = PedidoCliente.query.get_or_404(id)
    
    if request.method == 'POST':
        # Atualizar quantidade
        nova_quantidade = request.form.get('quantidade')
        if nova_quantidade and nova_quantidade.isdigit():
            pedido.quantidade = int(nova_quantidade)
        
        # Atualizar tamanho em altura
        novo_tamanho_altura = request.form.get('tamanho_altura')
        if novo_tamanho_altura and novo_tamanho_altura.isdigit():
            pedido.tamanho_altura = int(novo_tamanho_altura)
        
        # Atualizar tamanho em largura
        novo_tamanho_largura = request.form.get('tamanho_largura')
        if novo_tamanho_largura and novo_tamanho_largura.isdigit():
            pedido.tamanho_largura = int(novo_tamanho_largura)
        
        # Atualizar tela e alça
        nova_tela = request.form.get('tela')
        nova_alca = request.form.get('alca')
        
        if nova_tela:
            pedido.tela = nova_tela
        if nova_alca:
            pedido.alca = nova_alca
        
        db.session.commit()
        flash('Pedido atualizado com sucesso!', 'success')
        return redirect(url_for('Op_andamento'))
    
    return render_template('editar_pedido.html', pedido=pedido)
@app.route('/cancelar_pedido/<int:id>', methods=['POST'])
def cancelar_pedido(id):
    pedido = PedidoCliente.query.get_or_404(id)
    pedido.status = 'cancelado'  # Atualiza o status para "cancelado"
    db.session.commit()
    flash('Pedido cancelado com sucesso!', 'success')
    return redirect(url_for('Op_andamento'))

@app.route('/finalizar_pedido/<int:id>', methods=['POST'])
def finalizar_pedido(id):
    print(f"Pedido ID: {id}")  # Verifica se a rota está sendo chamada

    # Buscar o pedido
    pedido = PedidoCliente.query.get_or_404(id)
    print(f"Pedido encontrado: {pedido}")
    print(f"Ficha ID do Pedido: {pedido.ficha_id}")  # Verificar o ficha_id do pedido

    # Verificar o tipo de produto
    tipo_produto = pedido.tipo_produto.strip().lower() if pedido.tipo_produto else None
    print(f"Tipo de produto: {tipo_produto}")

    # Caso seja Big Bag, não faz verificação de tecido
    if tipo_produto == 'big bag':
        print("Tipo de produto: Big Bag. Ignorando verificação de tecido.")

        # Verificar se o pedido tem uma ficha técnica associada
        if pedido.ficha_id:
            ficha = FichaTecnica.query.get(pedido.ficha_id)
            if not ficha:
                flash('Ficha técnica não encontrada.')
                return redirect(url_for('Op_andamento'))
            print(f"Ficha técnica: {ficha.descricao}")

            # Converter os insumos da ficha de string para lista
            insumos = eval(ficha.insumos) if ficha.insumos else []
            print(f"Insumos da ficha técnica: {insumos}")

            if not insumos:
                flash('Nenhum insumo encontrado para a ficha técnica.')
                return redirect(url_for('Op_andamento'))

            # Descontar insumos do estoque com base na quantidade do pedido
            for insumo in insumos:
                nome = insumo['nome']
                quantidade_ficha = float(insumo['quantidade'].replace(',', '.'))  # Quantidade para uma unidade do produto
                quantidade_total_insumo = quantidade_ficha * pedido.quantidade  # Multiplica pela quantidade do pedido

                print(f"Processando insumo: {nome}, Quantidade Total: {quantidade_total_insumo}")

                # Verificar se o insumo é tecido ou alça e atualizar o estoque correspondente
                if insumo['tipo'] == 'Tecido':
                    tecido_insumo = Estoque_tecido.query.filter_by(nome_tela=nome).first()
                    if tecido_insumo:
                        print(f"Estoque atual de tecido {nome}: {tecido_insumo.quantidade_tela}")
                        if tecido_insumo.quantidade_tela >= quantidade_total_insumo:
                            tecido_insumo.quantidade_tela -= quantidade_total_insumo  # Descontar do estoque
                            print(f"Novo estoque de tecido {nome}: {tecido_insumo.quantidade_tela}")
                        else:
                            flash(f'Estoque insuficiente de {nome}.')
                            return redirect(url_for('Op_andamento'))
                    else:
                        flash(f'Tecido {nome} não encontrado.')
                        return redirect(url_for('Op_andamento'))

                elif insumo['tipo'] == 'Alça':
                    alca = Estoque_alca.query.filter_by(nome_alca=nome).first()
                    if alca:
                        print(f"Estoque atual de alça {nome}: {alca.quantidade_alca}")
                        if alca.quantidade_alca >= quantidade_total_insumo:
                            alca.quantidade_alca -= quantidade_total_insumo  # Descontar do estoque
                            print(f"Novo estoque de alça {nome}: {alca.quantidade_alca}")
                        else:
                            flash(f'Estoque insuficiente de {nome}.')
                            return redirect(url_for('Op_andamento'))
                    else:
                        flash(f'Alça {nome} não encontrada.')
                        return redirect(url_for('Op_andamento'))

        # Atualizar o status do pedido para 'finalizado'
        pedido.status = 'finalizado'
        pedido.operador = current_user.usuario
        db.session.commit()
        print(f"Status do pedido {pedido.id}: {pedido.status}")
        flash('Pedido Big Bag finalizado com sucesso!')
        return redirect(url_for('Op_andamento'))

    # Para Saco e Sacola, não precisa da ficha técnica
    # Verificar o tecido diretamente
    else:
        tecido = Estoque_tecido.query.filter_by(nome_tela=pedido.tela).first()
        if not tecido:
            flash(f'Tecido {pedido.tela} não encontrado no estoque.')
            return redirect(url_for('Op_andamento'))

        # Definir o tipo de tela com base no estoque de tecidos
        tipo_tela = tecido.tipo_tela  # 'PLANA' ou 'TUBULAR'
        print(f"Tipo de tela: {tipo_tela}")

        # Verifique se o tipo de tela é válido
        if tipo_tela not in ['PLANA', 'TUBULAR']:
            flash('Tipo de tela inválido.')
            return redirect(url_for('Op_andamento'))

        # Obter a gramatura do tecido
        gramatura_tela = tecido.gramatura / 1000  # Considera a gramatura em kg

        # Certifique-se de que altura e largura sejam números
        try:
            altura = float(pedido.tamanho_altura)  # Converta para float
            largura = float(pedido.tamanho_largura)  # Converta para float
        except ValueError:
            flash('Erro ao converter os tamanhos de altura ou largura.')
            return redirect(url_for('Op_andamento'))

        altura = altura / 100  # Convertendo para metros
        largura = largura / 100  # Convertendo para metros

        # Verificar o tipo de produto
        if tipo_produto == 'saco':
            corte = altura + 0.03  # adiciona 3 cm para sacos
        elif tipo_produto == 'sacola':
            corte = altura + 0.05  # adiciona 5 cm para sacolas
        else:
            flash('Tipo de produto inválido.')
            return redirect(url_for('Op_andamento'))

        # Cálculo da largura da tela
        if tipo_tela == 'PLANA':
            largura_tela = largura  # largura em metros
        elif tipo_tela == 'TUBULAR':
            largura_tela = largura * 2  # dobra a largura para tubular
        else:
            flash('Tipo de tela inválido.')
            return redirect(url_for('Op_andamento'))
        

        # Cálculo da quantidade total de material necessário
        quantidade = pedido.quantidade
        quantidade_total = largura_tela * corte * quantidade * gramatura_tela
        print(f"Quantidade total de material necessário: {quantidade_total}")

        # Verificar e descontar do estoque do tecido
        if tecido.quantidade_tela >= quantidade_total:
            tecido.quantidade_tela -= quantidade_total
            print(f"Novo estoque de tecido {pedido.tela}: {tecido.quantidade_tela}")
        else:
            flash(f'Estoque insuficiente de {pedido.tela}.')
            return redirect(url_for('Op_andamento'))

         # Verificar a alça no estoque apenas para sacolas
    if tipo_produto == 'sacola':  # Verificar alça apenas se for sacola
        alca = Estoque_alca.query.filter_by(nome_alca=pedido.alca).first()  # Buscar a alça pelo nome
        if alca:
            quantidade_total_alca = ((pedido.quantidade * 2) * float(pedido.medida_alca)) / 100  # Cálculo da quantidade total de alça necessária
            print(f"Quantidade total de alça necessária: {quantidade_total_alca}")

            if alca.quantidade_alca >= quantidade_total_alca:
                alca.quantidade_alca -= quantidade_total_alca  # Descontar do estoque
                print(f"Novo estoque de alça {alca.nome_alca}: {alca.quantidade_alca}")
            else:
                flash(f'Estoque insuficiente de alça {alca.nome_alca}.')
                return redirect(url_for('Op_andamento'))
        else:
            flash(f'Alça {pedido.alca} não encontrada no estoque.')
            return redirect(url_for('Op_andamento'))

    # Atualizar o status do pedido para 'finalizado'
    pedido.status = 'finalizado'
    pedido.operador = current_user.usuario
    db.session.commit()
    print(f"Status do pedido {pedido.id}: {pedido.status}")

    flash('Pedido finalizado com sucesso!')
    return redirect(url_for('Op_andamento'))
#-------------------------------------------------------------------------------------------------


#Rota de Pedidos Finalizados ---------------------------------------------------------------------
@app.route('/Op_finalizada', methods=['GET', 'POST'])
def Op_finalizada():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)  # Certifique-se de obter a página da requisição

    # Filtrar pedidos com status 'finalizado'
    filters = [or_(PedidoCliente.status == 'finalizado', PedidoCliente.status == 'cancelado')]  # Definimos `filters` fora do `if`

    if search_query:
        # Tenta converter `search_query` para data, caso esteja no formato 'YYYY-MM-DD'
        try:
                search_date = datetime.strptime(search_query, '%Y-%m-%d').date()
                filters.append(PedidoCliente.data_emissao == search_date)
        except ValueError:
            # Caso não seja uma data, aplica o filtro aos campos de texto
            filters.append(
                PedidoCliente.nome_cliente.ilike(f'%{search_query}%') |
                PedidoCliente.produto.ilike(f'%{search_query}%') |
                PedidoCliente.estampa.ilike(f'%{search_query}%')
            )

    pedidos = PedidoCliente.query.filter(*filters).order_by(PedidoCliente.id.desc()).paginate(page=page, per_page=10)

    return render_template('Op_finalizada.html', pedidos=pedidos, search_query=search_query)
#-------------------------------------------------------------------------------------------------

#Rotas de ficha técnica --------------------------------------------------------------------------

#Rota para buscar insumos
@app.route('/buscar_insumos')
def buscar_insumos():
    termo = request.args.get('q', '')
    
    # Filtrar tecidos e alças pelo termo de pesquisa
    tecidos = Estoque_tecido.query.filter(Estoque_tecido.nome_tela.ilike(f'%{termo}%')).all()
    alcas = Estoque_alca.query.filter(Estoque_alca.nome_alca.ilike(f'%{termo}%')).all()
    
    # Montar a lista de insumos encontrados
    insumos = []
    for tecido in tecidos:
        insumos.append({'id': tecido.id, 'nome': tecido.nome_tela, 'tipo': 'Tecido'})
    for alca in alcas:
        insumos.append({'id': alca.id, 'nome': alca.nome_alca, 'tipo': 'Alça'})
    
    return jsonify(insumos)
    

# Rota para cadastrar ficha técnica
@app.route('/cadastrar_ficha', methods=['POST'])
def cadastrar_ficha():
    descricao = request.form['descricao']
    custo_producao = request.form['custo_producao']
    
    # Captura insumos selecionados e suas respectivas quantidades
    
    insumos = []
    for insumo_id in request.form.getlist('insumo_ids[]'):
        quantidade = request.form.get(f'quantidade_insumo_{insumo_id}')
        
        # Buscar o insumo (tecido ou alça) pelo ID
        tecido = Estoque_tecido.query.get(insumo_id)
        if tecido:
            insumos.append({
                'nome': tecido.nome_tela,
                'quantidade': quantidade,
                'unidade': tecido.unidade_medida,
                'tipo': 'Tecido'
            })
        
        alca = Estoque_alca.query.get(insumo_id)
        if alca:
            insumos.append({
                'nome': alca.nome_alca,
                'quantidade': quantidade,
                'unidade': alca.unidade_medida,
                'tipo': 'Alça'
            })

    # Cadastrar a ficha técnica no banco de dados
    nova_ficha = FichaTecnica(
        descricao=descricao, 
        insumos=str(insumos),  # Convertendo a lista de insumos para string para salvar no banco
        custo_producao=custo_producao
    )
    db.session.add(nova_ficha)
    db.session.commit()

    # Redirecionar para a página que lista as fichas técnicas
    return redirect(url_for('Fichas_tecnicas'))

# Rota para editar ficha técnica (opcional)
@app.route('/editar_ficha/<int:id>', methods=['POST'])
def editar_ficha(id):
    form_data = request.form
    print(form_data)  # Verifique o que está sendo impresso

    # Verificar campos obrigatórios
    descricao = form_data.get('descricao')
    if not descricao:
        return "Erro: campo 'descricao' ausente", 400

    custo_producao = form_data.get('custo_producao')
    if custo_producao is None:
        return "Erro: campo 'custo_producao' ausente", 400

    ficha = FichaTecnica.query.get_or_404(id)
    ficha.descricao = descricao

    # Captura insumos selecionados e suas respectivas quantidades
    insumos = []
    
    # Verifique se existem tecidos selecionados
    tecidos_selecionados = request.form.getlist('tecidos')
    for tecido_id in tecidos_selecionados:
        quantidade = request.form.get(f'quantidade_tecido_{tecido_id}')
        tecido = Estoque_tecido.query.get(tecido_id)
        if tecido:
            insumos.append({'nome': tecido.nome_tela, 'quantidade': quantidade, 'unidade': tecido.unidade_medida})

    # Verifique se existem alças selecionadas
    alcas_selecionadas = request.form.getlist('alcas')
    for alca_id in alcas_selecionadas:
        quantidade = request.form.get(f'quantidade_alca_{alca_id}')
        alca = Estoque_alca.query.get(alca_id)
        if alca:
            insumos.append({'nome': alca.nome_alca, 'quantidade': quantidade, 'unidade': alca.unidade_medida})

    # Se nenhum insumo for selecionado, retornar erro
    if not insumos:
        return "Erro: Nenhum insumo selecionado", 400

    ficha.insumos = str(insumos)  # Atualiza os insumos
    ficha.custo_producao = custo_producao  # Atualiza o custo de produção

    db.session.commit()
    flash('Ficha técnica atualizada com sucesso!')
    return redirect(url_for('Fichas_tecnicas'))

@app.route('/Fichas_tecnicas')
def Fichas_tecnicas():
    fichas = FichaTecnica.query.all()
    tecidos = Estoque_tecido.query.all()  # Buscar tecidos disponíveis no estoque
    alcas = Estoque_alca.query.all()      # Buscar alças disponíveis no estoque
    
    # Formatar insumos para exibição
    for ficha in fichas:
        insumos_formatados = []
        insumos_lista = eval(ficha.insumos)  # Converter string de insumos de volta para lista
        for insumo in insumos_lista:
            formatted_insumo = f"{insumo['nome']} - {insumo['quantidade']} {insumo['unidade']}"
            insumos_formatados.append(formatted_insumo)
        ficha.insumos = ', '.join(insumos_formatados)  # Juntar insumos formatados em uma string

    return render_template('Fichas_tecnicas.html', fichas_tecnicas=fichas, tecidos=tecidos, alcas=alcas)

# Rota para deletar ficha técnica (opcional)
@app.route('/deletar_ficha/<int:id>', methods=['POST'])
def deletar_ficha(id):
    ficha = FichaTecnica.query.get_or_404(id)
    db.session.delete(ficha)
    db.session.commit()
    flash('Ficha técnica deletada com sucesso!')
    return redirect(url_for('Fichas_tecnicas'))
#-------------------------------------------------------------------------------------------------



#Rota de impressão de OP -------------------------------------------------------------------------
@app.route('/imprimir_op')
def imprimir_op():
    # Obtém os IDs dos pedidos da URL
    pedido_ids = request.args.get('pedido_ids')
    if pedido_ids:
        pedido_ids = pedido_ids.split(',')
        pedido_ids = [int(id) for id in pedido_ids]
        pedidos = PedidoCliente.query.filter(PedidoCliente.id.in_(pedido_ids)).all()
    else:
        pedidos = []

    # Renderiza o template com os dados dos pedidos
    return render_template('imprimir_op.html', pedidos=pedidos, math=math)

#-------------------------------------------------------------------------------------------------







if __name__ == '__main__':
    app.run(host='192.168.1.13', port=5000)