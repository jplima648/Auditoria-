
Projeto de Processamento de Arquivo .txt com Flask
Este projeto é uma aplicação web desenvolvida com Flask para processar arquivos de texto (.txt) e extrair informações específicas usando expressões regulares. O objetivo principal é extrair eventos, notas fiscais, elementos, valores e notas de sistema de um arquivo .txt fornecido pelo usuário, e exibir os dados em uma tabela HTML e em um arquivo Excel.

Funcionalidades
Envio de Arquivo: O usuário pode enviar um arquivo .txt que será processado pela aplicação.
Validação de Arquivo: Apenas arquivos com extensão .txt são permitidos.
Processamento de Dados: O arquivo enviado é lido, e dados específicos são extraídos utilizando expressões regulares.
Exibição dos Dados: Os dados extraídos são exibidos em uma tabela HTML e também salvos em um arquivo Excel.
Feedback ao Usuário: A aplicação fornece mensagens de sucesso ou erro, dependendo do resultado do processamento.
Tecnologias Utilizadas
Flask: Framework web para Python que facilita o desenvolvimento da aplicação.
Pandas: Biblioteca para manipulação de dados, utilizada para criar e salvar o arquivo Excel.
Expressões Regulares (Regex): Para extrair dados específicos do arquivo .txt.
HTML/CSS: Para exibir os dados de forma estruturada na página.
Como Usar
Clone o repositório ou faça o download do código.
Instale as dependências:
bash
Copiar código
pip install flask pandas
Execute a aplicação:
bash
Copiar código
python app.py
Acesse a aplicação no navegador, por padrão, em http://127.0.0.1:5000.
Envie um arquivo .txt através da interface web e aguarde o processamento.
O arquivo resultante será mostrado em uma tabela e também salvo na pasta uploads como um arquivo Excel.
Estrutura de Arquivos
app.py: Código principal da aplicação.
templates/: Contém os arquivos HTML para renderização das páginas.
index.html: Página inicial com o formulário para envio do arquivo.
resultado.html: Página que exibe a tabela com os dados extraídos.
uploads/: Diretório onde os arquivos enviados e processados são salvos.
Exemplo de Formato do Arquivo de Entrada
O arquivo .txt deve conter as informações em formato textual simples, onde a aplicação buscará por padrões específicos. Abaixo estão os padrões de dados que a aplicação tenta capturar:

EVENTO: Códigos 401002 ou 401005
NOTA: Códigos no formato 2024NE\d+
ELEMENTO: Códigos no formato 339\d{5}
VALOR: Valores monetários, como 1.234,56
NOTA SISTEMA: Códigos de 6 dígitos, como 123456
Exemplo de Saída
Após o processamento do arquivo, a aplicação gera uma tabela como a seguinte:

ID	EVENTO	NOTA	ELEMENTO	VALOR	NOTA SISTEMA
1	401002	2024NE12345	33912345	1.234,56	123456
2	401005	2024NE12346	33912346	2.345,67	123456
Os dados também são salvos em um arquivo Excel (linhas_filtradas_com_dados.xlsx).

Considerações Finais
A aplicação oferece uma interface simples e intuitiva para processar arquivos .txt.
O sistema valida os arquivos enviados e assegura que os dados extraídos sejam organizados de forma clara e acessível.
Em caso de erro no processamento ou na validação do arquivo, o usuário recebe mensagens informativas.
Licença
Este projeto está licenciado sob a MIT License.
