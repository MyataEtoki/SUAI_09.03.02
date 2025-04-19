using System.Windows.Forms;

namespace Симулятор_Кота
{
    public partial class Form1 : Form
    {
        Кот кот = Кот.GetInstance();        

        ЖительницаКвартиры мама = new ЖительницаКвартиры("Анна");
        ЖилецКвартиры папа = new ЖилецКвартиры("Борис");

        public Form1()
        {

            InitializeComponent();

        }
        private void Form1_Load(object sender, EventArgs e)
        {
        }

        // Функции кота
        private void btn_food_Click(object sender, EventArgs e)
        {
            кот.ОповеститьОГолоде();
        }

        private void btn_door_Click(object sender, EventArgs e)
        {
            кот.ОповеститьОЗакрытойДвери();
        }

        // МАМА
        private void btn_subscribe_mom_Click(object sender, EventArgs e)
        {
            кот.Subscribe(мама);
        }

        private void btn_Unsubscribe_mom_Click(object sender, EventArgs e)
        {
            кот.Unsubscribe(мама);
        }

        // ПАПА
        private void btn_subscribe_dad_Click(object sender, EventArgs e)
        {
            кот.Subscribe(папа);
        }

        private void btn_Unsubscribe_dad_Click(object sender, EventArgs e)
        {
            кот.Unsubscribe(папа);
        }

        private void btn_singleton_Click(object sender, EventArgs e)
        {
            Кот новыйКот = Кот.GetInstance();
            if (кот == новыйКот)
            {
                MessageBox.Show("Мы выгнали старого кота и взяли нового, но это оказался тот же кот. Нам от него не избавиться...");
            }
            else
            {
                MessageBox.Show("Получилось, у нас новый кот!");
            }
        }
    }
}
