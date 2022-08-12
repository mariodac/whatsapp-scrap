: Desenvolvido: Mario Cabral
: Atualizado:    08/08/2022
: Executa script para print automatizado no whatsapp
@echo off
: Verifica se ambiente existe e executa script, senão existir cria ambiente e executa script
IF EXIST "%CD%\env" (
	echo executando script
	"%CD%\env\Scripts\python" project/scraper_wa.py
) ELSE (
	echo criando ambiente
	py -3 -m venv ./env
	echo instalando requisitos
	"%CD%\env\Scripts\pip" install -r ./requirements.txt
	"%CD%\env\Scripts\python" project/scraper_wa.py
)
