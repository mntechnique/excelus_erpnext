import frappe

def execute():
	frappe.delete_doc("Custom Field","Item-excelus_sticker_cost_per_no")
	frappe.delete_doc("Custom Field","Item-excelus_tape_required_per_carton")
	frappe.delete_doc("Custom Field","Item-excelus_carton_width")
	frappe.delete_doc("Custom Field","Item-excelus_film_thickness")
	frappe.delete_doc("Custom Field","Item-excelus_film_wastage")
	frappe.delete_doc("Custom Field","Item-excelus_pack_width")
	frappe.delete_doc("Custom Field","Item-excelus_pack_length")
	frappe.delete_doc("Custom Field","Item-excelus_packs_per_carton")
	frappe.delete_doc("Custom Field","Item-excelus_pack_weight")
	frappe.db.commit()
