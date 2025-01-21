namespace HopeForPravilnost
{
    partial class Form2
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            label1 = new Label();
            textBox1 = new TextBox();
            label2 = new Label();
            button4 = new Button();
            label13 = new Label();
            listBox1 = new ListBox();
            numericUpDown1 = new NumericUpDown();
            checkBox1 = new CheckBox();
            pictureBox1 = new PictureBox();
            button1 = new Button();
            button2 = new Button();
            ((System.ComponentModel.ISupportInitialize)numericUpDown1).BeginInit();
            ((System.ComponentModel.ISupportInitialize)pictureBox1).BeginInit();
            SuspendLayout();
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(692, 74);
            label1.Name = "label1";
            label1.Size = new Size(120, 32);
            label1.TabIndex = 0;
            label1.Text = "Название";
            // 
            // textBox1
            // 
            textBox1.Location = new Point(692, 109);
            textBox1.Name = "textBox1";
            textBox1.Size = new Size(200, 39);
            textBox1.TabIndex = 1;
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(692, 151);
            label2.Name = "label2";
            label2.Size = new Size(160, 32);
            label2.TabIndex = 2;
            label2.Text = "Год создания";
            // 
            // button4
            // 
            button4.Location = new Point(51, 92);
            button4.Name = "button4";
            button4.Size = new Size(150, 115);
            button4.TabIndex = 32;
            button4.Text = "Загрузить данные";
            button4.UseVisualStyleBackColor = true;
            button4.Click += button4_Click;
            // 
            // label13
            // 
            label13.AutoSize = true;
            label13.Location = new Point(254, 9);
            label13.Name = "label13";
            label13.Size = new Size(121, 32);
            label13.TabIndex = 31;
            label13.Text = "Cубъекты";
            // 
            // listBox1
            // 
            listBox1.FormattingEnabled = true;
            listBox1.Location = new Point(254, 44);
            listBox1.Name = "listBox1";
            listBox1.Size = new Size(389, 228);
            listBox1.TabIndex = 30;
            // 
            // numericUpDown1
            // 
            numericUpDown1.Location = new Point(692, 186);
            numericUpDown1.Name = "numericUpDown1";
            numericUpDown1.Size = new Size(200, 39);
            numericUpDown1.TabIndex = 33;
            // 
            // checkBox1
            // 
            checkBox1.AutoSize = true;
            checkBox1.Location = new Point(692, 236);
            checkBox1.Name = "checkBox1";
            checkBox1.Size = new Size(164, 36);
            checkBox1.TabIndex = 35;
            checkBox1.Text = "Правитель";
            checkBox1.UseVisualStyleBackColor = true;
            // 
            // pictureBox1
            // 
            pictureBox1.Location = new Point(254, 337);
            pictureBox1.Name = "pictureBox1";
            pictureBox1.Size = new Size(389, 356);
            pictureBox1.TabIndex = 36;
            pictureBox1.TabStop = false;
            // 
            // button1
            // 
            button1.Location = new Point(32, 337);
            button1.Name = "button1";
            button1.Size = new Size(169, 46);
            button1.TabIndex = 37;
            button1.Text = "Картинка >>";
            button1.UseVisualStyleBackColor = true;
            button1.Click += button1_Click;
            // 
            // button2
            // 
            button2.Location = new Point(32, 414);
            button2.Name = "button2";
            button2.Size = new Size(169, 46);
            button2.TabIndex = 38;
            button2.Text = "< Фон >";
            button2.UseVisualStyleBackColor = true;
            button2.Click += button2_Click;
            // 
            // Form2
            // 
            AutoScaleDimensions = new SizeF(13F, 32F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(963, 748);
            Controls.Add(button2);
            Controls.Add(button1);
            Controls.Add(pictureBox1);
            Controls.Add(checkBox1);
            Controls.Add(numericUpDown1);
            Controls.Add(button4);
            Controls.Add(label13);
            Controls.Add(listBox1);
            Controls.Add(label2);
            Controls.Add(textBox1);
            Controls.Add(label1);
            Name = "Form2";
            Text = "Государство по-строчно";
            ((System.ComponentModel.ISupportInitialize)numericUpDown1).EndInit();
            ((System.ComponentModel.ISupportInitialize)pictureBox1).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label label1;
        private TextBox textBox1;
        private Label label2;
        private Button button4;
        private Label label13;
        private ListBox listBox1;
        private NumericUpDown numericUpDown1;
        private Label label3;
        private TextBox textBox2;
        private TextBox textBox3;
        private TextBox textBox4;
        private DateTimePicker dateTimePicker1;
        private CheckBox checkBox1;
        private PictureBox pictureBox1;
        private Button button1;
        private Button button2;
    }
}