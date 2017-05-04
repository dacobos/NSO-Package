# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service
import device_helper


# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        vplsID = service.vplsID
        originNode = service.originNode
        originNodeIP = '10.0.0.1'
        localInterface = service.localInterface
        vlanID = service.vlanID
        for spoke in service.spokes:
            pwID = spoke.pwID
            destinationNodeIP = '10.0.0.2'
            destinationNode = spoke.destinationNode
            remoteInterface = spoke.remoteInterface


        # loopback0 = None
        #
        # try :
        #     originNodeType = device_helper.get_device_type(root, originNode)
        #     originNodeConfig = root.ncs__devices.ncs__device[originNode].ncs__config
        #
        #     if originNodeType == TYPE_CISCO_IOSXR:
        #         loopback0 = originNodeConfig.cisco_ios_xr__interface.Loopback[loopback_interface]
        #         pe1_loopback = loopback0.ipv4.address.ip
        #         print pe1_loopback


        vars = ncs.template.Variables()
        vars.add('vplsID', vplsID)
        vars.add('originNode', originNode)
        vars.add('originNodeIP', originNodeIP)
        vars.add('localInterface', localInterface)
        vars.add('vlanID', vlanID)
        vars.add('pwID', pwID)
        vars.add('destinationNodeIP', destinationNodeIP)
        vars.add('destinationNode', destinationNode)
        vars.add('remoteInterface', remoteInterface)
        template = ncs.template.Template(service)
        template.apply('multipoint-template', vars)




# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('multipoint-servicepoint', ServiceCallbacks)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
