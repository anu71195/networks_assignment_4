

#include "ns3/core-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/network-module.h"
#include "ns3/applications-module.h"
#include "ns3/wifi-module.h"
#include "ns3/wifi-remote-station-manager.h"
#include "ns3/mobility-module.h"
#include "ns3/csma-module.h"
#include "ns3/internet-module.h"
#include "ns3/string.h"
#include "ns3/netanim-module.h"
#include "ns3/flow-monitor-helper.h"

#include <stdio.h>
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
#include <string.h>
#include <fstream>


using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("ThirdScriptExample");


//class is made to take care of schedule of packet transfer(socket related function is defined in this class)
class app6 : public Application 
{
public:

  app6 ();
  virtual ~app6();

  void Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate);

private:
  
  void ScheduleTx (void);
  void SendPacket (void);

  Ptr<Socket>     m_socket;
  Address         m_peer;
  uint32_t        m_packetSize;
  uint32_t        m_nPackets;
  DataRate        m_dataRate;
  EventId         m_sendEvent;
  bool            m_running;
  uint32_t        m_packetsSent;
};

app6::app6 ()
  : m_socket (0), 
    m_peer (), 
    m_packetSize (0), 
    m_nPackets (0), 
    m_dataRate (0), 
    m_sendEvent (), 
    m_running (false), 
    m_packetsSent (0)  
{
}

app6::~app6()
{
  m_socket = 0;
}

void
app6::Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate)
{
  m_socket = socket;
  m_peer = address;
  m_packetSize = packetSize;
  m_nPackets = nPackets;
  m_dataRate = dataRate;
  
}





void 
app6::SendPacket (void)
{
  Ptr<Packet> packet = Create<Packet> (m_packetSize);
  m_socket->Send (packet);

  if (++m_packetsSent < m_nPackets)
    {
      ScheduleTx ();
    }
}

void 
app6::ScheduleTx (void)
{
  if (m_running)
    {
      Time tNext (Seconds ((m_packetSize * 8 / static_cast<double> (m_dataRate.GetBitRate ()))/30));
      //std::cout << tNext << "seconds\n";
      m_sendEvent = Simulator::Schedule (tNext, &app6::SendPacket, this);   //Interval between two packet transfer is 0.88 ms
    }
}


int 
main (int argc, char *argv[])
{
  bool verbose = true;
  //uint32_t nCsma = 3;
  uint32_t nWifi = 3;
  bool tracing = true;
  int RTSTHRESHOLD = 0; //INt value to be taken from the command line
  float simulation_time = 50.0; //seconds
  
  CommandLine cmd;
 // cmd.AddValue ("nCsma", "Number of \"extra\" CSMA nodes/devices", nCsma);
  //cmd.AddValue ("nWifi", "Number of wifi STA devices", nWifi);
  //cmd.AddValue ("verbose", "Tell echo applications to log if true", verbose);
  //cmd.AddValue ("tracing", "Enable pcap tracing", tracing);
  cmd.AddValue ("rtsthreshold","RtsThreshold",RTSTHRESHOLD);
  cmd.Parse (argc,argv);
  std::string RtsThreshold = std::to_string(RTSTHRESHOLD); //RtsCtsThreshold set from the command line input
  // Check for valid number of wifi nodes
  // 250 should be enough, otherwise IP addresses 
  // soon become an issue
  if (nWifi > 250 )
    {
      std::cout << "Too many wifi nodes, no more than 250 each." << std::endl;
      return 1;
    }

  if (verbose)     
    {
      LogComponentEnable ("UdpEchoClientApplication", LOG_LEVEL_INFO);
      LogComponentEnable ("UdpEchoServerApplication", LOG_LEVEL_INFO);
    }

 

 
  /*uint32_t threshold = 512;
  thresholdClass rtsCtsThreshold ;
  rtsCtsThreshold.SetRtsCtsThreshold(threshold);*/	
  //SetRtsCtsThreshold(threshold);

  Config::SetDefault ("ns3::WifiRemoteStationManager::RtsCtsThreshold", StringValue(RtsThreshold));
  Config::SetDefault ("ns3::WifiRemoteStationManager::FragmentationThreshold", StringValue ("2000")); //max size of fragment .. if fragment size is greater than fragThreshold, the extra bytes will be lost


//creates three nodes of wifi type
  NodeContainer wifiStaNodes;
  wifiStaNodes.Create (nWifi);
  //NodeContainer wifiApNode = p2pNodes.Get (0);


//creates channel between two nodes
  YansWifiChannelHelper channel = YansWifiChannelHelper::Default ();
  YansWifiPhyHelper phy = YansWifiPhyHelper::Default ();
  phy.SetChannel (channel.Create ());

  WifiHelper wifi;
  wifi.SetRemoteStationManager ("ns3::ConstantRateWifiManager");

  NqosWifiMacHelper mac = NqosWifiMacHelper::Default ();

  Ssid ssid = Ssid ("ns-3-ssid");
  mac.SetType("ns3::AdhocWifiMac");    //adhocWifiMac allows node to directly semd data to other nodes without using any routers
  NodeContainer wifistaNodes;
  wifistaNodes.Create (nWifi);


//add a device to each channel and install all the required info to the device
  NetDeviceContainer staDevices;
  staDevices = wifi.Install (phy, mac, wifiStaNodes);

  
  MobilityHelper mobility;
  mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
  mobility.Install (wifiStaNodes);

 /* SetPosition (wifiStaNodes.Get(0), Vector (0.0, 0.0, 0.0));
  SetPosition (wifiStaNodes.Get(1), Vector (250.0, 0.0, 0.0));
  SetPosition (wifiStaNodes.Get(2), Vector (500.0, 0.0, 0.0));*/


//fix the position of nodes
  AnimationInterface::SetConstantPosition (wifistaNodes.Get(0), 0, 0);
  AnimationInterface::SetConstantPosition (wifistaNodes.Get(1), 250, 0);
  AnimationInterface::SetConstantPosition (wifistaNodes.Get(2), 500, 0);


//add all protocols like tcp, udp, IP, etc to nodes
  InternetStackHelper stack;
  stack.Install (wifiStaNodes);


//node 1, node 2 and node 3 will have ip address 10.1.1.1, 10.1.1.2, and 10.1.1.3 respectively
  Ipv4AddressHelper address;

  address.SetBase ("10.1.1.0", "255.255.255.0");
  
  Ipv4InterfaceContainer wifiInterfaces;
  wifiInterfaces = address.Assign( staDevices );
  //address.Assign (staDevices);
  //address.Assign (apDevices);

  /*UdpEchoServerHelper echoServer (9);

  ApplicationContainer serverApps = echoServer.Install (wifiStaNodes.Get(1));
  serverApps.Start (Seconds (1.0));
  serverApps.Stop (Seconds (50.0));

  UdpEchoClientHelper echoClient (wifiInterfaces.GetAddress (1), 9);
  echoClient.SetAttribute ("MaxPackets", UintegerValue (100));
  echoClient.SetAttribute ("Interval", TimeValue (Seconds (1.0)));
  echoClient.SetAttribute ("PacketSize", UintegerValue (1024));
*/
/* initialize random seed: */
/*
  srand (time(NULL));


  ApplicationContainer clientApps1 = 
    echoClient.Install (wifiStaNodes.Get (0));
  clientApps1.Start (Seconds ((float)(rand()%401)/100  + 1));
  clientApps1.Stop (Seconds (50.0));

  ApplicationContainer clientApps2 = 
    echoClient.Install (wifiStaNodes.Get (2));
  clientApps2.Start (Seconds ((float)(rand()%401)/100  + 1));
  clientApps2.Stop (Seconds (50.0));*/

  srand (time(NULL));
  uint16_t sinkPort = 8080;   //port of middle node (treat it as a server node 
  Address sinkAddress (InetSocketAddress (wifiInterfaces.GetAddress (1), sinkPort));
  PacketSinkHelper packetSinkHelper ("ns3::TcpSocketFactory", InetSocketAddress (wifiInterfaces.GetAddress (1), sinkPort));

  ApplicationContainer serverApp = packetSinkHelper.Install (wifiStaNodes.Get(1));
  serverApp.Start (Seconds (0.));
  serverApp.Stop (Seconds (simulation_time));

  Ptr<Socket> ns3TcpSocket1 = Socket::CreateSocket (wifiStaNodes.Get (0), TcpSocketFactory::GetTypeId ());
  

  Ptr<app6> app1 = CreateObject<app6> ();
  app1->Setup (ns3TcpSocket1, sinkAddress, 1000, 10000000, DataRate ("300kbps"));
  wifiStaNodes.Get (0)->AddApplication (app1);
  app1->SetStartTime (Seconds ((float)(rand()%401)/100  + 1));
  app1->SetStopTime (Seconds (simulation_time));


  Ptr<Socket> ns3TcpSocket2 = Socket::CreateSocket (wifiStaNodes.Get (2), TcpSocketFactory::GetTypeId ());
  //ns3TcpSocket1->TraceConnectWithoutContext ("CongestionWindow", MakeCallback (&CwndChange));

  Ptr<app6> app2 = CreateObject<app6> ();
  app2->Setup (ns3TcpSocket2, sinkAddress, 1000, 10000000, DataRate ("300kbps"));
  wifiStaNodes.Get (2)->AddApplication (app2);
  app2->SetStartTime (Seconds ((float)(rand()%401)/100  + 1));
  app2->SetStopTime (Seconds (simulation_time));


  //Ipv4GlobalRoutingHelper::PopulateRoutingTables ();

  Simulator::Stop (Seconds (simulation_time));

  if (tracing == true)
    {
      //pointToPoint.EnablePcapAll ("third");
      //AsciiTraceHelper ascii;
      //phy.EnableAsciiAll (ascii.CreateFileStream ("wifitcp.tr"));
      phy.EnablePcapAll ("node");
      //phy.EnablePcap ("node1", staDevices.Get (0));
      //phy.EnablePcap ("node2", staDevices.Get (1));
      //phy.EnablePcap ("node3", staDevices.Get (2));
     
    }

  /*AnimationInterface anim ("ConstantRate.xml"); 
  
  anim.UpdateNodeDescription (wifiStaNodes.Get (1) , "AP"); // Optional
  anim.UpdateNodeDescription (wifiStaNodes.Get (0), "STA"); //b Optional*/

  Simulator::Run ();
  Simulator::Destroy ();
  return 0;
}
