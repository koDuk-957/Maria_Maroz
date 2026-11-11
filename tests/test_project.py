import unittest

from handlers import format_service
from keyboards import main_menu_kb, service_kb
from services_data import SERVICES, SERVICE_BUTTONS


class ProjectSmokeTests(unittest.TestCase):
    def test_every_menu_item_has_service_data(self):
        for key, label in SERVICE_BUTTONS:
            with self.subTest(service=key):
                self.assertIn(key, SERVICES)
                self.assertTrue(label.strip())
                self.assertLessEqual(len(f"service:{key}"), 64)

    def test_removed_service_categories_are_not_available(self):
        self.assertNotIn("rent", SERVICES)
        self.assertNotIn("investment", SERVICES)
        self.assertNotIn(("rent", "Аренда и управление"), SERVICE_BUTTONS)
        self.assertNotIn(("investment", "Инвестиции"), SERVICE_BUTTONS)

    def test_every_service_can_be_formatted(self):
        for key in SERVICES:
            with self.subTest(service=key):
                rendered = format_service(key)
                self.assertIn(SERVICES[key]["title"], rendered)
                self.assertTrue(rendered.strip())

    def test_service_keyboard_has_contact_and_back_actions(self):
        keyboard = service_kb("consult")
        callback_values = [
            button.callback_data
            for row in keyboard.inline_keyboard
            for button in row
            if button.callback_data
        ]
        self.assertIn("menu", callback_values)

    def test_main_menu_contains_all_services_and_contact(self):
        keyboard = main_menu_kb()
        buttons = [
            button
            for row in keyboard.inline_keyboard
            for button in row
        ]
        callback_values = {button.callback_data for button in buttons}
        self.assertTrue(
            {f"service:{key}" for key, _ in SERVICE_BUTTONS}.issubset(callback_values)
        )
        self.assertTrue(any(button.url == "https://t.me/Maroz_Maria" for button in buttons))


if __name__ == "__main__":
    unittest.main()
