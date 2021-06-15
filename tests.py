import unittest
from utils import *
from models import *
from constants import *
from game import *

class TestUtils(unittest.TestCase):
    def test_score(self):
        obj = score(["John", "Derek"])
        self.assertEqual(obj,None)

    def test_convert_input_to_code_values(self):
        ret = convert_input_to_code_values("Derek")
        self.assertEqual(ret, ['D', 'e', 'r', 'e', 'k'])

    def test_get_peg_by_value(self):
        self.assertEqual(Peg.get_peg_by_value("R"), Peg.RED)

    def test_generate_random_peg(self):
        self.assertIs(type(Peg.generate_random_peg()), Peg)

    def test_Code_parse(self):
        ls = [Peg.RED, Peg.YELLOW, Peg.BLACK, Peg.GREEN,Peg.BLUE]
        self.assertEqual(Code.parse("RYBGL",MASTERMIND_GAMERULE).get_pegs(), ls)
    
    def test_make_a_guess(self):
        breaker = CodeBreaker("Test")
        result = breaker.make_a_guess(Code.parse("RYBGL",MASTERMIND_GAMERULE),Code.parse("RLBGY",MASTERMIND_GAMERULE))
        self.assertTrue((result.__str__()) == 'B W B B W')

    def test_make_new_final_code(self):
        comp = ComputerCodeMaker()
        self.assertIs(type(comp.make_new_final_code(MASTERMIND_GAMERULE)), Code)
        
unittest.main()
