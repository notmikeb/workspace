using System.Collections.Generic;
using System.Data;
using System.Windows.Forms;
using System;

namespace WindowsFormsApplication1
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1());
        }
    }

    public partial class Form1 : Form
    {
        /// <summary>
        /// Contains column names.
        /// </summary>
        List<string> _names = new List<string>();

        /// <summary>
        /// Contains column data arrays.
        /// </summary>
        List<double[]> _dataArray = new List<double[]>();

        public Form1()
        {
            InitializeComponent();

            // Example column.
            _names.Add("Cat");
            // Three numbers of cat data.
            _dataArray.Add(new double[]
            {
                1.0,
                2.2,
                3.4
            });

            // Another example column.
            _names.Add("Dog");
            // Add three numbers of dog data.
            _dataArray.Add(new double[]
            {
                3.3,
                5.0,
                7.0
            });
            // Render the DataGridView.
            dataGridView1.DataSource = GetResultsTable();
        }

        /// <summary>
        /// This method builds a DataTable of the data.
        /// </summary>
        public DataTable GetResultsTable()
        {
            // Create the output table.
            DataTable d = new DataTable();

            // Loop through all process names.
            for (int i = 0; i < this._dataArray.Count; i++)
            {
                // The current process name.
                string name = this._names[i];

                // Add the program name to our columns.
                d.Columns.Add(name);

                // Add all of the memory numbers to an object list.
                List<object> objectNumbers = new List<object>();

                // Put every column's numbers in this List.
                foreach (double number in this._dataArray[i])
                {
                    objectNumbers.Add((object)number);
                }

                // Keep adding rows until we have enough.
                while (d.Rows.Count < objectNumbers.Count)
                {
                    d.Rows.Add();
                }

                // Add each item to the cells in the column.
                for (int a = 0; a < objectNumbers.Count; a++)
                {
                    d.Rows[a][i] = objectNumbers[a];
                }
            }
            return d;
        }
    }
}