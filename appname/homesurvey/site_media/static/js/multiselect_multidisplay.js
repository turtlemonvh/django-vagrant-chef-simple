/*
 * @class
 * Manager object used to handle multi-select objects 
 * 
 * @param target_element The element in which to insert the html representation of the choices, as a jQuery object
 * @param options An objext with the following fields:
 *      choices: an object taking on the following structure
 *               {1: {id: 1, is_default: true, is_selected: true, label: "test1"}, ...}
 *      choice_url: a url which will respond with the choice object as json if it is not directly provided
 *      choice_url_data: an object containing additional GET parameters to pass to choice_url
 *      default_input_type: the type of display
 * 
 * Notes:
 * No errors are thrown explicitly if target_element does not exist.
 */
var msmd_manager = function(target_element, options){
    /*
     * Utility variables/constants used throughout
     */
    var input_type_options = ["checkbox","multiselect","textbox"];
    
    /*
     * Initialize variables passed in by user
     */
    var options = options || {};
    var choices = options.choices;
    
    // Check to make sure option is allowed
    if ($.inArray(options.default_input_type,input_type_options) == -1){
        var default_input_type = "textbox";
    } else {
        var default_input_type = options.default_input_type;
    }
    
    /*
     * Initialize the data object
     */
    function init (){
        // Operations executed once choices are loaded
        function processChoices(){
            target_element.html(getHTML(default_input_type));
            target_element.attr("input-type", default_input_type);
        }
        
        if (typeof choices === 'undefined'){
            // Fetch data from server
            $.getJSON(options.choice_url, options.choice_url_data, function(d){
                choices = d;
            }).done(function(){
                processChoices()
            })
        } else {
            // Process passed data directly
            processChoices();
        }
    }
    
    
    /*
     * Create html based on the requested type
     */
    this.getHTML = function(input_type){
        // Default assignments
        if (input_type == undefined){
            input_type = default_input_type;
        }
        
        // Get the numbers of extra and default elements
        var nextra_elements = $.map(choices, function(v){ if(!v.is_default) return 1;}).length;
        var ndefault_elements = $.map(choices, function(v){ if(v.is_default) return 1;}).length;

        var default_html = "";
        var extra_html = "";
        
        switch (input_type) {
            case "checkbox":
                var check_html;
                $.each(choices, function(k,v){
                    // Expect form: options as {id: {id: x, label: x, is_default: x, }}
                    check_html = (v.is_selected) ? "checked='checked'" : "";
                    if (v.is_default){
                        default_html += "<input type='checkbox' name='" + k + "' value='" + k + "' " + check_html + "/> " + v.label + "<br/>";
                    } else {
                        extra_html += "<input type='checkbox' name='" + k + "' value='" + k + "' " + check_html + "/> " + v.label + "<br/>";
                    }
                });
                break;
            case "multiselect":
                var select_html;
                default_html += "<select multiple='multiple' class='input-xlarge'>";
                extra_html += "<select multiple='multiple' class='input-xlarge'>";
                $.each(choices, function(k,v){
                    // Expect form: options as {id: {id: x, label: x, is_default: x, }}
                    select_html = (v.is_selected) ? "selected='selected'" : "";
                    if (v.is_default){
                        default_html += "<option title='" + v.label + "' value='" + k + "' " + select_html + "> " + v.label + "</option>";
                    } else {
                        extra_html += "<option title='" + v.label + "' value='" + k + "' " + select_html + "> " + v.label + "</option>";
                    }
                });
                default_html += "</select>";
                extra_html += "</select>";
                break;
            case "textbox":
                $.each(choices, function(k,v){
                    if (v.is_selected){
                        if (v.is_default){ 
                            default_html += v.id + ",";
                        } else {
                            extra_html += v.id + ",";
                        }
                    }
                });
                
                // Trim if anything was added
                if (default_html){
                    default_html = default_html.slice(0,-1);
                }
                if (extra_html){
                    extra_html = extra_html.slice(0,-1);
                }
                
                default_html = "<textarea rows='3' placeholder='Provide a list of ids, separated by commas or whitespace.'>" + default_html + "</textarea>"
                extra_html = "<textarea rows='3' placeholder='Provide a list of ids, separated by commas or whitespace.'>" + extra_html + "</textarea>"
                break;
            default:
                alert("Misunderstood type attribute for multi-select field.")
                return;
        };
        
        /*
         * Print format depends on whether default options are distingushed from extra options
         */
        var html = "";
        if (ndefault_elements && nextra_elements ){
            html += "<b>Default Options</b><br/>";
            html += default_html;
            html += "<br/>";
            html += "<b>Extra Options</b><br/>";
            html += extra_html;
        } else {
            html += (ndefault_elements ? default_html : extra_html); // whichever is not empty
        }
        
        return html;
    }
    
    /*
     * @returns Array of selected ids of provided choices
     */
    this.getSelectedIDs = function(){
        // Get current input type
        var cinput_type = target_element.attr("input-type");
        var ids;
        switch (cinput_type) {
            case "checkbox":
                ids = $.map(target_element.find(":checked"),function(v){return +v.name;});
                break;
            case "multiselect":
                ids = $.map(target_element.find(":checked"),function(v){return +v.value;});
                break;
            case "textbox":
                // Accepts tab separated, comma separated, newline separated, or any combination of those
                var non_integer_value_error = false; // set to true if an invalid value is entered
                ids = $.map($(target_element.find("textarea")).val().split(/[\s,]+/), function(v){ if (String(+v) != v){if (v != ""){ non_integer_value_error = true;}} else{ return +v;}});
                if (non_integer_value_error){
                    alert("Non integer values are not allowed in the 'Options' field.")
                }
                break;
            default:
                alert("Misunderstood type attribute for multi-select field.")
                return;
        }
        return ids;
    }
    
    this.getSelectObjectNames = function(){
        var ids = getSelectedIDs();
        data_obj = $.map(choices,function(v){
            if ($.inArray(+v.id,ids) != -1){
                if (v.label){
                    return v.label;
                } else {
                    return String(v.id);
                }
            }
        });
        return data_obj;
    }
    
    /*
     * @returns Choice object, modified so is_selected attributes match current object state
     */
    this.updateObjectWithIDs = function() {
        var ids = getSelectedIDs();
        var data_obj = choices;
        
        $.each(data_obj, function(k,v){
            if ($.inArray(+k,ids) != -1){
                v.is_selected = true;
            } else {
                v.is_selected = false;
            }
        })
        
        choices = data_obj;
        return choices;
    }
    
    /*
     * Updates the matching ids and switches the display to the requested format
     */
    this.changeInputType = function(new_type){
        if ($.inArray(new_type,input_type_options) !== -1){
            updateObjectWithIDs();
            target_element.html(getHTML(new_type));
            target_element.attr("input-type", new_type);
        }
    }
    
    /*
     * Add event handlers
     */

    
    /*
     * Initialize
     */
    init();
    
    /*
     * Return handler on object
     */
    return this;
};
