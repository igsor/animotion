from dependency_injector import containers, providers

from animotion.device.camera.null.null import Null


class CameraContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    camera = providers.Factory(Null)
