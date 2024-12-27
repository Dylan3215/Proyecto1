import re

def analizador_lex(source):
    expresiones = {
        "Modificador de clase": r"static",
        "clase": r"class",
        "Modificador de acceso": r"(private|public|protected)",
        "Simbolo {": r"{",
        "Simbolo }": r"}",
        "Simbolo ,": r",",
        "Fin de sentencia": r";",
        "TipoDato": r"(int|float|String|double|char|boolean|string)",
        "Identificador": r"[a-zA-Z_][a-zA-Z0-9_]*",
    }

    tokens = []

    for linea in source.splitlines():
        linea = linea.strip()
        if not linea:  # Ignore empty lines
            continue

        # Divide la línea en palabras y analiza cada palabra individualmente
        palabras = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*|[{},;]", linea)
        for palabra in palabras:
            coincide = False
            for tipo, expresion in expresiones.items():
                if re.fullmatch(expresion, palabra):
                    coincide = True
                    tokens.append((tipo, palabra))
                    break
            if not coincide:
                print(f"No hay coincidencias para: {palabra}")

    return tokens

class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type  # Node type (e.g., 'ClassDeclaration', 'VariableDeclaration')
        self.value = value  # Node value (e.g., class name, variable name)
        self.children = children or []  # Child nodes

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def parse(self):
        """Parses the tokens and returns the root of the AST."""
        return self.parse_ClassDeclaration()

    def parse_ClassDeclaration(self):
        """Parses a class declaration."""
        if self.current_token()[0] == "Modificador de acceso":
            self.consume_token()
        if self.current_token()[0] == "clase":
            self.consume_token()
            if self.current_token()[0] == "Identificador":
                class_name = self.current_token()[1]
                self.consume_token()
                if self.current_token()[0] == "Simbolo {":
                    self.consume_token()
                    class_body = self.parse_ClassBody()
                    if self.current_token()[0] == "Simbolo }":
                        self.consume_token()
                        return ASTNode("ClassDeclaration", class_name, [class_body])
        raise SyntaxError(f"Error Sintactico: Unexpected token {self.current_token()}")

    def parse_ClassBody(self):
        """Parses the body of a class."""
        body_nodes = []
        while self.current_token()[0] in ("TipoDato", "Modificador de acceso"):
            body_nodes.append(self.parse_VariableDeclaration())
        return ASTNode("ClassBody", children=body_nodes)

    def parse_VariableDeclaration(self):
      """Parses a variable declaration with support for multiple variables."""
      modifier = None
      if self.current_token()[0] == "Modificador de acceso":
          modifier = self.current_token()[1]
          self.consume_token()

      # Parse data type
      if self.current_token()[0] == "TipoDato":
          data_type = self.current_token()[1]
          self.consume_token()
      else:
          raise SyntaxError(f"Error Sintactico: Unexpected token {self.current_token()}, expected data type")

      # Parse variable names (comma-separated)
      variables = []
      while self.current_token()[0] == "Identificador":
          var_name = self.current_token()[1]
          variables.append(var_name)
          self.consume_token()
          if self.current_token()[0] == "Simbolo ,":
              self.consume_token()  # Consume comma and continue parsing
          else:
              break

      # Ensure the declaration ends with a semicolon
      if self.current_token()[0] == "Fin de sentencia":
          self.consume_token()
      else:
          raise SyntaxError(f"Error Sintactico: Unexpected token {self.current_token()}, expected ';'")

      # Create an AST node for each variable
      return ASTNode(
          "VariableDeclaration",
          value={"type": data_type, "variables": variables, "modifier": modifier}
      )

    def current_token(self):
        """Returns the current token."""
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return (None, None)  # End of tokens

    def consume_token(self):
        """Moves to the next token."""
        self.current_token_index += 1

def print_ast(node, level=0):
    """Prints the AST structure with indentation."""
    indent = "  " * level
    print(f"{indent}{node.type}: {node.value}")
    for child in node.children:
        print_ast(child, level + 1)

source_code = """
public class estudiante{
    int cr , t,e,q;
    string nombre;
    int edad;
    float var34h5;
}
"""
tokens = analizador_lex(source_code)
print(tokens)
parser = Parser(tokens)
ast_root = parser.parse()
print_ast(ast_root)