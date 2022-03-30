import sys, requests
import credentials

JB_BASE_ASSET_URL  = 'https://support.engineering.oregonstate.edu/Assets/Edit{}'
COETOOL_BASE_URL   = 'https://tools.engr.oregonstate.edu/coetools/jitbit/?name={}'
COETOOL_API_URL = 'https://tools.engr.oregonstate.edu/coetools/api/'
CYDER_BASE_URL     = 'https://cyder.oregonstate.edu/search/?search={}'
ACTLOG_BASE_URL    = 'https://tools.engr.oregonstate.edu/coetools/lablogs/labinfo.php?hostname={}'


class Jitbit():
  def __init__(self, asset_name):
    data = {
        'api': credentials.api,
        'name': asset_name
    }
    req = requests.post(COETOOL_API_URL, data=data)
    self.asset_json = req.json()
  
  def get_url(self):
    asset_id   = self.asset_json[0]['ItemID']
    asset_url  = JB_BASE_ASSET_URL.format(f"/{asset_id}")
    return asset_url

class Cyder():
    def __init__(self, asset_name):
      self.cyder_url = CYDER_BASE_URL.format(asset_name)
    
    def get_url(self):
      return self.cyder_url

class Log():
    def __init__(self, asset_name):
      self.log_url = ACTLOG_BASE_URL.format(asset_name)
    
    def get_url(self):
      return self.log_url