# Semana-da-Fisica

Sobre o compilador Python 3.6+ necessário para execução dos programas:
----

No Windows é possível executar o python direto no powershell ou com auxílio de programas como o Visual Studio Code (https://code.visualstudio.com/docs/setup/windows).

Nos sistemas Linux é mais fácil de usar o python, pois nas versões mais recentes de Ubuntu o compilador de python já vem pré instalado no sistema operacional, e podemos checar sua versão com o comando:
---

$ python --version

Caso não tenha o python no seu Linux, é simples de instalar com os comandos seguintes:

$ sudo apt update

$ sudo apt install build-essential

$ sudo apt install python3.8

Caso tenha problema, existe vários tutoriais na internet como:

https://phoenixnap.com/kb/how-to-install-python-3-ubuntu#:~:text=How%20to%20Install%20Python%203%20on%20Ubuntu%2018.04,Code%20%28Latest%20Version%29%20Step%201%3A%20Update%20Local%20Repositories

https://blog.eldernode.com/install-python-3-ubuntu-20/

------------------------------------------------------------------------------------------

Para instalar o matplotlib veja o site:
https://pypi.org/project/matplotlib/
---

Para gerar o Ex1.jpeg basta manter os arquivos metodos_SF.py e plot_simples.py na mesma pasta e executar no terminal:
  $ python3 plot_simples.py RadGyr.dat Exemplo_1
ou no windows
  $ python.exe .\plot_simples.py RadGyr.dat Exemplo_1
