"""
An app to count the carbohydrates for sweet mininio
"""

from typing import List, Tuple
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from pathlib import Path


class MininioDiet(toga.App):
    def startup(self) -> None:
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.main_window: toga.MainWindow = toga.MainWindow(title=self.formal_name)
        self.read_items()
        
        # Search input
        self.search_input: toga.TextInput = toga.TextInput(
            placeholder="Αναζήτηση...",
            on_change=self.filter_options,
            style=Pack(flex=1)
        )

        # Options for dropdown
        self.options: List[str] = self.items.keys()

        # Table to display options
        self.options_table: toga.Table = toga.Table(
            headings=["Options"],  # Define a single column
            data=[(opt,) for opt in self.options],  # Provide data as a list of tuples
            on_select=self.option_selected,
            style=Pack(flex=1)
        )

        # Layout for dropdown and search
        dropdown_box: toga.Box = toga.Box(
            children=[self.search_input, self.options_table],
            style=Pack(direction=COLUMN, padding=5)
        )

        # Main content box
        content: toga.Box = toga.Box(
            children=[dropdown_box],
            style=Pack(direction=COLUMN, padding=10)
        )

        self.main_window.content = content
        self.main_window.show()
        
    def read_items(self) -> None: 

        resources_folder = Path(__file__).joinpath("../resources").resolve()
        items_filepath = resources_folder.joinpath("processed_nutrition_table.csv")
        
        with open(items_filepath, "r") as fitems:
            self.items = dict()
            for line in fitems.readlines():
                columns = line.split(";")
                self.items[columns[0]] = {"queantinty_gr_ml": columns[1],
                                     "quantity_item": columns[2],
                                     "carbohydrates_g": columns[3]}
                
            

    def filter_options(self, input: toga.TextInput) -> None:
        """Filter the list of options based on the search input."""
        query: str = input.value.lower()
        filtered_options: List[Tuple[str]] = [(opt,) for opt in self.options if query in opt.lower()]
        self.options_table.data = filtered_options

    async def option_selected(self, widget: toga.Table) -> None:
        """Handle selection of an option."""
        if widget.selection is not None:
            self.selected_option = widget.selection.options # Access the selected option text
            await self.main_window.dialog(toga.InfoDialog("ΕΠΙΛΟΓΗ", f"Επιλέξατε: {self.selected_option}"))



def main() -> MininioDiet:
    return MininioDiet(formal_name="mininioDiet", app_id="com.kgiantsios.mininio-diet")
