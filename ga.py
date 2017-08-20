# -*- coding: utf-8 -*-
# Find a solution of a two-variable function using a genetic algorithm.

import numpy as np
import random
import copy
import matplotlib.pyplot as pl

x1 = []            # present generation's lists
x2 = []
next_x1 = []       # next generation's lists
next_x2 = []
y = []             # f(x) list
compatible = []    # compatible's list


def numget():
  if len(next_x1) == 0:
    return 7
  else:
    return len(next_x1)

def randnum():
  return random.randint(0,255),random.randint(0,255)

# Init
def syokichi(n):
  for i in range(n):
    a1,a2 = randnum()
    x1.append(a1)
    x2.append(a2)

def dainyuu(n):
  for i in range(n):
    num1 = x1[i]
    num2 = x2[i]
    y.append((num1**2)+(4*(num2**2)))

# Find compatibles
def comparison(n):
  sqy = []
  sum = 0
  for i in range(n):
    sqy.append(y[i]**2)
    sum += sqy[i]

  for i in range(n):
    compatible.append(round(100*(float(max(sqy)-sqy[i])/sum),5))
  
  del sqy[:]

# Leave excellent on the next generation
def elitecopy():
  per = copy.copy(compatible)
  per.sort()
  per.reverse()
  flag1 = 0
  flag2 = 0
  flag3 = 0
  flag4 = 0
  flag5 = 0
  for i, com in enumerate(compatible):
    if com == per[0] and flag1 == 0:
      next_x1.append(x1[i])
      next_x2.append(x2[i])
      flag1 = 1
    if com == per[1] and flag2 == 0:
      next_x1.append(x1[i])
      next_x2.append(x2[i])
      flag2 = 1
    if com == per[2] and flag3 == 0:
      next_x1.append(x1[i])      
      next_x2.append(x2[i])
      flag3 = 1
    if com == per[3] and flag4 == 0:
      next_x1.append(x1[i])
      next_x2.append(x2[i])
      flag4 = 1
    if com == per[4] and flag5 == 0:
      next_x1.append(x1[i])
      next_x2.append(x2[i])
      flag5 = 1

# Crossover
def crossover():
  i = 0
  max_x = [max(x1),max(x2)]
  cross = []
  while ((2**i)-1) < max(max_x):
    cross.append((2**i)-1)
    i += 1
  point = random.choice(cross)
  
  # choise
  father1 = random.choice(x1)
  mother1 = random.choice(x1)
  father2 = random.choice(x2)
  mother2 = random.choice(x2)
  
  # crossover (Logical AND)
  tmpf1 = point & father1
  tmpm1 = (((2**i)-1) - point) & mother1
  tmpf2 = point & father2
  tmpm2 = (((2**i)-1) - point) & mother2

  next_x1.append(tmpf1 | tmpm2)
  next_x2.append(tmpf2 | tmpm1)
  
# Mutation
def mutation():
  x1_maxbit = 2 ** (len(bin(max(x1)))-2) - 1
  x2_maxbit = 2 ** (len(bin(max(x2)))-2) - 1
  
  # choise
  dna1 = random.choice(x1)
  dna2 = random.choice(x2)

  # mutation (Logical XOR)
  next_x1.append(x1_maxbit ^ dna1) 
  next_x2.append(x2_maxbit ^ dna2)


num = numget()
syokichi(num)
for i in range(len(x1)):
  compatible.append(0.0)

cnt = 1
while max(compatible) < 100:
  num = numget()
  del compatible[:]
  if len(next_x1) != 0:
    del x1[:]
    del x2[:] 
    x1 = copy.copy(next_x1)
    x2 = copy.copy(next_x2)
    del next_x1[:]
    del next_x2[:]
    del y[:]
    
  dainyuu(num)
  print ('************************ 第{}世代 *************************'.format(cnt))
  print ('    x1 = {}'.format(x1))
  print ('    x2 = {}'.format(x2))
  print ('    y  = {}'.format(y))
  pl.plot(cnt,min(y),"r.")
  comparison(num)
  print ('適合率 = {}'.format(compatible))
  print ('最小値 = {}'.format(min(y)))
  elitecopy()
  crossover()
  mutation()
  cnt += 1

pl.title(u"Minimum value of $ y = x_1^2+4x_2^2 $")
pl.ylabel(u"最小値")
pl.xlabel(u"世代数")
pl.show()
