# whatsapp-scrap
Scrapping whatsapp web
Realiza a abertura de whatsapp web e realiza prints de conversas
## Modo de usar:

Há 3 modos que é realizado o print:
<a id="ancora2"></a>
- Pesquisa por nome: **FUNÇÃO** (*locate_chat_ignore_case*, *locate_all_chat_by_name*)
- Chats do dia: **FUNÇÃO** (*locate_chat_today*)
- Todos os chats: **FUNÇÃO** (*locate_all_chat_by_name*)

Dentro do arquivo [test.py](project/test.py), chame a [**FUNÇÃO**](#ancora2) desejada e execute o arquivo.

**Compatível com Windows, Linux**

Foi criado o arquivo *Batch* [start.bat](start.bat) para realizar a verificação e execução do projeto em sistemas Windows

### Requisitos
Python 3.10 ou superior

É recomendado a criação de ambiente virtual para execução do projeto:


No linux:
<a id="ancora1"></a>
- Para criação do ambiente:
```
python3 -m venv env
```
- Para ativar o ambiente:
```
. env/bin/activate
```
No windows:
- Para criação do ambiente:
```
py -3 -m venv env
```
- Para ativar o ambiente:
```
env\Scripts\activate
```
Todos as bibliotecas e suas versões estão no arquivo [requisitos](requirements.txt)

Para instalar as bibliotecas siga os passos:

**ATENÇÃO [Ative](#ancora1) o seu ambiente antes executar esses comandos!**

*Será criado o ambiente python*


No Linux:
```
env/bin/pip install -r requirements.txt
```
Ou execute o [Script Shell](requirements.sh)

No windows:
```
env\Scripts\pip install -r requirements.txt
```


