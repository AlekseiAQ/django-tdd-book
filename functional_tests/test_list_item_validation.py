from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')


    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # The browser intercepts the request, and does not load the
        # list page
        self.assertNotIn(
            'Buy milk',
            self.browser.find_element_by_tag_name('body').text
        )
        # She tries again with some text for the item, which now works
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys('\n')

        # Again, the browser will not comply
        self.check_for_row_in_list_table('1: Buy milk')
        rows = self.browser.find_elements_by_css_selector('#id_list_table tr')
        self.assertEqual(len(rows), 1)

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')


    def test_cannot_add_duplicate_items(self):
        # Edith goes to the home page and starts a new list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1: Buy wellies')

        # She accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys('Buy wellies\n')

        # She sees a helpful error message
        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")


    def test_error_messages_are_cleared_on_input(self):
        # Edith starts a list and causes a validation error:
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Banter too thick\n')
        self.check_for_row_in_list_table('1: Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick\n')

        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        # She starts typing in the input box to clear the error
        self.get_item_input_box().send_keys('a')

        # She is pleased to see that the error message disappears
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())
