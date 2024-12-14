## Задание №1
Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС. 
Эмулятор должен запускаться из реальной командной строки, а файл с
виртуальной файловой системой не нужно распаковывать у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата
`zip`. Эмулятор должен работать в режиме `CLI`.<br/>

Конфигурационный файл имеет формат csv и содержит:<br/>
• Имя пользователя для показа в приглашении к вводу<br/>
• Имя компьютера для показа в приглашении к вводу.<br/>
• Путь к архиву виртуальной файловой системы.<br/>
• Путь к лог-файлу.<br/>

Лог-файл имеет формат `xml` и содержит все действия во время последнего
сеанса работы с эмулятором. Для каждого действия указаны дата и время. Для
каждого действия указан пользователь.<br/>

Необходимо поддержать в эмуляторе команды ls, cd и exit, а также
следующие команды:
1. cal.
2. find.<br/>

Результат работы программы<br/>

![image](https://github.com/user-attachments/assets/dc2652d5-1849-479e-bd06-e4f71b0e5634)

## Задание №2
Разработать инструмент командной строки для визуализации графа
зависимостей, включая транзитивные зависимости. Сторонние средства для
получения зависимостей использовать нельзя.<br/>

Зависимости определяются для git-репозитория. Для описания графа
зависимостей используется представление Mermaid. Визуализатор должен
выводить результат на экран в виде графического изображения графа.<br/>

Построить граф зависимостей для коммитов, в узлах которого содержатся
номера коммитов в хронологическом порядке.<br/>

Ключами командной строки задаются:<br/>

• Путь к программе для визуализации графов.<br/>
• Путь к анализируемому репозиторию.<br/>

Результат работы программы<br/>



## Задание 3
Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.<br/>
Входной текст на языке yaml принимается из файла, путь к которому задан
ключом командной строки. Выходной текст на учебном конфигурационном
языке попадает в стандартный вывод.<br/>

Однострочные комментарии:<br/>
_|| Это однострочный комментарий_<br/>

Словари:<br>
_$[_<br/>
_имя : значение_<br/>
_имя : значение_<br/>
_имя : значение_<br/>
_. . ._<br/>
_]_<br/>

Имена:<br/>
[___A-Z]_[__a-zA-Z0-9]*_<br/>

Значения: <br/>
_• Числа._<br/>
_• Словари._<br/>

Объявление константы на этапе трансляции:<br/>
_имя: значение_<br/>

Вычисление константного выражения на этапе трансляции (префиксная
форма), пример:<br/>
_{+ имя 1}_<br/>

Результатом вычисления константного выражения является значение.
Для константных вычислений определены операции и функции:<br/>
_1. Сложение._<br/>
_2. pow()._<br/>

Пример конфигурационного файла на языке `yaml`<br/>
![image](https://github.com/user-attachments/assets/275490c9-b92d-4849-a9b4-1d375cc2c3a0)


Результат работы программы<br/>
![image](https://github.com/user-attachments/assets/90035c3e-af7e-4048-8a69-4772ac778294)

