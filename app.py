from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pandas as pd
import re

app = Flask(__name__)

# Configurações
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'segredo'

# Função para verificar a extensão do arquivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Verifica se um arquivo foi enviado
        if "file" not in request.files:
            flash("Nenhum arquivo enviado!", "danger")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("Nenhum arquivo selecionado!", "danger")
            return redirect(request.url)

        # Verifica se o arquivo tem a extensão permitida
        if not allowed_file(file.filename):
            flash("Arquivo inválido. Por favor, envie um arquivo .txt.", "danger")
            return redirect(request.url)

        # Salvar o arquivo enviado
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Processar o arquivo
        try:
            # Abrir o arquivo e ler as linhas
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Listas para armazenar dados extraídos
            eventos = []
            notas = []
            elementos = []
            valores = []
            notas_sistema = []  # Lista para armazenar o valor de 'NOTA SISTEMA'

            # Expressões regulares para capturar os dados necessários
            regex_evento = r"401002"  # Captura o evento 401002
            regex_nota = r"(2024NE\d+)"  # Captura a nota fiscal
            regex_elemento = r"\d{8}"  # Captura o código do elemento (ex: 44903004)
            regex_valor = r"\d{1,3}(?:\.\d{3})*,\d{2}"  # Captura o valor com vírgula como separador decimal
            regex_nota_sistema = r"^(\d{6})\s"  # Captura o número da nota do sistema (6 dígitos seguidos de um espaço)

            nota_sistema_atual = None  # Variável para armazenar a nota sistema atual

            for line in lines:
                # Depuração: Exibindo as linhas do arquivo para verificar se estão sendo lidas corretamente
                print("Linha analisada:", line.strip())

                # Procurar por cada expressão regular
                evento = re.search(regex_evento, line)
                nota = re.search(regex_nota, line)
                elemento = re.search(regex_elemento, line)
                valor = re.search(regex_valor, line)
                nota_sistema = re.search(regex_nota_sistema, line)

                # Se encontrar uma nova "NOTA SISTEMA", atualiza a variável
                if nota_sistema:
                    nota_sistema_atual = nota_sistema.group(1)

                # Se encontrar um evento, vamos associar o evento com a "NOTA SISTEMA" atual
                if evento:
                    # Adicionar o evento à lista
                    eventos.append(evento.group())

                    # Se outros dados também estiverem presentes, associamos
                    if nota and elemento and valor:
                        notas.append(nota.group())
                        elementos.append(elemento.group())
                        valores.append(valor.group())
                        notas_sistema.append(nota_sistema_atual)  # Adiciona a "NOTA SISTEMA" associada
                    else:
                        # Se algum dado não for encontrado, ainda adicionamos, mas com valores vazios
                        notas.append('')
                        elementos.append('')
                        valores.append('')
                        notas_sistema.append(nota_sistema_atual if nota_sistema_atual else '')

            # Verifica se dados foram extraídos
            if not eventos:
                flash("Nenhum dado correspondente encontrado no arquivo.", "warning")
                return redirect(url_for('index'))

            # Criar um DataFrame com os dados extraídos e adicionar a coluna 'ID'
            df = pd.DataFrame({
                "ID": range(1, len(eventos) + 1),  # Adiciona a coluna 'ID' com números sequenciais
                "EVENTO": eventos,
                "NOTA": notas,
                "ELEMENTO": elementos,
                "VALOR": valores,
                "NOTA SISTEMA": notas_sistema  # Inclui 'NOTA SISTEMA'
            })

            # Salvar os dados em um arquivo Excel
            output_file = os.path.join(app.config['UPLOAD_FOLDER'], 'linhas_filtradas_com_dados.xlsx')
            df.to_excel(output_file, index=False)

            # Converter o DataFrame para HTML
            html_table = df.to_html(index=False, classes="tabela-dados")

            flash("Arquivo processado com sucesso!", "success")
            return render_template("resultado.html", tabela=html_table)

        except Exception as e:
            flash(f"Erro ao processar o arquivo: {e}", "danger")
            return redirect(request.url)

    return render_template("index.html")

if __name__ == "__main__":
    # Criar pasta de upload se não existir
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
