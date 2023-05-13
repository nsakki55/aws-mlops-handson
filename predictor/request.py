from pydantic import BaseModel


class AdRequest(BaseModel):
    hour: str
    banner_pos: str
    site_id: str
    site_domain: str
    site_category: str
    app_id: str
    app_domain: str
    app_category: str
    device_id: str
    device_ip: str
    device_model: str
    device_type: str
