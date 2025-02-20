from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_secreta'

# Criar banco de dados
conn = sqlite3.connect('usuarios.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, usuario TEXT, senha TEXT)''')
conn.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        
        c.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
        user = c.fetchone()
        
        if user:
            session['usuario'] = usuario
            return redirect(url_for('dashboard'))  # Redireciona para o dashboard
        else:
            return 'Login falhou! Verifique suas credenciais.'
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        
        c.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
        conn.commit()
        
        return redirect(url_for('login'))  # Redireciona para login após cadastro
    
    return render_template('cadastro.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        return render_template('dashboard.html')  # Mostra dashboard
    return redirect(url_for('login'))  # Se não estiver logado, manda pro login

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('home'))  # Volta para a página inicial

if __name__ == '__main__':
    app.run(debug=True)
