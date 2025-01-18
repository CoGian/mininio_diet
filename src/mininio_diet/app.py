"""
An app to count the carbohydrates for sweet mininio
"""

from typing import List, Tuple
import toga
from toga.style import Pack
from toga.style.pack import CENTER, COLUMN, Pack, ROW
from pathlib import Path


class MininioDiet(toga.App):
    def startup(self) -> None:
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.main_window: toga.MainWindow = toga.MainWindow(title=self.formal_name)
        self.resources_folder = Path(__file__).joinpath("../resources").resolve()

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
            headings=["Επιλογές"],  # Define a single column
            data=[(opt,) for opt in self.options],  # Provide data as a list of tuples
            on_select=self.option_selected,
            style=Pack(flex=1)
        )

        # Layout for dropdown and search
        dropdown_box: toga.Box = toga.Box(
            children=[self.search_input, self.options_table],
            style=Pack(direction=COLUMN, padding=5)
        )
        
        
        # load main image
        main_image = toga.Image(self.resources_folder.joinpath("mininio_diet"))
        main_imageview = toga.ImageView(main_image, style=Pack(width=100, height=100))
        
        # Layuot for image
        main_image_box = toga.Box(
            style=Pack(
                padding=10,
                direction=COLUMN,
                alignment=CENTER
            )
            ,
            children=[main_imageview]
        )
        
        # quantity g/ml button
        quantity_g_ml_button = toga.Button("g/ml", on_press=self.quantity_button_handler)
        
        # quantity item button
        quantity_item_button = toga.Button("τμχ/κσ/φλ", on_press=self.quantity_button_handler)
        
        # Layout for buttons
        buttons_box = toga.Box(
            style=Pack(
                padding=10,
                direction=COLUMN,
                alignment=CENTER
            )
            ,
            children=[quantity_g_ml_button, quantity_item_button]
        )
        
        selected_item_carbohydrates_label = toga.Label("Υδατάνθρακες (g) επιλεγμένου προϊόντος")
        multiplcation_label = toga.Label("x")
        quantity_input = toga.TextInput(placeholder="Εισάγετε ποσότητα...")
        
        # Layout for quantity input
        quantity_input_box = toga.Box(
            style=Pack(
                padding=10,
                direction=ROW,
                alignment=CENTER
            )
            ,
            children=[selected_item_carbohydrates_label, multiplcation_label, quantity_input]
        )
        
        # Layout for divider
        divide_label = toga.Label("_" * 60)
        divider_box = toga.Box(
            style=Pack(
                padding=10,
                direction=ROW,
                alignment=CENTER,
            )
            ,
            children=[divide_label]
        )
        
        # Layout for selected item quantity
        selected_item_quantinty_label = toga.Label("Ποσότητα επιλεγμένου προϊόντος")
        selected_item_quantinty_box = toga.Box(
            style=Pack(
                padding=10,
                direction=ROW,
                alignment=CENTER
            )
            ,
            children=[selected_item_quantinty_label]
            )

        calculation_box = toga.Box(
            style=Pack(
                padding=10,
                direction=COLUMN,
                alignment=CENTER
            )
            ,
            children=[quantity_input_box, divider_box, selected_item_quantinty_box]
        )
        # Main content box
        content: toga.Box = toga.Box(
            children=[main_image_box, dropdown_box, buttons_box, calculation_box],
            style=Pack(direction=COLUMN, padding=10)
        )

        self.main_window.content = content
        self.main_window.show()
        
    def read_items(self) -> None: 
        """
        Read the items from the processed nutrition table and store them in a dictionary.
        """
        items_filepath = self.resources_folder.joinpath("processed_nutrition_table.csv")
        
        with open(items_filepath, "r") as fitems:
            self.items = dict()
            fitems.readline() # Skip the header
            for line in fitems.readlines():
                columns = line.strip("\n").split(";")
                self.items[columns[0]] = {"quantity_g_ml": columns[1],
                                     "quantity_item": columns[2],
                                     "carbohydrates_g": columns[3]}
                
            

    def filter_options(self, input: toga.TextInput) -> None:
        """
        Filter the list of options based on the search input.
        :param input: The search input widget.
        :return: None
        """
        query: str = input.value.lower()
        filtered_options: List[Tuple[str]] = [(opt,) for opt in self.options if query in opt.lower()]
        self.options_table.data = filtered_options

    async def option_selected(self, widget: toga.Table) -> None:
        """
        Handle selection of an option.
        :param widget: The table widget.
        :return: None
        """
        if widget.selection is not None:
            self.selected_item = widget.selection.επιλογές # Access the selected option text
            await self.main_window.dialog(toga.InfoDialog("ΕΠΙΛΟΓΗ", f"Επιλέξατε: {self.selected_item}"))
            self.selected_item_quantity = None
            self.selected_item_carbohydrates = self.items[self.selected_item]["carbohydrates_g"]
            self.main_window.content.children[3].children[0].children[0].text = f"{self.selected_item_carbohydrates}"
            self.main_window.content.children[3].children[2].children[0].text = "Ποσότητα επιλεγμένου προϊόντος"


    async def check_if_selected_item(self) -> None:
        """
        Check if an item has been selected.
        :return: None
        """
        if "selected_item" not in self.__dict__ or self.selected_item is None:
            await self.main_window.dialog(toga.InfoDialog("ΠΡΟΣΟΧΗ", "Δεν έχετε επιλέξει προϊόν."))
            return False
        
        return True
        
    async def quantity_button_handler(self, widget: toga.Button) -> None:
        """
        Handle the quantity button press.
        :param widget: The button widget.
        :return: None
        """
        
        if not await self.check_if_selected_item():
            return
        
        if widget.text == "g/ml":
            self.selected_item_quantity = self.items[self.selected_item]["quantity_g_ml"]
        else:
            self.selected_item_quantity = self.items[self.selected_item]["quantity_item"]
            
        if self.selected_item_quantity == '':
            await self.main_window.dialog(toga.InfoDialog("ΠΡΟΣΟΧΗ", f"Δεν έχεi οριστεί ποσότητα σε {widget.text} για {self.selected_item}."))
            self.main_window.content.children[3].children[2].children[0].text = "Ποσότητα επιλεγμένου προϊόντος"
            return
        
        self.main_window.content.children[3].children[2].children[0].text = f"{self.selected_item_quantity}"
            
def main() -> MininioDiet:
    return MininioDiet(formal_name="mininioDiet", 
                       app_id="com.kgiantsios.mininio-diet")
