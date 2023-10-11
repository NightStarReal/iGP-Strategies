import csv
import pygame
from tkinter import messagebox as mb

reader_object = open("pit_history.csv", encoding='UTF-8')
also_object = open("Qualifying.csv", encoding='UTF-8')
Strategies = {}
Simple = {'Super soft tyres': 'SS',
          'Soft tyres': 'S',
          'Medium tyres': 'M',
          'Hard tyres': 'H',
          'Intermediate wet tyres': 'I',
          'Full wet tyres': 'W'}
try:
    main = csv.reader(reader_object, delimiter=',')
    adv = csv.reader(also_object, delimiter=',')
    for row in adv:
        if row[1] != 'Driver':
            try:
                Strategies[row[1]] = [(int(row[0]), row[5])]
            except ValueError:
                mb.showerror("ValueError", f"invalid literal for int() with base 10: {row[0]}")
                raise ValueError
    for row in main:
        q = []
        for i in range(2, len(row), 2):
            if i + 1 < len(row):
                if row[i + 1] != 'NaN':
                    try:
                        q.append((Simple[row[i]], int(row[i+1])))
                    except ValueError:
                        mb.showerror("ValueError", f"invalid literal for int() with base 10: {row[i+1]}")
                        raise ValueError
                    except KeyError:
                        mb.showerror("KeyError", f"That is not compound {row[i]}")
                        raise ValueError
                else:
                    try:
                        q.append((Simple[row[i]], 0))
                    except KeyError:
                        mb.showerror("KeyError", f"That is not compound {row[i]}")
                        raise ValueError
        Strategies[row[1]] += q
        Strategies[row[1]].insert(0, int(row[0]))
finally:
    reader_object.close()
    also_object.close()

try:
    pygame.init()
    pygame.font.init()
    nf = pygame.font.SysFont('verdana', 12)
    f = pygame.font.SysFont('arial', 12)
    fs = pygame.font.SysFont('trebuchet', 12)
except NameError:
    mb.showerror("NameError", "Pygame isn't installed")
    raise NameError
Colors = {'SS': (200, 0, 0), 
          'S': (200, 180, 0),
          'M': (200, 200, 200),
          'H': (200, 120, 0),
          'I': (0, 200, 0),
          'W': (55, 55, 255)}
Stints = {'SS': [], 'S': [], 'M': [], 'H': [], 'I': [], 'W': []}
sc = pygame.display.set_mode((1400, 800))
sc.fill((0, 0, 0))
c = 0
order = sorted(Strategies.keys(), key=lambda t: Strategies[t][0])
temp = list(map(lambda t: t[1], Strategies[order[0]][2:]))
max_laps = 0
for i in temp:
    max_laps += i

lap_height = 8
lap_weight = 16
text_height = 20
text_weight = 150
q_extra = 5
empty = 10
pits_weight = 50

a = fs.render('qualy', 1, (255, 255, 255))
a_rect = a.get_rect(centerx=empty + q_extra / 2 + text_weight + text_height / 2, y=empty - 3)
sc.blit(a, a_rect)

for i in range(1, max_laps + 1):
    mtext = fs.render(str(i), 0, (255, 255, 255))
    m_rect = mtext.get_rect(centerx=text_height + 2 * empty + q_extra + pits_weight + text_weight + lap_weight*i,
                            y=empty)
    sc.blit(mtext, m_rect)

for i in order:
    text = nf.render(i, 1, (255, 255, 255))
    sc.blit(text, (empty, 2 * empty + text_height * c))

    laps = 0
    s = len(Strategies[i]) - 3
    qualy = Strategies[i][1]

    if qualy[0] == 1:
        qtext = f.render(str(qualy[0]), 1, (0, 0, 0))
        pygame.draw.rect(sc,
                         (120, 0, 240),
                         (empty + text_weight, 2 * empty + text_height * c, text_height, text_height))
    else:
        qtext = f.render(str(qualy[0]), 1, (255, 255, 255))
    pygame.draw.line(sc, Colors[qualy[1]],
                     (empty + text_weight + text_height + q_extra / 2, 2 * empty + text_height * c),
                     (empty + text_weight + text_height + q_extra / 2, 2 * empty + text_height * c + text_height), 5)
    q_rect = qtext.get_rect(center=(empty + text_weight + text_height / 2,
                                    2 * empty + text_height * c + text_height/2 - 1))
    sc.blit(qtext, q_rect)

    ptext = nf.render(str(s) + ' pits', 1, (255, 255, 255))
    sc.blit(ptext, (2 * empty + q_extra + text_weight + text_height, 2 * empty + text_height * c))

    for j in Strategies[i][2:]:
        Stints[j[0]].append(j[1])

        pygame.draw.rect(sc, Colors[j[0]],
                         (text_height + 2 * empty + q_extra + pits_weight + text_weight + lap_weight*laps,
                         2 * empty + text_height*c + (text_height - lap_height)/2,
                         lap_weight*j[1],
                         lap_height))
        laps += j[1]
    for q in range(1, laps + 1):
        pygame.draw.line(sc,
                         (50, 50, 50),
                         (text_height + 2 * empty + q_extra + pits_weight + text_weight + lap_weight*q,
                          2 * empty + text_height*c + (text_height - lap_height)/2),
                         (text_height + 2 * empty + q_extra + pits_weight + text_weight + lap_weight*q,
                          2 * empty + text_height*c + (text_height + lap_height)/2 - 1))
    laps = 0

    for k in Strategies[i][2:]:
        pygame.draw.circle(sc, Colors[k[0]],
                           (text_height + 2 * empty + q_extra + pits_weight + text_weight + lap_weight*laps,
                           2 * empty + text_height * c + text_height / 2),
                           text_height / 2 - 1)
        ltext = f.render(str(k[1]), 1, (0, 0, 0))
        l_rect = ltext.get_rect(center=(text_height + 2 * empty + q_extra + pits_weight + text_weight + lap_weight*laps,
                                2 * empty + text_height * c + text_height / 2 - 0.5))
        sc.blit(ltext, l_rect)
        laps += k[1]

    ftext = f.render(str(Strategies[i][0]), 1, (255, 255, 255))
    sc.blit(ftext, (text_height + text_height / 4 + 2 * empty + q_extra + pits_weight + text_weight + lap_weight*laps,
            2 * empty + text_height * c + text_height / 8))
    c += 1

n = 0
for i in Stints.keys():
    if len(Stints[i]) > 0:
        maxl = max(Stints[i])
        averl = 0
        for j in Stints[i]:
            averl += j
        averl /= len(Stints[i])
        averl *= 100
        averl = int(averl)
        averl /= 100
        pygame.draw.circle(sc, Colors[i],
                           (empty + text_height / 2, (len(order) + n) * text_height + 2 * empty + text_height / 2),
                           text_height / 2)
        maxtext = nf.render('Max: ' + str(maxl) + ' laps', 0, (255, 255, 255))
        avertext = nf.render('Average: ' + str(averl) + ' laps', 0, (255, 255, 255))
        sc.blit(maxtext, (2 * empty + text_height, (len(order) + n) * text_height + 2 * empty))
        sc.blit(avertext, (2 * empty + text_height + 120, (len(order) + n) * text_height + 2 * empty))
        n += 1
        

pygame.display.flip()

clock = pygame.time.Clock()
running = True
while running:
    for q in pygame.event.get():
        if q.type == pygame.QUIT:
            running = False
        clock.tick(10)
