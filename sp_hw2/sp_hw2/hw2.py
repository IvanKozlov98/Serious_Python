from sp_hw1.hw1 import task2_3


ARTIFACTS_DIR = "sp_hw2/artifacts/"

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


def get_artifacts_name(filename):
    return ARTIFACTS_DIR + filename


def generate_latex_image(filename):
    return "\\includegraphics[scale=0.8]{" + filename + "} "


def generate_tex_string():
    def generate_header():
        return "\\documentclass{article}\n\\usepackage{graphicx} % Required for inserting images\n\\title{Example_python}\n\\author{ivan.kozzloff98 }\n\\date{March 2023}\n\\begin{document}\n\\section{Homework 2}\n"
    
    def generate_footer():
        return "\\end{document}"

    ast_filename = get_artifacts_name("ast_tree.png")
    # generate ast tree
    task2_3(ast_filename)

    return "".join([
        generate_header(), 
        generate_latex_table([[1, 2], [4, 5], [7, 8]]),
        "\\newline \n",
        generate_latex_image(ast_filename),
        "\\newline \n",
        generate_footer()])


def generate_tex_file(filename):
    with open(get_artifacts_name(filename), 'w') as f:
        tex_string = generate_tex_string()
        f.write(tex_string)


if __name__ == '__main__':
    generate_tex_file("result_tex_file.tex")

