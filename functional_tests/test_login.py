import os
import poplib
import re
import time
from django.core import mail

from .base import FunctionalTest


SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        if self.against_staging:
            test_email = 'madspadestv@gmail.com'
        else:
            test_email = 'edith@example.com'

        self.browser.get(self.server_url)
        self.browser.find_element_by_name('email').send_keys(
            test_email + '\n'
        )

        # A message appears telling her an email has been sent
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Check your email', body.text)

        # She checks her email and finds a message
        body = self.wait_for_email(test_email, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(
                'Could not find url in email body:\n{}'.format(body)
            )
        url = url_search.group(0)
        self.assertIn(self.server_url, url)

        # she clicks it
        self.browser.get(url)

        # she is logged in!
        self.assert_logged_in(email=test_email)

        # Now she logs out
        self.browser.find_element_by_link_text('Log out').click()

        # She is logged out
        self.assert_logged_out(email=test_email)


    def wait_for_email(self, test_email, subject):
        if not self.against_staging:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        subject_line = 'Subject: {}'.format(subject)
        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.mail.yahoo.com')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['YAHOO_PASSWORD'])
            while time.time() - start < 60:
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    print(lines)
                    if subject_line in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()
