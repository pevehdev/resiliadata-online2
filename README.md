#1 - Instalar primeiro o flask via pip:

	pip install Flask

#2 - Depois criar pasta do ambiente virtual:

	python -m venv myvenv

#3 - ir até o caminho:

	cd myvenv/scripts/activate.bat

#4 - Caso deê algum erro ao executar o activate, você deve configurar a politica de segurança do powershell no CMD como administrador:

	Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

#5 - Reinicia sua aplicação do visual studio code e faça o processo #3 novamente.



#6 - Instalar o psycopg2 para utilizar o postgres dentro do python:

	pip install psycopg2