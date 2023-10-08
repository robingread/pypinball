import pypinball.display.pygame_lives


def test_get_surface_size() -> None:
    """Test the get_surface_size() method to ensure that the return tuple is as expected."""
    res = pypinball.display.pygame_lives.get_surface_size(
        num_lives=3, icon_size=10, icon_spacing=2
    )
    exp = (34, 10)
    assert res == exp


def test_get_life_icon_coordinate_0() -> None:
    """Test the get_life_icon_cooridnate() method when zero lives are left."""
    res = pypinball.display.pygame_lives.get_life_icon_coordinate(
        width=10,
        icon_spacing=2,
        life_index=0,
    )
    exp = (0, 0)
    assert res == exp


def test_get_life_icon_coordinate_1() -> None:
    """Test the get_life_icon_cooridnate() method when one life is left."""
    res = pypinball.display.pygame_lives.get_life_icon_coordinate(
        width=10,
        icon_spacing=2,
        life_index=1,
    )
    exp = (12, 0)
    assert res == exp


def test_get_life_icon_coordinate_2() -> None:
    """Test the get_life_icon_cooridnate() method when two lives is left."""
    res = pypinball.display.pygame_lives.get_life_icon_coordinate(
        width=10,
        icon_spacing=2,
        life_index=2,
    )
    exp = (24, 0)
    assert res == exp


def test_get_life_icon_coordinate_3() -> None:
    """Test the get_life_icon_cooridnate() method when three lives is left."""
    res = pypinball.display.pygame_lives.get_life_icon_coordinate(
        width=10,
        icon_spacing=2,
        life_index=3,
    )
    exp = (36, 0)
    assert res == exp
