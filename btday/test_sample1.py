# content of test_sample.py
import logging

def func(x):
    return x + 1

def test_answer1():
    logging.info("test_answer1")
    assert func(3) == 4

def test_wrong1():
    logging.info("test_wrong2 check fun(3) == 5")
    assert func(3) == 5

def test_answer11():
    logging.info("test_answer11 check fun(255) == 256")
    assert func(255) == 256
