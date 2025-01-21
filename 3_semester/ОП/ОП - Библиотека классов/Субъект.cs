using System;
using System.Collections.Generic;
using System.Drawing;
using System.Xml.Linq;
using System.Windows.Forms;
using System.Security.Cryptography.X509Certificates;
using System.Text;


namespace StavteClassy
{
    
    public delegate void Образование(string сообщение);
    public class Субъект : ГеографическийСубъект // Перемеиновать на Общество
    {
        //public int ID;
        public string название = "Undefined";
        public override string Название
        {
            get => название;
            set
            {
                if (!string.IsNullOrEmpty(value))
                {
                    название = value;
                }
            }
        }

        public event Образование? Образовалось;

        public Субъект(int id, string название) : base(id, название)
        {
            Название = название;
            ID = id;
            Образовалось?.Invoke($"Создан субъект {название}, его ID {id}");
        }

        public override string ПолучитьИнформацию()
        {
            return ToString(); // Вызов ToString из базового класса для основных данных
        }

        public string ПутьККартинке { get; set; }
        public void ВывестиКартинку(PictureBox box)
        {
            box.Image = Image.FromFile(ПутьККартинке);
        }
        public void ВывестиКартинку(Form form)
        {
            form.BackgroundImage = Image.FromFile(ПутьККартинке);
        }

        /* public static readonly Color BackColor;
        static Субъект() // статический конструктор 
        {
            DateTime now = DateTime.Now;
            if (now.DayOfWeek == DayOfWeek.Thursday || now.DayOfWeek == DayOfWeek.Tuesday)
            {
                Субъект.BackColor = Color.MistyRose;
            }
            else
            {
                Субъект.BackColor = Color.White;
            }
        }*/
    }
}
