import json
from datetime import datetime
from typing import Dict, Any

from .pii_masking import mask
from .transformer import Transformer


class PiiTransformer(Transformer):

    def transform(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data_ = json.loads(data["Body"])
        if "user_id" not in data_:
            print(data_, "yehi hai")
        masked_data = {
            "user_id": data_["user_id"],
            "device_type": data_["device_type"],
            "masked_ip": mask(data_["ip"]),
            "masked_device_id": mask(data_["device_id"]),
            "locale": data_["locale"],
            "app_version": int(data_["app_version"].split('.')[0]),
            "create_date": datetime.now()
        }
        return masked_data
