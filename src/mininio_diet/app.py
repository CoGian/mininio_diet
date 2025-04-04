"""
An app to count the carbohydrates for sweet mininio
"""

import re
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
        main_imageview = toga.ImageView(main_image, style=Pack(width=50, height=50))
        
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
        self.quantity_g_ml_button = toga.Button("g/ml", on_press=self.quantity_button_handler)
        
        # quantity item button
        self.quantity_item_button = toga.Button("τμχ/κσ/φλ", on_press=self.quantity_button_handler)
        
        # Layout for buttons
        buttons_box = toga.Box(
            style=Pack(
                padding=10,
                direction=COLUMN,
                alignment=CENTER
            )
            ,
            children=[self.quantity_g_ml_button, self.quantity_item_button]
        )
        
        self.selected_item_carbohydrates_label = toga.Label("Υδατάνθρακες (g)")
        self.multiplcation_label = toga.Label("x")
        self.quantity_textInput = toga.TextInput(placeholder="Εισάγετε ποσότητα")
        
        # Layout for quantity input
        quantity_input_box = toga.Box(
            style=Pack(
                padding=10,
                direction=ROW,
                alignment=CENTER
            )
            ,
            children=[self.selected_item_carbohydrates_label, 
                      self.multiplcation_label, 
                      self.quantity_textInput]
        )
        
        # Layout for divider
        self.divide_label = toga.Label("_" * 50)
        divider_box = toga.Box(
            style=Pack(
                padding=10,
                direction=ROW,
                alignment=CENTER,
            )
            ,
            children=[self.divide_label]
        )
        
        # Layout for selected item quantity
        self.selected_item_quantinty_label = toga.Label("Ποσότητα επιλεγμένου προϊόντος")
        selected_item_quantinty_box = toga.Box(
            style=Pack(
                padding=10,
                direction=ROW,
                alignment=CENTER
            )
            ,
            children=[self.selected_item_quantinty_label]
            )

        function_box = toga.Box(
            style=Pack(
                padding=10,
                direction=COLUMN,
                alignment=CENTER
            )
            ,
            children=[quantity_input_box, divider_box, selected_item_quantinty_box]
        )
        
        # Calculation buttons and layout
        self.calculate_button = toga.Button("Υπολογισμός", on_press=self.calculate_button_handler)
        self.result_label = toga.Label("Αποτέλεσμα: ")
        self.addition_button = toga.Button("Προσθήκη", on_press=self.addition_button_handler)
        
        # Layout for buttons
        calculation_buttons_box = toga.Box(
            style=Pack(
                padding=10,
                direction=COLUMN,
                alignment=CENTER
            )
            ,
            children=[self.calculate_button, self.result_label, self.addition_button]
        )
        
        self.added_items_results = []
        self.added_items_label = toga.Label("Προστέθηκαν τα παρακάτω προϊόντα:")
        self.items_multiline_text_input = toga.MultilineTextInput(style=Pack(height=100, font_size=9))
        
        # Layout for added items
        added_items_box = toga.Box(
            style=Pack(
                padding=10,
                direction=COLUMN,
                alignment=CENTER
            )
            ,
            children=[self.added_items_label, self.items_multiline_text_input]
        )
        
        self.special_divider = None
        morning_button = toga.Button("Πρωί", on_press=self.morning_button_handler)
        midday_button = toga.Button("Μεσημέρι", on_press=self.midday_button_handler)
        afternoon_button = toga.Button("Απόγευμα", on_press=self.afternoon_button_handler)

        # Layour for final calculation buttons
        final_calculation_buttons_box = toga.Box(    
            style=Pack(
                padding=10,
                direction=ROW,
                alignment=CENTER,
                flex=1
            )
            ,
            children=[morning_button, midday_button, afternoon_button]
        )
        
        self.final_result_label = toga.Label("Τελικό αποτέλεσμα: ")
        self.final_result_text_input = toga.TextInput(style=Pack(font_size=9))
        clear_button = toga.Button("Καθαρισμός", on_press=self.final_clear)
        
        # Layout for final result
        final_result_box = toga.Box(
            style=Pack(
                padding=10,
                direction=COLUMN,
                alignment=CENTER
            )
            ,
            children=[self.final_result_label, self.final_result_text_input, clear_button]
        )
        
        # Main unscrollable content box
        unscrollable_content: toga.Box = toga.Box(
            children=[main_image_box, 
                      dropdown_box],
            style=Pack(direction=COLUMN, padding=10)
        )
        
        # Main unscrollable content box
        scrollable_content: toga.Box = toga.Box(
            children=[ 
                      buttons_box, 
                      function_box, 
                      calculation_buttons_box,
                      added_items_box,
                      final_calculation_buttons_box,
                      final_result_box],
            style=Pack(direction=COLUMN, padding=10)
        )
        
        scroll_container = toga.ScrollContainer(content=scrollable_content, 
                                                style=Pack(height=400))

        # Main content box
        content: toga.Box = toga.Box(
            children=[unscrollable_content, scroll_container],
            style=Pack(direction=COLUMN, padding=10)
        )

        self.main_window.content = content
        self.main_window.show()
        
    def clear(self) -> None:
        """
        Clear the selected item and quantity.
        """
        self.selected_item_quantity = None
        self.selected_item_quantinty_label.text = "Ποσότητα επιλεγμένου προϊόντος"
        self.input_quantity = None
        self.quantity_textInput.placeholder = "Εισάγετε ποσότητα"
        self.quantity_textInput.value = None
        self.result_label.text = "Αποτέλεσμα: "
        self.result_label.style.color = "black"
        self.result = None
        self.selected_item_carbohydrates = None
        self.selected_item_carbohydrates_label.text = "Υδατάνθρακες (g)"
        
        
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
            self.clear()
            self.selected_item_carbohydrates = self.items[self.selected_item]["carbohydrates_g"]
            self.selected_item_carbohydrates_label.text = f"{self.selected_item_carbohydrates}"


    async def check_if_selected_item(self) -> None:
        """
        Check if an item has been selected.
        :return: None
        """
        if "selected_item" not in self.__dict__ or self.selected_item is None:
            await self.main_window.dialog(toga.InfoDialog("ΠΡΟΣΟΧΗ", "Δεν έχετε επιλέξει προϊόν."))
            return False
        
        return True
    
    async def check_if_selected_quantity(self) -> None:
        """
        Check if a quantity has been selected.
        :return: None
        """
        if "selected_item_quantity" not in self.__dict__ or self.selected_item_quantity is None:
            await self.main_window.dialog(toga.InfoDialog("ΠΡΟΣΟΧΗ", "Δεν έχετε επιλέξει (g/ml) ή τμχ/κσ/φλ."))
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
            self.selected_item_quantinty_label.text = "Ποσότητα επιλεγμένου προϊόντος"
            self.selected_item_quantity = None
            return
        
        self.selected_item_quantinty_label.text = f"{self.selected_item_quantity}"

    async def calculate_button_handler(self, widget: toga.Button) -> None:
        """
        Handle the calculate button press.
        :param widget: The button widget.
        :return: None
        """
        
        if not await self.check_if_selected_item() or not await self.check_if_selected_quantity():
            return
        
        self.input_quantity =  self.quantity_textInput.value
        if self.input_quantity == '' or self.input_quantity == '0':
            await self.main_window.dialog(toga.InfoDialog("ΠΡΟΣΟΧΗ", "Δεν έχετε εισάγει ποσότητα."))
        else:
            numerical_input_quantity = re.findall(r'(\d+(?:\.\d+)?)', self.input_quantity)
            if len(numerical_input_quantity) == 0:
                await self.main_window.dialog(toga.InfoDialog("ΠΡΟΣΟΧΗ", "Η ποσότητα που εισάγατε δεν περιεχει αριθμό."))
                return
            numerical_selected_item_quantity = re.findall(r'(\d+(?:\.\d+)?)', self.selected_item_quantity)
            numerical_selected_item_carbohydrates = re.findall(r'(\d+(?:\.\d+)?)', self.selected_item_carbohydrates)
            self.result = (float(numerical_input_quantity[0]) * float(numerical_selected_item_carbohydrates[0])) / float(numerical_selected_item_quantity[0])
            self.result_label.text = f"Αποτέλεσμα: {round(self.result, 3)} γρ. υδατάνθρακες."
            self.result_label.style.color = "green"
 
    async def addition_button_handler(self, widget: toga.Button) -> None:
        """
        Handle the addition button press.
        :param widget: The button widget.
        :return: None
        """
        if "result" not in self.__dict__ or self.result is None:
            await self.main_window.dialog(toga.InfoDialog("ΠΡΟΣΟΧΗ", "Δεν έχετε υπολογίσει το αποτέλεσμα."))
            return
        self.added_items_results.append(self.result)
        measurement_method = self.selected_item_quantity.split(" ")[1]
        self.items_multiline_text_input.value = self.items_multiline_text_input.value + f"{self.input_quantity} {measurement_method} {self.selected_item}: {round(self.result, 3)} g\n"
        self.clear()
        self.selected_item = None
    
        
    async def daytime_button_press(self, widget: toga.Button, special_divider: int) -> None:
        """
        Handle the button press for morning, afternoon, or midday.
        :param widget: The button widget.
        :param special_divider: The divider value for the calculation.
        :return: None
        """
        if len(self.added_items_results) == 0:
            await self.main_window.dialog(toga.InfoDialog("ΠΡΟΣΟΧΗ", "Δεν έχετε προσθέσει προϊόντα."))
            return
        self.special_divider = special_divider
        self.final_calculation()
    
    async def morning_button_handler(self, widget: toga.Button) -> None:
        await self.daytime_button_press(widget, special_divider=14)

    async def afternoon_button_handler(self, widget: toga.Button) -> None:
        await self.daytime_button_press(widget, special_divider=12)

    async def midday_button_handler(self, widget: toga.Button) -> None:
        await self.daytime_button_press(widget, special_divider=15)
    
    def final_calculation(self) -> None:
        """
        Perform the final calculation.
        """
        if self.special_divider is None:
            return
        final_result = sum(self.added_items_results) / self.special_divider
        self.final_result_label.text = f"Τελικό αποτέλεσμα: {round(final_result, 3)}"
        self.final_result_text_input.value = f" {round(sum(self.added_items_results), 3)} / {self.special_divider} = {round(final_result, 3)}"
        self.final_result_label.style.color = "green"
        
    def final_clear(self, widget: toga.Button) -> None:
        """
        Handle the final clear button press.
        :param widget: The button widget.
        :return: None
        """
        self.clear()
        self.selected_item = None
        self.added_items_results = []
        self.items_multiline_text_input.value = ""
        self.special_divider = None
        self.final_result_label.text = "Τελικό αποτέλεσμα: "
        self.final_result_label.style.color = "black"
        self.final_result_text_input.value = ""
        
def main() -> MininioDiet:
    return MininioDiet(formal_name="mininioDiet", 
                       app_id="com.kgiantsios.mininio-diet")
