# configure update, context

def test_start:   
    assert start(update, context) == FIRST

def test_new_iteration:
    assert new_iteration(update, context) == FIRST

def test_new_item:
    assert new_item(update, context) == SECOND

def test_get_items:
    assert get_items(update, context) == FOURTH

def test_get_items_type:
    assert get_items_type(update, context) == FIFTH

def test_get_items_number:
    