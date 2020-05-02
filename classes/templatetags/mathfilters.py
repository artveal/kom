from django import template
import random, math

register = template.Library()

@register.filter(name='mult')
def mult(value, arg):
    "Multiplies the arg and the value"
    return int(value * arg)

@register.filter(name='sub')
def sub(value, arg):
    "Subtracts the arg from the value"
    return int(value) - int(arg)

@register.filter(name='sum')
def sum(value, arg):
    "Subtracts the arg from the value"
    return int(value) + int(arg)

@register.filter(name='sumstr')
def sumstr(value, arg):
    "Subtracts the arg from the value"
    return value + arg

@register.filter(name='div')
def div(value, arg):
    "Divides the value by the arg"
    return str(round(float(value) / float(arg), 2))

@register.filter(name='times')
def times(value, arg=0):
    "Divides the value by the arg"
    return range(arg, value+arg)

@register.simple_tag
def rand(start=0, end=1):
    return int(int(start) + random.random() * (int(end)-int(start)))