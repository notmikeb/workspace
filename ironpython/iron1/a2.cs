using System;
// The IronPython and Dynamic Language Runtime (DLR)
using IronPython.Hosting;
using IronPython.Runtime;
using Microsoft.Scripting;
using Microsoft.Scripting.Hosting; 

// full example  a winform to execute ironpython
// https://derekwill.com/2014/08/15/ironpython-sample-application/

using System.Threading;

public class Alpha
{
   int myid = 0;
   Random myr;
   // This method that will be called when the thread is started
   public Alpha(int id, Random r){
   myid = id;
   myr = r;
   }

   public void ThreadRun( ){
      int i = 0;
      int t = 0;
      while ( i < 10)
      {
         i = i + 1;
         t = myr.Next(2,1000);
         Console.WriteLine("Alpha {0} {1} r:{2}", myid, i, t);
         Thread.Sleep(t);
      }
   }
};

public class Beta
{
   int myid = 0;
   dynamic engine;
   // This method that will be called when the thread is started
   public Beta(int id){
   myid = id;
   engine = Python.CreateEngine();
   }

   public void ThreadRun( ){
var theScript = @"
import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
#import os
#import time
#import random
#print 'yes'
for i in range(10):
  print 'id:{} {}'.format( " + myid + @" , i)
  #time.sleep(random.random()*3)
";
engine.Execute(theScript);
   }
};


namespace a1
{
    class Program
    {
        static void Main(string[] args)
        {
    try
    {
      dynamic engine = Python.CreateEngine();
      dynamic scope = engine.CreateScope();
      scope.Add = new Func<int, int, int>((x, y) => x + y);
      Console.WriteLine(scope.Add(2, 3)); // prints 5
    }
    catch (Exception e)
    {
        Console.WriteLine(e.Message);
    }
    Random r = new Random();
    Alpha A1 = new Alpha(1, r);
    Alpha A2 = new Alpha(2, r);
    //Beta A1 = new Beta(1);
    //Beta A2 = new Beta(2);
    Thread p1 = new Thread(new ThreadStart(A1.ThreadRun));
    Thread p2 = new Thread(new ThreadStart(A2.ThreadRun));
    p1.Start();
    p2.Start();    

      // Put the Main thread to sleep for 1 millisecond to allow oThread
      // to do some work:
      Console.WriteLine("Sleep 5");
      Thread.Sleep(5000);

        }
    }
}