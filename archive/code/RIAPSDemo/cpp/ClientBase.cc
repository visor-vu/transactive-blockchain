//
// Auto-generated by edu.vanderbilt.riaps.generator.ComponenetGenerator.xtend
//
#include <ClientBase.h>

namespace transactiveenergy {
   namespace components {
      
      ClientBase::ClientBase(_component_conf &config, riaps::Actor &actor) : ComponentBase(config, actor) {
         
      }
      
      void ClientBase::DispatchMessage(capnp::FlatArrayMessageReader* capnpreader, riaps::ports::PortBase *port,std::shared_ptr<riaps::MessageParams> params) {
         auto portName = port->GetPortName();
         
      }
      
      void ClientBase::DispatchInsideMessage(zmsg_t* zmsg, riaps::ports::PortBase* port) {
         //empty the header
      }
      
      bool ClientBase::SendDso(capnp::MallocMessageBuilder &messageBuilder,
      ReqAddr::Builder &message) {
         //std::cout<< "ClientBase::SendDso()"<< std::endl;
         return SendMessageOnPort(messageBuilder, PORT_REQ_DSO);
      }
      
      bool ClientBase::RecvDso(RepAddr::Reader &message) {
         //std::cout<< "ClientBase::RecvDso()"<< std::endl;
         auto port = GetRequestPortByName(PORT_REQ_DSO);
         if (port == NULL) return false;
         
         capnp::FlatArrayMessageReader* messageReader;
         
         if (port->Recv(&messageReader)){
            message = messageReader->getRoot<RepAddr>();
            return true;
         }
         return false;
      }
      
      ClientBase::~ClientBase() {
         
      }
   }
}
