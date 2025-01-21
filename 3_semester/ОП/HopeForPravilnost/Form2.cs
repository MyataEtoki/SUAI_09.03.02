using StavteClassy;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

namespace HopeForPravilnost
{
    public partial class Form2 : Form
    {
        private List<Государство> государства = new List<Государство>();
        public Form2()
        {
            InitializeComponent();
            numericUpDown1.Maximum = 2500;
        }
        private void SetupListBox()
        {
            // Привязка данных
            listBox1.DataSource = null;
            listBox1.DataSource = государства; // Установка источника данных
            listBox1.DisplayMember = "Название"; // Отображаем только название

            // Установка привязки для текстовых полей
            textBox1.DataBindings.Clear();
            textBox1.DataBindings.Add("Text", государства, "Название");

            numericUpDown1.DataBindings.Clear();
            numericUpDown1.DataBindings.Add("Text", государства, "ГодСоздания");

            checkBox1.DataBindings.Clear();
            checkBox1.DataBindings.Add("Checked", государства, "КтоТоПравит");
        }
        private void button4_Click(object sender, EventArgs e)
        {
            using (OpenFileDialog openFileDialog = new OpenFileDialog())
            {
                openFileDialog.Filter = "Text files (*.txt)|*.txt|All files (*.*)|*.*";
                openFileDialog.Title = "Выберите файл для загрузки";

                if (openFileDialog.ShowDialog() == DialogResult.OK)
                {
                    string filePath = openFileDialog.FileName;

                    // Очищаем коллекцию перед загрузкой
                    государства.Clear();

                    // Загружаем данные из файла
                    if (File.Exists(filePath))
                    {
                        var lines = File.ReadAllLines(filePath);
                        foreach (var line in lines)
                        {
                            var parts = line.Split(',');

                            // Создаем новый объект Государства
                            var государство = new Государство(int.Parse(parts[0].Trim()), parts[1].Trim());
                            //государство.ID = int.Parse(parts[0].Trim());
                            if (parts.Length > 2)
                                государство.ГодСоздания = int.Parse(parts[2].Trim());

                            if (parts.Length > 3) // если есть данные о правителе
                            {
                                var правитель = new Правитель
                                {
                                    Имя = parts[3].Trim(),
                                    Фамилия = parts[4].Trim(),
                                    Отчество = parts[5].Trim(),
                                    Возраст = int.Parse(parts[6].Trim()),
                                    НачалоПравления = DateTime.Parse(parts[7].Trim()),
                                    Существует = true,
                                };

                                государство.ТекущийПравитель = правитель;
                                государство.КтоТоПравит = true;
                            }

                            государства.Add(государство);
                        }

                    }
                    else
                    {
                        MessageBox.Show("Файл не найден.");
                    }
                    SetupListBox();
                }
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (listBox1.SelectedItem != null)
            {
                using (OpenFileDialog openFileDialog = new OpenFileDialog())
                {
                    openFileDialog.InitialDirectory = "C:\\";
                    openFileDialog.Filter = "Image Files|*.jpg;*.jpeg;*.png;*.bmp|All Files|*.*";
                    openFileDialog.Title = "Select an Image";

                    if (openFileDialog.ShowDialog() == DialogResult.OK)
                    {
                        (listBox1.SelectedItem as Субъект).ПутьККартинке = openFileDialog.FileName;
                        (listBox1.SelectedItem as Субъект).ВывестиКартинку(pictureBox1);
                    }
                }
            }
            else { MessageBox.Show("Загрузите данные."); }
        }
        private void button2_Click(object sender, EventArgs e)
        {
            if (listBox1.SelectedItem != null)
            {
            using (OpenFileDialog openFileDialog = new OpenFileDialog())
            {
                
                    openFileDialog.InitialDirectory = "C:\\";
                    openFileDialog.Filter = "Image Files|*.jpg;*.jpeg;*.png;*.bmp|All Files|*.*";
                    openFileDialog.Title = "Select an Image";

                    if (openFileDialog.ShowDialog() == DialogResult.OK)
                    {
                        (listBox1.SelectedItem as Субъект).ПутьККартинке = openFileDialog.FileName;
                        (listBox1.SelectedItem as Субъект).ВывестиКартинку(ActiveForm);
                    }
                }
            }
            else { MessageBox.Show("Загрузите данные."); }
        }
    }
}
