from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont


class DestBoardTable:
    """
    e-Paper DestBoardTable class.
    """
    class DestBoardCell:
        """
        Inner cell class.
        """
        __name = ''
        __status = ''

        def __init__(self, outer: 'DestBoardTable', x1: int, y1: int, x2: int, y2: int, padding_left: int, padding_top: int, cell_name_ratio: float) -> None:
            """
            Constructor.

            Parameters
            ----------
            outer : 
                Outer instance.
            x1 : int
                Cell start pos x.
            y1 : int
                Cell start pos y.
            x2 : int
                Cell end pos x.
            y2 : int
                Cell end pos y.
            padding_left : int
                Cell left padding.
            padding_top : int
                Cell top padding.
            cell_name_ratio : float
                Width ratio of 'name' column (0.1 to 0.9).
            """
            self.__outer = outer
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
            self.padding_left = padding_left
            self.padding_top = padding_top
            self.cell_name_ratio = cell_name_ratio
            self.width = self.x2 - self.x1
            self.height = self.y2 - self.y1
            self.name_width = int(self.width * self.cell_name_ratio)
            self.status_width = self.width - self.name_width
            self.name_x1 = self.x1
            self.name_y1 = self.y1
            self.name_x2 = self.x1 + self.name_width
            self.name_y2 = self.y2
            self.status_x1 = self.name_x2
            self.status_y1 = self.y1
            self.status_x2 = self.x2
            self.status_y2 = self.y2

        def set_name(self, text: str) -> None:
            """
            Set name text.

            Parameters
            ----------
            text : str
                name
            """
            self.__name = text
            self.__outer.draw.text((self.name_x1 + self.padding_left, self.name_y1 + self.padding_top), text, font=self.__outer.font, fill=0)

        def set_status(self, text: str) -> None:
            """
            Set status text.

            Parameters
            ----------
            text : str
                status
            """
            self.__status = text
            self.__outer.draw.text((self.status_x1 + self.padding_left, self.status_y1 + self.padding_top), text, font=self.__outer.font, fill=0)

        def get_name(self) -> str:
            """
            Get name text.

            Returns
            -------
            str
                name
            """
            return self.__name

        def get_status(self) -> str:
            """
            Get status text.

            Returns
            -------
            str
                status
            """
            return self.__status


    __cells: List[List[DestBoardCell]] = []
    """cells in the table."""

    def __init__(
            self,
            epd_width: int, epd_height: int,
            margin_width: int, margin_height: int,
            padding_left: int, padding_top: int,
            rows: int, columns: int,
            cell_name_ratio: float,
            font_path: str, font_size: int) -> None:
        """
        Constructor.

        Parameters
        ----------
        epd_width : int
            e-Paper display's width.
        epd_height : int
            e-Paper display's height.
        margin_width : int
            Outline width margin.
        margin_height : int
            Outline height margin.
        padding_left : int
            Cell left padding.
        padding_top : int
            Cell top padding.
        rows : int
            Number of rows of table.
        columns : int
            Number of columns of table.
        cell_name_ratio : int
            Width ratio of 'name' column (0.1 to 0.9).
        font_path: str
            Font file path.
        font_size: int
            Font size.
        """
        self.epd_width = epd_width
        self.epd_height = epd_height
        self.margin_width = margin_width
        self.margin_height = margin_height
        self.padding_left = padding_left
        self.padding_top = padding_top
        self.rows = rows
        self.columns = columns
        self.cell_name_ratio = cell_name_ratio
        self.font = ImageFont.truetype(font_path, font_size)

        self.width, self.height = self.__get_table_size()
        self.x1, self.y1, self.x2, self.y2 = self.__get_table_position()
        self.cell_width, self.cell_height = self.__get_cell_size()
        self.__generate_cells()

        self.Himage = Image.new('1', (self.epd_width, self.epd_height), 255)
        self.draw = ImageDraw.Draw(self.Himage)

        self.__draw_lines()

    def __get_table_size(self) -> Tuple[int, int]:
        """
        Get table size (width, height).

        Returns
        -------
        Tuple[int, int]
            Table size (width, height).
        """
        width = self.epd_width - (self.margin_width * 2)
        height = self.epd_height - (self.margin_height * 2)
        return width, height

    def __get_table_position(self) -> Tuple[int, int, int, int]:
        """
        Get table position (x1, y1, x2, y2).

        Returns
        -------
        Tuple[int, int, int, int]
            Table position (x1, y1, x2, y2).
        """
        x1 = self.margin_width
        y1 = self.margin_height
        x2 = self.epd_width - self.margin_width
        y2 = self.epd_height - self.margin_height
        return x1, y1, x2, y2

    def __get_cell_size(self) -> Tuple[int, int]:
        """
        Get each cell size (width, height).

        Returns
        -------
        Tuple[int, int]
            Cell size (width, height).
        """
        width = int((self.epd_width - (self.margin_width * 2)) / self.columns)
        height = int((self.epd_height - (self.margin_height * 2)) / self.rows)
        return width, height

    def __generate_cells(self) -> None:
        start_x = self.x1
        start_y = self.y1

        for c in range(0, self.columns):
            self.__cells.append([])
            for r in range(0, self.rows):
                cell_x1 = start_x + (self.cell_width * c)
                cell_y1 = start_y + (self.cell_height * r)
                cell_x2 = cell_x1 + self.cell_width
                cell_y2 = cell_y1 + self.cell_height
                cell = self.DestBoardCell(self, cell_x1, cell_y1, cell_x2, cell_y2, self.padding_left, self.padding_top, self.cell_name_ratio)
                self.__cells[c].append(cell)
    
    def __draw_lines(self) -> None:
        """
        Draw table lines.
        """
        # table outline
        self.draw.line((self.x1, self.y1, self.x2, self.y1), fill=0, width=2)
        self.draw.line((self.x2, self.y1, self.x2, self.y2), fill=0, width=2)
        self.draw.line((self.x2, self.y2, self.x1, self.y2), fill=0, width=2)
        self.draw.line((self.x1, self.y2, self.x1, self.y1), fill=0, width=2)

        # horizontal line
        for r in range(1, self.rows):
            self.draw.line((self.x1, self.y1 + (self.cell_height * r), self.x2, self.y1 + (self.cell_height * r)), fill=0, width=2)

        # vertical line
        for c in range(1, self.columns):
            self.draw.line((self.x1 + (self.cell_width * c), self.y1, self.x1 + (self.cell_width * c), self.y2), fill=0, width=2)

        # name/status separator line
        for c in range(0, self.columns):
            cell = self.__get_cell(0, c)
            last_cell = self.__get_cell(self.rows - 1, c)
            self.draw.line((cell.name_x2, cell.name_y1, last_cell.name_x2, last_cell.y2), fill=0, width=2)

    def __get_cell(self, x: int, y:int) -> DestBoardCell:
        """
        Get specific cell object.

        Parameters
        ----------
        x : int
            index of X.
        y : int
            index of Y.

        Returns
        -------
        DestBoardCell
            Cell object.
        """
        return self.__cells[y][x]

    def set_name(self, x: int, y: int, text: str) -> None:
        """
        Set name text.

        Parameters
        ----------
        x : int
            index of X.
        y : int
            index of Y.
        text : str
            name
        """
        self.__get_cell(x, y).set_name(text)

    def set_status(self, x: int, y: int, text: str) -> None:
        """
        Set status text.

        Parameters
        ----------
        x : int
            index of X.
        y : int
            index of Y.
        text : str
            status
        """
        self.__get_cell(x, y).set_status(text)

    def get_name(self, x: int, y: int) -> str:
        """
        Get name text.

        Parameters
        ----------
        x : int
            index of X.
        y : int
            index of Y.

        Returns
        -------
        str
            name
        """
        return self.__get_cell(x, y).get_name()

    def get_status(self, x: int, y: int) -> str:
        """
        Get name text.

        Parameters
        ----------
        x : int
            index of X.
        y : int
            index of Y.

        Returns
        -------
        str
            status
        """
        return self.__get_cell(x, y).get_status()
