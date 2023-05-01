import re
import unittest
from datetime import datetime
from lesson_3.server import create_socket_server, msg_to_client, get_params

test_data = {
    "action": "ERROR_ACTION",  # Wrong action
    "time": datetime.timestamp(datetime.now()),
    "type": "status",
    "user": {"account_name": "account_name", "status": "status"},
}


class TestServer(unittest.TestCase):
    def test_create_socket_server(self):
        search_point = re.search("laddr=(.*)>", str(create_socket_server("", 7777)))
        self.assertEqual(search_point.group(), "laddr=('0.0.0.0', 7777)>")

    def test_msg_to_client(self):
        # Wrong action == None
        self.assertEqual(msg_to_client(test_data, client="test_client"), None)

    def test_get_addr_port(self):
        # Default port test
        self.assertEqual(str(get_params()), "Namespace(addr='', port=7777)")

    def test_get_another_port(self):
        # Non-default port test
        parsed = get_params()
        parsed.port = "8888"
        self.assertEqual(str(parsed.port), "8888")


if __name__ == "__main__":
    unittest.main()
