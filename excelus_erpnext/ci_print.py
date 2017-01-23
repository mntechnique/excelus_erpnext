import frappe
from api import calculate_tape_qty_per_kg, calculate_film_qty_per_kg, calculate_carton_qty_per_kg, excelus_get_pdf

def prepare_ci(ci_name, requirements):
	ci_requirements = []
	requirements = requirements.split(",")

	for req in requirements:
		oreq = frappe.get_doc("Excelus Customer Inquiry Requirement", req)
		ci_requirements.append(oreq)


	html = ""

	for requirement in ci_requirements:
		ci = frappe.get_doc("Excelus Customer Inquiry", ci_name)

		item_details = frappe._dict({
			"item_code": frappe.db.get_value("Item", requirement.item, "item_code") or frappe.db.get_value("Item", requirement.item, "name"),
			"item_name": frappe.db.get_value("Item", requirement.item, "item_name")})

		pack_weight = frappe.db.get_value("Item", requirement.item, "net_weight")
		item_details.update({"pack_weight": pack_weight})

		# Fetch Packs Per Carton: Look up Carton among BOM items for the FG
		carton_item_code = frappe.db.get_value("BOM Item", {"parent": requirement.bom, "excelus_item_group": "PM - Carton"}, "item_code")
		# for x in xrange(1,10):
		# 	print "BOM", requirement.bom
		# 	print "Carton item code", carton_item_code
		item_details.update({"packs_per_carton": frappe.db.get_value("Item", carton_item_code, "excelus_packs_per_carton")})

		carton_content_weight = (item_details["packs_per_carton"] * item_details["pack_weight"]) / (10**3)
		item_details.update({"carton_content_weight": carton_content_weight})

		#Prepare BOM
		bom_items_rm = frappe.get_all("BOM Item", filters=[["parent","=", requirement.bom],["item_code", "like", "RM%"]], fields=['*'])
		bom_items_pm = frappe.get_all("BOM Item", filters=[["parent","=", requirement.bom],["item_code", "like", "PM%"]], fields=['*'])


		prepared_bom_items_rm = frappe._dict({"items": [], "total": 0.0 })
		prepared_bom_items_pm = frappe._dict({"items": [], "total": 0.0 })

		#Calculate total cost/kg for fg for RM
		total_cost_per_kg_fg_rm = 0.0

		#print {"RM Items" : bom_items_rm}

		for item_rm in bom_items_rm:
			customer_rate_item_rm = frappe.db.get_value("Excelus Customer Inquiry Item", {"parent": ci_name, "item": item_rm.item_code}, "customer_rate")
			cost_per_kg_fg_rm = item_rm.qty * customer_rate_item_rm
			total_cost_per_kg_fg_rm += float(cost_per_kg_fg_rm)
			prepared_bom_item_rm = frappe._dict(
				{
				"item_code": item_rm.item_code or item_name.name,
				"item_name": item_rm.item_name,
				"qty": item_rm.qty,
				"rate": customer_rate_item_rm,
				"cost": cost_per_kg_fg_rm})
			
			

			prepared_bom_items_rm['items'].append(prepared_bom_item_rm)

		prepared_bom_items_rm["total"] = total_cost_per_kg_fg_rm
		prepared_bom_items_rm["total_in_words"] = frappe.utils.data.money_in_words(total_cost_per_kg_fg_rm)

		total_cost_per_kg_fg_pm = 0.0
		for item_pm in bom_items_pm:
			customer_rate_item_pm = frappe.db.get_value("Excelus Customer Inquiry Item", {"parent": ci_name, "item": item_pm.item_code}, "customer_rate")
			cost_per_kg_fg_pm = item_pm.qty * customer_rate_item_pm
			total_cost_per_kg_fg_pm += float(cost_per_kg_fg_pm)

			prepared_bom_item_pm = frappe._dict(
				{
				"item_code": item_pm.item_code or item_name.name,
				"item_name": item_pm.item_name,
				"item_group": item_pm.excelus_item_group,
				"qty": item_pm.qty,
				"rate": customer_rate_item_pm,
				"cost": cost_per_kg_fg_pm})

			print "PM ITEM NAME", item_pm.item_code, "QTY", item_pm.qty, "RATE", customer_rate_item_pm, "COST",  cost_per_kg_fg_pm

			prepared_bom_items_pm["items"].append(prepared_bom_item_pm)

		prepared_bom_items_pm["total"] = total_cost_per_kg_fg_pm
		prepared_bom_items_pm["total_in_words"] = frappe.utils.data.money_in_words(total_cost_per_kg_fg_pm)


		prepared_conversion_item = frappe._dict(
			{"item_name": requirement.item,
			"conversion_cost": frappe.db.get_value("Item", requirement.item, "excelus_conversion_cost") })

		item_details.update({"rm_cost_per_kg": prepared_bom_items_rm.get("total") })
		item_details.update({"pm_cost_per_kg": prepared_bom_items_pm.get("total") })
		item_details.update({"processing_cost_per_kg": prepared_conversion_item.get("conversion_cost") })

		total_cost_per_kg = item_details["rm_cost_per_kg"] + item_details["pm_cost_per_kg"] + item_details["processing_cost_per_kg"]
		item_details.update({"total_cost_per_kg": total_cost_per_kg})

		cost_per_case  = total_cost_per_kg * carton_content_weight
		item_details.update({"cost_per_case": cost_per_case})

		cost_per_pouch = (total_cost_per_kg * pack_weight) / (10**3)
		item_details.update({"cost_per_pouch": cost_per_pouch})

		print_params = frappe._dict({
			"ci": ci,
			"item_details": item_details,
			"rm_items": prepared_bom_items_rm,
			"pm_items": prepared_bom_items_pm,
			"conversion_item": prepared_conversion_item, 
			"print_date": frappe.utils.datetime.datetime.strftime(frappe.utils.datetime.datetime.today(), "%d-%b-%Y"),
			"print_time": frappe.utils.datetime.datetime.strftime(frappe.utils.datetime.datetime.today(), "%H:%M:%S %p")  
		})

		ci_print_html = frappe.render_template("excelus_erpnext/templates/includes/excelus_cost_sheet.html", print_params)

		html += ci_print_html

	return html


@frappe.whitelist()
def print_ci(ci_name, requirements):
	from .api import print_pdf
	html = prepare_ci(ci_name, requirements)
	#frappe.respond_as_web_page("ci", html)
	print_pdf(html)