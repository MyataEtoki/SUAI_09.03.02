Универсальные/Обобщённые/Родовые типы - Generic-и.
# Динамические члены обобщённых классов
Универсальные шаблоны имеют универсальные параметры, тип которых определяется в момент создания экземпляра.
У каждого экземпляра типы универсальных параметров м.б. различны.
```C#
System.Collection.Generic // растут от этого
List<T> // универсальная коллекция
ArrayList // сразу список с перебором, неуниверсальный
```
Обобщения м.б. применимы к:
- Интерфейсы [[10 - Интерфейсы]]
- Классы [[Класс в CS]]
- Структурам
- Методам
- Делегаты [[7 - Событие - Event]]

Преимущества:
- Многократное, вариативное использование.
- Типобезопасность(для типов), эффективность.

```C#
public class MyList<T>{ //T - Tamplate - Темплейт
public double Id {get; set;}
public T? Name {get; set;}
public MyList(T name) => Name = name;
public override string ToString() {
return Name.ToString();
}
}

MyList<int> ints1 = new MyList<int>((int)t1.Text);
MyList<string> strings1 = new MyList<string>(t2.Text);
MyList<bool> b1 = new MyList<bool>((bool)checkBox1.Checked);
// MyList<int> ints2 = new MyList<int>(Name = 'Абракадабра';);

List<MyList<int>> l = new List<MyList<int>>();
l.Add(ints1);
l.Add(ints2);
listBa1.DateSource=l;
listBox1.DisplayMember = "Name";

```

# Статические члены обобщённых классов
```C#
public class MyList<T>{ //T - Tamplate - Темплейт
public double Id {get; set;}
public T? Name {get; set;}
public MyList(T name) => Name = name;
public override string ToString() {
return Name.ToString();
}
public static T? Description;
}

MyList<int>.Description = 123; // int это псевдоним int32
MyList<bool>.Description = true;
MyList<DateTime>.Description = new DateTime (21/10/2024) // для DateTime нет псевдонима, это класс 
```

Для каждого типа создаётся свой набор статических членов.

```C#
public class Person<P> {
private P? Lio;
public P? Fio {get; set;} // универсальный параметр м.б. возвращаемым типом для свойств
public Personality(P? name) => Fio = name;
}

Personality<string> p1 = new Personality<string>("Сидоров");
MyList<Personality<string>> l = new MyList<Personality<string>>(p1);
t1.Text = l.Name.Fio;
```
# Использование нескольких универсальных параметров
При инициализации шаблона универсальные параметры м.б. одного или разных типов.
```C#
public class MyList<K,T>{
public T? Name {get;set;}
public R? Code {get;set;}
public static string Description {get;set;} // неуниверсальное статическое свойство
public MyList(K? code,T? name) {
Name = name;
Code = code;
}
}

MyList<int,string> el1 = new MyList<int,string>(123, "Кот");
MyList<double,string> el2 = new MyList<double,string>(123.321, "Собака")
MyList<string,string> el3 = new MyList<string,string>("123.321", "Собака")
MyList<int,string>.Description = "lol"; // Что? 
```
# Обобщённые методы
Обобщённые методы используют универсальные параметры.
```C#
public class MyList<K,T>{
public T? Name {get;set;}
public R? Code {get;set;}
public static string Description {get;set;} // неуниверсальное статическое свойство
public MyList(K? code,T? name) {
Name = name;
Code = code;

public bool Egv<N,M>(N? x, M? y)
{ if (x.ToString().lenght == y.ToString().lenght) {return true;} //длины строчек
 else {return false;}
}
}

MyList<int,string> el1 = new MyList<int,string>(123, "1234");
t1.Text = el1.Egv<int, double>(123, 123.321).ToString(); // выведет false
```
Совпадать *** не обязаны, но нужно это пометить.
# Ограничения обобщений
Универсальные классы и универсальные методы м.б. ограничены определёнными типами (классами, структурами)
```C#
class Letter {}
class Email:Letter {}
class MyList<K,T> {
...
public void SendMsg<S>(S msg) where S:Letter {}
}
// тип ограничивающий - сам тип или его производные типы

cl1.SendMsg(new Letter());
cl1.SendMsg(new Email()));
cl1.SenMsg<Letter>(new Letter));

// ограничения для класса
class Discipline{}
class Prepod<T> where T:Discipline {
public List<T> discipline;
public Prepod(string n, int  kaf, List<T> dis){}
}

List<Discipline> Dis = new List<Discipline>();
for(int i = 0; i<listBox1.Items.Count; i++) {
	dis.Add(new Discipline((string) listbox1.Items[i]));
}
Prepod<Discipline> prep1 = new Prepod(t.Text, numericUpDown.Value, Dis);

```
# Наследование
## Оба типизированы одними и теми же типами.
```C#
class Emp<T>{
public T? Name{get;set;}
}
class Prepod<T>:Emp{
public T? ID;
public Prepod(T? ID):base(id){this.Id = id}
}
Emp<string> emp1 = new Emp<string>(t.Text);
Prepod<int> Prep1 = new Prepod<int>((int)t2.Text);
```
## Необобщённый класс наследник 
(<> - есть у родителя, но нет у наследника)
При создании иерархии, у базового класса нужно явно определить используемый тип.
```C#
public class Prepod:Emp<string>{
...
}
```
Базовый класс д.б. не универсальным. // да?
## Типизация дочернего класса параметром другого типа.
У базового класса типы надо определить явно.
```C#
public class Prepod<T>:Emp<int>{
...
}
Prepod<string> p = new Prepod<string>(...);
// Prepod<int> p = ... - тоже м.б.
```
## Сочетание
В классах наследниках могут сочетаться универсальные параметры базового класса и свои параметры.
```C#
public class Prepod<T,K>:Emp<T> where K:Coding{
...
}

Prepod<string, int> p = new Prepod("Добряк"<string, int> new Coding(...));
Emp<string> p1 = new Prepod<string, int>() // итд
```
