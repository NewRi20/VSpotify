from pyfiglet import Figlet
from termcolor import colored

figlet = Figlet(font='slant')
text_ = text_color = colored(figlet.renderText("Hello World"), 'cyan')
print(text_)