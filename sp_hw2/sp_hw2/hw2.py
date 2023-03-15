
def generate_latex_table(data):
    """
    Generate a LaTeX table from a two-dimensional list of data.

    Args:
        data (list[list]): A two-dimensional list of data.

    Returns:
        str: A string containing the LaTeX code for the table.
    """
    # Determine the number of columns in the table
    num_cols = len(data[0])

    # Generate the LaTeX table header
    table_header = "\\begin{tabular}{" + " | ".join(["c"] * num_cols) + "}\n"

    # Generate the LaTeX table body
    table_body = ""
    for row in data:
        table_body += "\\hline\n"
        table_body += " & ".join([str(cell) for cell in row]) + " \\\\\n"
    
    # Generate the LaTeX table footer
    table_footer = "\\hline\n\\end{tabular}\n"

    # Combine the table components into a single LaTeX table string
    latex_table = table_header + table_body + table_footer

    return latex_table



if __name__ == '__main__':
    data = [[1, 2], [4, 5], [7, 8]]
    latex_table = generate_latex_table(data)
    print(latex_table)