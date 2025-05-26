import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import random
import math

# funkcja licząca dystans między dwoma punktami na osi liczbowej
# korzystamy tutaj z klasycznego wzoru na odległośc euklidesową
def euc_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


# przechodzi przez wszystkie miasta w kolejności tour
# dodaje odległość pomiędzy kolejnymi punktami oraz powrót do startu przez %
def total_distance(tour, points):
    distance = 0
    for i in range(len(tour)):
        current_point = points[tour[i]]
        next_point = points[tour[(i+1) % len(tour)]]
        distance += euc_distance(current_point, next_point)
    return distance

# Przesunięcie świetlika w strone lepszego (jaśniejszego)
# im bardziej różny od lepszego świetlika tym bardziej się przyciąga przez zmiany elementów
def move_firefly(firefly, target):
    new_tour = firefly[:] # kopia obecnej trasy
    for i in range(len(firefly)):
        # Jeśli punkt różni się od lepszego, zamień miejscami
        if firefly[i] != target[i]:
            j = new_tour.index(target[i])
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
        return new_tour

# Algorytm świetlika
def firefly_algorithm(points, num_firefly = 15, generations = 100):
    num_points = len(points)

    # Tworzenie początkowych losowych tras świetlików
    firefly = [random.sample(range(num_points), num_points) for _ in range(num_firefly)]
    distances = [total_distance(f, points) for f in firefly]

    # Wybór najlepszego, najkrótkszego na start
    best = firefly[distances.index(min(distances))]
    best_distance = min(distances)

    # Iteracyjna poprawa trasy przez kolejny pokolenia
    for gen in range(generations):
        for i in range(num_firefly):
            for j in range(num_firefly):
                # jeśli (j) świetlik jest lepszy, przyciągnij (i) świetlika w jego stronę
                if total_distance(firefly[j], points) < total_distance(firefly[i], points):
                    firefly[i] = move_firefly(firefly[i], firefly[j])

        # aktualizacja najlepszago po każdej generacji
        distances = [total_distance(f, points) for f in firefly]
        if min(distances) < best_distance:
            best = firefly[distances.index(min(distances))]
            best_distance = min(distances)
        print(f"Pokolenie {gen + 1}: Najlepsza odległość: {best_distance}")

    return best, best_distance

# Rysowanie trasy
def draw_tour(tour, points):
    # dołączenie powrotu do punktu startowego
    tour_points = [points[i] for i in tour] + [points[tour[0]]]

    x = [p[0] for p in tour_points]
    y = [p[1] for p in tour_points]

    plt.figure(figsize=(10, 10))
    plt.plot(x, y, marker='o', color='red')
    for i, point in enumerate(tour):
        plt.text(points[point][0], points[point][1], str(point), fontsize = 12)

    plt.title("Najlepsza znaleziona trasa przez algorytm świetlików")
    plt.grid(True)
    plt.show()

# generuje 10 losowych punktów na osi 2D
points = [(random.randint(0, 100), random.randint(0,100)) for _ in range(10)]

# Uruchomienie algorytmu
best_tour, best_distance = firefly_algorithm(points)

print(f"Najlepsza trasa: {best_tour}, Najkrótsza odległość: {best_distance}")

draw_tour(best_tour,points)



