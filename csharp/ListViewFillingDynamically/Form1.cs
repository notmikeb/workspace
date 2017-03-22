using System;
using System.Drawing;
using System.Collections;
using System.ComponentModel;
using System.Windows.Forms;
using System.Data;
using System.Data.SqlClient;
using System.Threading;

namespace DatabaseSearhHelper
{
	/// <summary>
	/// Summary description for Form1.
	/// </summary>
	public class Form1 : System.Windows.Forms.Form
	{
		private System.Windows.Forms.Panel panel1;
		private System.Windows.Forms.ListView listView1;
		private System.Windows.Forms.Label label1;
		private System.Windows.Forms.Label label2;
		private System.Windows.Forms.TextBox txtConString;
		private System.Windows.Forms.TextBox txtQueryString;
		private System.Windows.Forms.ToolTip toolTip1;
		private System.Windows.Forms.Label label3;
		private System.Windows.Forms.NumericUpDown numericUpDown1;
		private System.Windows.Forms.Label lblStatus;
		private System.Windows.Forms.Button btnXML;
		private System.Windows.Forms.OpenFileDialog openFileDialog1;
		private System.Windows.Forms.Button btnLoadTable;
		private System.ComponentModel.IContainer components;

		public Form1()
		{
			//
			// Required for Windows Form Designer support
			//
			InitializeComponent();

			//
			// TODO: Add any constructor code after InitializeComponent call
			//
		}

		/// <summary>
		/// Clean up any resources being used.
		/// </summary>
		protected override void Dispose( bool disposing )
		{
			if( disposing )
			{
				if (components != null) 
				{
					components.Dispose();
				}
			}
			base.Dispose( disposing );
		}

		#region Windows Form Designer generated code
		/// <summary>
		/// Required method for Designer support - do not modify
		/// the contents of this method with the code editor.
		/// </summary>
		private void InitializeComponent()
		{
			this.components = new System.ComponentModel.Container();
			this.panel1 = new System.Windows.Forms.Panel();
			this.btnLoadTable = new System.Windows.Forms.Button();
			this.lblStatus = new System.Windows.Forms.Label();
			this.numericUpDown1 = new System.Windows.Forms.NumericUpDown();
			this.label3 = new System.Windows.Forms.Label();
			this.label2 = new System.Windows.Forms.Label();
			this.label1 = new System.Windows.Forms.Label();
			this.txtQueryString = new System.Windows.Forms.TextBox();
			this.txtConString = new System.Windows.Forms.TextBox();
			this.listView1 = new System.Windows.Forms.ListView();
			this.btnXML = new System.Windows.Forms.Button();
			this.toolTip1 = new System.Windows.Forms.ToolTip(this.components);
			this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
			this.panel1.SuspendLayout();
			((System.ComponentModel.ISupportInitialize)(this.numericUpDown1)).BeginInit();
			this.SuspendLayout();
			// 
			// panel1
			// 
			this.panel1.AutoScroll = true;
			this.panel1.Controls.Add(this.btnLoadTable);
			this.panel1.Controls.Add(this.lblStatus);
			this.panel1.Controls.Add(this.numericUpDown1);
			this.panel1.Controls.Add(this.label3);
			this.panel1.Controls.Add(this.label2);
			this.panel1.Controls.Add(this.label1);
			this.panel1.Controls.Add(this.txtQueryString);
			this.panel1.Controls.Add(this.txtConString);
			this.panel1.Controls.Add(this.listView1);
			this.panel1.Controls.Add(this.btnXML);
			this.panel1.Dock = System.Windows.Forms.DockStyle.Fill;
			this.panel1.Location = new System.Drawing.Point(0, 0);
			this.panel1.Name = "panel1";
			this.panel1.Size = new System.Drawing.Size(664, 413);
			this.panel1.TabIndex = 0;
			// 
			// btnLoadTable
			// 
			this.btnLoadTable.Location = new System.Drawing.Point(456, 16);
			this.btnLoadTable.Name = "btnLoadTable";
			this.btnLoadTable.Size = new System.Drawing.Size(75, 72);
			this.btnLoadTable.TabIndex = 14;
			this.btnLoadTable.Text = "Load Table";
			this.btnLoadTable.Click += new System.EventHandler(this.btnLoadTable_Click);
			// 
			// lblStatus
			// 
			this.lblStatus.Location = new System.Drawing.Point(248, 96);
			this.lblStatus.Name = "lblStatus";
			this.lblStatus.Size = new System.Drawing.Size(240, 16);
			this.lblStatus.TabIndex = 13;
			// 
			// numericUpDown1
			// 
			this.numericUpDown1.Increment = new System.Decimal(new int[] {
																			 5,
																			 0,
																			 0,
																			 0});
			this.numericUpDown1.Location = new System.Drawing.Point(104, 96);
			this.numericUpDown1.Maximum = new System.Decimal(new int[] {
																		   1000,
																		   0,
																		   0,
																		   0});
			this.numericUpDown1.Name = "numericUpDown1";
			this.numericUpDown1.TabIndex = 12;
			this.numericUpDown1.Value = new System.Decimal(new int[] {
																		 60,
																		 0,
																		 0,
																		 0});
			this.numericUpDown1.ValueChanged += new System.EventHandler(this.numericUpDown1_ValueChanged);
			// 
			// label3
			// 
			this.label3.Location = new System.Drawing.Point(0, 96);
			this.label3.Name = "label3";
			this.label3.Size = new System.Drawing.Size(88, 23);
			this.label3.TabIndex = 10;
			this.label3.Text = "ColumnsWidth";
			// 
			// label2
			// 
			this.label2.Location = new System.Drawing.Point(0, 48);
			this.label2.Name = "label2";
			this.label2.Size = new System.Drawing.Size(80, 23);
			this.label2.TabIndex = 5;
			this.label2.Text = " Query string";
			// 
			// label1
			// 
			this.label1.Location = new System.Drawing.Point(0, 8);
			this.label1.Name = "label1";
			this.label1.Size = new System.Drawing.Size(96, 23);
			this.label1.TabIndex = 4;
			this.label1.Text = "Connection string";
			// 
			// txtQueryString
			// 
			this.txtQueryString.Location = new System.Drawing.Point(104, 51);
			this.txtQueryString.Multiline = true;
			this.txtQueryString.Name = "txtQueryString";
			this.txtQueryString.ScrollBars = System.Windows.Forms.ScrollBars.Both;
			this.txtQueryString.Size = new System.Drawing.Size(336, 37);
			this.txtQueryString.TabIndex = 3;
			this.txtQueryString.Text = "SELECT * FROM Customers";
			// 
			// txtConString
			// 
			this.txtConString.Location = new System.Drawing.Point(104, 8);
			this.txtConString.Multiline = true;
			this.txtConString.Name = "txtConString";
			this.txtConString.ScrollBars = System.Windows.Forms.ScrollBars.Both;
			this.txtConString.Size = new System.Drawing.Size(336, 32);
			this.txtConString.TabIndex = 2;
			this.txtConString.Text = "DataBase=(LCOAL);Initial Catalog=NorthWind;Integrated Security=SSPI";
			// 
			// listView1
			// 
			this.listView1.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
				| System.Windows.Forms.AnchorStyles.Left) 
				| System.Windows.Forms.AnchorStyles.Right)));
			this.listView1.FullRowSelect = true;
			this.listView1.GridLines = true;
			this.listView1.Location = new System.Drawing.Point(104, 128);
			this.listView1.Name = "listView1";
			this.listView1.Size = new System.Drawing.Size(528, 272);
			this.listView1.TabIndex = 1;
			this.toolTip1.SetToolTip(this.listView1, "Double Click A Row To see its Details");
			this.listView1.View = System.Windows.Forms.View.Details;
			this.listView1.DoubleClick += new System.EventHandler(this.listView1_DoubleClick);
			this.listView1.MouseHover += new System.EventHandler(this.listView1_MouseHover);
			this.listView1.MouseEnter += new System.EventHandler(this.listView1_MouseEnter);
			this.listView1.MouseLeave += new System.EventHandler(this.listView1_MouseLeave);
			// 
			// btnXML
			// 
			this.btnXML.Location = new System.Drawing.Point(544, 16);
			this.btnXML.Name = "btnXML";
			this.btnXML.Size = new System.Drawing.Size(75, 72);
			this.btnXML.TabIndex = 1;
			this.btnXML.Text = "Load Xml";
			this.btnXML.Click += new System.EventHandler(this.btnXML_Click);
			// 
			// Form1
			// 
			this.AutoScaleBaseSize = new System.Drawing.Size(6, 13);
			this.ClientSize = new System.Drawing.Size(664, 413);
			this.Controls.Add(this.panel1);
			this.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.Name = "Form1";
			this.Text = "Filling ListView";
			this.Load += new System.EventHandler(this.Form1_Load);
			this.panel1.ResumeLayout(false);
			((System.ComponentModel.ISupportInitialize)(this.numericUpDown1)).EndInit();
			this.ResumeLayout(false);

		}
		#endregion

		/// <summary>
		/// The main entry point for the application.
		/// </summary>
		[STAThread]
		static void Main() 
		{
			Application.Run(new Form1());
		}
	   //Global scoped objects of SqlDataAdapter and DataSet
		SqlDataAdapter da;
		DataSet ds;
		private void FillListView()
		{
			
			
			foreach(DataColumn c in ds.Tables[0].Columns)
			{
				//adding names of columns as Listview columns				
				ColumnHeader h=new ColumnHeader();
				h.Text=c.ColumnName;
				h.Width=Convert.ToInt32(this.numericUpDown1.Value);
				this.listView1.Columns.Add(h);
			}
		
				
				DataTable dt=ds.Tables[0];
				string[] str=new string[ds.Tables[0].Columns.Count];
			/**********IMPORTANT PART OF CODE ****************/
			/************************************************/
			//adding Datarows as listview Grids
			    foreach(DataRow rr in dt.Rows)
				{
					for(int col=0;col<=this.ds.Tables[0].Columns.Count-1;col++)
					{				
						//filling the array of string
						str[col]=rr[col].ToString();
					}
					ListViewItem ii;
					ii=new ListViewItem(str);	
					this.listView1.Items.Add(ii);
					//showing the number of records still added
					this.ShowStatus();
							
				}
			
			}
		//Thread used for making application flexible
		
		bool runThread;
		private void ThreadStarter()
		{
			
			try
			{
				ThreadStart ts=new ThreadStart(this.FillMethod);
				//check if thread is allow to run
				if(this.runThread)
				{
					Thread t=new Thread(ts);
					t.Start();
				}
				
			}
			catch(Exception ex)
			{
				this.listView1.Clear();
				this.lblStatus.Text="";
				this.lblStatus.BackColor=this.BackColor;
				MessageBox.Show(ex.Message,ex.GetType().ToString());
			}

		}
		
		private void FillDatSet()
		{
			//filling dataset add the base of given connection and query strings
			da=new SqlDataAdapter(this.txtQueryString.Text,this.txtConString.Text);
			da.Fill(ds);
		}
		//a general method used to fill Listvew when required
		private void FillMethod()
		{
			
			try
			{
				this.lblStatus.Text="";
				this.runThread=true;
				this.numericUpDown1.Enabled=false;
				
				this.Cursor=Cursors.WaitCursor;	
				
				this.listView1.Columns.Clear();
				this.listView1.Items.Clear();
			
				this.FillListView();
				this.Cursor=Cursors.Default;
				this.numericUpDown1.Enabled=true;
				

				
			}
			catch(Exception ex)
			{
				this.runThread=false;
				this.listView1.Clear();
				this.lblStatus.Text="";
				this.lblStatus.BackColor=this.BackColor;
				MessageBox.Show(ex.Message,ex.GetType().ToString());
				this.numericUpDown1.Enabled=true;
				
				this.Cursor=Cursors.Default;
				this.lblStatus.Text="";
			}

		
		}
		//shows the various stutuses
		void ShowStatus()
		{
			this.lblStatus.ForeColor=Color.White;
			this.lblStatus.BackColor=Color.Indigo;
			
			if(this.listView1.Items.Count!=0)
			{
				
				this.lblStatus.Text=string.Format(" {0} Columns and {1} Rows ",this.ds.Tables[0].Columns.Count,this.listView1.Items.Count);
			}
			else
			{
				lblStatus.BackColor=this.BackColor;
			}
		}

		//Message box showing data when listview double clicked
		private void listView1_DoubleClick(object sender, System.EventArgs e)
		{
			string str=null;
			for(int i=0;i<=this.listView1.Columns.Count-1;i++)
			{
				str+=this.ds.Tables[0].Columns[i];
				str+=" = ";
				str+=this.listView1.FocusedItem.SubItems[i].Text;
				str+="\n";
			}
			MessageBox.Show(str,"Selected Row");
		}

		//event fires when finds any change in the NumericUpDown ontrol
		//to resize Columns  widths
		private void numericUpDown1_ValueChanged(object sender, System.EventArgs e)
		{
			try
			{
			this.runThread=true;	
			 this.ThreadStarter();	
				
				
			}

			catch(Exception ex)
			{
				this.listView1.Clear();
				this.lblStatus.Text="";
				this.lblStatus.BackColor=this.BackColor;
				MessageBox.Show(ex.Message);
				this.Cursor=Cursors.Default;
			}
		}

		private void listView1_MouseHover(object sender, System.EventArgs e)
		{
		  
			if(this.listView1.Items.Count!=0)
			{
			this.lblStatus.ForeColor=Color.White;
			this.lblStatus.BackColor=Color.Indigo;
			this.lblStatus.Text="DoubleClick A Row To See Details";
			}
			else
			{
				this.BackColor=this.BackColor;
			}

		}

		private void listView1_MouseLeave(object sender, System.EventArgs e)
		{
			if(this.listView1.Items.Count!=0)
			{
			this.lblStatus.Text="";
			this.ShowStatus();
			}
			else
			{
				this.BackColor=this.BackColor;
			}
			
		}

		private void listView1_MouseEnter(object sender, System.EventArgs e)
		{
			if(this.listView1.Items.Count!=0)
			{
				this.lblStatus.ForeColor=Color.White;
				this.lblStatus.BackColor=Color.Red;
				this.lblStatus.Text="DoubleClick A Row To See Details";
			}
			else
			{
				this.BackColor=this.BackColor;
			}
		}
	
		private void btnXML_Click(object sender, System.EventArgs e)
		{
			try
			{
				this.listView1.Clear();
				openFileDialog1.Title="Open XML Files";
				openFileDialog1.Filter = "xml files (*.xml)|*.xml" ;
				openFileDialog1.RestoreDirectory = true ;
				if(this.openFileDialog1.ShowDialog()==DialogResult.OK)
				{
				
					this.ds.Reset();
					this.ds.ReadXml(this.openFileDialog1.FileName);

			
					this.runThread=true;
					this.ThreadStarter();
				}
			}

			catch(Exception ex)
			{
				this.listView1.Clear();
				this.lblStatus.Text="";
				this.lblStatus.BackColor=this.BackColor;
				MessageBox.Show(ex.Message);
				this.Cursor=Cursors.Default;
			}

		}

		private void Form1_Load(object sender, System.EventArgs e)
		{
			this.ds=new DataSet();
		}

		private void btnLoadTable_Click(object sender, System.EventArgs e)
		{
			
			try
			{
				this.listView1.Clear();
				this.ds.Reset();
				this.FillDatSet();
				this.runThread=true;
				this.ThreadStarter();
				
				
			}

			catch(Exception ex)
			{
				this.listView1.Clear();
				this.lblStatus.Text="";
				this.lblStatus.BackColor=this.BackColor;
				MessageBox.Show(ex.Message);
				this.Cursor=Cursors.Default;
			}
			
		}
		
		}

	}

