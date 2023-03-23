import unittest
from sp_hw2.hw2 import generate_latex_table


class TestGeneratLatexTable(unittest.TestCase):

    def test_generate_latex_table(self):
        self.assertEqual(generate_latex_table([[1, 2], [4, 5], [7, 8]]), '\\begin{tabular}{c | c}\n\\hline\n1 & 2 \\\\\n\\hline\n4 & 5 \\\\\n\\hline\n7 & 8 \\\\\n\\hline\n\\end{tabular}\n')

if __name__ == '__main__':
    unittest.main()
