using System;

namespace Симулятор_Кота
{
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
    // абстракция + наследование
    public abstract class Питомец
    {
        public abstract void Notify(string message);
        public abstract void ОповеститьОГолоде();

    }
    // Кот — издатель
    public class Кот : Питомец, ISubject
    {
        private List<IObserver> _observers = new List<IObserver>();

        private static Кот _instance;
        private Кот() { }
        public static Кот GetInstance()
        {
            if (_instance == null)
                _instance = new Кот();

            return _instance;
        }

        public void Subscribe(IObserver observer)
        {
            _observers.Add(observer);
        }

        public void Unsubscribe(IObserver observer)
        {
            _observers.Remove(observer);
        }

        public override void Notify(string message)
        {
            foreach (var observer in _observers)
            {
                observer.Update(message);
            }
        }

        public override void ОповеститьОГолоде()
        {
            MessageBox.Show("Кот: Я голоден!");
            Notify("Кот голоден. Пора покормить.");
        }

        public void ОповеститьОЗакрытойДвери()
        {
            MessageBox.Show("Кот: Дверь закрыта!");
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
            MessageBox.Show($"{_имя} получила уведомление: {message}");
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
            MessageBox.Show($"{_имя} получил уведомление: {message}");
        }
    }
}