# Теория
События позволяют сообщить о ситуациях другим.
Источник события comboBox1
Объекты, порождающие/генерирующие событие - отправители/издатели
Кто принимает событие - подписчик.
В VS - значок молнии в свойствах элемента интерфейса.

```C#
private void com1.SelfIndex(Object sender, EventArgs e){
e.
}
```
## 1. Подписка на событие
Не видим, но пишется автоматически.
 ```C#
 this.comboBox1.SelectedIndexChange += new System.EventHandler(this.comboBox1.SelectedIndexChange)
```
comboBox1 - издатель
System.EventHandler - делегат - delegate
this - обработчик (подписчик) - в данном случае форма.
Если -=, то это отписка.
## 2. Базовые классы событий
Издатель публикует или генерирует событие. Обработчик определяет ответное действие. У любого события м.б. любое кол-во подписчиков.
В .NET для событий имеются базовые классы:
1) System.EventArgs - хранит данные о событии.
Они могут быть в конкретных событиях расширены.
2) System.EvetHandler - delegate
## 3. Delegate
Протокол, обязательный к исполнению, будущего взаимодействия события и его обработчика.
Тип, сигнатура которого определяет сигнатуру обработчика событий - подписчиков.
Для события делегат должен чётко прописать возвращаемое значение и ***
Delegate могут быть как статические, так и динамические методы.
Принято к названию делегата дописывать "Handler" - дрессировщик, обработчик, чтобы действия делегата выполнялись по протоколу.
# Пример
Библиотека классов:
```C#
class Emp{
public DateTime Birth {get; set;}
// delegate - тип, определяющий событие.
public delegate void BirthHandler(string msg);
public event BrithHandler Note; 
// метод в котором м.б. сгенерировано событие
public int HowOld(){
if (DateTime.Now.Month == this.Birth.Month && DateTime.Now.Day == this.Birth.Day) {
Note.Invote("С др, братан!"); //генерируем событие, записываем информацию
}//это только, если подписались на Note.
return DateTime.Now.Year - this.Birth.Year
}
}

public class EmpEventArgs:EventArgs{
public string msg{get;}
public int Old{get;}
public EmpEventArgs(int old, string msg):base(){
this.Msg = msg;
this.Old = old;
}
// изменяем делегат
public delegate void BithHandler(object sender, EmpEventArgs e);
// отправитель sender - любой объект
// изменяем метод, вызывающий событие Invote
public int HowOld(){
if (DateTime.Now.Month == this.Birth.Month && DateTime.Now.Day == this.Birth.Day) {
Note.Invote(this, new EmpEventArgs(DateTime.Now.Year - this.Birth.Year, "С др, братан!")) // кто послал, что послал
}
}

}
```
Форма:
```C#
// статический обработчик события
private static void Message(string m){
messageBox.Show(m);
} // сигнатура от делегата

private static void Message(object sender, EmpEventArgs e){
// делаем то, чего мы хотим делать
messageBox.Show(e.message + e.Old);
}

// ещё один обработчик для Note
private void Congratulation(object sender, EmpEventArgs e){
pictureBox1.Image = ImageFromFile("...");
}

// подписываемся:
Emp emp1 = new Emp(...);
// хотим про Emp1 знать день рождение, чтобы поздравлять.
emp1.Note += Message; // подписались
t1.Text = emp1.HowOld().ToString();

emp1.Note -= Message; // отписались
```
Событие - это круто, потому что в контексте он дохуя всего сохраняет.
Если событие содержит данные, которые нужно сохранить, то нужно создать класс-наследник *блаблабла*.

# Организация списка обработчика событий.
MgEvent⚡ => Method1 => Method3

*блаблабла*

# Ещё теория
Модификаторы событий - уровни доступа - любые
М.б. virtual, override, sealed итд
События могут перекрывать события с таким же именем.
М.б. статичными, но тип события = тип делегата.
Делегаты многоадресные - там много ссылок м.б. на *блаблабла*
