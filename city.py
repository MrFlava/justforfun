import random
list = open("cities.txt","r")
cities = [list.read()]
list.close()
for i in cities:
    new_data = i.split()
    def beggining (step_of_player):
        first = step_of_player[0]
        return first
    def end (step_of_player):
        i = -1
        while step_of_player[i] in ["ъ","ь","ы"]:
            i -= 1
        end = step_of_player[i].upper()
        return end

    def next_steps(step_of_player):
        first_letter = end(step_of_player)
        new_data.remove(step_of_player)
        new_list = []
        for i in new_data:
            if first_letter == beggining(i):
                new_list.append(i)
        new_choice = random.choice(new_list)
        new_data.remove(new_choice)
        return new_choice



    step_computer = print("Я выбрал город ", random.choice(new_data))
    step_of_player = str(input("Игрок выбрал город "))
    while True:
        if step_of_player in new_data:
            step_computer = print("Я выбрал город ", next_steps(step_of_player))
            step_of_player = str(input("Игрок выбрал город "))
        else:
            if step_of_player not in new_data:
                print("Такой город не существует или он уже был в списке")
                break
