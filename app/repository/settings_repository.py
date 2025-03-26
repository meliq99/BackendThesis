from models.settings_models import Device

def create_device(device: Device, session):
    session.add(device)
    session.commit()
    session.refresh(device)
    return device