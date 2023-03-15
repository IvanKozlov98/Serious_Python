
def generate_latex_table(data):
    """
    Generate a LaTeX table from a two-dimensional list of data.

    Args:
        data (list[list]): A two-dimensional list of data.

    Returns:
        str: A string containing the LaTeX code for the table.
    """

    def generate_header():
        # Generate the LaTeX table header
        return "\\begin{tabular}{" + " | ".join(["c"] * len(data[0])) + "}\n" + "\\hline\n"

    def generate_body():
        return "\\hline\n".join([(" & ".join([str(cell) for cell in row]) 
                                  + " \\\\\n") for row in data])
    
    def generate_footer():
    # Generate the LaTeX table footer
        return "\\hline\n\\end{tabular}\n"

    return "".join([generate_header(), generate_body(), generate_footer()])



if __name__ == '__main__':
    data = [[1, 2], [4, 5], [7, 8]]
    latex_table = generate_latex_table(data)
    print(latex_table)