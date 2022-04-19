import click

from extract_rb import RbExtractor


@click.command()
@click.argument("rb_id", default=367482)
def crawl(rb_id: int):
    rb = RbExtractor(rb_id, "be")
    rb.extract()


if __name__ == "__main__":
    # rb_id = 368066
    crawl()
