from datetime import datetime
import glob

import pandas as pd

from chess_analyzer.core import parse_game_file


class AnalyzeGameSet:
    def __init__(self, df, username):
        self.df = df
        self.username = username

    @property
    def best_win(self):
        return self.df[self.df.is_win].sort_values("elo_spread").iloc[0]

    @property
    def game_count(self):
        return len(self.df)

    @property
    def win_count(self):
        return len(self.df[self.df.is_win])

    @property
    def last_elo(self):
        return (
            self.last_game.whiteelo
            if self.last_game.is_white
            else self.last_game.blackelo
        )

    @property
    def last_game(self):
        return self.df.sort_values("start_datetime").iloc[-1]

    @property
    def loss_count(self):
        return len(self.df[~self.df.is_win])

    @property
    def opponent_list(self):
        return (
            self.df[self.df.white != self.username].white.values.tolist()
            + self.df[self.df.black != self.username].black.values.tolist()
        )


def load_games(src):
    all_games = []
    filename_list = glob.glob(src)
    for filename in filename_list:
        with open(filename, "r") as f:
            all_games += [f.read()]
    return all_games


def enrich_game_dataframe(df, username):
    df["color"] = ["white" if item == username else "black" for item in df.white]
    df["ranking"] = [
        item.whiteelo if item.white == username else item.blackelo for item in df.iloc
    ]
    df["ranking"] = df.ranking.astype(int)
    df["is_win"] = [True if username in item.termination else False for item in df.iloc]
    df["termination_mode"] = [item.split(" ")[-1] for item in df.termination.iloc]
    df["whiteelo"] = df.whiteelo.astype(int)
    df["blackelo"] = df.blackelo.astype(int)
    df["is_white"] = [item.white == username for item in df.iloc]
    df["elo_spread"] = [
        item.whiteelo - item.blackelo
        if item.is_white
        else item.blackelo - item.whiteelo
        for item in df.iloc
    ]
    df["start_datetime"] = [
        datetime.strptime(f"{item.utcdate} {item.utctime}", "%Y.%m.%d %H:%M:%S")
        for item in df.iloc
    ]
    df["end_datetime"] = [
        datetime.strptime(f"{item.enddate} {item.endtime}", "%Y.%m.%d %H:%M:%S")
        for item in df.iloc
    ]
    df["gametime"] = [
        (item.end_datetime - item.start_datetime).seconds for item in df.iloc
    ]
    return df


def print_win_loss_report(analyze_game_set_object):
    print(f"Total Games: {analyze_game_set_object.game_count}")
    print(
        f"Total Wins: {analyze_game_set_object.win_count} "
        f"({analyze_game_set_object.win_count / analyze_game_set_object.game_count * 100 :.0f}%)"
    )
    print(
        f"Total Losses: {analyze_game_set_object.loss_count} "
        f"({analyze_game_set_object.loss_count / analyze_game_set_object.game_count * 100 :.0f}%)"
    )
    last_game = analyze_game_set_object.last_game
    print(f"Latest ELO: {analyze_game_set_object.last_elo}" f" ({last_game.date})")
    best_win = analyze_game_set_object.best_win
    print(
        f"Best Win: {best_win.elo_spread} - {best_win.white} ({best_win.whiteelo}) vs "
        f"{best_win.black} ({best_win.blackelo}) "
        f"{best_win.result} "
    )


def main(src, username):
    raw_games = load_games(src)
    parsed_games = [parse_game_file(item) for item in raw_games]
    df = pd.DataFrame(parsed_games)
    return enrich_game_dataframe(df, username)


if __name__ == "__main__":
    src = "data/*.pgn"
    username = "acviana"
    game_dataframe = main(src=src, username=username)
    print(f"{len(game_dataframe)} games found in {src}")

    ags = AnalyzeGameSet(df=game_dataframe, username=username)
    opponent_df = pd.DataFrame(ags.opponent_list)
    repeat_opponent_df = opponent_df[0].value_counts()[
        opponent_df[0].value_counts() > 1
    ]
    print_win_loss_report(ags)
    print(f"Total Opponents: {len(set(ags.opponent_list))}")
    print(f"Repeat Opponents: {len(repeat_opponent_df)}")
    print("\n")

    print(f"By time control: ")
    for item in game_dataframe.timecontrol.value_counts().index:
        print("\n")
        print(f"Time Control: {item}s")
        print_win_loss_report(
            AnalyzeGameSet(
                df=game_dataframe[game_dataframe.timecontrol == item], username=username
            )
        )
