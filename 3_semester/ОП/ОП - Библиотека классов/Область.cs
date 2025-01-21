using StavteClassy;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace StavteClassy
{
    // Интерфейс - поведение класса Область
    public interface IОбласть
    {
        void ДобавитьГород(Город город);
        void УдалитьГород(Город город);
        string ПолучитьСписокГородов();
    }

    public sealed class Область : Субъект, IОбласть
    {
        public List<Город> Города; // ассоциация

        // Индексатор для доступа к городам по индексу
        public Город this[int index]
        {
            get
            {
                if (index >= 0 && index < Города.Count)
                    return Города[index];
                throw new ArgumentOutOfRangeException(nameof(index), "Индекс вне диапазона");
            }
        }

        public new string Название
        {
            get => $"{base.Название} обл.";
            set => base.Название = value;
        }
        public Область(int id, string название) : base(id, название)
        {
            Города = new List<Город>(); // композиция
        }
        Государство ГосударствоВКоторомНаходится; // агрегация
        public Область(int id, string название, Государство государство) : base(id, название)
        {
            Города = new List<Город>(); // композиция
            ГосударствоВКоторомНаходится = государство; // агрегация
        }

        public void ДобавитьГород(Город город) 
        {
            Города.Add(город);
        }
        public void УдалитьГород(Город город) 
        {
            Города.Remove(город);
        }

        public override string ПолучитьИнформацию()
        {
            var информация = base.ПолучитьИнформацию(); // Получаем информацию от базового класса
            информация += $", Города: {Города.Count}"; // Информация о городах, содержащихся в области
            return информация;
        }

        public string ПолучитьСписокГородов()
        {
            return string.Join(", ", Города.Select(город => город.Название));
        }
        public override string ToString()
        {
            return $"ID: {ID}, Название: {Название}, Областной центр не ищите.";
        }

        public string ГдеНаходится()
        {
            if (ГосударствоВКоторомНаходится != null)
            {
                return $"\nНаходится в стране: {ГосударствоВКоторомНаходится.Название}";
            }
            else { return ""; }
        }

        /* public static Область ИзСубъект(Субъект субъект)
        {
            return new Область(субъект.Название)
            {
                ID = субъект.ID
            };
        } */
    }
}
