using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Паттерны_Проектирования;
using Паттерны_Проектирования.model;
using System.Windows.Forms;

namespace Паттерны_Проектирования.presenter
{
    public class MainPresenter
    {
        private IFormView view;
        //private Db db;
        public MainPresenter(IFormView view)
        {
            this.view = view;
            //db = new Db();
        }
    }
}
