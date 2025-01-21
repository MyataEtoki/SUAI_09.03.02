using StavteClassy;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace StavteClassy
{
    // Интерфейс - поведение класса Район
    public interface IРайон
    {
        string ВывестиУлицы();
        void NameText(PictureBox box);
    }
    public sealed class Район : Субъект, IРайон
    {
        private string[,] дома; // 2D массив для хранения информации о домах
        private int улицы; // Количество улиц
        private int домаНаУлице; // Количество домов на каждой улице
        Школа школарайона;
        public Район(int id, string название, int улицы = 0, int домаНаУлице = 0) : base(id, название)
        {
            //тут мз субъекта подтянулось - id = id, название = название
            this.улицы = улицы;
            this.домаНаУлице = домаНаУлице;
            дома = new string[улицы, домаНаУлице]; // Инициализация двумерного массива
            школарайона = new Школа($"{название}ская"); // Композиция
        }
        Город ГородВКоторомНаходится;
        public Район(int id, string название, Город город, int улицы = 0, int домаНаУлице = 0) : base(id, название)
        {
            //тут мз субъекта подтянулось - id = id, название = название
            this.улицы = улицы;
            this.домаНаУлице = домаНаУлице;
            дома = new string[улицы, домаНаУлице]; // Инициализация двумерного массива
            школарайона = new Школа($"{название}ская"); // Композиция
            ГородВКоторомНаходится = город; // агрегация
        }

        // Демонстрация полиморфизма - переопределение метода
        public override string ToString()
        {
            return $"ID: {ID}, Район: {Название}, Мы подошли из-за угла. \nВ районе действует школа под названием {школарайона.Название}";
        }
        public string ГдеНаходится()
        {
            if (ГородВКоторомНаходится != null)
            {
                return $"\nНаходится в городе: {ГородВКоторомНаходится.Название}";
            }
            else { return ""; }
        }

        // Индексатор для доступа к домам по улице и номеру дома
        public string this[int улица, int номерДома]
        {
            get
            {
                if (улица < 0 || улица >= улицы || номерДома < 0 || номерДома >= домаНаУлице)
                    throw new IndexOutOfRangeException("Индекс вне диапазона массива.");

                return дома[улица, номерДома];
            }
            set
            {
                if (улица < 0 || улица >= улицы || номерДома < 0 || номерДома >= домаНаУлице)
                    throw new IndexOutOfRangeException("Индекс вне диапазона массива.");

                дома[улица, номерДома] = value;
            }
        }

        // Метод для вывода информации о всех домах
        public string ВывестиУлицы()
        {
            // Инициализация результатирующей строки
            StringBuilder result = new StringBuilder();
            for (int i = 0; i < улицы; i++)
            {
                result.Append($"\nУлица {i + 1}: ");
                for (int j = 0; j < домаНаУлице; j++)
                {
                    result.Append($" {дома[i, j]}");
                }
            }
            return result.ToString(); // Возвращаем преобразованную строку
        }

        // Метод - Табличка района
        public void NameText(PictureBox box)
        {
            using (FontDialog fontDialog = new FontDialog())
            using (ColorDialog colorDialog = new ColorDialog())
            {
                // Открытие диалоговых окон для выбора шрифта и цвета
                if (fontDialog.ShowDialog() == DialogResult.OK &&
                    colorDialog.ShowDialog() == DialogResult.OK)
                {
                    // Получаем выбранный шрифт и цвет
                    Font currFont = fontDialog.Font;
                    Color textColor = colorDialog.Color;

                    // Используем Graphics для отрисовки текста
                    using (Graphics g = box.CreateGraphics())
                    {
                        // Используем Brush с выбранным цветом
                        using (Brush brush = new SolidBrush(textColor))
                        {
                            g.DrawString(this.Название, currFont, brush, new PointF(1, 1));
                        }
                    }
                }
            }
        }
        

        // Событие БезопасностьИзменилась
        private string безопасность = "Undefined";

        public string СостояниеБезопасности
        {
            get { return безопасность; }
            set
            {
                if (безопасность != value)
                {
                    безопасность = value;
                    OnБезопасностьИзменилась(new БезопасностьИзмениласьEventArgs(Название, безопасность));
                }
            }
        }

        public event БезопасностьИзмениласьEventHandler БезопасностьИзменилась;

        public void OnБезопасностьИзменилась(БезопасностьИзмениласьEventArgs e)
        {
            БезопасностьИзменилась?.Invoke(this, e);
        }
    }

    // Событие БезопасностьИзменилась - СостояниеБезопасности
    public delegate void БезопасностьИзмениласьEventHandler(object sender, БезопасностьИзмениласьEventArgs e);
    public class БезопасностьИзмениласьEventArgs : EventArgs
    {
        public string НазваниеРайона { get; }
        public string НовоеСостояние { get; }

        public БезопасностьИзмениласьEventArgs(string названиеРайона, string новоеСостояние)
        {
            НазваниеРайона = названиеРайона;
            НовоеСостояние = новоеСостояние;
        }
    }
}
