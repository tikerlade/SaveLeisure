# configure update, context

def test_send_book:
    # configure update, context
    stage = start(update, context)
    assert stage == FIRST
    # TODO