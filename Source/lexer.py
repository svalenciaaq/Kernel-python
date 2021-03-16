import threading


class Lexer:
    def checkGrammar(st):
        cad = str(st).split(",")
        if cad[0] == "create" or cad[0] == "delete":
            return_file(cad)
        if cad[0] == "startapp":
            return "starapp"

    def return_file(so):
        return so
