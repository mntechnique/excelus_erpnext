
def calculate_film_qty_per_kg(item_code):
	pack_weight = frappe.db.get_value("Item", item_code, "net_weight")
	packs_per_kg = 1000/pack_weight
	pack_width = frappe.db.get_value("Item", item_code, "excelus_pm_width")
	pack_length = frappe.db.get_value("Item", item_code, "excelus_pm_length")
	film_wastage = frappe.db.get_value("Item", item_code, "excelus_pm_wastage")
	thickness = frappe.db.get_value("Item", item_code, "excelus_pm_thickness")

	film_per_pack = ((pack_length * pack_width)/(1 / film_wastage)) / (10**6)
	film_per_kg = film_per_pack * packs_per_kg

	return film_per_kg/(10*3)

def calculate_carton_qty_per_kg(item_code):
	pack_weight = frappe.db.get_value("Item", item_code, "net_weight")
	packs_per_carton = frappe.db.get_value("Item", item_code, "packs_per_carton")
	carton_height =  frappe.db.get_value("Item", item_code, "excelus_pm_height")
	carton_width =  frappe.db.get_value("Item", item_code, "excelus_pm_width")
	carton_length =  frappe.db.get_value("Item", item_code, "excelus_pm_length")	
	carton_board_area = ((carton_height * carton_length)*2 + (carton_length * carton_width)*2 + (carton_width * carton_height)*2) / (10**6)
	carton_thickness = frappe.db.get_value("Item", item_code, "excelus_pm_thickness")
	carton_weight = (carton_board_area * carton_thickness) / (10**3)
	fg_weight_per_carton = (pack_weight * packs_per_carton) / (10**3)
	carton_per_kg = 1/fg_weight_per_carton
		
	return ((carton_per_kg * fg_weight_per_carton) / (10**3))

def calculate_tape_qty_per_kg(item_code, packs_per_carton, carton_width):


def calculate_pm_qtys(item_code):
	film_qty_per_kg = calculate_film_qty_per_kg(item_code)
	carton_qty_per_kg = calculate_carton_qty_per_kg(item_code)
	tape_qty_per_kg = calculate_tape_qty_per_kg(item_code)

	return frappe.dict({ "film_qty": film_qty_per_kg, "carton_qty": carton_qty_per_kg, "tape_qty": tape_qty_per_kg })
