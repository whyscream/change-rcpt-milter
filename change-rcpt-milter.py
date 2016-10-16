"""Main class file for the Change Recipient Milter."""

import logging

import Milter

MILTER_NAME = "change-rcpt-milter"
MILTER_VERSION = "0.1"

logger = logging.getLogger(MILTER_NAME)


class ChangeRecipientMilter(Milter.Base):
    """
    An e-mail milter that changes the envelope recipient of messages passed trough it.

    The milter can be used to redirect messages from one user to another, or from
    spamtrap address to a single spam storage account.
    """

    mapping = {'test@whyscream.net': 'tom@whyscream.net'}
    replacements = []

    def envrcpt(self, rcpt, *params):
        """Store the received recipients."""
        if params:
            logger.info("Received recipient address '{}' with params '{}'".format(rcpt, " ".join(params)))
        else:
            logger.info("Received recipient address '{}'".format(rcpt))
        try:
            match = self.mapping[rcpt.lower()]
            self.replacements.append((rcpt, match))
            logger.info("Will replace '{}' with new recipient '{}'".format(rcpt, match))
        except KeyError:
            # nothing found
            pass

    def data(self):
        """All recipients have been sent, evaluate the list and change recipient(s) if necessary."""
        for (original, new) in self.replacements:
            self.delrcpt(original)
            logger.info("Deleted original recipient: '{}'".format(original))
            self.addrcpt(new)
            logger.info("Added new recipient '{}'".format(new))


def main():
    """Start the milter."""
    socket = "/tmp/change-rcpt-milter.sock"
    timeout = 600
    Milter.factory = ChangeRecipientMilter
    logger.info("{} {} starting".format(MILTER_NAME, MILTER_VERSION))
    Milter.runmilter(MILTER_NAME, socket, timeout)
    logger.info("{} {} shutting down".format(MILTER_NAME, MILTER_VERSION))


if __name__ == "__main__":
    main()
