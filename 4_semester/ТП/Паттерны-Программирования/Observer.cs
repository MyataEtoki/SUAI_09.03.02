// See https://aka.ms/new-console-template for more information

using System;
using System.Collections.Generic;

// Интерфейс подписчика
public interface IObserver
{
    void Update(string message);
}

// Интерфейс издателя
public interface ISubject
{
    void Subscribe(IObserver observer);
    void Unsubscribe(IObserver observer);
    void Notify(string message);
}

// Кот — издатель
public class Кот : ISubject
{
    private List<IObserver> _observers = new List<IObserver>();

    public void Subscribe(IObserver observer)
    {
        _observers.Add(observer);
    }

    public void Unsubscribe(IObserver observer)
    {
        _observers.Remove(observer);
    }

    public void Notify(string message)
    {
        foreach (var observer in _observers)
        {
            observer.Update(message);
        }
    }

    public void ОповеститьОГолоде()
    {
        Console.WriteLine("Кот: Я голоден!");
        Notify("Кот голоден. Пора покормить.");
    }

    public void ОповеститьОЗакрытойДвери()
    {
        Console.WriteLine("Кот: Дверь закрыта!");
        Notify("Кот жалуется, что дверь закрыта.");
    }
}


// Жительница квартиры — подписчик
public class ЖительницаКвартиры : IObserver
{
    private string _имя;

    public ЖительницаКвартиры(string имя)
    {
        _имя = имя;
    }

    public void Update(string message)
    {
        Console.WriteLine($"{_имя} получила уведомление: {message}");
    }
}

// Жилец квартиры — подписчик
public class ЖилецКвартиры : IObserver
{
    private string _имя;

    public ЖилецКвартиры(string имя)
    {
        _имя = имя;
    }

    public void Update(string message)
    {
        Console.WriteLine($"{_имя} получил уведомление: {message}");
    }
}

// Пример использования
class Observer
{
    static void Main()
    {
        var кот = new Кот();

        var анна = new ЖительницаКвартиры("Анна");
        var борис = new ЖилецКвартиры("Борис");

        кот.Subscribe(анна);
        кот.Subscribe(борис);

        кот.ОповеститьОГолоде();
        Console.WriteLine();

        кот.ОповеститьОЗакрытойДвери();
        Console.WriteLine();

        кот.Unsubscribe(борис);
        кот.ОповеститьОГолоде();
    }
}
