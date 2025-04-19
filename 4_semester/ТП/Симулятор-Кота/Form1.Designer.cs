namespace Симулятор_Кота
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
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
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            btn_food = new Button();
            btn_door = new Button();
            btn_subscribe_mom = new Button();
            btn_subscribe_dad = new Button();
            btn_Unsubscribe_dad = new Button();
            btn_Unsubscribe_mom = new Button();
            btn_singleton = new Button();
            SuspendLayout();
            // 
            // btn_food
            // 
            btn_food.Location = new Point(34, 72);
            btn_food.Name = "btn_food";
            btn_food.Size = new Size(287, 46);
            btn_food.TabIndex = 1;
            btn_food.Text = "Возжелать покушать";
            btn_food.UseVisualStyleBackColor = true;
            btn_food.Click += btn_food_Click;
            // 
            // btn_door
            // 
            btn_door.Location = new Point(34, 136);
            btn_door.Name = "btn_door";
            btn_door.Size = new Size(287, 82);
            btn_door.TabIndex = 2;
            btn_door.Text = "Возмутиться закрытой двери";
            btn_door.UseVisualStyleBackColor = true;
            btn_door.Click += btn_door_Click;
            // 
            // btn_subscribe_mom
            // 
            btn_subscribe_mom.Location = new Point(390, 54);
            btn_subscribe_mom.Name = "btn_subscribe_mom";
            btn_subscribe_mom.Size = new Size(219, 82);
            btn_subscribe_mom.TabIndex = 3;
            btn_subscribe_mom.Text = "Сделать маму ответственной";
            btn_subscribe_mom.UseVisualStyleBackColor = true;
            btn_subscribe_mom.Click += btn_subscribe_mom_Click;
            // 
            // btn_subscribe_dad
            // 
            btn_subscribe_dad.Location = new Point(632, 54);
            btn_subscribe_dad.Name = "btn_subscribe_dad";
            btn_subscribe_dad.Size = new Size(219, 82);
            btn_subscribe_dad.TabIndex = 4;
            btn_subscribe_dad.Text = "Сделать папу ответственным";
            btn_subscribe_dad.UseVisualStyleBackColor = true;
            btn_subscribe_dad.Click += btn_subscribe_dad_Click;
            // 
            // btn_Unsubscribe_dad
            // 
            btn_Unsubscribe_dad.Location = new Point(632, 152);
            btn_Unsubscribe_dad.Name = "btn_Unsubscribe_dad";
            btn_Unsubscribe_dad.Size = new Size(219, 82);
            btn_Unsubscribe_dad.TabIndex = 5;
            btn_Unsubscribe_dad.Text = "Снять с папы ответственность";
            btn_Unsubscribe_dad.UseVisualStyleBackColor = true;
            btn_Unsubscribe_dad.Click += btn_Unsubscribe_dad_Click;
            // 
            // btn_Unsubscribe_mom
            // 
            btn_Unsubscribe_mom.Location = new Point(390, 153);
            btn_Unsubscribe_mom.Name = "btn_Unsubscribe_mom";
            btn_Unsubscribe_mom.Size = new Size(219, 82);
            btn_Unsubscribe_mom.TabIndex = 6;
            btn_Unsubscribe_mom.Text = "Снять с мамы ответственность";
            btn_Unsubscribe_mom.UseVisualStyleBackColor = true;
            btn_Unsubscribe_mom.Click += btn_Unsubscribe_mom_Click;
            // 
            // btn_singleton
            // 
            btn_singleton.Location = new Point(132, 270);
            btn_singleton.Name = "btn_singleton";
            btn_singleton.Size = new Size(599, 82);
            btn_singleton.TabIndex = 7;
            btn_singleton.Text = "Выгнать старого кота и взять нового?";
            btn_singleton.UseVisualStyleBackColor = true;
            btn_singleton.Click += btn_singleton_Click;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(13F, 32F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(880, 376);
            Controls.Add(btn_singleton);
            Controls.Add(btn_Unsubscribe_mom);
            Controls.Add(btn_Unsubscribe_dad);
            Controls.Add(btn_subscribe_dad);
            Controls.Add(btn_subscribe_mom);
            Controls.Add(btn_door);
            Controls.Add(btn_food);
            Name = "Form1";
            Text = "Симулятор кота";
            Load += Form1_Load;
            ResumeLayout(false);
        }

        #endregion
        private Button btn_food;
        private Button btn_door;
        private Button btn_subscribe_mom;
        private Button btn_subscribe_dad;
        private Button btn_Unsubscribe_dad;
        private Button btn_Unsubscribe_mom;
        private Button btn_singleton;
    }
}
