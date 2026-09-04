from ace_agent.actions import parse_call, normalize


def test_click_action():
    action = normalize(parse_call("Action: click(start_box='<|box_start|>(123,456)<|box_end|>')"))
    assert action.name == "click"
    assert action.args["box"] == [123, 456, 123, 456]


def test_double_click_action():
    action = normalize(parse_call("Action: left_double(start_box='<|box_start|>(10,20)<|box_end|>')"))
    assert action.name == "left_double"
    assert action.args["box"] == [10, 20, 10, 20]


def test_drag_action():
    action = normalize(
        parse_call(
            "Action: drag(start_box='<|box_start|>(10,20)<|box_end|>', "
            "end_box='<|box_start|>(100,200)<|box_end|>')"
        )
    )
    assert action.args["start_box"] == [10, 20, 10, 20]
    assert action.args["end_box"] == [100, 200, 100, 200]


def test_hotkey_action():
    action = normalize(parse_call("Action: hotkey(key='ctrl c')"))
    assert action.args["keys"] == ["ctrl", "c"]
