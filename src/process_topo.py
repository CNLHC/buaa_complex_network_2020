from xml.dom.minidom import parse, parseString
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LineSet:
    def __init__(self):
        self._stable = {}
        self._dtable = {}

    def _append_line(self, d1: dict, sid: str, did: str, line: ET.Element):
        if d1.get(sid) is None:
            d1[sid] = {did: line}
        else:
            d1[sid][did] = line

    def add_line(self, obj: ET.Element):
        print(obj)
        src_id = obj.get("srcDeviceID")
        dst_id = obj.get("destDeviceID")
        self._append_line(self._stable, src_id, dst_id, obj)
        self._append_line(self._dtable, dst_id, src_id, obj)

    def get_by_srcid(self, sid):
        return self._stable.get(sid)

    def get_by_dstid(self, did):
        return self._stable.get(did)

    def get_by_pair(self, sid, did):
        t = self.get_by_srcid(sid).get(did)
        if t is None:
            return self.get_by_srcid(did).get(sid)


class DeviceSet:
    def __init__(self):
        self._table = {}
        self._name2id = {}

    def add_device(self, obj: ET.Element):
        _id = obj.get('id')
        self._table[_id] = obj
        self._name2id[obj.get('name')] = _id

    def get_device_by_id(self, _id):
        return self._table.get(_id)

    def get_device_by_name(self,name):
        return self._table.get(self._name2id.get())

    def get_all_ids(self):
        return self._table.keys()

    def get_all_names(self):
        return self._name2id.keys()


class Topo:
    def __init__(self):
        self.device = DeviceSet()
        self.line = LineSet()

    def load_topo(self, fp):
        self.parser = ET.XMLParser(encoding='utf-8')
        self.tree = ET.parse('./sample/as4.topo', parser=self.parser)
        for device in self.tree.find('devices'):
            self.device.add_device(device)
        for line in self.tree.find('lines'):
            self.line.add_line(line)


tp = Topo()
tp.load_topo(1)
