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
        private List<IObserver> owners = new List<IObserver>();

        private static Кот cat_exist;
        private Кот() { }
        public static Кот Take_cat()
        {
            if (cat_exist == null)
                cat_exist = new Кот();

            return cat_exist;
        }

        public void Subscribe(IObserver observer)
        {
            owners.Add(observer);
        }

        public void Unsubscribe(IObserver observer)
        {
            owners.Remove(observer);
        }

        public override void Notify(string message)
        {
            foreach (var observer in owners)
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


    // Жительница квартиры — подписчик - женский пол
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

    // Жилец квартиры — подписчик - мужской пол
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