using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace StavteClassy
{
    // В каждом районе есть 1 Школа, создаётся при создании Района - композиция.
    internal class Школа
    {
        private string название;
        public string Название {  get=> название; set => название = value; }
        public Школа(string название)
        {
            Название = название;
        }
    }
}
