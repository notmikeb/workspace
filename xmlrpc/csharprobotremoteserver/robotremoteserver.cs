/* Copyright (c) 2011 David Luu
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * 
 * XML-RPC.NET Copyright (c) 2006 Charles Cook
 * FYI, XML-RPC.NET is licensed under MIT License
 * 
 *     http://www.xml-rpc.net/faq/xmlrpcnetfaq.html#6.12
 */
using System;
using System.IO;
using System.Net;		//used for XML-RPC server
using CookComputing.XmlRpc; //get from www.xml-rpc.net
using System.Reflection; //for the get_keyword methods and run_keyword method
using System.Xml;		//for use with get_keyword_documentation
using System.Xml.XPath; //to generate documentation for remote library
using System.Threading; //to shutdown server from remote request and at same time, return XML-RPC response
using System.Diagnostics; //for planned use with TraceListener

namespace RobotFramework
{
	/// <summary>
	/// RobotFramework .NET implementation of generic remote library server.
	/// Based on RobotFramework spec at
	/// http://code.google.com/p/robotframework/wiki/RemoteLibrary
	/// http://robotframework.googlecode.com/svn/tags/robotframework-2.5.6/doc/userguide/RobotFrameworkUserGuide.html#remote-library-interface
	/// http://robotframework.googlecode.com/svn/tags/robotframework-2.5.6/doc/userguide/RobotFrameworkUserGuide.html#dynamic-library-api
	/// 
	/// Uses .NET reflection to serve the dynamically loaded remote library.
	/// You may alternatively modify this starting code base to natively integrate
	/// your .NET test library code into the server rather than load it dynamically.
	/// 
	/// Remote server uses built-in .NET HTTP web server library so doesn't require IIS, etc.
	/// to simplify deployment and ease the life of QA personnel. However, if desired, you can
	/// modify the codebase to depend on IIS or .NET Remoting, etc. by switching out the code
	/// based of
	/// http://www.xml-rpc.net/faq/xmlrpcnetfaq.html#3.12
	/// to any of these
	/// http://www.xml-rpc.net/faq/xmlrpcnetfaq.html#3.2
	/// http://www.xml-rpc.net/faq/xmlrpcnetfaq.html#3.4
	/// http://www.xml-rpc.net/faq/xmlrpcnetfaq.html#3.3 
	/// 
	/// Compile this into a console application, and then you can dynamically load a
	/// separately compiled .NET class (Robot Framework keyword) library to use at startup.
	/// You may alternatively modify the code to work as a Windows service, etc. instead
	/// of a console application.
	/// </summary>
	class RemoteServer
	{
		public static bool enableStopServer;
		
		public static void Main(string[] args)
		{
			//set defaults for RobotFramework XML-RPC server spec
			string host = "127.0.0.1"; //localhost
			string port = "8270";
			enableStopServer = true;
			//params to load test library and documentation
			string remoteLibrary = "";
			string className = "";
			string docFile = "";			

			//parse arguments
			for(int i = 0; i < args.Length; i++){
				if(args[i] == "--library")
					remoteLibrary = args[i+1];
				if(args[i] == "--class")
					className = args[i+1];
				if(args[i] == "--doc")
					docFile = args[i+1];
				if(args[i] == "--host")
					host = args[i+1];
				if(args[i] == "--port")
					port = args[i+1];
				if(args[i] == "--nostopsvr")
					enableStopServer = false;
			}
			
			//check required arguments
			if(remoteLibrary == "" || className == "")
			{
				displayUsage();
				System.Environment.Exit(0);				
			}
			
			Console.WriteLine("");
			Console.WriteLine("Robot Framework remote library started at {0} on port {1}, on {2}",host,port,System.DateTime.Now.ToString());
			Console.WriteLine("");
			Console.WriteLine("To stop remote server/library, send XML-RPC method request 'run_keyword' with");
			Console.WriteLine("single argument of 'stop_remote_server' to do so, or hit Ctrl + C, etc.");
			Console.WriteLine("");
			
			//Using .NET HTTP listener to remove dependence on IIS, etc. using code snippet from
			// http://www.xml-rpc.net/faq/xmlrpcnetfaq.html#3.12
			HttpListener listener = new HttpListener();
			listener.Prefixes.Add("http://"+host+":"+port+"/");
			listener.Start();
			while (true)
			{
				HttpListenerContext context = listener.GetContext();
				XmlRpcListenerService svc;
				if(docFile == "")
				{
					svc = new XmlRpcMethods(remoteLibrary,className);
				}
				else
				{
					svc = new XmlRpcMethods(remoteLibrary,className,docFile);
				}				
				svc.ProcessRequest(context);
			}
		}
		
		/// <summary>
		/// Display the usage information for robotremoteserver.
		/// </summary>
		public static void displayUsage()
		{
			Console.WriteLine("");
			Console.WriteLine("robotremoteserver - v1.1");
			Console.WriteLine("");
			Console.WriteLine("Usage Info:");
			Console.WriteLine("");
			Console.WriteLine("  robotremoteserver --library pathToLibraryAssemblyFile");
			Console.WriteLine("    --class RemoteLibraryClassName [--doc pathToDocumentationFile]");
			Console.WriteLine("    [--host address] [--port portNumber] [--nostopsvr]");
			Console.WriteLine("");
			Console.WriteLine("  Assembly file = DLL or EXE, etc. w/ keyword class methods to execute.");
			Console.WriteLine("  Class name = keyword class w/ methods to execute. Include namespace as needed.");
			Console.WriteLine("  Documentation file = .NET compiler generated XML documentation file for the");
			Console.WriteLine("    class library. Optional for passing documentation to Robot Framework.");
			Console.WriteLine("");
			Console.WriteLine("  Optionally specify IP address or host name to bind remote server to.");
			Console.WriteLine("    Default of 127.0.0.1 (localhost).");
			Console.WriteLine("  Optionally specify port to bind remote server to. Default of 8270.");
			Console.WriteLine("  Optionally set whether to allow remote shut down of server. Default yes.");
			Console.WriteLine("");
			Console.WriteLine("Example:");
			Console.WriteLine("");
			Console.WriteLine("  robotremoteserver --library C:\\MyLibrary.dll --class MyNamespace.MyClass ");
			Console.WriteLine("    --doc C:\\MyLibrary_doc.xml --host 192.168.0.10 --port 8080");
		}
	}
	
	/// <summary>
	/// Class of XML-RPC methods for remote library (server)
	/// that conforms to RobotFramework remote library API
	/// </summary>
	public class XmlRpcMethods : XmlRpcListenerService
	{
		//.NET Robot Framework test library components
		private Assembly library;
		private string libraryClass;
		private XPathDocument doc;
		
		//I/O management components
		private TextWriter libout;
		private TextWriter liberrs;
		
		//.NET reflection components to handle the .NET library being served
		private Type classType;
		private object libObj;
		
		/// <summary>
		/// Basic constructor for XML-RPC method class.
		/// Load specified library (assembly) for use.
		/// No XML documentation provided to Robot Framework.
		/// </summary>
		/// <param name="libraryFile">Path to .NET assembly (DLL) file that contains the remote library class to load.</param>
		/// <param name="libraryClassName">Name of remote library class to load, specified in the format of "NamespaceName.ClassName" without the quotes.</param>
		public XmlRpcMethods(string libraryFile, string libraryClassName): this(libraryFile,libraryClassName,null)
		{
			//instantiate by calling the other constructor
		}
		
		/// <summary>
		/// Best constructor for XML-RPC method class.
		/// Load specified library (assembly) for use
		/// and provide XML documentation to Robot Framework.
		/// </summary>
		/// <param name="libraryFile">Path to .NET assembly (DLL) file that contains the remote library class to load.</param>
		/// <param name="libraryClassName">Name of remote library class to load, specified in the format of "NamespaceName.ClassName" without the quotes.</param>
		/// <param name="docFile">Path to XML documentation file for the specified .NET class assembly file.</param>
		public XmlRpcMethods(string libraryFile, string libraryClassName, string docFile)
		{						
			libraryClass = libraryClassName;
			try{
				doc = new XPathDocument(docFile);
			}catch{
				doc = null; //failed to load XML documentation file, set null for further processing
			}
			//initialize reflection components
			library = Assembly.LoadFrom(libraryFile);
			classType = library.GetType(libraryClass);
			libObj = Activator.CreateInstance(classType);

			//initialize the I/O management components
			libout = new StringWriter();
			liberrs = new StringWriter();			
		}
		
		/// <summary>
		/// Get a list of RobotFramework keywords available in remote library for use.
		/// 
		/// NOTE: Current implementation will return 
		/// extra unanticipated keywords from .NET remote class library, just ignore them
		/// for now, until we can optimize this .NET implementation.
		/// </summary>
		/// <returns>A string array of RobotFramework keywords available in remote library for use.</returns>
		[XmlRpcMethod]
		public string[] get_keyword_names()
  		{
			//MethodInfo[] mis = classType.GetMethods(BindingFlags.Public | BindingFlags.Static);
			//seem to have issue when trying to only get public & static methods, so get all instead
			MethodInfo[] mis = classType.GetMethods();
			
			//add one more for stop server that's part of the server
			string[] keyword_names = new string[mis.Length+1];
			int i = 0;			
			foreach(MethodInfo mi in mis)
			{
				keyword_names[i++] = mi.Name;
			}
			keyword_names[i] = "stop_remote_server";
			return keyword_names;
		}
		
		/// <summary>
		/// Run specified Robot Framework keyword from remote server.
		/// </summary>
		/// <param name="keyword">Keyword class library method to run for Robot Framework.</param>
		/// <param name="args">Arguments, if any, to pass to keyword method.</param>
		/// <returns></returns>
		[XmlRpcMethod]
		public XmlRpcStruct run_keyword(string keyword, object[] args)
  		{
			XmlRpcStruct kr = new XmlRpcStruct();
			
			if(keyword == "stop_remote_server")
			{				
				if(RemoteServer.enableStopServer){
					//reset output back to stdout
					StreamWriter stdout = new StreamWriter(Console.OpenStandardOutput());
					stdout.AutoFlush = true;
        			Console.SetOut(stdout);
        			
					//spawn new thread to do a delayed server shutdown
					//and return XML-RPC response before delay is over
					new Thread(stop_remote_server).Start();
					Console.WriteLine("Shutting down remote server/library in 5 seconds, from Robot Framework remote");
					Console.WriteLine("library/XML-RPC request.");
					Console.WriteLine("");
					kr.Add("output","NOTE: remote server shutting/shut down.");
				}else{
					kr.Add("output","NOTE: remote server not configured to allow remote shutdowns. Your request has been ignored.");
					//in case RF spec changes to report failure in this case in future
					//kr.Add("status","FAIL");
					//kr.Add("error","NOTE: remote server not configured to allow remote shutdowns. Your request has been ignored.");
				}
				kr.Add("return",1);
				kr.Add("status","PASS");
				kr.Add("error","");
				kr.Add("traceback","");
				return kr;
			}
			//redirect output from test library to send back to Robot Framework			
			Console.SetOut(libout); //comment out when debugging
			Console.SetError(liberrs);
			
			MethodInfo mi = classType.GetMethod(keyword);			
			
			try
			{
				/* we let XML-RPC.NET library handle the data type conversion
				 * hopefully, the test library returns one of the supported XML-RPC data types:
 				 * http://xml-rpc.net/faq/xmlrpcnetfaq-2-5-0.html#1.9
				 * http://xml-rpc.net/faq/xmlrpcnetfaq-2-5-0.html#1.12
				 * Otherwise, an error may occur.
				 * 
				 * FYI, and this is the spec for Robot Framework remote library keyword argument and return type
				 * http://robotframework.googlecode.com/svn/tags/robotframework-2.5.6/doc/userguide/RobotFrameworkUserGuide.html#supported-argument-and-return-value-types
				 * on how data types should map, particularly for the non-native-supported types.
				 * Hopefully XML-RPC.NET converts them closely to those types, otherwise, you will have to make some
				 * changes in the remote server code here to adjust return type according to Robot Framework spec.
				 * Or change the test library being served by the remote server to use simpler data structures (e.g. primitives)
				 */
				if (mi.ReturnType == typeof(void))
				{
					mi.Invoke(libObj, args);
					kr.Add("return",""); 
				}
				else
				{
					kr.Add("return",mi.Invoke(libObj, args));
				}
									
				kr.Add("status","PASS");				
				kr.Add("output",libout.ToString());
				libout.Flush();
				kr.Add("error",liberrs.ToString());
				liberrs.Flush();
				kr.Add("traceback","");
				return kr;
			}			
			catch(TargetInvocationException iex)
			{
				//exception message is probably more useful at this point than standard error?
				liberrs.Flush();
				
				kr.Add("traceback",iex.InnerException.StackTrace);
				kr.Add("error",iex.InnerException.Message);
				
				kr.Add("output",libout.ToString());
				libout.Flush();
				kr.Add("status","FAIL");
				kr.Add("return","");
				return kr;
			}
			catch(System.Exception ex)
			{
				//to catch all other exceptions that are not nested or from target invocation (i.e. reflection)
				
				//exception message is probably more useful at this point than standard error?
				liberrs.Flush();

				kr.Add("traceback",ex.StackTrace);
				kr.Add("error",ex.Message);
				 
				kr.Add("output",libout.ToString());
				libout.Flush();
				kr.Add("status","FAIL");
				kr.Add("return","");
				return kr;
			}
		}
		
		/// <summary>
		/// As defined by Robot Framework spec, this keyword will remotely stop remote library server.
		/// To be called by Robot Framework remote library interface
		/// or by XML-RPC request to run_keyword() XML-RPC method,
		/// passing it "stop_remote_server" as single argument.
		/// 
		/// NOTE: Currently will not return any XML-RPC response after being called, unlike the Python implementation.
		/// </summary>
		private static void stop_remote_server()
  		{
			//delay shutdown for some time so can return XML-RPC response
			int delay = 5000; //let's arbitrarily set delay at 5 seconds
			Thread.Sleep(delay);
			Console.WriteLine("Remote server/library shut down at {0}",System.DateTime.Now.ToString());
			System.Environment.Exit(0);
		}
		
		/// <summary>
		/// Get list of arguments for specified Robot Framework keyword.
		/// </summary>
		/// <param name="keyword">The keyword to get a list of arguments for.</param>
		/// <returns>A string array of arguments for the given keyword.</returns>
		[XmlRpcMethod]
		public string[] get_keyword_arguments(string keyword)
		{
			if(keyword == "stop_remote_server") return new String[0];
			MethodInfo mi = classType.GetMethod(keyword);
			ParameterInfo[] pis = mi.GetParameters();
			string[] args = new String[pis.Length];
			int i = 0;
			foreach(ParameterInfo pi in pis)
			{
				args[i++] = pi.Name;
			}
			return args;		
		}		

		/// <summary>
		/// Get documentation for specified Robot Framework keyword.
		/// Done by reading the .NET compiler generated XML documentation
		/// for the loaded class library.
		/// </summary>
		/// <param name="keyword">The keyword to get documentation for.</param>
		/// <returns>A documentation string for the given keyword.</returns>
		[XmlRpcMethod]
		public string get_keyword_documentation(string keyword)
		{
			string retval = ""; //start off with no documentation, in case keyword is not documented
			
			if(keyword == "stop_remote_server"){
				retval = "Remotely shut down remote server/library w/ Robot Framework keyword.\n\n";
				retval += "If server is configured to not allow remote shutdown, keyword 'request' is ignored by server.\n\n";
				retval += "Always returns status of PASS with return value of 1. Output value contains helpful info and may indicate whether remote shut down is allowed or not.";
				return retval;
			}
			if(doc == null)
			{
				return retval; //no XML documentation provided, return blank doc
			}//else return keyword (class method) documentation from XML file
			
			XPathNavigator docFinder;
			XPathNodeIterator docCol;
			try{
				docFinder = doc.CreateNavigator();
			}catch{
				docFinder = null; //failed to load XML documentation file, set null
			}			
			string branch = "/doc/members/member[starts-with(@name,'M:"+libraryClass+"."+keyword+"')]/summary";
			try
			{
				retval = docFinder.SelectSingleNode(branch).Value + System.Environment.NewLine + System.Environment.NewLine;
			}
			catch
			{
				//no summary info provided for .NET class method
			}
			try
			{
				branch = "/doc/members/member[starts-with(@name,'M:"+libraryClass+"."+keyword+"')]/param";
				docCol = docFinder.Select(branch);
				while (docCol.MoveNext())
				{
					retval = retval + docCol.Current.GetAttribute("name","") + ": " + docCol.Current.Value + System.Environment.NewLine;
				};
				retval = retval + System.Environment.NewLine;
			}
			catch
			{
				//no parameter info provided or some parameter info missing for .NET class method
			}
			try
			{
				branch = "/doc/members/member[starts-with(@name,'M:"+libraryClass+"."+keyword+"')]/returns";
				retval = retval + "Returns: " + docFinder.SelectSingleNode(branch).Value;
			}
			catch
			{
				//.NET class method either does not return a value (e.g. void) or documentation not provided
			}			
			return retval; //return whatever documentation was found for the keyword
		}
	}
	
	/// <summary>
	/// Deprecated static data structure for Robot Framework run_keyword return value, based on spec at
	/// http://robotframework.googlecode.com/svn/tags/robotframework-2.5.6/doc/userguide/RobotFrameworkUserGuide.html#remote-library-interface
	/// 
	/// Due to strict data typing by .NET, return value will always be cast as a string with this implementation.
	/// Alternative is could be to use .NET generics? In any case, design has been superseded
	/// by using XmlRpcStruct type from XML-RPC.NET library.
	/// 
	/// Recommend not to use, but kept here for reference.
	/// </summary>
	public struct keyword_results
	{
		public string status; //Mandatory execution status. Either PASS or FAIL.
		public string output; //Possible output to write into the RobotFramework log file. Must be given as a single string but can contain multiple messages and different log levels in format *INFO* First message\n*INFO* Second\n*WARN* Another message.
		public string traceback; //Possible stack trace to write into the RobotFramework log file using DEBUG level when the execution fails.
		public string error; //Possible error message. Used only when the execution fails.
		[XmlRpcMember("return")]
		public string Return; //Possible return value. Must be one of the supported RobotFramework/Python data types.
		//due to strict data typing by .NET, return value will always be cast as a string with this implementation.
	}
}