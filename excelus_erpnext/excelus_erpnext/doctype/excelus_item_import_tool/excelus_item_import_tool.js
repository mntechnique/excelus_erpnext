// Copyright (c) 2016, MN Technique and contributors
// For license information, please see license.txt

frappe.ui.form.on('Excelus Item Import Tool', {
	refresh: function(frm) {

	},
	btn_import_items: function(frm) {
		frappe.call({
			method: "excelus_erpnext.api.excelus_import_items",
			args: { 
				path_to_sheet: frm.doc.attach_items_csv
			},
			freeze: true,
			freeze_message: "Importing...",
			callback: function(r) {
				if(r) {
					console.log(r.message);
				}
			}
		});
	}
});
