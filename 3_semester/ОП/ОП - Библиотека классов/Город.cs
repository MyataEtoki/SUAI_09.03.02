using StavteClassy;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace StavteClassy
{
    // Интерфейс - поведение класса Город
    public interface IГород
    {
        void ДобавитьРайон(Район район);
    }

    public sealed class Город : Субъект, IГород
    {
        public List<Район> Районы; // ассоциация

        // Индексатор для доступа к районам по индексу
        public Район this[int index]
        {
            get
            {
                if (index >= 0 && index < Районы.Count)
                    return Районы[index];
                throw new ArgumentOutOfRangeException(nameof(index), "Индекс вне диапазона");
            }
        }
        Область ОбластьВКоторойНаходится;
        public Город(int id, string название) : base(id, название) // метод-конструктор
        {
            Районы = new List<Район>(); // композиция
        }
        public Город(int id, string название, Область область) : base(id, название) // метод-конструктор
        {
            Районы = new List<Район>(); // композиция
            ОбластьВКоторойНаходится = область; // агрегация
        }

        public void ДобавитьРайон(Район район)
        {
            Районы.Add(район);
        }
        public string ГдеНаходится()
        {
            if (ОбластьВКоторойНаходится != null)
            {
                return $"\nНаходится в области: {ОбластьВКоторойНаходится.Название}";
            }
            else { return ""; }
        }
        public override string ПолучитьИнформацию()
        {
            var информация = base.ПолучитьИнформацию(); // Получаем информацию от базового класса
            информация += ", Районы: " + (Районы != null ? Районы.Count.ToString() : "0"); // Информация о районах
            return информация;
        }
        // Сокрытие метода
        public new string ToString()
        {
            return $"Был создан новый субъект: {Название}";
        }

    }
}
