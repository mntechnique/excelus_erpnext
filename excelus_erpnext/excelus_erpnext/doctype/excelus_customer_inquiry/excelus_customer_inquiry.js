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
        frm.add_custom_button(__("Fetch Items"), function(){
            /*var req_items = [];
            var req = frm.doc.ci_requirements;
            for (var i = req.length - 1; i >= 0; i--) {
                req_items.push(req[i].item);
            }*/
            frappe.call({
                method: "excelus_erpnext.excelus_erpnext.doctype.excelus_customer_inquiry.excelus_customer_inquiry.calculate_fetch_item",
                args: {
                    "req_items": frm.doc.ci_requirements
                },
                callback: function(r){
                    // msgprint(r.message);
                   console.log(r.message);
                }
            });
        });
	}
});

cur_frm.add_fetch("item" ,"default_bom","bom")
