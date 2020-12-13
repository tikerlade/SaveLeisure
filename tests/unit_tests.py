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
    assert get_items_number(update, context) == END_CONFIRMATION

def test_get_info:
    assert get_info(update, context) == END_CONFIRMATION

def test_stat:
    assert stat(update, context) == END_CONFIRMATION

def test_new_item_type:
    assert new_item_type(update, context) == THIRD

def test_end:
    assert end(update, context) == END