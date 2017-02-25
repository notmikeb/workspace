

using System.Windows.Forms;
using System.Drawing;


public class ExampleForm: Form
{
	public ExampleForm()
	{
		this.Text = "I love wikiboooks";
		this.Width = 300;
		this.Height = 300;
		
		Button HelloButton = new Button();
		HelloButton.Location = new Point(20,30);
		HelloButton.Size = new Size(100,30);
		HelloButton.Text = "Click Me";
		HelloButton.Click += new System.EventHandler(WhenHelloButtonClick);
		
		this.Controls.Add(HelloButton);
	}
	
	void WhenHelloButtonClick(object sendor, System.EventArgs e)
	{
		MessageBox.Show("you clicked !!!");
	}
	
	
	public static void Main(string[] str)
	{
		Application.Run(new ExampleForm());
	}
}
