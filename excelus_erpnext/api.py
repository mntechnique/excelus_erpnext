import frappe
from frappe import _
import json
from frappe.utils.pdf import get_pdf
import pdfkit
import os

#Pack weight comes from bom.item

def calculate_film_qty_per_kg(pack_weight, item_code):
	packs_per_kg_fg = 1000/pack_weight
	pack_width = frappe.db.get_value("Item", item_code, "excelus_pm_width")
	pack_length = frappe.db.get_value("Item", item_code, "excelus_pm_length")
	film_wastage = frappe.db.get_value("Item", item_code, "excelus_pm_wastage")
	avg_film_thickness = frappe.db.get_value("Item", item_code, "excelus_pm_thickness")

	film_per_pack = ((pack_length * pack_width)/(1-(film_wastage/100))) / (10**6)
	fg_film_per_kg = film_per_pack * packs_per_kg_fg

	return (avg_film_thickness * fg_film_per_kg)/(10**3)

def calculate_carton_qty_per_kg(pack_weight, item_code):
	packs_per_carton = frappe.db.get_value("Item", item_code, "excelus_packs_per_carton")
	carton_height =  frappe.db.get_value("Item", item_code, "excelus_pm_height")
	carton_width =  frappe.db.get_value("Item", item_code, "excelus_pm_width")
	carton_length =  frappe.db.get_value("Item", item_code, "excelus_pm_length")
	carton_fold_bleed = frappe.db.get_value("Item", item_code, "excelus_pm_fold_bleed")
	carton_flap_bleed = frappe.db.get_value("Item", item_code, "excelus_pm_flap_bleed")
	# carton_board_area = ((carton_height * carton_length)*2 + (carton_length * carton_width)*2 + (carton_width * carton_height)*2) / (10**6)
	#carton_board_area = ((2*(carton_length*(2*carton_height)))+(2*(carton_width*(2*carton_height)))+(3*(carton_height*carton_fold_bleed))+(carton_height*carton_flap_bleed)) / (10**6)
	carton_board_area = ((2*(carton_length*(2*carton_height))) +(2*(carton_width*(2*carton_height)))+(3*(carton_height*carton_fold_bleed))+(carton_height*carton_flap_bleed)) / (10**6)
	carton_gsm = frappe.db.get_value("Item", item_code, "excelus_pm_thickness")
	carton_weight = (carton_board_area * carton_gsm) / (10**3)
	fg_weight_per_carton = (pack_weight * packs_per_carton) / (10**3)
	#fg_carton_per_kg = 1/fg_weight_per_carton
	fg_carton_per_kg = carton_weight/fg_weight_per_carton

	return fg_carton_per_kg, packs_per_carton, carton_width
	#return (fg_carton_per_kg * fg_weight_per_carton), packs_per_carton, carton_width
	#return ((fg_carton_per_kg * fg_weight_per_carton) / (10**3)), packs_per_carton, carton_width

def calculate_tape_qty_per_kg(pack_weight, item_code, packs_per_carton, carton_width):
	roll_width =  frappe.db.get_value("Item", item_code, "excelus_pm_width")
	tape_gsm = frappe.db.get_value("Item", item_code, "excelus_pm_thickness")
	fg_weight_per_carton  = (pack_weight * packs_per_carton) / (10**3)
	tape_reqd_per_carton = ((carton_width*2)+(80*2)) / (10**3)
	fg_tape_reqd_per_kg = tape_reqd_per_carton / fg_weight_per_carton

	return (fg_tape_reqd_per_kg * tape_gsm) / (10**3)

@frappe.whitelist()
def calculate_pm_qtys(item_code, items):

	pack_weight = frappe.db.get_value("Item", item_code, "net_weight")

	repeating_items = []

	items = json.loads(items)

	for item in items:
		item.update({"item_group": frappe.db.get_value("Item", item.get("item_code"), "item_group")})
		if process_item_group(item.get("item_group")) in ["pm-tape", "pm-laminate", "pm-carton"]:
			repeating_items.append(item.get("item_group"))

	distinct_items = set(repeating_items)

	if len(repeating_items)!= len(distinct_items):
		frappe.throw(_("Same Item has been entered more than once."))


	film = [x.get("item_code") for x in items if process_item_group(x.get("item_group")) == "pm-laminate"]
	film_qty_per_kg = calculate_film_qty_per_kg(pack_weight, film[0])

	carton = [x.get("item_code") for x in items if process_item_group(x.get("item_group")) == "pm-carton"]
	carton_qty_per_kg, packs_per_carton, carton_width = calculate_carton_qty_per_kg(pack_weight, carton[0])

	tape = [x.get("item_code") for x in items if process_item_group(x.get("item_group")) == "pm-tape"]
	tape_qty_per_kg = calculate_tape_qty_per_kg(pack_weight,  tape[0], packs_per_carton, carton_width)

	return frappe._dict({ "laminate_qty": film_qty_per_kg, "carton_qty": carton_qty_per_kg, "tape_qty": tape_qty_per_kg })


def process_item_group(item_group):
	return item_group.replace(" ", "").lower()


@frappe.whitelist()
def awfis_test():
	for x in xrange(1,10):
		print frappe.request.headers




html_params = frappe._dict({
})

html = frappe.render_template("excelus_erpnext/templates/includes/excelus_cost_sheet.html", html_params)

@frappe.whitelist()
def excelus_get_pdf(html, options=None):
	fname = os.path.join("/tmp", "excelus-ci-{0}.pdf".format(frappe.generate_hash()))

	try:
		pdfkit.from_string(html, fname, options=options or {})

		with open(fname, "rb") as fileobj:
			filedata = fileobj.read()

	except IOError, e:
		if ("ContentNotFoundError" in e.message
			or "ContentOperationNotPermittedError" in e.message
			or "UnknownContentError" in e.message
			or "RemoteHostClosedError" in e.message):

			# allow pdfs with missing images if file got created
			if os.path.exists(fname):
				with open(fname, "rb") as fileobj:
					filedata = fileobj.read()

			else:
				frappe.throw(_("PDF generation failed because of broken image links"))
		else:
			raise

	finally:
		cleanup(fname)


	return filedata

def cleanup(fname):
	if os.path.exists(fname):
		os.remove(fname)