/*       Client Program      */

using System;
using System.IO;
using System.Net;
using System.Text;
using System.Net.Sockets;
using System.Linq;

public class clnt {
// show data in hex format
    public static void test1(){
byte[] ba = { 1, 2, 4, 8, 16, 32 };

string s = string.Concat(ba.Select(b => b.ToString("X2")));
string t = string.Concat(ba.Select(b => b.ToString("X2")).ToArray());

Console.WriteLine (s);
Console.WriteLine (t);
    }
    public static void Main() {
        test1();   
        try {
            TcpClient tcpclnt = new TcpClient();
            Console.WriteLine("Connecting.....");
            
            tcpclnt.Connect("localhost",8001);
            // use the ipaddress as in the server program
            
            Console.WriteLine("Connected");
            Console.Write("Enter the string to be transmitted : ");
            
            String str=Console.ReadLine();
            Stream stm = tcpclnt.GetStream();
                        
            ASCIIEncoding asen= new ASCIIEncoding();
            byte[] ba=asen.GetBytes(str);
            Console.WriteLine("Transmitting.....");
            
            stm.Write(ba,0,ba.Length);
            
            byte[] bb=new byte[100];
            int k=stm.Read(bb,0,100);
            
            for (int i=0;i<k;i++)
                Console.Write(Convert.ToChar(bb[i]));
            Console.WriteLine("");
            Console.WriteLine("Get " + k + " bytes");
            tcpclnt.Close();
        }
        
        catch (Exception e) {
            Console.WriteLine("Error..... " + e.StackTrace);
        }
    }

}