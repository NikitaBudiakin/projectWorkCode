import numpy as np
from sympy import *
import matplotlib.pyplot as plt
import tkinter as tk
import datetime

# Ініціалізація змінних
H = None  # Товщина пластини на першій ділянці
h = None  # Товщина пластини на другій ділянці
b = None  # Довжина першої ділянки
c = None  # Загальна довжина
q = None  # Нормальний тиск
Q = None  # Розподілене зусилля
E = None  # Модуль пружності
v = None  # Коефіцієнт Пуассона


# calculate() - основна функція програми, у якій викорнуються усі розрахунки
def calculate():
    # Відкриття та подальший запис даних у лог-файл
    log_file = open('log.txt', 'w', encoding='utf-8')
    log_file.write("____________________________\n\n" + str(datetime.datetime.now()) +
                   "\n____________________________")

    global H, h, b, c, q, Q, E, v
    wrongValue = False

    label_output.configure(text="")
    entry_H.configure(state='normal')
    entry_h.configure(state='normal')
    entry_b.configure(state='normal')
    entry_c.configure(state='normal')
    entry_q.configure(state='normal')
    entry_Q.configure(state='normal')
    entry_E.configure(state='normal')
    entry_v.configure(state='normal')
    clearButton.configure(state='normal')

    entry_H.configure(bg='#FFFFFF')
    entry_h.configure(bg='#FFFFFF')
    entry_b.configure(bg='#FFFFFF')
    entry_c.configure(bg='#FFFFFF')
    entry_q.configure(bg='#FFFFFF')
    entry_Q.configure(bg='#FFFFFF')
    entry_E.configure(bg='#FFFFFF')
    entry_v.configure(bg='#FFFFFF')

    # Зчитування та перевірка введених даних
    try:
        H = float(str(entry_H.get()))
        if H <= 0:
            label_output.configure(text="Невірне значення! Товщина не може бути\nменше або дорівнювати нулю",
                                   font=("Cambria", 12), justify="left", anchor='sw', fg='#FF0000')
            entry_H.configure(bg='#FF0000')
            wrongValue = True

        h = float(str(entry_h.get()))
        if h <= 0:
            label_output.configure(text="Невірне значення! Товщина не може бути\nменше або дорівнювати нулю",
                                   font=("Cambria", 12), justify="left", anchor='sw', fg='#FF0000')
            entry_h.configure(bg='#FF0000')
            wrongValue = True

        b = float(str(entry_b.get()))
        if b <= 0:
            label_output.configure(text="Невірне значення! Довжина ділянки не може бути\nменше або дорівнювати нулю",
                                   font=("Cambria", 12), justify="left", anchor='sw', fg='#FF0000')
            entry_b.configure(bg='#FF0000')
            wrongValue = True

        c = float(str(entry_c.get()))
        if c <= b:
            label_output.configure(text="Невірне значення! Довжина ділянки не b може\nбути менше або дорівнювати "
                                        "довжині ділянки c",
                                   font=("Cambria", 12), justify="left", anchor='sw', fg='#FF0000')
            entry_c.configure(bg='#FF0000')
            wrongValue = True

        q = float(str(entry_q.get()))
        Q = float(str(entry_Q.get()))

        E = float(str(entry_E.get())) * (10 ** 11)
        if E <= 0:
            label_output.configure(text="Невірне значення! Модуль пружності не може бути\nменше або дорівнювати нулю",
                                   font=("Cambria", 12), justify="left", anchor='sw', fg='#FF0000')
            entry_E.configure(bg='#FF0000')
            wrongValue = True

        v = float(str(entry_v.get()))
        if v < 0 or v > 0.5:
            label_output.configure(text="Невірне значення! Коефіцієнт Пуассона\n"
                                        "знаходиться в межах [0, 0.5]",
                                   font=("Cambria", 12), justify="left", anchor='sw', fg='#FF0000')
            entry_v.configure(bg='#FF0000')
            wrongValue = True

    except ValueError:
        label_output.configure(text="Неправильний тип даних!", font=("Cambria", 12), justify="left", anchor='sw',
                               fg='#FF0000')
        entry_H.configure(bg='#FF0000')
        entry_h.configure(bg='#FF0000')
        entry_b.configure(bg='#FF0000')
        entry_c.configure(bg='#FF0000')
        entry_q.configure(bg='#FF0000')
        entry_Q.configure(bg='#FF0000')
        entry_E.configure(bg='#FF0000')
        entry_v.configure(bg='#FF0000')
        wrongValue = True

    if not wrongValue:
        if ((H + h) / 2) / c > 1 / 20:
            label_output.configure(text="Товщина пластини занадто велика\nу порівнянні з її іншими розмірами",
                                   font=("Cambria", 12), justify="left", anchor='sw', fg='#FF0000')
            wrongValue = True

    if not wrongValue:
        # Блокування полів від редагування
        entry_H.configure(state='disabled')
        entry_h.configure(state='disabled')
        entry_b.configure(state='disabled')
        entry_c.configure(state='disabled')
        entry_q.configure(state='disabled')
        entry_Q.configure(state='disabled')
        entry_E.configure(state='disabled')
        entry_v.configure(state='disabled')
        calcButton.configure(state='disabled')

        log_file.write("\n\nВхідні дані:\n\t H = " + str(H) + " м\n\t h = " + str(h) +
                       " м\n\t b = " + str(b) + " м\n\t c = " + str(c) + " м\n\t q0 = " + str(q) +
                       " Па\n\t Q = " + str(Q) + " Н/м\n\t E = " + str(Q) + "Па\n\t v = " + str(v) +
                       "\n\nРозрахунок...\n\n\t1.Складання системи рівнянь...")

        D1 = E * (H ** 3) / (12 * (1 - v ** 2))  # Жорсткість згину пластини на ділянці I
        D2 = E * (h ** 3) / (12 * (1 - v ** 2))  # Жорсткість згину пластини на ділянці II

        C1, C2, C3, C4, C5, C6, r = symbols('C1,C2,C3,C4,C5,C6,r')

        # Знаходження загальних рішень для переміщень

        w1 = (q / (b * D1)) * (b * (r ** 4) / 64 - r ** 5 / 225) + C1 * (r ** 2) + C2
        w2 = C3 * r ** 2 * log(r) + C4 * r ** 2 + C5 * log(r) + C6

        log_file.write("\n\n\tЗагальні рішення для переміщень:\n\t\tw1 = " + str(w1) + "\n\t\tw2 = " + str(w2))

        # Задання та розв'язання системи рівнянь для пошуку констант інтегрування

        equations = [w1.subs(r, b),
                     w2.subs(r, b),
                     (-D2 * diff(diff(diff(w2, r), r) + 1 / r * diff(w2, r), r) - Q).subs(r, c),
                     (diff(diff(w2, r), r) + v / r * diff(w2, r)).subs(r, c),
                     (diff(w1, r) - diff(w2, r)).subs(r, b),
                     (-D1 * (diff(diff(w1, r), r) + v / r * diff(w1, r)) + D2 * (
                             diff(diff(w2, r), r) + v / r * diff(w2, r))).subs(r, b),

                     (-D1 * diff(diff(diff(w1, r), r) + 1 / r * diff(w1, r), r) + D2 * diff(
                         diff(diff(w2, r), r) + 1 / r * diff(w2, r), r)).subs(r, b),

                     (-D1 * (v * diff(diff(w1, r), r) + diff(w1, r) / r) + D2 * (
                             diff(v * diff(w2, r), r) + diff(w2, r) / r)).subs(r, b)]

        log_file.write("\n\n\t2.Знаходження констант інтегрування...")

        solution = solve([equations[0], equations[1], equations[2], equations[3], equations[4],
                          equations[5]], [C1, C2, C3, C4, C5, C6])

        l1 = np.linspace(0, b, int(b * 1000))
        l2 = np.linspace(b, c, int((c - b) * 1000))

        Qr1 = np.zeros(len(l1))
        Qr2 = np.zeros(len(l2))

        W1 = np.zeros(len(l1))
        W2 = np.zeros(len(l2))

        Mr1 = np.zeros(len(l1))
        Mr2 = np.zeros(len(l2))

        M_theta1 = np.zeros(len(l1))
        M_theta2 = np.zeros(len(l2))

        Qr_max = 0
        Mr_max = 0
        M_theta_max = 0

        Qr_max_loc = 0
        Mr_max_loc = 0
        Mt_max_loc = 0

        log_file.write("\n\n\t\tC1 = " + str(solution[C1]) + "\n\t\tC2 = " + str(solution[C2]) +
                       "\n\t\tC3 = " + str(solution[C3]) + "\n\t\tC4 = " + str(solution[C4]) +
                       "\n\t\tC5 = " + str(solution[C5]) + "\n\t\tC6 = " + str(solution[C6]) + "\n")

        w1 = w1.subs([(C1, solution[C1]), (C2, solution[C2])])
        w2 = w2.subs([(C3, solution[C3]), (C4, solution[C4]), (C5, solution[C5]), (C6, solution[C6])])

        # Знаходження переміщень, поперечних сил та моментів для I та II ділянки

        log_file.write("\n\t3.Обчислення w, Qr, Mrr та Mθθ для першої ділянки (0 ≤ r ≤ " + str(b) + ")...")

        for i in range(0, len(l1)):
            W1[i] = w1.subs(r, l1[i])
            Qr1[i] = (-D1 * diff((diff(diff(w1, r), r) + diff(w1, r) / r), r)).subs(r, l1[i])

            if abs(Qr1[i]) > Qr_max:
                Qr_max = abs(Qr1[i])
                Qr_max_loc = l1[i]

            Mr1[i] = (-D1 * (diff(diff(w1, r), r) + v / r * diff(w1, r))).subs(r, l1[i])

            if abs(Mr1[i]) > Mr_max:
                Mr_max = abs(Mr1[i])
                Mr_max_loc = l1[i]

            M_theta1[i] = (-D1 * (v * diff(diff(w1, r), r) + 1 / r * diff(w1, r))).subs(r, l1[i])

            if abs(M_theta1[i]) > M_theta_max:
                M_theta_max = abs(M_theta1[i])
                Mt_max_loc = l1[i]

        log_file.write("\n\t4.Обчислення w, Qr, Mrr та Mθθ для другої ділянки (" + str(b) + " ≤ r ≤ " + str(c) + ")...")

        for i in range(0, len(l2)):
            W2[i] = w2.subs(r, l2[i])
            Qr2[i] = (-D2 * diff((diff(diff(w2, r), r) + diff(w2, r) / r), r)).subs(r, l2[i])

            if abs(Qr2[i]) > Qr_max:
                Qr_max = abs(Qr2[i])
                Qr_max_loc = l2[i]

            Mr2[i] = (-D2 * (diff(diff(w2, r), r) + v / r * diff(w2, r))).subs(r, l2[i])

            if abs(Mr2[i]) > Mr_max:
                Mr_max = abs(Mr2[i])
                Mr_max_loc = l2[i]

            M_theta2[i] = (-D2 * (v * diff(diff(w2, r), r) + 1 / r * diff(w2, r))).subs(r, l2[i])

            if abs(M_theta2[i]) > M_theta_max:
                M_theta_max = abs(M_theta2[i])
                Mt_max_loc = l2[i]

        if buildPlot:
            # Побудова графіків

            log_file.write("\n\t5.Побудова графіків...")

            plt.subplot(2, 2, 1)  # Побудова графіку прогину
            plt.plot(l1, W1, 'b-')
            plt.plot(l2, W2, 'r-')
            plt.title("Прогин, [м]", size=10)
            plt.grid()
            plt.ylabel('w')

            plt.subplot(2, 2, 2)  # Побудова графіку перерізуючої сили
            plt.plot(l1, Qr1, 'b-')
            plt.plot(l2, Qr2, 'r-')
            plt.plot(np.linspace(b, b + 10 ** (-20), 5), np.linspace(Qr1[len(Qr1) - 1], Qr2[0], 5), 'b-')
            plt.title("Перерізуюча сила, [Н/м]", size=10)
            plt.grid()
            plt.ylabel('Qr')

            plt.subplot(2, 2, 3)  # Побудова графіку радіального згинального моменту
            plt.plot(l1, Mr1, 'b-')
            plt.plot(l2, Mr2, 'r-')
            plt.title("Радіальний знинальний момент, [Н]", size=10)
            plt.grid()
            plt.ylabel('Mrr')

            plt.subplot(2, 2, 4)  # Побудова графіку окружного згинального моменту
            plt.plot(l1, M_theta1, 'b-')
            plt.plot(l2, M_theta2, 'r-')
            plt.plot(np.linspace(b, b + 10 ** (-20), 5), np.linspace(M_theta1[len(M_theta1) - 1], M_theta2[0], 5), 'b-')
            plt.title("Окружний згинальний момент, [Н]", size=10)
            plt.grid()
            plt.ylabel('Mθθ')

            plt.subplots_adjust(right=0.95, wspace=0.45, hspace=0.45)
            plt.show()

        log_file.write("\n\t6.Обчислення максимальних напружень...")

        # Обчислення максимальних поперечних сил та моментів

        if Qr_max_loc < b:
            sigma_rz = (3 * abs(Qr_max)) / (2 * H)
        else:
            sigma_rz = (3 * abs(Qr_max)) / (2 * h)

        if Mr_max_loc < b:
            sigma_rr = (6 * abs(Mr_max)) / (H ** 2)
        else:
            sigma_rr = (6 * abs(Mr_max)) / (h ** 2)

        if Mt_max_loc < b:
            sigma_theta = (6 * abs(M_theta_max)) / (H ** 2)
        else:
            sigma_theta = (6 * abs(M_theta_max)) / (h ** 2)

        label_output.configure(text="Максимальні напруження:"
                                    "\n\nРадіальні |σrr| = " + str(sigma_rr / 1000000) + " МПа"
                                    "\nОкружні |σθθ| = " + str(sigma_theta / 1000000) + " МПа"
                                    "\nДотичні |σrz| = " + str(sigma_rz / 1000000) + " МПа",
                               font=("Cambria", 12), fg='#000000', bg='#FFFFFF', justify="left", anchor='sw')

        log_file.write("\n\n\t\tРадіальні напруження |σrr| = " + str(sigma_rr / 1000000) + " МПа"
                       "\n\t\tОкружні напруження |σθθ| = " + str(sigma_theta / 1000000) + " МПа"
                       "\n\t\tДотичні напруження |σrz| = " + str(sigma_rz / 1000000) + " МПа")

        log_file.close()


# clear() - функція, яка повертає програму до початкового стану(очищає поля, скидає значення змінних)
def clear():
    global H, h, b, c, q, Q, E, v
    label_output.configure(text="")

    # Розблокування полів для вводу
    entry_H.configure(state='normal')
    entry_h.configure(state='normal')
    entry_b.configure(state='normal')
    entry_c.configure(state='normal')
    entry_q.configure(state='normal')
    entry_Q.configure(state='normal')
    entry_E.configure(state='normal')
    entry_v.configure(state='normal')

    # Очищення полів для вводу
    entry_H.configure(bg='#FFFFFF')
    entry_h.configure(bg='#FFFFFF')
    entry_b.configure(bg='#FFFFFF')
    entry_c.configure(bg='#FFFFFF')
    entry_q.configure(bg='#FFFFFF')
    entry_Q.configure(bg='#FFFFFF')
    entry_E.configure(bg='#FFFFFF')
    entry_v.configure(bg='#FFFFFF')

    entry_H.delete(0, len(entry_H.get()))
    entry_h.delete(0, len(entry_h.get()))
    entry_b.delete(0, len(entry_b.get()))
    entry_c.delete(0, len(entry_c.get()))
    entry_q.delete(0, len(entry_q.get()))
    entry_Q.delete(0, len(entry_Q.get()))
    entry_E.delete(0, len(entry_E.get()))
    entry_v.delete(0, len(entry_v.get()))

    calcButton.configure(state='normal')
    clearButton.configure(state='disabled')

    # Скидання значень змінних
    H = None
    h = None
    b = None
    c = None
    q = None
    Q = None
    E = None
    v = None


# Ініціалізація інтерфейсу
window = tk.Tk()

buildPlot = tk.BooleanVar()
window.geometry("750x500")
window.resizable(False, False)
window.wm_title("АНАЛІЗ ОСЕСИМЕТРИЧНОГО ЗГИНУ КРУГЛИХ І КІЛЬЦЕВИХ ПЛАСТИН")
img = tk.PhotoImage(file="bg.png")
imageLabel = tk.Label(image=img)
imageLabel.pack()
imageLabel.place(x=0, y=0)

nameLabel = tk.Label(text="Розрахункова схема", font=("Cambria", 15))
nameLabel.pack()
nameLabel.place(x=20, y=20)

inputDataLabel = tk.Label(text="Вхідні дані", font=("Cambria", 15))
inputDataLabel.pack()
inputDataLabel.place(x=500, y=20)

outputDataLabel = tk.Label(text="Вихідні дані", font=("Cambria", 15))
outputDataLabel.pack()
outputDataLabel.place(x=20, y=270)

label_offset_X = -10
label_offset_Y = 0

label_m1 = tk.Label(text="[м]", font=("Cambria", 12))
label_m1.pack()
label_m1.place(x=655, y=70)

label_m2 = tk.Label(text="[м]", font=("Cambria", 12))
label_m2.pack()
label_m2.place(x=655, y=110)

label_m3 = tk.Label(text="[м]", font=("Cambria", 12))
label_m3.pack()
label_m3.place(x=655, y=150)

label_m4 = tk.Label(text="[м]", font=("Cambria", 12))
label_m4.pack()
label_m4.place(x=655, y=190)

label_m5 = tk.Label(text="[Па]", font=("Cambria", 12))
label_m5.pack()
label_m5.place(x=655, y=230)

label_m6 = tk.Label(text="[Н/м]", font=("Cambria", 12))
label_m6.pack()
label_m6.place(x=655, y=270)

label_m7 = tk.Label(text="*10^11 [Па]", font=("Cambria", 12))
label_m7.pack()
label_m7.place(x=599, y=310)

label_m8 = tk.Label(text="[  ]", font=("Cambria", 12))
label_m8.pack()
label_m8.place(x=655, y=350)

label_H = tk.Label(text="H =", font=("Cambria", 12))
label_H.pack()
label_H.place(x=500 + label_offset_X, y=70 + label_offset_Y)

entry_H = tk.Entry()
entry_H.pack()
entry_H.place(x=530, y=73)

label_h = tk.Label(text="h =", font=("Cambria", 12))
label_h.pack()
label_h.place(x=500 + label_offset_X, y=110 + label_offset_Y)

entry_h = tk.Entry()
entry_h.pack()
entry_h.place(x=530, y=113)

label_b = tk.Label(text="b =", font=("Cambria", 12))
label_b.pack()
label_b.place(x=500 + label_offset_X, y=150)

entry_b = tk.Entry()
entry_b.pack()
entry_b.place(x=530, y=153)

label_c = tk.Label(text="c =", font=("Cambria", 12))
label_c.pack()
label_c.place(x=500 + label_offset_X, y=190 + label_offset_Y)

entry_c = tk.Entry()
entry_c.pack()
entry_c.place(x=530, y=193)

label_q = tk.Label(text="q0 =", font=("Cambria", 12))
label_q.pack()
label_q.place(x=500 + label_offset_X, y=230 + label_offset_Y)

entry_q = tk.Entry()
entry_q.pack()
entry_q.place(x=530, y=233)

label_Q = tk.Label(text="Q =", font=("Cambria", 12))
label_Q.pack()
label_Q.place(x=500 + label_offset_X, y=270 + label_offset_Y)

entry_Q = tk.Entry()
entry_Q.pack()
entry_Q.place(x=530, y=273)

label_E = tk.Label(text="E =", font=("Cambria", 12))
label_E.pack()
label_E.place(x=500 + label_offset_X, y=310 + label_offset_Y)

entry_E = tk.Entry()
entry_E.pack()
entry_E.place(x=530, y=313, width=70)

label_v = tk.Label(text="v =", font=("Cambria", 12))
label_v.pack()
label_v.place(x=500 + label_offset_X, y=350 + label_offset_Y)

entry_v = tk.Entry()
entry_v.pack()
entry_v.place(x=530, y=353)

plotCheckbox = tk.Checkbutton(text="Побудувати графіки\nW, Qx, Mrr, Mθθ", font=("Cambria", 11), justify="left",
                              onvalue=True, offvalue=False, variable=buildPlot)
plotCheckbox.pack()
plotCheckbox.place(x=500, y=390)

calcButton = tk.Button(text="Розрахувати", font=("Cambria", 12), command=calculate)
calcButton.pack()
calcButton.place(x=500, y=440)

clearButton = tk.Button(text="Очистити дані", font=("Cambria", 12), command=clear)
clearButton.pack()
clearButton.place(x=610, y=440)
clearButton.configure(state='disabled')

label_output = tk.Label(text="", font=("Cambria", 12), width=50, justify="left", bg='#FFFFFF')
label_output.pack()
label_output.place(x=30, y=310, width=380)

window.mainloop()
