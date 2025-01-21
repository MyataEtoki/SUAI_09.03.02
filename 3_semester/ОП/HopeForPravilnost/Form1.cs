using StavteClassy;
using System.Threading.Tasks.Sources;
using System.Windows.Forms;
namespace HopeForPravilnost
{
    public partial class Form1 : Form
    {
        private List<Государство> государства = new List<Государство>();
        private List<Область> области = new List<Область>();
        private List<Город> города = new List<Город>();
        private List<Район> районы = new List<Район>();

        public Form1()
        {
            InitializeComponent();
            comboBox1.Items.Add("Государство");
            comboBox1.Items.Add("Область");
            comboBox1.Items.Add("Город");
            comboBox1.Items.Add("Район");
            // Инициализация нескольких объектов государства для демонстрации
            var франция = new Государство(0, "Франция", 111);
            var испания = new Государство(1, "Испания") { ГодСоздания = 1211 };
            var лапландия = new Государство(2, "Лапландия");
            var россия = new Государство(3, "Россия") { ГодСоздания = 2222 };
            var шампань = new Область(0, "Шампань", франция);
            var ростовская = new Область(1, "Ростовская", россия);
            var мухоженуи = new Город(0, "Мухоженуи",шампань);
            var мухосранск = new Город(1, "Мухосранск",ростовская);
            var тринадцатый = new Район(0, "Тринадцатый", мухоженуи, 3, 2);
            // Заполнение информации о домах
            тринадцатый[0, 0] = "Хаус 1A"; // Улица 1, Дом 1
            тринадцатый[0, 1] = "Хаус 1B"; // Улица 1, Дом 2
            тринадцатый[1, 0] = "Хаус 2A"; // Улица 2, Дом 1
            тринадцатый[1, 1] = "Хаус 2B"; // Улица 2, Дом 2
            тринадцатый[2, 0] = "Хаус 3A"; // Улица 3, Дом 1

            var московский = new Район(1, "Московский", мухосранск, 2, 3);
            московский[0, 0] = "Дом 1A"; // Улица 1, Дом 1
            московский[0, 1] = "Дом 1B"; // Улица 1, Дом 2
            московский[1, 0] = "Дом 2A"; // Улица 2, Дом 1
            московский[1, 1] = "Дом 2B"; // Улица 2, Дом 2
            московский[1, 2] = "Дом 3A"; // Улица 2, Дом 1

            районы.Add(московский);
            районы.Add(тринадцатый);
            города.Add(мухоженуи);
            города.Add(мухосранск);
            области.Add(шампань);
            области.Add(ростовская);
            государства.Add(франция);
            государства.Add(испания);
            государства.Add(лапландия);
            государства.Add(россия);

            россия.ДобавитьОбласть(ростовская);
            ростовская.ДобавитьГород(мухосранск);
            мухосранск.ДобавитьРайон(московский);

            франция.ДобавитьОбласть(шампань);
            шампань.ДобавитьГород(мухоженуи);
            мухоженуи.ДобавитьРайон(тринадцатый);
            SetupListBox();

            //this.BackColor = Субъект.BackColor;
            if (DateTime.Now.DayOfWeek == DayOfWeek.Thursday || DateTime.Now.DayOfWeek == DayOfWeek.Tuesday)
            {
                this.BackColor = Color.MistyRose;
            }
            else
            {
                this.BackColor = Color.White;
            }

            numericUpDown1.Maximum = 2500;
        }

        private void SetupListBox()
        {
            // Привязка данных
            listBox1.DataSource = null;
            listBox1.DataSource = государства;
            listBox1.DisplayMember = "Название"; // Отображаем только название
            listBox2.DataSource = null;
            listBox2.DataSource = области;
            listBox2.DisplayMember = "Название";
            listBox3.DataSource = null;
            listBox3.DataSource = города;
            listBox3.DisplayMember = "Название";
            listBox4.DataSource = null;
            listBox4.DataSource = районы;
            listBox4.DisplayMember = "Название";

        }
        private bool ЗагрузитьДанные(string filePath, out int количествоЗаписей)
        {
            государства.Clear(); // очищаем коллекции перед загрузкой
            области.Clear();
            города.Clear();
            районы.Clear();

            количествоЗаписей = 0;

            if (File.Exists(filePath))
            {
                var lines = File.ReadAllLines(filePath);
                var stateMap = new Dictionary<int, Государство>(); // для привязки ID к Государству

                foreach (var line in lines)
                {
                    количествоЗаписей++;
                    var parts = line.Split(',');

                    if (parts.Length >= 2)
                    {
                        if (parts[0].Trim() == "Государство")
                        {
                            int id = int.Parse(parts[1].Trim());
                            string название = parts[2].Trim();
                            int годСоздания = int.Parse(parts[3].Trim());
                            var правитель = new Правитель
                            {
                                Имя = parts[4].Trim(),
                                Фамилия = parts[5].Trim(),
                                Отчество = parts[6].Trim(),
                                Возраст = int.Parse(parts[7].Trim()),
                                НачалоПравления = DateTime.Parse(parts[8].Trim())
                            };
                            string путьККартинке = parts.Length > 9 ? parts[9] : null;
                            var государство = new Государство(id, название, годСоздания)
                            {
                                ТекущийПравитель = правитель,
                                ПутьККартинке = путьККартинке
                            };
                            if (parts[4].Trim() != "") { государство.КтоТоПравит = true; }
                            государства.Add(государство);
                            stateMap[id] = государство; // запомнить ссылку на государство
                        }
                        else if (parts[0].Trim() == "Область")
                        {
                            int id = int.Parse(parts[1].Trim());
                            string название = parts[2].Trim();
                            int idГосударства = int.Parse(parts[3].Trim());

                            var область = new Область(id, название);
                            области.Add(область);

                            // Привязываем область к соответствующему государству
                            if (stateMap.TryGetValue(idГосударства, out var государство))
                            {
                                государство.ДобавитьОбласть(область);
                            }
                        }
                        else if (parts[0].Trim() == "Город")
                        {
                            int id = int.Parse(parts[1].Trim());
                            string название = parts[2].Trim();
                            int idОбласти = int.Parse(parts[3].Trim());

                            var город = new Город(id, название);
                            города.Add(город);

                            // Привязываем город к соответствующей области
                            var область = области.Find(o => o.ID == idОбласти);
                            область?.ДобавитьГород(город);
                        }
                        else if (parts[0].Trim() == "Район")
                        {
                            int id = int.Parse(parts[1].Trim());
                            string название = parts[2].Trim();
                            int idГорода = int.Parse(parts[3].Trim());

                            var район = new Район(id, название);
                            районы.Add(район);

                            // Привязываем район к соответствующему городу
                            var город = города.Find(g => g.ID == idГорода);
                            город?.ДобавитьРайон(район);
                        }
                    }
                }
                return true;
            }
            else
            {
                return false;
            }
        }



        // обращаемся к государству напрямую - через ref.
        private void ИзменитьНазвание(ref Государство государство, string новоеНазвание)
        {
            государство.Название = новоеНазвание;
        }
        private void button1_Click(object sender, EventArgs e) // кнопка - Поиск по ID
        {
            richTextBox1.Clear();
            // Получаем ID из numericUpDown
            int id = (int)numericUpDown1.Value;

            if (comboBox1.Text == "Государство")
            {

                // Поиск государства по ID
                Государство найденноеГосударство = государства.Find(g => g.ID == id);

                if (найденноеГосударство != null)
                {
                    richTextBox1.Text = найденноеГосударство.ПолучитьИнформацию();
                    //richTextBox1.Text = $"Государство: {найденноеГосударство.Название}, ID: {id}";
                    if (найденноеГосударство.ГодСоздания != 0)
                    {
                        richTextBox1.Text += $", Год создания: {найденноеГосударство.ГодСоздания}";
                        richTextBox1.Text += $", Возраст: {найденноеГосударство.ВычислитьВозраст()}";
                    }
                    richTextBox1.Text += найденноеГосударство.ПоказатьИнформациюОПравителе();

                    if (найденноеГосударство.ПутьККартинке != null)
                    {
                        pictureBox1.ImageLocation = найденноеГосударство.ПутьККартинке;
                    }
                    else { pictureBox1.ImageLocation = null; }

                }
                else
                {
                    richTextBox1.Text = $"Государство с ID {id} не найдено.";
                }
            }
            else if (comboBox1.Text == "Область")
            {

                // Поиск области по ID
                Область найденнаяОбласть = области.Find(g => g.ID == id);

                if (найденнаяОбласть != null)
                {
                    richTextBox1.Text = найденнаяОбласть.ПолучитьИнформацию();
                }
            }
            else if (comboBox1.Text == "Город")
            {
                Город найденныйГород = города.Find(g => g.ID == id);
                if (найденныйГород != null)
                {
                    richTextBox1.Text = найденныйГород.ПолучитьИнформацию();
                }
            }
            else if (comboBox1.Text == "Район")
            {
                Район найденныйРайон = районы.Find(g => g.ID == id);
                if (найденныйРайон != null)
                {
                    richTextBox1.Text = найденныйРайон.ПолучитьИнформацию();
                }
            }
        }

        private void button2_Click(object sender, EventArgs e) // кнопка - Создание государств
        {
            // Получаем значение ID и название
            int id = (int)numericUpDown2.Value; // явное преобразование
            string название = textBox2.Text;

            if (comboBox1.Text == "Государство")
            {
                // Проверка, существует ли уже государство с таким ID
                if (государства.Exists(g => g.ID == id))
                {
                    MessageBox.Show($"Государство с ID {id} уже существует. Пожалуйста, выберите другой ID.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                int _годСоздания = (int)numericUpDown4.Value;
                // Создание нового государства в списке
                Государство новоеГосударство = new Государство(id, название) { ГодСоздания = _годСоздания };
                государства.Add(новоеГосударство);

                // Выводим сообщение об успешном создании
                MessageBox.Show($"Государство '{название}' с ID {id} успешно создано!", "Успех", MessageBoxButtons.OK, MessageBoxIcon.Information);
                SetupListBox();

                // Очистка полей для ввода
                textBox2.Clear();
                numericUpDown1.Value = 0; // Сброс ID или установите его на значение по умолчанию
            }
            else if (comboBox1.Text == "Область")
            {

                // Проверка, существует ли уже субъект с таким ID
                if (области.Exists(o => o.ID == id))
                {
                    MessageBox.Show($"Область с ID {id} уже существует. Пожалуйста, выберите другой ID.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                /*Субъект новыйСубъект = new Область(id, название);
                Область новаяОбласть = (Область)новыйСубъект;*/
                if (государства.Exists(g => g.ID == (int)numericUpDown5.Value))
                {
                    Государство найденноеГосударство = государства.Find(g => g.ID == (int)numericUpDown5.Value);
                    Область новаяОбласть = new Область(id, название, найденноеГосударство);
                    области.Add(новаяОбласть);
                    найденноеГосударство.ДобавитьОбласть(новаяОбласть);
                }
                else { Область новаяОбласть = new Область(id, название); области.Add(новаяОбласть); }
                

                // Выводим сообщение об успешном создании
                MessageBox.Show($"Область '{название}' с ID {id} успешно создано!", "Успех", MessageBoxButtons.OK, MessageBoxIcon.Information);

                SetupListBox();
                // Очистка полей для ввода
                textBox2.Clear();
                numericUpDown1.Value = 0; // Сброс ID или установите его на значение по умолчанию
            }
            else if (comboBox1.Text == "Город")
            {
                // Проверка, существует ли уже государство с таким ID
                if (города.Exists(g => g.ID == id))
                {
                    MessageBox.Show($"Город с ID {id} уже существует. Пожалуйста, выберите другой ID.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                //Демонстрация явного-неявного преобразования
                Субъект новыйСубъект = new Город(id, название); // Неявное преобразование
                //новыйСубъект.ПутьККартинке = "\"C:\\Users\\etoki\\Pictures\\ну ничего полежу так часика 2 позагоняюсь поплачу а потом точно усну.jpg\"";
                //новыйСубъект.ВывестиКартинку(pictureBox1);
                MessageBox.Show($"Вы ввели данные: {новыйСубъект.ToString()}"); // так как new - скрытие - то метод вызывается из класса Субъект
                Город новыйГород = (Город)новыйСубъект; // явное преобразование
                MessageBox.Show($"На основе данных => {новыйГород.ToString()}"); // так как new - скрытие - то метод вызывается из класса Город

                if (области.Exists(o => o.ID == (int)numericUpDown5.Value))
                {
                    Область найденнаяОбласть = области.Find(o => o.ID == (int)numericUpDown5.Value);
                    Город реальноНовыйГород = new Город(id, название, найденнаяОбласть);
                    города.Add(реальноНовыйГород);
                    найденнаяОбласть.ДобавитьГород(реальноНовыйГород);
                }
                else { Город реальноНовыйГород = new Город(id, название); города.Add(реальноНовыйГород); }

                MessageBox.Show($"Город '{название}' с ID {id} успешно создано!", "Успех", MessageBoxButtons.OK, MessageBoxIcon.Information);
                SetupListBox();
                // Очистка полей для ввода
                textBox2.Clear();
                numericUpDown1.Value = 0; // Сброс ID или установите его на значение по умолчанию
            }
            else if (comboBox1.Text == "Район")
            {

                // Проверка, существует ли уже субъект с таким ID
                if (районы.Exists(g => g.ID == id))
                {
                    MessageBox.Show($"Район с ID {id} уже существует. Пожалуйста, выберите другой ID.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                if (города.Exists(g => g.ID == (int)numericUpDown5.Value))
                {
                    Город найденныйГород = города.Find(g => g.ID == (int)numericUpDown5.Value);
                    Район новыйРайон = new Район(id, название, найденныйГород);
                    районы.Add(новыйРайон);
                    найденныйГород.ДобавитьРайон(новыйРайон);
                }
                else {
                    Район новыйРайон = new Район(id, название);
                    районы.Add(новыйРайон);
                }                

                SetupListBox();
                // Очистка полей для ввода
                textBox2.Clear();
                numericUpDown1.Value = 0; // Сброс ID или установите его на значение по умолчанию
            }
        }

        private void button3_Click(object sender, EventArgs e) // кнопка - создать правителя
        {
            int id = (int)numericUpDown1.Value;
            Государство найденноеГосударство = государства.Find(g => g.ID == id);
            if (найденноеГосударство != null)
            {
                найденноеГосударство.УстановитьПравителя(textBox3.Text, textBox4.Text, textBox5.Text, (int)numericUpDown3.Value, DateTime.Now);
            }
        }

        //Загрузка БД
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
                    if (ЗагрузитьДанные(filePath, out int колЗаписей))
                    {
                        MessageBox.Show($"Успешно загружено {колЗаписей} записей.");
                    }
                    else
                    {
                        MessageBox.Show("Не удалось загрузить данные из файла.");
                    }
                    SetupListBox();
                }
            }
        }

        //Сохранение БД
        private void button5_Click(object sender, EventArgs e)
        {
            using (SaveFileDialog saveFileDialog = new SaveFileDialog())
            {
                saveFileDialog.Filter = "Text files (*.txt)|*.txt|All files (*.*)|*.*";
                saveFileDialog.Title = "Сохранить файл как";

                if (saveFileDialog.ShowDialog() == DialogResult.OK)
                {
                    string filePath = saveFileDialog.FileName;

                    using (StreamWriter writer = new StreamWriter(filePath))
                    {
                        foreach (var государство in государства)
                        {
                            // Сохраняем данные о государстве
                            writer.WriteLine($"Государство,{государство.ID},{государство.Название},{государство.ГодСоздания}," +
                                $"{государство.ТекущийПравитель.Имя},{государство.ТекущийПравитель.Фамилия}," +
                                $"{государство.ТекущийПравитель.Отчество},{государство.ТекущийПравитель.Возраст}," +
                                $"{государство.ТекущийПравитель.НачалоПравления},{государство.ПутьККартинке}");

                            // Сохраняем области
                            foreach (var область in государство.Области)
                            {
                                writer.WriteLine($"Область,{область.ID},{область.название},{государство.ID}");

                                // Сохраняем города
                                foreach (var город in область.Города)
                                {
                                    writer.WriteLine($"Город,{город.ID},{город.Название},{область.ID}");

                                    // Сохраняем районы
                                    foreach (var район in город.Районы)
                                    {
                                        writer.WriteLine($"Район,{район.ID},{район.Название},{город.ID}");
                                    }
                                }
                            }
                        }
                    }

                    MessageBox.Show("Данные успешно сохранены в файл.");
                }
            }
        }

        // Государство по-строчно (каждая строчка - переменная)
        private void button6_Click(object sender, EventArgs e)
        {
            Form2 form2 = new Form2();
            form2.Show();
        }
        // Добавление картинки
        private void button7_Click(object sender, EventArgs e)
        {
            int id = (int)numericUpDown1.Value;
            Государство найденноеГосударство = государства.Find(g => g.ID == id);
            using (OpenFileDialog openFileDialog = new OpenFileDialog())
            {
                openFileDialog.InitialDirectory = "C:\\";
                openFileDialog.Filter = "Image Files|*.jpg;*.jpeg;*.png;*.bmp|All Files|*.*";
                openFileDialog.Title = "Select an Image";

                if (openFileDialog.ShowDialog() == DialogResult.OK && найденноеГосударство != null)
                {
                    string imagePath = openFileDialog.FileName;
                    pictureBox1.ImageLocation = imagePath;
                    найденноеГосударство.ПутьККартинке = imagePath;
                }
            }
        }

        //Выбираешь страну в listBox1, она сразу ищется. ДОПОЛНИТЕЛЬНО
        private void listBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            richTextBox1.Clear();

            if (listBox1.SelectedItem != null)
            {
                // Получаем выбранное название из ListBox
                string название = listBox1.GetItemText(listBox1.SelectedItem);

                // Поиск государства по названию
                Государство найденноеГосударство = государства.Find(g => g.Название == название);

                if (найденноеГосударство != null)
                {
                    // Вывод информации о государстве
                    richTextBox1.Text = найденноеГосударство.ToString();

                    if (найденноеГосударство.ГодСоздания != 0)
                    {
                        richTextBox1.Text += $", Год создания: {найденноеГосударство.ГодСоздания}";
                        richTextBox1.Text += $", Возраст: {найденноеГосударство.ВычислитьВозраст()}";
                    }

                    // Перебираем районы с помощью индексатора
                    for (int i = 0; i < найденноеГосударство.Области.Count; i++)
                    {
                        richTextBox1.Text += $"\nОбласть {i + 1}: {найденноеГосударство[i].Название}\n";
                    }

                    richTextBox1.Text += найденноеГосударство.ПоказатьИнформациюОПравителе();

                    if (!string.IsNullOrEmpty(найденноеГосударство.ПутьККартинке))
                    {
                        pictureBox1.ImageLocation = найденноеГосударство.ПутьККартинке;
                    }
                    else
                    {
                        pictureBox1.ImageLocation = null;
                    }
                }
            }
        }

        // Изменить название государства - применение ref
        private void button8_Click(object sender, EventArgs e)
        {
            int id = (int)numericUpDown1.Value;
            Государство найденноеГосударство = государства.Find(g => g.ID == id);
            if (найденноеГосударство != null)
            {
                ИзменитьНазвание(ref найденноеГосударство, textBox6.Text);
            }
            SetupListBox();
        }

        // ListBoxs //
        private void listBox2_SelectedIndexChanged(object sender, EventArgs e) // listBox поиск Область
        {
            richTextBox1.Clear();

            if (listBox2.SelectedItem != null)
            {
                // Получаем выбранное название из ListBox2
                string название = listBox2.GetItemText(listBox2.SelectedItem);

                // Поиск области по названию
                Область найденнаяОбласть = области.Find(g => g.Название == название);

                if (найденнаяОбласть != null)
                {
                    // Вывод информации об области
                    richTextBox1.Text = найденнаяОбласть.ToString();
                    richTextBox1.Text += найденнаяОбласть.ГдеНаходится();

                    // Перебираем города с помощью индексатора
                    for (int i = 0; i < найденнаяОбласть.Города.Count; i++)
                    {
                        richTextBox1.Text += $"\nГород {i + 1}: {найденнаяОбласть[i].Название}";
                    }
                }
            }
        }

        private void listBox3_SelectedIndexChanged(object sender, EventArgs e) // listBox поиск Город
        {
            if (listBox3.SelectedItem != null)
            {
                // Получаем выбранное название из ListBox2
                string название = listBox3.GetItemText(listBox3.SelectedItem);

                // Поиск города по названию
                Город найденныйГород = города.Find(g => g.Название == название);

                if (найденныйГород != null)
                {
                    // Вывод информации о городе
                    richTextBox1.Text = $"ID: {найденныйГород.ID}, Название: {найденныйГород.Название}";
                    richTextBox1.Text += найденныйГород.ГдеНаходится();

                    // Перебираем районы с помощью индексатора
                    for (int i = 0; i < найденныйГород.Районы.Count; i++)
                    {
                        richTextBox1.Text += $"\nРайон {i + 1}: {найденныйГород[i].Название}";
                    }
                }
            }

        }

        private void listBox4_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (listBox4.SelectedItem != null)
            {
                // Получаем выбранное название из ListBox2
                string название = listBox4.GetItemText(listBox4.SelectedItem);

                // Поиск района по названию
                Район найденныйРайон = районы.Find(g => g.Название == название);

                if (найденныйРайон != null)
                {
                    // Вывод информации о районе
                    richTextBox1.Text = найденныйРайон.ToString();
                    richTextBox1.Text += найденныйРайон.ГдеНаходится();
                    richTextBox1.Text += найденныйРайон.ВывестиУлицы();
                }
            }
        }

        // Табличка района в пикчюр бокс
        private void button9_Click(object sender, EventArgs e)
        {
            // Проверяем, выбран ли район в listBox4
            if (listBox4.SelectedItem != null)
            {
                // Получаем выбранный район
                string названиеРайона = listBox4.GetItemText(listBox4.SelectedItem);
                Район выбранныйРайон = районы.Find(r => r.Название == названиеРайона);

                if (выбранныйРайон != null)
                {
                    // Вызываем метод NameText и передаем pictureBox1 для отображения текста
                    выбранныйРайон.NameText(pictureBox1);
                }
            }
        }
        // Очистить пикчюр бокс от района
        private void button10_Click(object sender, EventArgs e)
        {
            pictureBox1.Image = null;
        }

        // Устроить революцию - удаление правителя с событием
        private void Государство_ПравителяНет(string сообщение) // Обработчик события
        {
            MessageBox.Show(сообщение, "Сообщение о революции", MessageBoxButtons.OK, MessageBoxIcon.Information);

            // обновляем состояние безопасности районов
            var id = (int)numericUpDown1.Value;
            Государство найденноеГосударство = государства.Find(g => g.ID == id);

            if (найденноеГосударство != null)
            {
                foreach (var область in найденноеГосударство.Области)
                {
                    foreach (var город in область.Города)
                    {
                        foreach (var район in город.Районы)
                        {
                            if (район != null)
                            {
                                район.БезопасностьИзменилась -= Район_СостояниеИзменилось;
                                район.БезопасностьИзменилась += Район_СостояниеИзменилось;
                                район.СостояниеБезопасности = "Опасный";
                            }
                        }
                    }
                }
            }
        }


        private void button11_Click(object sender, EventArgs e) // кнопка - устроить революцию
        {
            int id = (int)numericUpDown1.Value;
            Государство найденноеГосударство = государства.Find(g => g.ID == id);

            if (найденноеГосударство != null)
            {
                найденноеГосударство.ПравителяНет -= Государство_ПравителяНет; // отписка, чтобы избежать повтора
                найденноеГосударство.ПравителяНет += Государство_ПравителяНет; // подписка на событие
                найденноеГосударство.Революция(); // вызываем революцию
            }
        }
        // Блок с событиями - изменения состояния безопасности Района
        private void button12_Click(object sender, EventArgs e) // кнопка - проверить опасность района
        {
            int id = (int)numericUpDown1.Value;
            Район найденныйСубъект = районы.Find(g => g.ID == id);

            if (найденныйСубъект != null)
            {
                MessageBox.Show($"Состояние района '{найденныйСубъект.Название}': '{найденныйСубъект.СостояниеБезопасности}'.",
                            "Проверка состояния",
                            MessageBoxButtons.OK,
                            MessageBoxIcon.Information);
            }
        }
        private void Район_СостояниеИзменилось(object sender, БезопасностьИзмениласьEventArgs e)
        {
            MessageBox.Show($"Состояние района '{e.НазваниеРайона}' изменилось на '{e.НовоеСостояние}'.",
                            "Изменение состояния",
                            MessageBoxButtons.OK,
                            MessageBoxIcon.Information);
        }
        private void button13_Click(object sender, EventArgs e) // кнопка - сделать район опасным
        {
            int id = (int)numericUpDown1.Value;
            Район найденныйСубъект = районы.Find(g => g.ID == id);

            if (найденныйСубъект != null)
            {
                найденныйСубъект.БезопасностьИзменилась -= Район_СостояниеИзменилось;
                найденныйСубъект.БезопасностьИзменилась += Район_СостояниеИзменилось;
                найденныйСубъект.СостояниеБезопасности = "Опасный";
            }
            
        }

        private void button14_Click(object sender, EventArgs e) // кнопка - сделать район безопасным
        {
            int id = (int)numericUpDown1.Value;
            Район найденныйСубъект = районы.Find(g => g.ID == id);

            if (найденныйСубъект != null)
            {
                найденныйСубъект.БезопасностьИзменилась -= Район_СостояниеИзменилось;
                найденныйСубъект.БезопасностьИзменилась += Район_СостояниеИзменилось;
                найденныйСубъект.СостояниеБезопасности = "Безопасный";
            }
        }
    }
}
