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