import json
from unittest import TestCase, main
from lesson_3.client import presence, get_addr_port, read_answer


test_data = {
    "action": "presence",
    "time": 1.123,
    "type": "status",
    "user": {"account_name": "account_name", "status": "status"},
}


def for_test_msg_to_client(d):
    if d["action"] == "presence":
        msg = {"response": 200, "time": 1.123, "alert": "All clear"}
        msg = json.dumps(msg, indent=4).encode("utf-8")
        return msg


class TestClient(TestCase):
    def test_presence(self):
        test_result = presence(account_name="account_name", status="status")
        test_result["time"] = 1.123  # time = 1.123
        self.assertEqual(test_result, test_data)

    def test_get_addr_port(self):
        self.assertEqual(
            str(get_addr_port()),
            "Namespace(addr='localhost', port=7777, user='Varvara', status='2 "
            "years')",
        )

    def test_read_answer(self):
        # server imitation
        test_result = json.loads(for_test_msg_to_client(test_data))
        expected_output = read_answer(test_result)
        actual_result = (200, "All clear")  # tougt out result
        self.assertEqual(expected_output, actual_result)


if __name__ == "__main__":
    main()
