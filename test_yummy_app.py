import unittest
from unittest.mock import patch

import gps_service
from yummy_app import YummyApp


class TestEasyLevel(unittest.TestCase):
    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        self.assertEqual(self.app.calculate_order_total({"pho": 2}), 100000)

    def test_calculate_total_for_multiple_items(self):
        self.assertEqual(self.app.calculate_order_total({"pho": 1, "bun": 1}), 95000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        self.assertEqual(self.app.calculate_order_total({"pho": 0}), 0.0)


class TestMediumLevel(unittest.TestCase):
    def test_online_valid_promo(self):
        self.assertEqual(YummyApp().apply_promo_code(100000, "GIAM10"), 90000)

    def test_offline_connection_error(self):
        with self.assertRaises(ConnectionError):
            YummyApp(network_status="offline").apply_promo_code(100000, "GIAM10")

    def test_new_os_promo_on_os_15(self):
        self.assertEqual(
            YummyApp(os_version=15).apply_promo_code(100000, "NEW_OS_ONLY"),
            80000,
        )

    def test_new_os_promo_on_os_14_raises_value_error(self):
        with self.assertRaises(ValueError):
            YummyApp(os_version=14).apply_promo_code(100000, "NEW_OS_ONLY")

    def test_invalid_promo_code(self):
        with self.assertRaises(ValueError):
            YummyApp().apply_promo_code(100000, "INVALID")


class TestHardLevel(unittest.TestCase):
    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_inside_supported_area(self, mock_location):
        mock_location.return_value = (10.0, 105.0)
        self.assertEqual(
            YummyApp().get_nearby_restaurants(),
            ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"],
        )
        mock_location.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_outside_supported_area(self, mock_location):
        mock_location.return_value = (20.0, 110.0)
        self.assertEqual(YummyApp().get_nearby_restaurants(), [])

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_signal_lost(self, mock_location):
        mock_location.side_effect = gps_service.GPSSignalLostError()
        self.assertEqual(
            YummyApp().get_nearby_restaurants(),
            "Khong the xac dinh vi tri.",
        )


if __name__ == "__main__":
    unittest.main()
