
A = []
print('Введите элементы матрицы A (4 строки по 4 числа):')
for i in range(4):
    строка = list(map(int, input(f'Строка {i+1}: ').split()))
    A.append(строка)
сумма = 0
for i in range(4):
    for j in range(i + 1, 4):
        сумма += A[i][j]
print('Сумма элементов выше главной диагонали:', сумма)
