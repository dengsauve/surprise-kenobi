from pulumi.provider.experimental import component_provider_host
from surprisekenobi import SurpriseKenobi

if __name__ == "__main__":
    component_provider_host(name="surprise-kenobi-component", components=[SurpriseKenobi])

