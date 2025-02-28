from flask import Flask, render_template, request, redirect, url_for, session, Response
import requests
import sqlite3
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Inicializa o banco de dados e cria usuários padrão
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    # Adiciona os usuários apenas se ainda não existirem no banco
    users = [
        ('admin', '1234', 'admin'),
        ('sistemas', '1234', 'sistemas'),
        ('expansao', '1234', 'expansao')
    ]
    for user in users:
        c.execute('SELECT * FROM users WHERE username = ?', (user[0],))
        if not c.fetchone():
            c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', user)

    conn.commit()
    conn.close()




# Rota de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['username'] = username
            session['role'] = user[3]  # Armazena o papel do usuário na sessão
            return redirect(url_for('hello'))
        else:
            return "Credenciais inválidas!"
    
    return render_template('login.html')

# Rota protegida para exibir as divs
@app.route('/acessos')
def hello():
    if 'username' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/proxy_zabbix')
def proxy_zabbix():
    if 'role' not in session or session['role'] not in ['admin', 'sistemas', 'expansao']:
        return "Acesso não autorizado!", 403

    # URL do site que você deseja proxyficar
    target_url = "https://rogeriolago.github.io/"  # Substitua pelo seu URL alvo
    
    # Realiza a requisição GET para o site
    response = requests.get(target_url)
    
    # Verifica se a resposta foi bem-sucedida
    if response.status_code != 200:
        return f"Erro ao acessar o site: {response.status_code}", response.status_code
    
    # Modifica o conteúdo HTML da resposta
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Modifica todas as URLs dentro do HTML
    for tag in soup.find_all(['link', 'script', 'img']):
        if tag.name == 'link' and tag.get('href'):
            tag['href'] = url_for('static', filename=tag['href'].replace(target_url, ''))
        elif tag.name == 'script' and tag.get('src'):
            tag['src'] = url_for('static', filename=tag['src'].replace(target_url, ''))
        elif tag.name == 'img' and tag.get('src'):
            tag['src'] = url_for('static', filename=tag['src'].replace(target_url, ''))

    # Retorna o HTML modificado
    return Response(str(soup), status=response.status_code, content_type=response.headers['Content-Type'])

# Rota para logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Inicia o servidor Flask e cria o banco de dados
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
