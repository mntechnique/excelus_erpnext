import frappe

def execute():
	item_list = frappe.get_all("Item")

	for i in item_list:
		old_item = frappe.get_doc("Item",i.name)
		if(frappe.db.exists("Excelus Item Parameters",{"item": old_item.name})):
			new_item = frappe.get_doc("Excelus Item Parameters",(frappe.db.exists("Excelus Item Parameters",{"item": old_item.name})))
		else:
			new_item = frappe.new_doc("Excelus Item Parameters") 
		new_item.item = old_item.item_name
		new_item.length = old_item.excelus_pm_length
		new_item.width = old_item.excelus_pm_width
		new_item.heigth = old_item.excelus_pm_height
		new_item.thickness = old_item.excelus_pm_thickness
		new_item.fold_bleed = old_item.excelus_pm_fold_bleed
		new_item.flap_bleed = old_item.excelus_pm_flap_bleed
		new_item.tape_bleed = old_item.excelus_tape_bleed
		new_item.packs_per_carton = old_item.excelus_packs_per_carton
		new_item.length_uom = old_item.excelus_pm_length_uom
		new_item.width_uom = old_item.excelus_pm_width_uom
		new_item.height_uom = old_item.excelus_pm_height_uom
		new_item.thickness_uom = old_item.excelus_pm_thickness_uom
		new_item.fold_bleed_uom = old_item.excelus_pm_fold_bleed_uom
		new_item.flap_bleed_uom = old_item.excelus_pm_flap_bleed_uom
		new_item.tape_bleed_uom = old_item.excelus_tape_bleed_uom
		new_item.conversion_cost = old_item.excelus_conversion_cost
		new_item.wastage = old_item.excelus_pm_wastage
		new_item.mrp_rate = old_item.mrp_rate
		new_item.hsm_code = old_item.hsm_code
		new_item.abatement_rate = old_item.abetment_rate
		new_item.save()

	frappe.db.commit() 