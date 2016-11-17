// Copyright (c) 2016, MN Technique and contributors
// For license information, please see license.txt

frappe.ui.form.on('Excelus Customer Inquiry', {
	refresh: function(frm) {
		cur_frm.set_query("item", "ci_requirements", function() {
        return {
           filters: [
				['Item', 'item_group', '=', 'Products']
		   ]
        };
    });
	}
});
