from ASTVisualizer import ASTVisualizer


def visualize_ast(ast):
    visualizer = ASTVisualizer()
    dot = visualizer.visualize(ast)

    try:
        dot.render('DSL_Laboratory_works/lab6/Report/process_ast', format='png', cleanup=True)
        print("AST visualization saved as 'src/process_ast.png'")
    except Exception as e:
        print(f"Could not render graph: {e}")
        print("To use visualization, install graphviz: pip install graphviz")
        print("And ensure the Graphviz binaries are in your PATH")