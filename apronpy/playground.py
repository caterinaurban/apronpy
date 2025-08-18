import faulthandler

from apronpy.abstract1 import PyAbstract1
from apronpy.cdll import libapron
from apronpy.coeff import PyMPQScalarCoeff
from apronpy.environment import PyEnvironment
from apronpy.lincons0 import ConsTyp
from apronpy.lincons1 import PyLincons1, PyLincons1Array
from apronpy.linexpr1 import PyLinexpr1
from apronpy.manager import PyManager, MemBuf
from apronpy.polka import PyPolkaMPQstrictManager, PyPolka, libpolkaMPQ
from apronpy.tcons1 import PyTcons1, PyTcons1Array
from apronpy.texpr0 import TexprOp, TexprRtype, TexprRdir
from apronpy.texpr1 import PyTexpr1
from apronpy.var import PyVar

faulthandler.enable()

# libapron.ap_texpr1_print.argtypes = [POINTER(Texpr1)]
# libapron.ap_texpr1_print(t.texpr1)
# print()

e = PyEnvironment([], [
    PyVar('i1'), PyVar('i2'),
    PyVar('b1'), PyVar('h1'),
    PyVar('h2'), PyVar('b2'),
    PyVar('o1'), PyVar('o2'),
])
# outcome: o1 < o2
x0 = PyLinexpr1(e)
x0.set_coeff(PyVar('o1'), PyMPQScalarCoeff(-1))
x0.set_coeff(PyVar('o2'), PyMPQScalarCoeff(1))
c0 = PyLincons1(ConsTyp.AP_CONS_SUP, x0)
print('c0', c0)
o1 = PyTexpr1.var(e, PyVar('o1'))
o2 = PyTexpr1.var(e, PyVar('o2'))
x0bis = PyTexpr1.binop(TexprOp.AP_TEXPR_SUB, o2, o1, TexprRtype.AP_RTYPE_DOUBLE, TexprRdir.AP_RDIR_RND)
c0bis = PyTcons1.make(x0bis, ConsTyp.AP_CONS_SUP)
print('c0bis', c0bis)

a0 = PyLincons1Array([c0])
m0 = PyPolkaMPQstrictManager()
p0 = PyPolka(m0, e) #.meet(a0)
print('p0', p0)

s = libapron.ap_abstract1_serialize_raw(m0, p0)

man_p = PyManager
pya1 = PyAbstract1
# ap_membuf_t ap_abstract1_serialize_raw(ap_manager_t* man, ap_abstract1_t* a);
libapron.ap_abstract1_serialize_raw.argtypes = [man_p, pya1]
libapron.ap_abstract1_serialize_raw.restype = MemBuf

#p0 = PyPolkaMPQstrictManager(e).meet(a0)
# p0bis = PyPolkaMPQstrictManager(e).meet(a0)
# print('p0/p0bis', p0, p0bis)
# a0bis = PyTcons1Array([c0bis.tcons1])
# p0bisbis = PyPolkaMPQstrictManager(e).meet(a0bis)
# print('p0bisbis', p0bisbis)

# o1 = 4 * h1 -1 * h2 + 4
# o2 = -0.2 * h1 + 0.3 * h2 + 0.4
# h1 = PyTexpr1.var(e, PyVar('h1'))
# h2 = PyTexpr1.var(e, PyVar('h2'))
# w1 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.4))
# w2 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.1))
# b1 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.4))
# c1 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, w1, h1, TexprRtype.AP_RTYPE_DOUBLE, TexprRdir.AP_RDIR_RND)
# c2 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, w2, h2, TexprRtype.AP_RTYPE_DOUBLE, TexprRdir.AP_RDIR_RND)
# x0 = PyTexpr1.binop(TexprOp.AP_TEXPR_SUB, c1, c2, TexprRtype.AP_RTYPE_DOUBLE, TexprRdir.AP_RDIR_RND)
# x2a = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x0, b1, TexprRtype.AP_RTYPE_DOUBLE, TexprRdir.AP_RDIR_RND)
# w3 = PyTexpr1.cst(e, PyMPQScalarCoeff(-0.2))
# w4 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.3))
# b2 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.4))
# c3 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, w3, h1, TexprRtype.AP_RTYPE_DOUBLE, TexprRdir.AP_RDIR_RND)
# c4 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, w4, h2, TexprRtype.AP_RTYPE_DOUBLE, TexprRdir.AP_RDIR_RND)
# x1 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, c3, c4, TexprRtype.AP_RTYPE_DOUBLE, TexprRdir.AP_RDIR_RND)
# x2b = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x1, b2, TexprRtype.AP_RTYPE_DOUBLE, TexprRdir.AP_RDIR_RND)
# p1 = p0.substitute(PyVar('o2'), x2b)
# p2 = p1.substitute(PyVar('o1'), x2a)
# print('x2b', x2b)
# p2bis = p0bis.substitute([PyVar('o1'), PyVar('o2')], [x2a, x2b])
# p1bis = p0bisbis.substitute(PyVar('o2'), x2b)
# print(p1, p2, p2bis, p1bis)

# ALT

#(- 3602879701896397/18014398509481984) · h1 + 5404319552844595/18014398509481984 · h2 + 3602879701896397/9007199254740992

# # e
# e = PyEnvironment([], [
#     PyVar('i1'), PyVar('i2'),
#     PyVar('b1'), PyVar('h1'),
#     PyVar('h2'), PyVar('b2'),
#     PyVar('o1'), PyVar('o2'),
#     # PyVar('i3'), PyVar('i4'),
#     # PyVar('b3'), PyVar('h3'),
#     # PyVar('h4'), PyVar('b4'),
#     # PyVar('o3'), PyVar('o4'),
#     # PyVar('i5'), PyVar('i6'),
#     # PyVar('b5'), PyVar('h5'),
#     # PyVar('h6'), PyVar('b6'),
#     # PyVar('o5'), PyVar('o6'),
#     # PyVar('i7'), PyVar('i8'),
#     # PyVar('b7'), PyVar('h7'),
#     # PyVar('h8'), PyVar('b8'),
#     # PyVar('o7'), PyVar('o8'),
#     # PyVar('i9'), PyVar('i10'),
#     # PyVar('b9'), PyVar('h9'),
#     # PyVar('h10'), PyVar('b10'),
#     # PyVar('o9'), PyVar('o10'),
#     # PyVar('i11'), PyVar('i12'),
#     # PyVar('b11'), PyVar('h11'),
#     # PyVar('h12'), PyVar('b12'),
#     # PyVar('o11'), PyVar('o12')
# ])
# result = PyPolkaMPQstrict.bottom(e)
#
# for i in range(4):
#     for j in range(4):
#
#         # outcome: o1 < o2
#         x0 = PyLinexpr1(e)
#         x0.set_coeff(PyVar('o1'), PyMPFRScalarCoeff(-1))
#         x0.set_coeff(PyVar('o2'), PyMPFRScalarCoeff(1))
#         c0 = PyLincons1(ConsTyp.AP_CONS_SUP, x0)
#         a0 = PyLincons1Array([c0])
#         p0 = PyPolkaMPQstrict(e).meet(a0)
#         p0bis = PyPolkaMPQstrict(e)
#
#         print('Output')
#         print('p0: {}'.format(p0))
#         print('p0bis: {}'.format(p0bis))
#         print('p0 <= p0bis (expected: True): {}'.format(p0 <= p0bis))
#         print('p0bis <= p0 (expected: False): {}'.format(p0bis <= p0))
#         print()
#
#         if i == 0:
#             # relu: assumption 0 <= o1, 0 <= o2
#             x1a = PyLinexpr1(e)
#             x1a.set_coeff(PyVar('o1'), PyMPFRScalarCoeff(1))
#             c1a = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x1a)  # 0 <= o1
#             x1b = PyLinexpr1(e)
#             x1b.set_coeff(PyVar('o2'), PyMPFRScalarCoeff(1))
#             c1b = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x1b)  # 0 <= o2
#             a1 = PyLincons1Array([c1a, c1b])
#             p1 = p0.meet(a1)
#             p1bis = p0bis.meet(a1)
#         elif i == 1:
#             # relu: o2 = 0, assumption 0 <= o1, o2 < 0
#             x1a = PyLinexpr1(e)
#             x1a.set_cst(PyMPFRScalarCoeff(0.0))
#             p1a = p0.substitute(PyVar('o2'), x1a)
#             p1abis = p0bis.substitute(PyVar('o2'), x1a)
#             x1b = PyLinexpr1(e)
#             x1b.set_coeff(PyVar('o1'), PyMPFRScalarCoeff(1))
#             c1b = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x1b)  # 0 <= o1
#             x1c = PyLinexpr1(e)
#             x1c.set_coeff(PyVar('o2'), PyMPFRScalarCoeff(-1))
#             c1c = PyLincons1(ConsTyp.AP_CONS_SUP, x1c)  # o2 < 0
#             a1 = PyLincons1Array([c1b, c1c])
#             p1 = p1a.meet(a1)
#             p1bis = p1abis.meet(a1)
#         elif i == 2:
#             # relu: o1 = 0, assumption o1 < 0, 0 <= o2
#             x1a = PyLinexpr1(e)
#             x1a.set_cst(PyMPFRScalarCoeff(0.0))
#             p1a = p0.substitute(PyVar('o1'), x1a)
#             p1abis = p0bis.substitute(PyVar('o1'), x1a)
#             x1b = PyLinexpr1(e)
#             x1b.set_coeff(PyVar('o1'), PyMPFRScalarCoeff(-1))
#             c1b = PyLincons1(ConsTyp.AP_CONS_SUP, x1b)  # o1 < 0
#             x1c = PyLinexpr1(e)
#             x1c.set_coeff(PyVar('o2'), PyMPFRScalarCoeff(1))
#             c1c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x1c)  # 0 <= o2
#             a1 = PyLincons1Array([c1b, c1c])
#             p1 = p1a.meet(a1)
#             p1bis = p1abis.meet(a1)
#         else:
#             # relu: o1 = 0, o2 = 0, assumption o1 < 0, o2 < 0
#             x1a = PyLinexpr1(e)
#             x1a.set_cst(PyMPFRScalarCoeff(0.0))
#             p1a = p0.substitute(PyVar('o1'), x1a)
#             p1abis = p0bis.substitute(PyVar('o1'), x1a)
#             x1b = PyLinexpr1(e)
#             x1b.set_cst(PyMPFRScalarCoeff(0.0))
#             p1b = p1a.substitute(PyVar('o2'), x1b)
#             p1bbis = p1abis.substitute(PyVar('o1'), x1b)
#             x1c = PyLinexpr1(e)
#             x1c.set_coeff(PyVar('o1'), PyMPFRScalarCoeff(-1))
#             c1c = PyLincons1(ConsTyp.AP_CONS_SUP, x1c)  # o1 < 0
#             x1d = PyLinexpr1(e)
#             x1d.set_coeff(PyVar('o2'), PyMPFRScalarCoeff(-1))
#             c1d = PyLincons1(ConsTyp.AP_CONS_SUP, x1d)  # o2 < 0
#             a1 = PyLincons1Array([c1c, c1d])
#             p1 = p1b.meet(a1)
#             p1bis = p1bbis.meet(a1)
#
#         print('ReLU(o1, o2) {}:{}'.format(i, j))
#         print('p1: {}'.format(p1))
#         print('p1bis: {}'.format(p1bis))
#         print('p1 <= p1bis (expected: True): {}'.format(p1 <= p1bis))
#         print('p1bis <= p1 (expected: False): {}'.format(p1bis <= p1))
#         print()
#
#         # o1 = -0.7566400101700294 * h1 -0.7521230014426193 * h2 + 0.6
#         # o2 = 66145339249.11405 * h1 + 68702343992.50064 * h2 + 0.6
#         x2a = PyLinexpr1(e)
#         x2a.set_coeff(PyVar('h1'), PyMPFRScalarCoeff(4))
#         x2a.set_coeff(PyVar('h2'), PyMPFRScalarCoeff(-1))
#         x2a.set_cst(PyMPFRScalarCoeff(4))
#         x2b = PyLinexpr1(e)
#         x2b.set_coeff(PyVar('h1'), PyMPFRScalarCoeff(-2))
#         x2b.set_coeff(PyVar('h2'), PyMPFRScalarCoeff(3))
#         x2b.set_cst(PyMPFRScalarCoeff(4))
#         p2a = p1.substitute(PyVar('o1'), x2a)
#         p2b = p2a.substitute(PyVar('o2'), x2b)
#         p2abis = p1bis.substitute(PyVar('o1'), x2a)
#         p2bbis = p2abis.substitute(PyVar('o2'), x2b)
#
#         print('Layer(o1,o2) {}:{}'.format(i, j))
#         print('p2b: {}'.format(p2b))
#         print('p2bis: {}'.format(p2bbis))
#         print('p2b <= p2bbis (expected: True): {}'.format(p2b <= p2bbis))
#         print('p2bis <= p2b (expected: False): {}'.format(p2bbis <= p2b))
#         print()
#
#         if j == 0:
#             # relu: assumption 0 <= h1, 0 <= h2
#             x3a = PyLinexpr1(e)
#             x3a.set_coeff(PyVar('h1'), PyMPFRScalarCoeff(1))
#             c3a = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x3a)  # 0 <= h1
#             x3b = PyLinexpr1(e)
#             x3b.set_coeff(PyVar('h2'), PyMPFRScalarCoeff(1))
#             c3b = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x3b)  # 0 <= h2
#             a3 = PyLincons1Array([c3a, c3b])
#             p3 = p2b.meet(a3)
#             p3bis = p2bbis.meet(a3)
#         elif j == 1:
#             # relu: h2 = 0, assumption 0 <= h1, h2 < 0
#             x3a = PyLinexpr1(e)
#             x3a.set_cst(PyMPFRScalarCoeff(0.0))
#             p3a = p2b.substitute(PyVar('h2'), x3a)
#             p3abis = p2bbis.substitute(PyVar('h2'), x3a)
#             x3b = PyLinexpr1(e)
#             x3b.set_coeff(PyVar('h1'), PyMPFRScalarCoeff(1))
#             c3b = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x3b)  # 0 <= h1
#             x3c = PyLinexpr1(e)
#             x3c.set_coeff(PyVar('h2'), PyMPFRScalarCoeff(-1))
#             c3c = PyLincons1(ConsTyp.AP_CONS_SUP, x3c)  # h2 < 0
#             a3 = PyLincons1Array([c3b, c3c])
#             p3 = p3a.meet(a3)
#             p3bis = p3abis.meet(a3)
#         elif j == 2:
#             # relu: h1 = 0, assumption h1 < 0, 0 <= h2
#             x3a = PyLinexpr1(e)
#             x3a.set_cst(PyMPFRScalarCoeff(0.0))
#             p3a = p2b.substitute(PyVar('h1'), x3a)
#             p3abis = p2bbis.substitute(PyVar('h1'), x3a)
#             x3b = PyLinexpr1(e)
#             x3b.set_coeff(PyVar('h1'), PyMPFRScalarCoeff(-1))
#             c3b = PyLincons1(ConsTyp.AP_CONS_SUP, x3b)  # h1 < 0
#             x3c = PyLinexpr1(e)
#             x3c.set_coeff(PyVar('h2'), PyMPFRScalarCoeff(1))
#             c3c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x3c)  # 0 <= h2
#             a3 = PyLincons1Array([c3b, c3c])
#             p3 = p3a.meet(a3)
#             p3bis = p3abis.meet(a3)
#         else:
#             # relu: h1 = 0, h2 = 0, assumption h1 < 0, h2 < 0
#             x3a = PyLinexpr1(e)
#             x3a.set_cst(PyMPFRScalarCoeff(0.0))
#             p3a = p2b.substitute(PyVar('h1'), x3a)
#             p3abis = p2bbis.substitute(PyVar('h1'), x3a)
#             x3b = PyLinexpr1(e)
#             x3b.set_cst(PyMPFRScalarCoeff(0.0))
#             p3b = p3a.substitute(PyVar('h2'), x3b)
#             p3bbis = p3abis.substitute(PyVar('h1'), x3b)
#             x3c = PyLinexpr1(e)
#             x3c.set_coeff(PyVar('h1'), PyMPFRScalarCoeff(-1))
#             c3c = PyLincons1(ConsTyp.AP_CONS_SUP, x3c)  # h1 < 0
#             x3d = PyLinexpr1(e)
#             x3d.set_coeff(PyVar('h2'), PyMPFRScalarCoeff(-1))
#             c3d = PyLincons1(ConsTyp.AP_CONS_SUP, x3d)  # h2 < 0
#             a3 = PyLincons1Array([c3c, c3d])
#             p3 = p3b.meet(a3)
#             p3bis = p3bbis.meet(a3)
#
#         print('ReLU(h1,h2) {}:{}'.format(i, j))
#         print('p3: {}'.format(p3))
#         print('p3bis: {}'.format(p3bis))
#         print('p3 <= p3bis (expected: True): {}'.format(p3 <= p3bis))
#         print('p3is <= p3 (expected: False): {}'.format(p3bis <= p3))
#         print()
#
#         # h1 = -3563343016573.1133 * i1 + -7126686033146.326 * i2 + 0.35
#         # h2 = -4042063042100.3296 * i1 + -8084126084200.859 * i2 + 0.35
#         x4a = PyLinexpr1(e)
#         x4a.set_coeff(PyVar('i1'), PyMPFRScalarCoeff(1))
#         x4a.set_coeff(PyVar('i2'), PyMPFRScalarCoeff(-1))
#         x4a.set_cst(PyMPFRScalarCoeff(1))
#         x4b = PyLinexpr1(e)
#         x4b.set_coeff(PyVar('i1'), PyMPFRScalarCoeff(-1))
#         x4b.set_coeff(PyVar('i2'), PyMPFRScalarCoeff(2))
#         x4b.set_cst(PyMPFRScalarCoeff(1))
#         p4a = p3.substitute(PyVar('h1'), x4a)
#         p4b = p4a.substitute(PyVar('h2'), x4b)
#         p4abis = p3bis.substitute(PyVar('h1'), x4a)
#         p4bbis = p4abis.substitute(PyVar('h2'), x4b)
#
#         print('Layer(h1,h2) {}:{}'.format(i, j))
#         print('p4b: {}'.format(p4b))
#         print('p4bis: {}'.format(p4bbis))
#         print('p4b <= p4bbis (expected: True): {}'.format(p4b <= p4bbis))
#         print('p4bbis <= p4b (expected: False): {}'.format(p4bbis <= p4b))
#         print()
#
#         # 0 <= i1 <= 1, 0 <= i2 <= 1
#         x5a = PyLinexpr1(e)
#         # x5a.set_coeff(PyVar('i1'), PyMPFRScalarCoeff(1))
#         c5a = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x5a)  # i1 >= 0
#         x5b = PyLinexpr1(e)
#         # x5b.set_coeff(PyVar('i1'), PyMPFRScalarCoeff(-1))
#         # x5b.set_cst(PyMPFRScalarCoeff(1))
#         c5b = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x5b)  # -i1 + 1 >= 0
#         x5c = PyLinexpr1(e)
#         x5c.set_coeff(PyVar('i2'), PyMPFRScalarCoeff(1))
#         c5c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x5c)  # i2 >= 0
#         x5d = PyLinexpr1(e)
#         x5d.set_coeff(PyVar('i2'), PyMPFRScalarCoeff(-1))
#         x5d.set_cst(PyMPFRScalarCoeff(1))
#         c5d = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x5d)  # -i2 + 1 >= 0
#         a5 = PyLincons1Array([c5a, c5b, c5c, c5d])
#         p5 = p4b.meet(a5)
#         p5bis = p4bbis.meet(a5)
#
#         print('Input {}:{}'.format(i, j))
#         print('p5: {}'.format(p5))
#         print('p5is: {}'.format(p5bis))
#         print('p5 <= p5bis (expected: True): {}'.format(p5 <= p5bis))
#         print('p5bis <= p5b (expected: False): {}'.format(p5bis <= p5))
#         print()
#         print()
#
#         result = result.join(p5)
#
# print('Result: {}'.format(result))
# print()

print("Done")
