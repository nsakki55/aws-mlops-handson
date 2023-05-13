from predictor.request import AdRequest


def test_ad_request():
    input = {
        "hour": "21011500",
        "banner_pos": "1",
        "site_id": "AAA",
        "site_domain": "site_A",
        "site_category": "A",
        "app_id": "111",
        "app_domain": "app_A",
        "app_category": "A",
        "device_id": "device_1",
        "device_ip": "192.0.2.1",
        "device_model": "model_A",
        "device_type": "1",
    }
    request = AdRequest(**input)

    assert request.hour == "21011500"
    assert request.banner_pos == "1"
    assert request.site_id == "AAA"
    assert request.site_domain == "site_A"
    assert request.site_category == "A"
    assert request.app_id == "111"
    assert request.app_domain == "app_A"
    assert request.app_category == "A"
    assert request.device_id == "device_1"
    assert request.device_ip == "192.0.2.1"
    assert request.device_model == "model_A"
    assert request.device_type == "1"
