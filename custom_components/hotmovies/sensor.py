"""
A component which allows you to parse http://58921.com/ get hot movies

For more details about this component, please refer to the documentation at
https://github.com/aalavender/HotMovies/

"""
import logging
import asyncio
import voluptuous as vol
from datetime import timedelta
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (PLATFORM_SCHEMA)
from homeassistant.const import (CONF_NAME)
from requests import request
from bs4 import BeautifulSoup

__version__ = '0.1.0'
_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['requests', 'beautifulsoup4']

COMPONENT_REPO = 'https://github.com/aalavender/HotMovies/'
SCAN_INTERVAL = timedelta(hours=8)
ICON = 'mdi:movie-roll'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
})


@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    _LOGGER.info("async_setup_platform sensor HotMoviesSensor")
    async_add_devices([HotMoviesSensor(config[CONF_NAME])], True)


class HotMoviesSensor(Entity):
    def __init__(self, name):
        self._name = name
        self._state = None
        self._update_time = None
        self._entries = []

    def update(self):
        _LOGGER.info("HotMoviesSensor update info from http://58921.com/ ")
        self._entries = []
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
        }
        response = request('GET', 'http://58921.com/', headers=header)  # 定义头信息发送请求返回response对象
        response.encoding = 'utf-8'   #不写这句会乱码
        soup = BeautifulSoup(response.text, "lxml")
        trs = soup.select('#box_office_live_summary > div > table > tbody > tr')
        self._state = len(trs)
        self._update_time = trs[len(trs)-1].text[12:].strip()
        for i in range(0, self.state-1):
            entryValue = {}
            tds = trs[i].select('td')
            entryValue["title"] = tds[0].text
            entryValue["day"] = tds[3].text
            entryValue["total"] = tds[4].text
            self._entries.append(entryValue)

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return ICON

    @property
    def update_time(self):
        return self._update_time

    @property
    def device_state_attributes(self):
        return {
            'entries': self._entries
        }
