# Задание на знание SQL 1

Есть 3 таблицы (Students, Friends, Packages):
Students содержит ID и имя студентов.
Friends содержит связи между студентами.
Packages содержит информацию о зарплате. 


Задача: написать SQL запрос, который выведет имена студентов, друзья которых, получили бОльшую зарплату, чем они. Имена должны быть отсортированы в порядке убывания зарплаты, предлагаемой их друзьям.


```sql
    Select s1.name
    FROM Friends F
    JOIN Students s1 ON F.student_id = s1.id
    JOIN Students s2 ON F.friend_id = s2.id
    JOIN Packages P1 ON S1.id = P1.student_id
    JOIN Packages P2 ON S2.id = P2.student_id
    WHERE P1.salary < P2.salary
    ORDER BY P2.salary DESC;
```

# Задание на знание SQL 2

Дана таблица Projects, в которой содержатся данные о начале и завершении задач. Длительность 1 задачи равна 1 дню. Если задачи выполняются подряд, они относятся к 1 проекту.
```sql
    WITH ProjectGroups AS (
        SELECT 
            Task_ID,
            Start_Date,
            End_Date,
            DATE(Start_Date, '-' || (ROW_NUMBER() OVER (ORDER BY Start_Date) - 1) || ' DAY') AS GroupDate
        FROM Projects
    ),
    ProjectRanges AS (
        SELECT 
            MIN(Start_Date) AS Project_Start,
            MAX(End_Date) AS Project_End,
            GroupDate
        FROM ProjectGroups
        GROUP BY GroupDate
    )
    SELECT 
        Project_Start,
        Project_End
    FROM ProjectRanges
    ORDER BY (JULIANDAY(Project_End) - JULIANDAY(Project_Start) + 1), Project_Start;
```
