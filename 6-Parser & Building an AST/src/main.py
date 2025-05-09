
"""
Process Description Language Parser

This is the main entry point for the parser application.
"""
import sys
import os
from lexer import Lexer
from parser import Parser
from visualize import visualize_ast

def process_file(file_path):
    """
    Process a file containing process description language code
    
    Args:
        file_path: Path to the file to process
        
    Returns:
        The AST root node
    """
    # Read the file
    try:
        with open(file_path, 'r') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None
    
    return process_text(text, file_path)

def process_text(text, source_name="<input>"):
    """
    Process text containing process description language code
    
    Args:
        text: The text to process
        source_name: Name of the source (for error messages)
        
    Returns:
        The AST root node
    """
    print(f"Processing {source_name}...")
    
    # Tokenize the input
    try:
        lexer = Lexer()
        tokens = lexer.tokenize(text)
        print(f"Lexical analysis complete: {len(tokens)} tokens found")
    except Exception as e:
        print(f"Lexical error: {e}")
        return None
    
    # Parse the tokens
    try:
        parser = Parser(tokens)
        ast = parser.parse()
        print("Parsing complete")
        return ast
    except Exception as e:
        print(f"Parse error: {e}")
        return None

def main():
    """Main entry point"""
    # Check if a file was provided
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        ast = process_file(file_path)
    else:
        # Sample input if no file provided
        sample = """
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
        print("No input file provided. Using sample input:")
        print("-" * 40)
        print(sample)
        print("-" * 40)
        ast = process_text(sample, "sample input")
    
    # Print the AST and visualize if possible
    if ast:
        print("\nAST structure:")
        print(ast)
        
        # Try to visualize the AST
        output_file = "process_ast"
        if len(sys.argv) > 1:
            # Use the input filename as base for the output
            base = os.path.basename(sys.argv[1])
            output_file = os.path.splitext(base)[0] + "_ast"
        
        visualize_ast(ast, output_file)

if __name__ == "__main__":
    main()
