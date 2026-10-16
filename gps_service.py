class GPSSignalLostError(Exception):
    """Ngoai le khi thiet bi mat tin hieu GPS."""


def get_current_location():
    """Mo phong phan cung GPS."""
    return (10.0, 105.0)
