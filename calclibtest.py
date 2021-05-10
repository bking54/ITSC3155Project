import pytest
import calclib as cl

def test_decompose1():
    decompose_input = 'x+4'
    list = ['x+4']
    test = cl.decompose(decompose_input)
    assert test == list

def test_decompose2():
    decompose_input = '(x+4)+2'
    list = [['x+4'], '+2']
    test = cl.decompose(decompose_input)
    assert test == list

def test_decompose3():
    decompose_input = '(x+4)(x+5)+2'
    list = [['x+4'], ['x+5'], '+2']
    test = cl.decompose(decompose_input)
    assert test == list

def test_decompose4():
    decompose_input = '2((x/2)^3)+x'
    list = ['2', [['x/2'], '^3'], '+x']
    test = cl.decompose(decompose_input)
    assert test == list

def test_decompose5():
    decompose_input = '-2x(x-3(x-1)^2)-49'
    list = ['-2x', ['x-3', ['x-1'], '^2'], '-49']
    test = cl.decompose(decompose_input)
    assert test == list

def test_format1():
    format_input = ['x+4']
    list = ['x', '+', '4']
    test = cl.format(format_input)
    assert test == list

def test_format2():
    format_input = [['x+4'], '+200']
    list = [['x', '+', '4'], '+', '200']
    test = cl.format(format_input)
    assert test == list

def test_format3():
    format_input = ['-x+4']
    list = ['0', '-', 'x', '+', '4']
    test = cl.format(format_input)
    assert test == list

def test_format4():
    format_input = ['2x+40']
    list = ['2', '*', 'x', '+', '40']
    test = cl.format(format_input)
    assert test == list

def test_format4():
    format_input = ['-2x+40']
    list = ['0', '-', '2', '*', 'x', '+', '40']
    test = cl.format(format_input)
    assert test == list

def test_eval1():
    xval = 2
    eval_input = ['x', '+', '4']
    test = cl.eval(eval_input, xval)
    assert xval + 4 == test

def test_eval2():
    xval = 2
    eval_input = ['2', '*', ['x', '-', '4'], '+', '10']
    test = cl.eval(eval_input, xval)
    assert 2 * (xval - 4) + 10  == test

def test_eval3():
    xval = 2
    eval_input = ['x', '^', 'x']
    test = cl.eval(eval_input, xval)
    assert xval ** xval == test

def test_eval4():
    xval = 2
    eval_input = ['x', '/', '4']
    test = cl.eval(eval_input, xval)
    assert xval / 4 == test

def test_gettype1():
    test_val = '1'
    test = cl.getType(test_val)
    assert test == 0

def test_gettype2():
    test_val = '+'
    test = cl.getType(test_val)
    assert test == 1

def test_gettype3():
    test_val = 'x'
    test = cl.getType(test_val)
    assert test == 2

def test_gettype4():
    test_val = 'g'
    test = cl.getType(test_val)
    assert test == -1

def test_parseelement1():
    element = '1'
    test = cl.parseElement(element, 0)
    assert test == 1

def test_parseelement2():
    element = '0.5'
    test = cl.parseElement(element, 0)
    assert type(test) == type(0.5)

def test_parseelement3():
    element = 1
    test = cl.parseElement(element, 0)
    assert test == 1

def test_parseelement4():
    element = ['x', '+', '4']
    test = cl.parseElement(element, 0)
    assert test == 4

def test_evalrange1():
    element = ['x', '^', '2']
    check = [[-5, 25], [-4, 16], [-3, 9], [-2, 4], [-1, 1], [0,0], [1, 1], [2, 4], [3, 9], [4, 16], [5, 25]]
    test = cl.evalRange(element, -5, 6, 1)
    assert test == check

def test_evalrange2():
    element = ['x', '^', '3']
    check = [[-5, -125], [-4, -64], [-3, -27], [-2, -8], [-1, -1], [0,0], [1, 1], [2, 8], [3, 27], [4, 64], [5, 125]]
    test = cl.evalRange(element, -5, 6, 1)
    assert test == check

def test_limit1():
    element = ['x', '^', '2']
    test = cl.limit(element, 0, 10)
    assert test[0] <= 0.00000001 and test[0] >= -0.00000001