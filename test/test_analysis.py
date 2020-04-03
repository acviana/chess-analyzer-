from datetime import datetime
import json

import pandas as pd

from chess_analyzer.analysis import enrich_game_dataframe
from chess_analyzer.core import parse_game_file


def load_fixture():
    with open("test/test_game.pgn") as f:
        return f.read()


def load_expected_result():
    return {
        "event": "Hello!",
        "site": "Chess.com",
        "date": "2009.09.17",
        "round": "-",
        "white": "jsssuperstar",
        "black": "erik",
        "result": "0-1",
        "eco": "A04",
        "ecourl": "https://www.chess.com/openings/Reti-Opening-Pirc-Invitation",
        "currentposition": "8/8/8/p7/8/6k1/4n1b1/6K1 w - - 51 90",
        "timezone": "UTC",
        "utcdate": "2009.09.17",
        "utctime": "21:40:19",
        "whiteelo": 1306,
        "blackelo": 2061,
        "timecontrol": "1/259200",
        "termination": "erik won by checkmate",
        "starttime": "21:40:19",
        "enddate": "2009.10.31",
        "endtime": "17:53:17",
        "link": "https://www.chess.com/daily/game/28103371",
        "game": "1. Nf3 d6 2. Nc3 g6 3. e4 Bg7 4. Bc4 Nf6 5. d4 O-O 6. O-O a6 7. a4 c5 8. dxc5 dxc5 9. Be3 b6 10. Qd2 Qc7 11. Bh6 Rd8 12. Qc1 Bb7 13. e5 Ng4 14. Bxg7 Kxg7 15. Qf4 f5 16. h3 Nh6 17. Ng5 Bc8 18. Be6 Rd4 19. Qh2 Bb7 20. Bxf5 Kh8 21. Be4 Bxe4 22. Ne6 Qb7 23. Qf4 Bf5 24. Nxd4 cxd4 25. Qxh6 Nc6 26. Ne2 Bxc2 27. Qd2 d3 28. Nc1 Rd8 29. f4 a5 30. f5 Nxe5 31. fxg6 Nxg6 32. Rf7 Qd5 33. Rf3 Ne5 34. Rf5 Qe4 35. Qf2 Rg8 36. Rf8 Nc4 37. Rxg8+ Kxg8 38. Qg3+ Kf7 39. b3 Qe3+ 40. Qxe3 Nxe3 41. Nxd3 Bxd3 42. Rc1 Bf5 43. Rc3 Nd5 44. Rf3 Ke6 45. g4 Bg6 46. h4 Be4 47. Rg3 Ke5 48. h5 Kf4 49. Kh2 Ne3 50. Kh3 Bc2 51. g5 Bxb3 52. g6 hxg6 53. Rxg6 Bf7 54. Rxb6 Bxh5 55. Rb5 Bg4+ 56. Kh2 Nc4 57. Kg2 Be2 58. Kf2 Bd3 59. Rd5 Ke4 60. Rb5 Kd4 61. Ke1 Bc2 62. Rg5 e5 63. Ke2 Bxa4 64. Rxe5 Nxe5 65. Kd2 Bb5 66. Kc2 Nf3 67. Kb3 Kc5 68. Ka3 Kc4 69. Kb2 Kb4 70. Ka2 Bc4+ 71. Kb2 Ne5 72. Ka1 Kb3 73. Kb1 Kc3 74. Ka1 Nd3 75. Kb1 Nb4 76. Kc1 Ba2 77. Kd1 Kd3 78. Kc1 Kc3 79. Kd1 Bc4 80. Ke1 Kd3 81. Kf2 Ke4 82. Kg3 Be6 83. Kh2 Kf3 84. Kh1 Nd3 85. Kg1 Bh3 86. Kh2 Nf4 87. Kg1 Kg3 88. Kh1 Bg2+ 89. Kg1 Ne2# 0-1",
        "color": "black",
        "ranking": 2061,
        "is_win": True,
        "termination_mode": "checkmate",
        "is_white": False,
        "elo_spread": 755,
        "start_datetime": datetime(2009, 9, 17, 21, 40, 19),
        "end_datetime": datetime(2009, 10, 31, 17, 53, 17),
        "gametime": 72778,
    }


def test_enrich_game_dataframe():
    expected_result = load_expected_result()
    test_fixture = load_fixture()
    parsed_game = parse_game_file(test_fixture)
    df = pd.DataFrame([parsed_game])
    username = "erik"
    enriched_game = enrich_game_dataframe(df=df, username=username)
    assert enriched_game.loc[0].to_dict() == expected_result
