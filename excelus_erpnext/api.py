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

	return fg_carton_per_kg, packs_per_carton, carton_width, carton_length
	#return (fg_carton_per_kg * fg_weight_per_carton), packs_per_carton, carton_width
	#return ((fg_carton_per_kg * fg_weight_per_carton) / (10**3)), packs_per_carton, carton_width

def calculate_tape_qty_per_kg(pack_weight, item_code, packs_per_carton, carton_length):
	tape_bleed = frappe.db.get_value("Item", item_code, "excelus_tape_bleed")
	roll_width =  frappe.db.get_value("Item", item_code, "excelus_pm_width")
	tape_gsm = frappe.db.get_value("Item", item_code, "excelus_pm_thickness")
	fg_weight_per_carton  = (pack_weight * packs_per_carton) / (10**3)
	tape_reqd_per_carton = ((carton_length*2) + (tape_bleed*4)) / (10**3)
	#tape_reqd_per_carton = ((carton_length*2)) / (10**3)
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
	carton_qty_per_kg, packs_per_carton, carton_width, carton_length = calculate_carton_qty_per_kg(pack_weight, carton[0])

	tape = [x.get("item_code") for x in items if process_item_group(x.get("item_group")) == "pm-tape"]
	#tape_qty_per_kg = calculate_tape_qty_per_kg(pack_weight,  tape[0], packs_per_carton, carton_width)
	tape_qty_per_kg = calculate_tape_qty_per_kg(pack_weight,  tape[0], packs_per_carton, carton_length)

	return frappe._dict({ "laminate_qty": film_qty_per_kg, "carton_qty": carton_qty_per_kg, "tape_qty": tape_qty_per_kg })


def process_item_group(item_group):
	return item_group.replace(" ", "").lower()


@frappe.whitelist()
def awfis_test():
	for x in xrange(1,10):
		print frappe.request.headers

@frappe.whitelist()

def print_pdf(html):
	# if not frappe.has_permission("Excelus Customer Inquiry ", "write"):
	#   frappe.throw(_("Not permitted"), frappe.PermissionError)

	# html_params = frappe._dict({
	#     "ci_requirements": ci_requirements
	# })

	#html = "<h1>Hello world</h1>"

	pdf_options = {
		"orientation" : "Landscape",
		"no-outline": None,
		"encoding": "UTF-8",
		"title": "Cost Sheet"
	}

	frappe.local.response.filename = "{filename}.pdf".format(filename="customer".replace(" ", "-").replace("/", "-"))
	frappe.local.response.filecontent = excelus_get_pdf(html, options=pdf_options) #get_pdf(final_html, pdf_options)
	frappe.local.response.type = "download"

	# excelus_get_pdf(html)


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

	finally:
		cleanup(fname)


	return filedata

def cleanup(fname):
	if os.path.exists(fname):
		os.remove(fname)

def excelus_bom_validate(self, method):
	for item in self.items:
		item.excelus_item_group = frappe.get_value("Item", item.item_code, "item_group")


#Item csv is treated. All spaces removed. Cannot deal with variants.. Handles conversion factor.
@frappe.whitelist()
def excelus_import_items(path_to_sheet):
	items_json = csv_to_json(path_to_sheet)

	msgs = []

	for item in items_json["data"]:
		msg = ""
		msg += "Name: {0}, ".format(item["name"])

		name = frappe.db.get_value("Item", {"name": item["name"]}, "name")

		if not name:
			i = frappe.new_doc("Item")

			keys = [ik for ik in item.keys() if ik not in ["conversion_factor", "uom", "name"]]

			for key in keys:
				i.set(key, item[key])

			i.append("uoms", {
				"uom": item["uom"],
				"conversion_factor": item["conversion_factor"]
			})

			try:
				i.save()
				msg += "Saved: {0}, ".format(i.name)

				print "About to rename {0} to {1}".format(i.name, item["name"])

				frappe.rename_doc("Item", i.name, item["name"], force=True)
				frappe.db.commit()

				msg += "Renamed: {0}".format(item["name"])
			except Exception as e:
				msg += "Exception: {0}".format(e)
				frappe.db.rollback()
		else:
			msg += "Already exists"

		print msg

		msgs.append(msg)

	return "\n".join(msgs)

def csv_to_json(path, column_headings_row_idx=1, start_parsing_from_idx=2):
	def process_val(value):
		out = value.replace("\\", "\\\\").replace('"', '\\"')
		return out

	import csv

	file_rows = []
	out_rows = []

	csv_path = frappe.utils.get_site_path() + path 

	#with open('/home/gaurav/Downloads/25a4cbe4397b494a_2016-12-03_2017-01-02.csv', 'rb') as csvfile:
	with open(csv_path, 'rb') as csvfile:

		rdr = csv.reader(csvfile, delimiter=str(','), quotechar=str('"'))
	   
		for row in rdr:
			file_rows.append(row)

		final_json = {}
		json_data = final_json.setdefault("data", [])
		column_headings_row = file_rows[column_headings_row_idx]

		#Handle repeating columns
		processed_headings_row = []
		for col in column_headings_row:
			count = len([x for x in processed_headings_row if x == col])
			if count > 0:
				col = col + "_" + str(count)
			processed_headings_row.append(col)

		for i in xrange(start_parsing_from_idx, len(file_rows)):
			record_core = ""

			if len(file_rows[i]) == len(processed_headings_row):
				for j in range(0, len(processed_headings_row)):
					record_core += '"' +  processed_headings_row[j] + '" : "' + process_val(file_rows[i][j]) + '", '

					#print "Orig", file_rows[i][j], "Treated", process_val(file_rows[i][j])

				record_json_string = "{" + record_core[:-2] + "}"

				json_data.append(json.loads(record_json_string))

		return final_json

		#print "FINAL JSON", final_json

def sqtn_autoname(self, method):
	finyr_start = frappe.utils.datetime.datetime.strptime(frappe.defaults.get_defaults().year_start_date, "%Y-%m-%d").strftime("%y") #frappe.utils.datetime.datetime.strptime(frappe.defaults.get_defaults().year_start_date, "%Y-%m-%d").strftime("%m/%y")
	finyr_end = frappe.utils.datetime.datetime.strptime(frappe.defaults.get_defaults().year_end_date, "%Y-%m-%d").strftime("%y")

	self.name = self.name + "-" + finyr_start + "/" + finyr_end
	