# Move Item Parameters from Item to Excelus Item Parameters

import frappe

def execute():
	for i in frappe.get_all("Item"):
		item = frappe.get_doc("Item", i.get("name"))
		eip = frappe.new_doc("Excelus Item Parameters")
		eip.item = item.name
		eip.excelus_pm_length = item.excelus_pm_length
		eip.excelus_pm_length_uom = item.excelus_pm_length_uom
		eip.excelus_pm_width = item.excelus_pm_width
		eip.excelus_pm_width_uom = item.excelus_pm_width_uom
		eip.excelus_pm_height = item.excelus_pm_height
		eip.excelus_pm_height_uom = item.excelus_pm_height_uom
		eip.excelus_pm_thickness = item.excelus_pm_thickness
		eip.excelus_pm_thickness_uom = item.excelus_pm_thickness_uom
		eip.excelus_pm_fold_bleed = item.excelus_pm_fold_bleed
		eip.excelus_pm_fold_bleed_uom = item.excelus_pm_fold_bleed_uom
		eip.excelus_pm_flap_bleed = item.excelus_pm_flap_bleed
		eip.excelus_pm_flap_bleed_uom = item.excelus_pm_flap_bleed_uom
		eip.excelus_tape_bleed_uom = item.excelus_tape_bleed_uom
		eip.excelus_tape_bleed = item.excelus_tape_bleed
		eip.excelus_packs_per_carton = item.excelus_packs_per_carton
		eip.excelus_conversion_cost = item.excelus_conversion_cost
		eip.excelus_pm_wastage = item.excelus_pm_wastage
		eip.hsm_code = item.hsm_code
		eip.abatement_rate = item.abetment_rate
		eip.mrp_rate = item.mrp_rate
		eip.save()

	frappe.db.commit()
