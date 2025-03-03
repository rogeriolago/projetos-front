from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

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



# Rota para logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Inicia o servidor Flask e cria o banco de dados
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
