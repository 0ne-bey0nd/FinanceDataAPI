import typer

app = typer.Typer()


@app.command()
def dayK(begin: int, end: int):
    """
    Get the dayK data from the begin date to the end date.
    """

    # arg check
    assert begin < end, "The begin date should be earlier than the end date."

    print(f"Get the dayK data from {begin} to {end}.")


if __name__ == '__main__':
    app()
