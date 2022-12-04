import argparse
import logging
import time

from typing import Any
from lib.waveshare_epd import epd7in5_V2
from DestBoardTable import DestBoardTable


logging.basicConfig(level=logging.INFO)


def main(args: Any) -> None:
    """
    Main method.

    Parameters
    ----------
    args : Any
        Command line arguments.
    """
    logging.info('----- start -----')
    try:
        table_row: int = args.tr
        table_column: int = args.tc
        margin_width: int = args.mw
        margin_height: int = args.mh
        padding_left: int = args.pl
        padding_top: int = args.pt
        cell_name_ratio: float = args.cnr

        epd = epd7in5_V2.EPD()
        # 7in5: 800 x 480
        logging.info(f"(epd.width, epd.height) = ({epd.width}, {epd.height})")

        # generate Table instance
        table = DestBoardTable(
                epd.width, epd.height,
                margin_width, margin_height,
                padding_left, padding_top,
                table_row, table_column, cell_name_ratio,
                '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 36)

        # get table info
        logging.info(f"(width, height) = ({table.width}, {table.height})")
        logging.info(f"(x1, y1, x2, y2) = ({table.x1}, {table.y1}, {table.x2}, {table.y2})")

        logging.info('init and Clear')
        epd.init()
        epd.Clear()

        table.set_name(0, 0, "小林")
        table.set_status(0, 0, "12/31 AM休暇")

        while True:
            try:
                epd.display(epd.getbuffer(table.Himage))
                time.sleep(3600)
                logging.info('Clear...')
                epd.init()
                epd.Clear()

            except KeyboardInterrupt:
                raise

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info('ctrl + c:')
        epd7in5_V2.epdconfig.module_exit()

        logging.info('Clear...')
        epd.init()
        epd.Clear()

        logging.info('Goto Sleep...')
        epd.sleep()

    logging.info('----- end -----')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Electronic destination board for Waveshare e-Paper display.')
    _ = parser.add_argument('--tr', metavar='TABLE_ROW', type=int, default=6, help='Number of table row, by default 6.')
    _ = parser.add_argument('--tc', metavar='TABLE_COLUMN', type=int, default=2, help='Number of table column, by default 2.')
    _ = parser.add_argument('--mw', metavar='MARGIN_WIDTH', type=int, default=5, help='Width margin size of table, by default 5.')
    _ = parser.add_argument('--mh', metavar='MARGIN_HEIGHT', type=int, default=5, help='Height margin size of table, by default 5.')
    _ = parser.add_argument('--pl', metavar='PADDING_LEFT', type=int, default=5, help='Left padding size of each cell, by default 5.')
    _ = parser.add_argument('--pt', metavar='PADDINT_TOP', type=int, default=5, help='Height margin size of each cell, by default 5.')
    _ = parser.add_argument('--cnr', metavar='CELL_NAME_RATIO', type=float, default=0.3, help='Width ratio of "name" column (0.1 to 0.9), by default 0.3.')
    args = parser.parse_args()
    main(args)
