import logging

# content of test_sample.py
def func(x):
    return x + 1

def test_answer2():
    logging.info("test_answer2")
    assert func(3) == 4

def test_wrong2():
    logging.info("test_wrong2 check fun(3) == 6")
    assert func(3) == 6

def test_answer22():
    logging.info("test_answer22 check fun(1255) == 1256")
    assert func(1255) == 1256
