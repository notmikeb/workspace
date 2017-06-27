// USBPeripheral

using LibUsbDotNet;
using LibUsbDotNet.Info;
using LibUsbDotNet.LudnMonoLibUsb;
using LibUsbDotNet.Main;
using MonoLibUsb;
using MonoLibUsb.Profile;
using MonoLibUsb.Transfer;


using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading;
using System.Windows.Forms;
using System.Runtime.InteropServices;


// 20170627 create a csharp program to send data to bt dongle



namespace Peripheral
{
	public class USBPeripheral
	{
		private short bt_vid = -1, bt_pid = -1, usb_port = -1, usb_hub = -1;
		private short FinalDeviceIndex = -1;
		private MonoUsbTransferDelegate controlTransferDelegate;
		private MonoUsbSessionHandle sessionHandle;
		public UsbDevice MyUsbDevice;
		public UsbDeviceFinder MyUsbFinder = new UsbDeviceFinder(0x0a12, 0x0001);
		private MonoUsbProfileList profileList = null;
		
		private UsbDeviceInfo usbDeviceInfo;
		
		public UsbDevice[] MyUsbDeviceArray;
		public short UsbDeviceCount;
		public List<MonoUsbProfile> MatchingUsbDeviceList = null;
		public List<MonoUsbDevice> MonoUsbDeviceList = null;
		
		MonoUsbDeviceHandle myDeviceHandle = null;
		
		public UsbEndpointReader globalReader = null;
		public Action<byte[], int> globalCallback = null;
		private const int MAX_USB_DEVICE_COUNT = 40;
		
		public static void Main(){
            var a = new USBPeripheral();
			a.SetUsbDeviceIdentification(0x0a12, 0x0001);
            a.Connect();
			System.Console.WriteLine( String.Format("UsbDeviceCount {0}", a.UsbDeviceCount));
			
			System.Console.WriteLine("Main done");
			return ;
		}
		
		public bool Connect()
		{
			bool isConnect = false;
			Console.WriteLine("usb:connect");
			
			if((bt_vid ==-1) || (bt_pid == -1)){
				throw new Exception("USBDevice identification data not set");
			}
			
			controlTransferDelegate  = ControlTransferCB;
			
			sessionHandle = new MonoUsbSessionHandle();
			if(sessionHandle.IsInvalid){
				throw new Exception( String.Format("failed init libusb contenxt {0}:{1}", MonoUsbSessionHandle.LastErrorCode,
				MonoUsbSessionHandle.LastErrorString));
			}
			
			profileList = new MonoUsbProfileList();
			MonoUsbDeviceList = MonoUsbDevice.MonoUsbDeviceList;
			
			MyUsbDeviceArray = new UsbDevice[MAX_USB_DEVICE_COUNT];
			UsbDeviceCount = 0;
			
			DiscoveryUsbDevice(true);
			SetConfigUsbDevice();
			
			return isConnect;
		}

        public String SendByteArray(byte[] data, short length)
        {
            string getString = "";
            int ret;

            byte rquestType = (byte)(UsbCtrlFlags.Direction_Out | UsbCtrlFlags.Recipient_Device | UsbCtrlFlags.RequestType_Class);
            byte request = 0x0;
            MonoUsbControlSetupHandle controlSetupHandle = new MonoUsbControlSetupHandle(rquestType, request, 0, 0, length);
			controlSetupHandle.ControlSetup.SetData(data, 0, length);
			
			ret = libusb_control_transfer(myDeviceHandle, controlSetupHandle, 1000);
			Console.WriteLine("libusb control transfer complete");
			return getString;
        }
		
		public String SetReadDataCallback(Action<byte[], int> callback){
			String getString = "";
			
			if(globalReader == null)
				throw new Exception("Reading Endpoint has not been opened.");
			
			globalReader.DataReceived += (OnRxEndPointData);
			globalReader.DataReceivedEnabled = true;
			globalCallback = callback;
			return getString;
		}
		
		public void Close(){
			profileList.Close();
			if (myDeviceHandle != null) myDeviceHandle.Close();
			sessionHandle.Close();
			
			if(MyUsbDevice != null)
			{
				if(MyUsbDevice.IsOpen){
					IUsbDevice wholeUsbDevice = MyUsbDevice as IUsbDevice;
					if(! ReferenceEquals(wholeUsbDevice, null) ){
						wholeUsbDevice.ReleaseInterface(0);
					}
					MyUsbDevice.Close();
				}
					
				MyUsbDevice = null;
			}
			
		}

		public void Dispose()
		{
			UsbDevice.Exit();  
		}
		public Boolean isConnect()
		{
			return true;
		}
		
		public Boolean SetUsbDeviceIdentification(short vid, short pid, short port = -1, short hub = -1)
		{
			bt_vid = vid;
			bt_pid = pid;
			usb_hub = hub;
			usb_port = port;
			return true;
		}
		
		private void ControlTransferCB(MonoUsbTransfer transfer)
		{
			ManualResetEvent completeEvent = GCHandle.FromIntPtr(transfer.PtrUserData).Target as ManualResetEvent;
			completeEvent.Set();
		}
		
		private bool MyVidPidPredicate(MonoUsbProfile profile)
		{
			if(profile.DeviceDescriptor.VendorID == bt_vid &&profile.DeviceDescriptor.ProductID == bt_pid){
			System.Console.WriteLine( String.Format("profile vid:{0} pid:{1}", profile.DeviceDescriptor.VendorID, profile.DeviceDescriptor.ProductID));
			return true;
			}
			//return true;
			return false;
		}
		
		private bool SetConfigUsbDevice()
		{
				int ret;
				if(FinalDeviceIndex == -1)
				{
					throw new Exception("No valid device index exists. Discovery of device wasnot successful.");
				}
				
				if ( false) {
					try{
						MyUsbDevice = MyUsbDeviceArray[FinalDeviceIndex];
						
						if(MyUsbDevice == null ) throw new Exception("Device not found");
						
						IUsbDevice wholeUsbDevice = MyUsbDevice as IUsbDevice;
						if(!ReferenceEquals(wholeUsbDevice, null)){
							// Select config #1
							wholeUsbDevice.SetConfiguration(1);
							wholeUsbDevice.ClaimInterface(0);
						}
						
						// open read endpoint 1
						UsbEndpointReader reader = MyUsbDevice.OpenEndpointReader(ReadEndpointID.Ep01);
						globalReader = reader;
					}
					catch(Exception ex){
						Console.WriteLine(ex);
					}
				}
				
				MonoUsbError e;
				myDeviceHandle = MatchingUsbDeviceList[FinalDeviceIndex].OpenDeviceHandle();
				
				if(myDeviceHandle == null || myDeviceHandle.IsInvalid)
				{
					throw new Exception(String.Format("Device not open previously {0}:{1}",
					MonoUsbDeviceHandle.LastErrorCode,
					MonoUsbDeviceHandle.LastErrorString
					));
				}
				
				
				// set configuration
				e = (MonoUsbError)(ret = MonoUsbApi.SetConfiguration(myDeviceHandle, 1));
				if(ret < 0){
					throw new Exception(String.Format("Failed SetConfiguration. {0}:{1}", e, MonoUsbApi.StrError(e)));
				}
				;;;
				// cliam interface
				e = (MonoUsbError)(ret = MonoUsbApi.ClaimInterface(myDeviceHandle, 0));
				if(ret < 0){
					throw new Exception(String.Format("Failed ClaimInterface. {0}:{1}", e, MonoUsbApi.StrError(e)));
				}
				;;;
				return true;
		}	
		
		public bool DiscoveryUsbDevice(Boolean assignFlag = false)
		{
			UsbRegDeviceList allDevices = UsbDevice.AllDevices;
			if(assignFlag){
				profileList = new MonoUsbProfileList();
				sessionHandle = new MonoUsbSessionHandle();
				
				if(sessionHandle.IsInvalid)
					throw new Exception(String.Format("libusb {0}:{1}", MonoUsbSessionHandle.LastErrorCode, 
					MonoUsbSessionHandle.LastErrorString));
				MyUsbDeviceArray = new UsbDevice[MAX_USB_DEVICE_COUNT];
			}else{
				
			}
			
			foreach(UsbRegistry usbRegistry in allDevices)
			{
				System.Console.WriteLine("Open one more ");
				if(usbRegistry.Open(out MyUsbDevice)){
					
					if((bt_vid == MyUsbDevice.Info.Descriptor.VendorID) && (bt_pid == MyUsbDevice.Info.Descriptor.ProductID)){
						MyUsbDeviceArray[UsbDeviceCount] = MyUsbDevice;
						UsbDeviceCount++;
					}else{
						System.Console.WriteLine( String.Format("device vid {0} pid {1}", MyUsbDevice.Info.Descriptor.VendorID, MyUsbDevice.Info.Descriptor.ProductID) );
					}
					
					for(int iConfig = 0; iConfig < MyUsbDevice.Configs.Count; iConfig++){
						UsbConfigInfo configInfo = MyUsbDevice.Configs[iConfig];
						Console.WriteLine(configInfo.ToString());
					}
				}
			}
			
			System.Console.WriteLine( String.Format("Open  {0}", UsbDeviceCount) );
			
			System.Console.WriteLine("begin");
			if(profileList != null)
				profileList.Refresh(sessionHandle);
			
			MonoUsbProfile myProfile = profileList.GetList().Find(MyVidPidPredicate);
			MatchingUsbDeviceList = profileList.GetList().FindAll(MyVidPidPredicate);
			
			if(myProfile == null ){
				Console.WriteLine("myProfile is 0");
				return false;
			}
			
			// Open the device handle to perfom I/O
			myDeviceHandle = myProfile.OpenDeviceHandle();
			if(myDeviceHandle.IsInvalid)
				throw new Exception(String.Format("{0}, {1}", MonoUsbDeviceHandle.LastErrorCode,
			MonoUsbDeviceHandle.LastErrorString));
			
			for(int i = 0; i< UsbDeviceCount; i++){
				object thisHubPort;
				int thisPortNum = -1;
				int thisHubNum = -1;
				char[] separatingChars = {'_', '.', '#'};
				
				MyUsbDeviceArray[i].UsbRegistryInfo.DeviceProperties.TryGetValue("LocationInformation", out thisHubPort);
				
				System.Console.WriteLine( String.Format("thisHubPort {0}", thisHubPort));
				string[] words = thisHubPort.ToString().Split(separatingChars, System.StringSplitOptions.RemoveEmptyEntries);
				
				if(words[0].Equals("Port")){
					thisPortNum = Convert.ToInt32(words[1]);
				}
				if(words[2].Equals("Hub")){
					thisHubNum = Convert.ToInt32(words[3]);
				}
				
				if(assignFlag){
					usbDeviceInfo = new UsbDeviceInfo();
					usbDeviceInfo.MyUsbDevice = MyUsbDeviceArray[i];
					usbDeviceInfo.Port = thisPortNum;
					usbDeviceInfo.Hub = thisHubNum;
					Console.WriteLine( String.Format("info {0},{1}", thisPortNum, thisHubNum));
					FinalDeviceIndex = (short)i;
				}
				else{
					if((usb_port == thisPortNum) && (usb_hub == thisHubNum))
					{
						System.Console.WriteLine( String.Format("usb_port {0}, usb_hub {1}", usb_port, usb_hub));
 						FinalDeviceIndex = (short)i;
						break;
					}
				}
				
			}
			
			return true;
		}
		
		//Async Read Method
		private void OnRxEndPointData(object sender, EndpointDataEventArgs e)
		{
			if(globalCallback != null)
			{
				Console.WriteLine("OnRxEndPointData");
				globalCallback(e.Buffer, e.Count);
			}
		}
		
		// 
		private int libusb_control_transfer(MonoUsbDeviceHandle deviceHandle, MonoUsbControlSetupHandle controlSetupHandle, int timeout)
		{
			MonoUsbTransfer transfer = MonoUsbTransfer.Alloc(0);
			ManualResetEvent completeEvent = new ManualResetEvent(false);
			GCHandle gcCompleteEvent = GCHandle.Alloc(completeEvent);
			
			transfer.FillControl(deviceHandle, controlSetupHandle, controlTransferDelegate, GCHandle.ToIntPtr(gcCompleteEvent), timeout);
			
			int r = (int)transfer.Submit();
			if(r < 0){
				transfer.Free();
				gcCompleteEvent.Free();
				return r;
			}
			
			while( !completeEvent.WaitOne(0, false) ){
				r = MonoUsbApi.HandleEvents(sessionHandle);
				if(r < 0){
					if (r == (int)MonoUsbError.ErrorInterrupted)
						continue;
					transfer.Cancel();
					while(!completeEvent.WaitOne(0, false)){
					    if(MonoUsbApi.HandleEvents(sessionHandle)< 0){
							System.Console.WriteLine("handleEvent < 0");
							break;
						}
					}
				}
			}
			
			if (transfer.Status == MonoUsbTansferStatus.TransferCompleted)
				r = transfer.ActualLength;
			else
				r = (int)MonoUsbApi.MonoLibUsbErrorFromTransferStatus(transfer.Status);
			
			transfer.Free();
			gcCompleteEvent.Free();
			return r;
		}
		
		public bool DisengageInterruptReader()
		{
			if (globalReader != null)
			{
				globalReader.DataReceived -= (OnRxEndPointData);
				globalReader.DataReceivedEnabled = false;
				globalCallback = null;
				Console.WriteLine("disengageInterruptReader");
			}
			return true;
		}
		
		public String Send(String cmd){
			String output = String.Empty;
			if(String.IsNullOrEmpty(cmd)) return "";
			
			int PDUSize = 2;
			int retryTime = 0;
			String OrgCmd = cmd;
			
			cmd = cmd.Replace(" ", "");
			
			byte[] byteData = new byte[(cmd.Length+1)/2];
			short index_in_array = 0;
			for(int i = 0; i< cmd.Length; i= i+PDUSize)
			{
				String subcmd = null;
				if( cmd.Length -i >= PDUSize ){
					subcmd = cmd.Substring(i, PDUSize);
				}else{
					subcmd = cmd.Substring(i);
				}
			}
			
			SendByteArray(byteData, index_in_array);
			
			return output;
		}
		
		private byte[] HexToByte(string msg)
		{
			byte[] comBuffer = null;
			try{
				msg = msg.Replace(" ", "");
				comBuffer = new byte[msg.Length/2];
				for(int i = 0; i < msg.Length; i +=2){
					comBuffer[i/2] = (byte) Convert.ToByte(msg.Substring(i,2), 16);
				}
			}catch(Exception ex)
			{
				
			}
			return comBuffer;
		}
	}
	
	public class UsbDeviceInfo{
		private UsbDevice myUsbDevice;
		private int port;
		private int hub;
		private Boolean reverved = false;
		
		public UsbDevice MyUsbDevice
		{
			get{return myUsbDevice;}
			set{myUsbDevice = value;}
		}
		public int Port
		{
			get{return port;}
			set{port = value;}
		}

		public int Hub
		{
			get{return hub;}
			set{hub = value;}
		}

		public Boolean Reverved
		{
			get{return reverved;}
			set{reverved = value;}
		}
		
	}
	
}


