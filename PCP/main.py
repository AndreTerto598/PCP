from flask import Flask, render_template, redirect, request, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, update
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

def __repr__(self):
        return f'<Usuario {self.usuario}>'

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


# Função para obter a quantidade de um tecido pelo nome
def get_quantidade_tecido(nome_tela):
    tecido = Estoque_tecido.query.filter_by(nome_tela=nome_tela).first()
    if tecido:
        return tecido.quantidade_tela  # Retorna a quantidade encontrada
    return 0  # Retorna 0 se o tecido não for encontrado

app.jinja_env.globals['get_quantidade_tecido'] = get_quantidade_tecido

#Função para obter a quantidade de alças pelo nome
def get_quantidade_alca(nome_alca):
    alca = Estoque_alca.query.filter_by(nome_alca=nome_alca).first()
    if alca:
        return alca.quantidade_alca #Retorna a quantidade encontrada
    return 0 #Retorna 0 se a alça não for encontrada
app.jinja_env.globals['get_quantidade_alca'] = get_quantidade_alca

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
    medida_alca = db.Column(db.Float, nullable=False)
    estampa = db.Column(db.String(255), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    quantidade_volumes = db.Column(db.Integer, nullable=False)
    observacao = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='andamento')

    def __repr__(self):
        return f'<PedidoCliente {self.nome_cliente}>'
    
    # Modelo de Dados para Ficha Técnica
class FichaTecnica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    insumos = db.Column(db.Text, nullable=False)  # Pode ser uma string ou lista de insumos
    custo_producao = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<FichaTecnica {self.descricao}>'

    
        

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
@app.template_filter('formatar_quantidade')
def formatar_quantidade(quantidade):
    try:
        quantidade = float(quantidade)  # Convertendo para float se necessário
        return f"{quantidade:,.0f}".replace(',', '.')  # Exibe a quantidade com separador de milhar
    except (ValueError, TypeError):
        return "0"

@app.route('/tecido')
def tecido():
    itens = Estoque_tecido.query.all()
    itens_formatados = []

    for item in itens:
        item_formatado = {
            'id': item.id,
            'nome_tela': item.nome_tela,
            'quantidade_tela': item.quantidade_tela,  # Mantenha o valor original aqui
            'quantidade_tela_formatada': formatar_quantidade(item.quantidade_tela),  # Exibição formatada
            'tipo_tela': item.tipo_tela,
            'unidade_medida': item.unidade_medida,
        }
        itens_formatados.append(item_formatado)

    return render_template('Estoque_tecido.html' , itens=itens_formatados)

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
    item.quantidade_tela = int(request.form['quantidade_tela'])
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

@app.template_filter('formatar_quantidade_alca')
def formatar_quantidade_alca(quantidade):
    try:
        quantidade = float(quantidade)  # Convertendo para float se necessário
        return f"{quantidade:,.0f}".replace(',', '.')  # Exibe a quantidade com separador de milhar
    except (ValueError, TypeError):
        return "0"
    

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
    item.quantidade_alca = int(request.form['quantidade_alca'])  # Garantindo que o valor seja um inteiro
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


# Rota para processar o cadastro de Sacos e Bolsas
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
    medida_alca = request.form['medida_alca']
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
        medida_alca=medida_alca,
        estampa=estampa,
        quantidade=quantidade,
        quantidade_volumes=quantidade_volumes,
        observacao=observacao
    )

    db.session.add(novo_pedido)
    db.session.commit()
    flash('Pedido cadastrado com sucesso!')
    return redirect(url_for('Op_andamento'))

#Rota para Cadastro de Big Bags
@app.route('/add_bigbag', methods=['POST'])
def add_bigbag():
    # Obtendo os dados do formulário de Big Bags
    nome_cliente = request.form['nome_cliente']
    produto = request.form['produto']
    data_emissao = request.form['data_emissao']
    data_entrega = request.form['data_entrega']
    entregador = request.form['entregador']
    emissor_pedido = request.form['emissor_pedido']
    ficha_tecnica = request.form['ficha_tecnica']
    estampa = request.form['estampa']
    quantidade = request.form['quantidade']
    quantidade_volumes = request.form['quantidade_volumes']
    observacao = request.form['observacao']

    # Criar uma nova instância de PedidoCliente
    novo_pedido_bigbag = PedidoCliente(
        nome_cliente=nome_cliente,
        produto=produto,
        data_emissao=data_emissao,
        data_entrega=data_entrega,
        entregador=entregador,
        emissor_pedido=emissor_pedido,
        ficha_tecnica=ficha_tecnica,
        estampa=estampa,
        quantidade=quantidade,
        quantidade_volumes=quantidade_volumes,
        observacao=observacao,
        status='em andamento'  # Definir status inicial como 'em andamento'
    )

    # Adicionar o pedido ao banco de dados
    db.session.add(novo_pedido_bigbag)
    db.session.commit()

    # Exibir mensagem de sucesso
    flash('Pedido de Big Bags cadastrado com sucesso!')
    return redirect(url_for('Op_pedidos'))

# Rota para exibir o formulário de cadastro de pedidos
@app.route('/Op_cadastro', methods=['GET', 'POST'])
def Op_cadastro():
    return render_template('Op_cadastro.html')


#Rota para exibir os pedidos em andamento
@app.route('/Op_andamento')
def Op_andamento():
    pedidos = PedidoCliente.query.filter_by(status='andamento').all()
    return render_template('Op_andamento.html', pedidos=pedidos)

#Rota para finalizar pedido
@app.route('/finalizar_pedido/<int:id>', methods=['POST'])
def finalizar_pedido(id):
    pedido = PedidoCliente.query.get_or_404(id)
    pedido.status = 'finalizado'
    db.session.commit()
    return redirect(url_for('Op_andamento'))


#Rota de Pedidos Finalizados
@app.route('/Op_finalizada', methods=['GET', 'POST'])
def Op_finalizada():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)  # Certifique-se de obter a página da requisição

    # Filtrar pedidos com status 'finalizado'
    if search_query:
        pedidos = PedidoCliente.query.filter(
            PedidoCliente.status == 'finalizado',
            PedidoCliente.nome_cliente.ilike(f'%{search_query}%')
        ).paginate(page=page, per_page=10)
    else:
        pedidos = PedidoCliente.query.filter_by(status='finalizado').paginate(page=page, per_page=10)

    return render_template('Op_finalizada.html', pedidos=pedidos, search_query=search_query)

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













if __name__ == '__main__':
    app.run(debug=True)
