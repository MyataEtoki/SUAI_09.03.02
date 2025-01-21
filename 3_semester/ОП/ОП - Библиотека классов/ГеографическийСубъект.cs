using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace StavteClassy
{
    public abstract class ГеографическийСубъект // Переименовать на Субъект
    {
        public int ID { get; set; }
        public abstract string Название { get; set; }

        protected ГеографическийСубъект(int id, string название)
        {
            ID = id;
            Название = название;
        }

        public override string ToString()
        {
            return $"Название: {Название}, ID: {ID}";
        }

        public abstract string ПолучитьИнформацию();
    }
}
