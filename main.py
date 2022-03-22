
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    #функция для проставления оценок лекторам за курсы
    def rate_lect(self, lecturer, course, grade):
        if isinstance(lecturer,
                      Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    #функция для подсчета средней оценки за все дз
    def mean_hw_rate(self):
        grades_list = []
        for course in self.courses_in_progress:
            if course in self.grades.keys():
                for number in (0, 1): #по одному курсу м.б. несколько оценок; вместо 1 идеально поставить макс. кол-во дз
                    if number < len(self.grades.get(course)):
                        grades_list.append(self.grades.get(course)[number])
                    else:
                        grades_list = grades_list
            else:
                grades_list = grades_list
        return sum(grades_list) / len(grades_list)

    #перегрузка print (выдает карточку студента)
    def __str__(self):
        text = f'''Имя: {self.name}\nФамилия: {self.surname}
Средняя оценка за домашние задания: {self.mean_hw_rate()}
Курсы в процессе изучения: {self.courses_in_progress}
Завершенные курсы: {self.finished_courses}\n'''
        return text

    #перегрузка < (по средним оценкам)
    def __lt__(self, other):
        if not isinstance(other, Student):
            return
        return self.mean_hw_rate() < other.mean_hw_rate()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    #функция для подсчета средней оценки работы лектора
    def mean_lect_rate(self):
        grades_list = []
        for course in self.courses_attached:
            if course in self.grades.keys():
                for number in (0, 1): #по одному курсу м.б. несколько оценок; список идеально продлить до макс. кол-ва студентов
                    if number < len(self.grades.get(course)):
                        grades_list.append(self.grades.get(course)[number])
                    else:
                        grades_list = grades_list
            else:
                grades_list = grades_list
        return sum(grades_list) / len(grades_list)

    #перегрузка print (выдает карточку лектора)
    def __str__(self):
        text = f'''Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.mean_lect_rate()}\n'''
        return text

    #перегрузка < (по средним оценкам)
    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return
        return self.mean_lect_rate() < other.mean_lect_rate()


class Reviewer(Mentor):
    #функция оценивания дз у конкретного студента по конкретному курсу
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    #перегрузка print (выдает карточку ревьюера)
    def __str__(self):
        text = f'''Имя: {self.name}\nФамилия: {self.surname}\n'''
        return text

#создаем экземпляры классов
Harry = Student("Harry", "Potter", "male")
Hermione = Student("Hermione", "Granger", "female")

Severus = Lecturer("Severus", "Snape")
Minerva = Lecturer("Minerva", "McGonagall")

Fred = Reviewer("Fred", "Weasley")
George = Reviewer("George", "Weasley")

# добавляем текущие и пройденные предметы у Гарри
Harry.courses_in_progress += ['Potions', 'Charms']
Harry.finished_courses += ['Herbology', 'Transfiguration']

# добавляем текущие и пройденные предметы у Гермионы
Hermione.courses_in_progress += ['Potions', 'Transfiguration', 'History of magic']
Hermione.finished_courses += ['Numerology', 'Charms', 'Ancient runes']

# распределяем дисциплины между преподавателями
Severus.courses_attached += ['Potions', 'Herbology']
Minerva.courses_attached += ['Transfiguration', 'Charms']

# назначаем проверяющих на дисциплины
Fred.courses_attached += ['Potions', 'Herbology']
George.courses_attached += ['Transfiguration', 'Charms']

# Проверяющие оценили работы Гарри и Гермионы
Fred.rate_hw(Harry, 'Potions', 7)
Fred.rate_hw(Hermione, 'Potions', 9)
George.rate_hw(Harry, 'Charms', 8)
George.rate_hw(Hermione, 'Transfiguration', 10)

# Гарри и Гермиона оценили работу лекторов
Harry.rate_lect(Severus, 'Potions', 2)
Harry.rate_lect(Minerva, 'Charms', 7)
Hermione.rate_lect(Severus, 'Potions', 9)
Hermione.rate_lect(Minerva, 'Transfiguration', 10)


#функция считает среднюю оценку по курсу для выбранных студентов
def mean_grades_st(student_list, course):
    grades_list = []
    for student in student_list:
        if course in student.courses_in_progress:
            grades_list.append(student.grades.get(course)[0])
        else:
            grades_list = grades_list
    print(sum(grades_list) / len(grades_list))

#пример:
#mean_grades_st((Harry, Hermione), 'Potions')

#функция считаeт среднюю оценку по курсу для выбранных преподавателей
def mean_grades_lec(lecturer_list, course):
    grades_list = []
    for lecturer in lecturer_list:
        if course in lecturer.courses_attached:
            for number in (0, 1):  # по одному курсу м.б. несколько оценок; список идеально продлить до макс. кол-ва студентов
                if number < len(lecturer.grades.get(course)):
                    grades_list.append(lecturer.grades.get(course)[number])
                else:
                    grades_list = grades_list
        else:
            grades_list = grades_list
    print(sum(grades_list) / len(grades_list))

#пример:
#за 1 курсом закреплен 1 преподаватель, поэтому в нашем случае результаты равны их оценкам
#mean_grades_lec((Severus, Minerva), 'Potions')

#Вывод карточек студентов, преподавателей, ревьюеров
print(Harry)
print(Hermione)

print(Minerva)
print(Severus)

print(Fred)
print(George)

#сравнение по средним оценкам
print(Harry<Hermione)
print(Hermione<Harry)
print(Minerva>Severus)
print(Minerva<Severus)