from Lexer import Lexer
from Parser import Parser
from visualize_ast import visualize_ast

test_process = """
PROCESS {
    TITLE: "Mass Production of Sedan Model X";
    YIELD: 1000;
    TIME: 30 days;
    COMPONENT: 1000 "chassis frames";
    COMPONENT: 2000 "body panels";
    COMPONENT: 1000 "engines";
    COMPONENT: 1000 "transmissions";
    COMPONENT: 1000 "wheel assemblies";
    COMPONENT: 5000 "interior modules";
    COMPONENT: 1000 "painting kits";
    STEP: "Design validation and prototyping";
    STEP: "Procure and inspect raw steel and alloys";
    STEP: "Stamp body panels in press shop";
    STEP: "Weld panels and chassis into body-in-white";
    STEP: "Apply corrosion protection and primer";
    STEP: "Bake in paint oven at 180 C for 45 minutes";
    STEP: "Assemble powertrain (engine, transmission)";
    STEP: "Install powertrain into body-in-white";
    STEP: "Fit interior modules and wiring harnesses";
    STEP: "Mount wheel assemblies and brakes";
    STEP: "Final quality inspection and road-testing";
    STEP: "Logistics packaging and dispatch";
    TEMP: 180 C;
}
"""

Lexer = Lexer()
tokens = Lexer.tokenize(test_process)

print("Tokens:")
for token in tokens:
    print(token)
print()

Parser = Parser(tokens)
process_ast = Parser.parse()

print("Abstract Syntax Tree:")
print(process_ast)
visualize_ast(process_ast)
