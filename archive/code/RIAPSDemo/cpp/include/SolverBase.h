//
// Auto-generated by edu.vanderbilt.riaps.generator.ComponenetGenerator.xtend
//

#ifndef RIAPS_CORE_SOLVER_H
#define RIAPS_CORE_SOLVER_H

#include "componentmodel/r_componentbase.h"
#include "ReqAddr.capnp.h"
#include "RepAddr.capnp.h"

// Name of the ports from the model file
#define PORT_REQ_CONTRACTADDR "contractAddr"
#define PORT_TIMER_POLLER "poller"
#define PORT_TIMER_SOLVE "solve"

namespace transactiveenergy {
   namespace components {
      
      class SolverBase : public riaps::ComponentBase {
         
         public:
         SolverBase(_component_conf &config, riaps::Actor &actor);
         
         bool SendContractAddr(capnp::MallocMessageBuilder&    messageBuilder,
         ReqAddr::Builder& message);
         
         bool RecvContractAddr(RepAddr::Reader &message);
         
         virtual void OnPoller(riaps::ports::PortBase *port)=0;
         
         virtual void OnSolve(riaps::ports::PortBase *port)=0;
         
         virtual ~SolverBase();
         protected:
         virtual void DispatchMessage(capnp::FlatArrayMessageReader* capnpreader, riaps::ports::PortBase *port,std::shared_ptr<riaps::MessageParams> params=nullptr );
         virtual void DispatchInsideMessage(zmsg_t* zmsg, riaps::ports::PortBase* port);
      };
   }
}
#endif //RIAPS_CORE_SOLVER_H
