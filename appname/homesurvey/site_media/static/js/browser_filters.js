/*
 * 
 */
(function(){
    // Convenience extension
    jQuery.fn.exists = function(){return this.length>0;}
    
    // Activate sideways accordian
    $('#accordian-div').liteAccordion({
        linkable : true,
        enumerateSlides : true,
        containerHeight : $(window).height()-180, // account for enough space so no scrolling
        containerWidth : $(window).width()*.8
    });
    
    $('#accordian-div').parent().width($(window).width()*.8)
    
    // Create variables for panels
    var left_pane = $($("#accordian-div li div.content-swipe-panel").get(0));
    var middle_pane = $($("#accordian-div li div.content-swipe-panel").get(1));
    var right_pane = $($("#accordian-div li div.content-swipe-panel").get(2));

    /*
     * Load pages into each panel and load necessary data
     */            
    $.when(
        left_pane.load("/browser/filter/views/create/", function(){
            loadValueFilterOptions();
        }),
        middle_pane.load("/browser/filter/views/create_meta/", function(){
            createMiddlePaneForms();
        }),
        right_pane.load("/browser/filter/views/browse/", function(){
            load_matching_participants();
        })
    ).done(function(lp, mp, rp){
        /*
         * Load filters
         */
        $.getJSON("/api/v1/participantfilter/", {'format': 'json'}, function(data){
            var filters_html = "";
            $.each(data.objects, function(k,v){
                filters_html += "<div class='filter' filter-id='" + v.id + "'><span class='filter-tag-title'>" + v.name + "</span><p>" + v.description + "</p></div>";
            })
            
            left_pane.find(".display-box").html(filters_html);
            right_pane.find(".display-box").prepend("<div class='value-filters'>" + filters_html + "</div>");
            middle_pane.find(".display-list").prepend("<div class='value-filters'>" + filters_html + "</div>");
        }).done(function(){
            activateMiddlepaneDragDrop();
        })

        $.getJSON("/api/v1/participantmetafilter/", {'format': 'json'}, function(data){
            var meta_filters_html = "";
            $.each(data.objects, function(k,v){
                meta_filters_html += "<div class='filter meta' filter-id='" + v.id + "'><span class='filter-tag-title'>" + v.name + "</span><p>" + v.description + "</p></div>";
            })

            middle_pane.find(".display-box").html(meta_filters_html);
            right_pane.find(".display-box").append("<div class='meta-filters'>" + meta_filters_html + "</div>");
            middle_pane.find(".display-list").append("<div class='meta-filters'>" + meta_filters_html + "</div>");
        }).done(function(){
            activateMiddlepaneDragDrop();
        })
    })
    
    
    /*********************************************************************
     * LEFT PANE
     */
    
    /*
     * Left pane helper functions
     */            
    
    // Load filter options
    function loadValueFilterOptions(){
        // Get filter option list
        $.ajax({
            url: "/browser/filter/filteroptions/",
            dataType: 'json',
            data: {'formatted_for_list': true},
            success: function(data){
                $("#options-list img").addClass('hidden');
                var html = build_level_ul(data);
                $("#options-list .options-tree").html(html);
            },
            beforeSend: function(){
                $("#options-list img").removeClass('hidden');
            }
        }).done(function(){
            $("ul > ul > li.filter-option-category").trigger("click"); // start with everything past level 2 collapsed
        })                
    }
    
    // Build ul structure for collapsing list out of layered json
    function build_level_ul(obj){
        var html = "";
        if (obj.short_name == undefined){
            html += "<ul>";
            $.each(obj,function(k,v){
               var next_level_html = build_level_ul(v);
               if (next_level_html == ""){
                   html += "<li><a filter-id='" + v.id + "' title='" + v.full_name + "' href='#'>" + v.short_name + "</a></li>";
               } else {
                   html += "<li class='filter-option-category'>" + k + "</li>";
                   html += next_level_html;
               }
            })
            html += "</ul>";
        }
        return html;
    }                  

    /*
     * Get the currently selected value(s) for filtering on
     * 
     * type = [text, ratio, ordinal, boolean, multi_select, single_select]
     * msmd_manager = msmd_manager object
     */
    function getValueFilterValue(type, nm, human_readable){
        var vfv;
        
        if (type == "text" || type == "ratio" || type == "ordinal"){
            vfv = String($("#inputValue").val());
        } else if (type == "boolean") {
            if (!$("#inputValue").closest("div.control-group").hasClass("hidden")){
                vfv = $("#inputValue :selected").html().toLowerCase();
            } else {
                vfv = "";
            }
        } else {
            if (human_readable){
                vfv = String(nm.getSelectObjectNames())
            } else {
                vfv = String(nm.getSelectedIDs())
            }
        }
        // If the string is blank, return a nicer form to show this
        return vfv;
    }
    
    /*
     * Left pane event handlers
     */
    left_pane.on("click", ".options-tree a", function(){
        // Load html from server; attach event handlers / multi-select stuff in .don() method
        var filtertype_id = $(this).attr('filter-id');
        $.ajax({
            url: "/browser/filter/filterform/",
            dataType: 'json',
            data: {"filtertype-id": filtertype_id},
            success: function(d){
                $("#edit-filter-display img").addClass("hidden");
                $("#edit-filter-display .content").html(d.html);
                
                /*
                 * Get recommended name
                 * 
                 * Url must be built up to handle __in sorting on ManyToMany fields
                 * 
                 * http://localhost:7000/api/v1/participantfilter/?format=json&groups__id=1&filter_field=QualityLife4_7
                 */
                var group_ids = [1,2,3,4];
                var rec_name = filtertype_id + "_g" + group_ids.join("-") + "_f";
                
                var filter_url = "/api/v1/participantfilter/?";
                $.each(group_ids, function(k,v){
                    filter_url += "groups__id__in=" + v + "&"
                })
                filter_url + "format=json&filter_field=" + filtertype_id;
                
                $.get(filter_url, function(d){
                    rec_name += String(d.objects.length + 1);
                }).done(function(){
                    // replace default name with recommendation
                    $("#inputName").attr("value",rec_name);
                })
                postLoadValueFilterForm(d, filtertype_id);
            },
            beforeSend: function(){
                $("#edit-filter-display img").removeClass("hidden");
            }
        })
        return false;
    })
    
    /*
     * Re-load filter for further editing
     * 
     * - get html from template
     * - bind functions
     * - change values to values fetched from api
     * - change save() to POST id if available
     * 
     */
    left_pane.on("click", ".display-box .filter", function(){
        var filter_id = $(this).attr("filter-id");
        
        $.ajax({
            url: "/browser/filter/filterform/",
            dataType: 'json',
            data: {'filter-id': filter_id},
            success: function(d){
                $("#edit-filter-display img").addClass("hidden");
                $("#edit-filter-display .content").html(d.html);
                var filtertype_id = d.filter_field;
                
                /*
                 * Actions specific for re-loaded filters
                 */
                // Load the selected action
                $("#inputFilterOperator option[value='" + d.filter.action + "']").attr('selected',true);
                
                // Load the selected value for non single and multi-select fields
                if (d.type == "text" || d.type == "ratio" || d.type == "ordinal"){
                    $("#inputValue").val(d.filter.argument);
                } else if (d.type == "boolean") {
                    if (!$("#inputValue").closest("div.control-group").hasClass("hidden")){
                        $("#inputValue option[value='" + d.filter.argument + "']").attr('selected',true);
                    }
                }
                postLoadValueFilterForm(d, filtertype_id);                        
            },
            beforeSend: function(){
                $("#edit-filter-display img").removeClass("hidden");
            }
        })
    })

    // Wipe out entered information and return to default view
    left_pane.on("click","#edit-filter-display .btn.cancel",function(){
        $("#edit-filter-display .content").html('<div class="centered-info"><p>Select a filter type to create a new filter, or select an existing filter to display</p></div>');
        return false;
    })
    
    // Hide and show sub-categories
    left_pane.on("click", ".options-tree li.filter-option-category", function(){
        if ($(this).find("span").exists()){
            $(this).children().remove()
            $(this).next().show('fast')
        } else {
            $(this).next().hide('fast')
            $(this).append("<span>[+]</span>")
        }
        return false;
    })
    
    /*
     * Functions to call after loading the HTML for the ValueFilter
     */
    function postLoadValueFilterForm(d, filtertype_id){
        /*
         * Specific adjustments based on dataType
         */
        var nm; // preallocate variable for msmd_manager if needed                        
        if (d.type == "multi_select" || d.type == "single_select"){
            d.default_representation_type = d.default_representation_type ? d.default_representation_type : "checkbox";
            
            var nm_options = {  default_input_type: d.default_representation_type,
                                choices: d.options}
                                
            nm = msmd_manager(  target_element = $("#edit-filter-display .optionSelect"), 
                                    options = nm_options);
        }
        
        if (d.type == "text"){
            $("#inputFilterOperator").change(function(d){
                if (d.currentTarget.selectedIndex > 1){
                    // selected a filter which does not require a value
                    $("#inputValue").closest("div.control-group").addClass("hidden");
                } else {
                    $("#inputValue").closest("div.control-group").removeClass("hidden");
                }
            })
        }
                        
        // Turn on preview
        var filter_id = parseInt($("#new-filter-form :input[name=filter-id]").val());
        if (filter_id){
            left_pane.find("button.preview").removeClass("disabled");
            left_pane.find("button.saveas").removeClass("hidden");
            left_pane.find("button.btn-danger").removeClass("hidden");
            left_pane.find(".btn.save").html("Save Changes");
        }

        /*
         * Save filter
         */
        function saveValueFilter(){
            var filter_name = $("#inputName").val();
            var filter_desc = $("#inputDescription").val();                    
            
            var filter_data = JSON.stringify({
                filter_field: filtertype_id,
                groups: {},
                name: filter_name,
                description: filter_desc,
                action: $("#inputFilterOperator :selected").val(),
                argument: getValueFilterValue(d.type, nm),
                
            })
            
            $.ajax({
                url: "/api/v1/participantfilter/",
                type: "POST",
                contentType: 'application/json',
                data: filter_data,
                complete: function(d){
                    // Grab new filter id
                    var new_filter_id = d.getResponseHeader("Location").split("participantfilter")[1].split("/")[1];
                    $("#new-filter-form :input[name=filter-id]").val(new_filter_id);
                    
                    // Code to handle addition of filter into dom
                    var new_filter_html = "<div class='filter' filter-id='" + new_filter_id + "'>";
                    new_filter_html += "<span class='filter-tag-title'>" + filter_name + "</span>";
                    new_filter_html += "<p>" + filter_desc + "</p>";
                    new_filter_html += "</div>";

                    left_pane.find(".display-box").prepend(new_filter_html); // left_pane
                    middle_pane.find(".display-list .value-filters").prepend(new_filter_html); // middle pane
                    right_pane.find(".display-box .value-filters").prepend(new_filter_html); // right pane
                    activateMiddlepaneDragDrop();
                },
                dataType: 'json',
                processData: false
            })
        }
        
        /*
         * Print out a nice human readable expression of the filter that changes as fields are updated
         */
        function setHumanReadableFilterDisplay(){
            $("#new-filter-form button.saveas").closest("div").find("p > em").html(function(){
                var filter_field_name = $("span.sub-title").html();
                var filter_operation =  $("#inputFilterOperator :selected").html().toLowerCase();
                return filter_field_name + " " + filter_operation + ' "' + getValueFilterValue(d.type, nm, true) + '"';
            })                            
        }

        // Set up selector for tracked elements
        var monitoredInputElements = "";
        monitoredInputElements += "#inputFilterOperator"
        monitoredInputElements += "," + "#inputValue"
        monitoredInputElements += "," + "#edit-filter-display .optionSelect textarea"
        monitoredInputElements += "," + "#edit-filter-display .optionSelect select"
        monitoredInputElements += "," + "#edit-filter-display .optionSelect input[type=checkbox]"
        
        // Re-create the label when stuff changes
        $(monitoredInputElements).change(function(){
            setHumanReadableFilterDisplay();
        })
        
        // Initialize the form
        setHumanReadableFilterDisplay();
        
        $("#edit-filter-display .btn.save").click(function(){
            var filter_id = parseInt($("#new-filter-form :input[name=filter-id]").val());
            if (filter_id){
                alert("NOT IMPLEMENTED");
            } else {
                // save new
                saveValueFilter();
            }
            return false;
        })
        
        $("#edit-filter-display .btn.saveas").click(function(){
            alert("NOT IMPLEMENTED")
            return false;
        })
        
        $("#edit-filter-display .btn.btn-danger").click(function(){
            alert("NOT IMPLEMENTED")
            return false;
        })
    }

    /**********************************************************************
     * MIDDLE PANE
     */

    /*
     * Make draggable
     * 
     * Takes an array pf DOM elements (result of jQuery selection) and makes them draggable
     */
    function activateMiddlepaneDragDrop(){
        makeDraggable(middle_pane.find(".display-list .filter"), $("#edit-meta-filter-display .meta-create-block .meta"));
        makeDraggable(middle_pane.find(".display-box .filter.meta"), $("#edit-meta-filter-display .meta-create-block .meta"));
        middle_pane.find(".meta-create-block .meta").droppable({
            hoverClass: "ui-drop-ready", 
            tolerance: "pointer",
            drop: function(event, ui){
                var drag_obj = $(ui.draggable);
                //console.log(ui.draggable)
                $(this).html(drag_obj.html());
                $(this).addClass("ui-drop-dropped");
                $(this).attr("filter-id", drag_obj.attr("filter-id"))
                $(this).attr("filter-type", drag_obj.hasClass("meta") ? "meta": "value")
                
                if ( $("#metaFilterAutoName")[0].checked){
                    // Update suggested name automatically
                    $("#inputMetaName").val(getMetaFilterName());
                }
            }
        })
    }
    
    function makeDraggable(elements, snap_target){
        elements.addClass("ui-widget-content").draggable({ 
            scroll: false, containment: middle_pane, 
            zIndex: 10000, helper: "clone",
            snap: snap_target});
    }

    /*
     * Helper functions for middle pane
     */
    function createMiddlePaneForms(){
        /*
         * Auto naming
         */
        $("#metaFilterAutoName").change(function(){
            if (this.checked){
                $("#inputMetaName").attr("disabled","");
                $("#inputMetaName").val(getMetaFilterName());
            } else {
                $("#inputMetaName").removeAttr("disabled");
            }
        })
        
        middle_pane.on('change', '.meta-create-block select', function(){
            if ( $("#metaFilterAutoName")[0].checked){
                $("#inputMetaName").val(getMetaFilterName());
            }
        })

       /*
         * Middle pane action buttons
         */                
        middle_pane.find(".btn.save").click(function(event){
            if ($(this).hasClass("disabled")){
                return false;
            }
            event.preventDefault();
            
            var filter_id = parseInt($("#new-meta-filter-form :input[name=filter-id]").val());
            if (filter_id){
                alert("NOT IMPLEMENTED");
            } else {
                saveMetaFilter();
            }
        })
        
        middle_pane.find(".btn.saveas").click(function(){
            alert("NOT IMPLEMENTED")
            return false;
        })

        middle_pane.find(".btn.cancel").click(function(){
            clearMetaFilterForm();
            return false;
        })
        
        middle_pane.find(".btn.btn-danger").click(function(){
            alert("NOT IMPLEMENTED")
            return false;
        })
        
        /*
         * Checking data validity
         * 
         * @returns True if everything is ok
         */
        function checkFormData(){
            var retval = true;
            
            if ($("#inputMetaName").val()){
                $("#inputMetaName").closest("div.control-group").removeClass("error");
                $("#inputMetaName").parent().find(".help-inline").addClass("hidden");
            } else {
                $("#inputMetaName").closest("div.control-group").addClass("error");
                $("#inputMetaName").parent().find(".help-inline").removeClass("hidden");
                retval = false;
            }
            
            var filter_ids = _.map($(".meta-create-block .meta"), function(v){ return parseInt($(v).attr("filter-id"))});
            if (_.any(filter_ids, function(v){ return isNaN(v)})){
                //alert("Both filters must be assigned before saving.  Please make sure both filters are defined and try again.");
                $(".meta-create-block").closest("div.control-group").addClass("error");
                $(".meta-create-block").parent().find(".help-inline").removeClass("hidden");
                retval = false;
            } else {
                $(".meta-create-block").closest("div.control-group").removeClass("error");
                $(".meta-create-block").parent().find(".help-inline").addClass("hidden");
            }
            return retval;
        }
        
        /*
         * Save filter
         */
        function saveMetaFilter(){
            var filter_name = $("#inputMetaName").val();
            var filter_desc = $("#inputMetaDescription").val();
            var valuefilter_ids = _.map($(".meta-create-block .meta[filter-type=value]"), function(v){ return parseInt($(v).attr("filter-id"))}); // NaN if not assigned
            var metafilter_ids = _.map($(".meta-create-block .meta[filter-type=meta]"), function(v){ return parseInt($(v).attr("filter-id"))}); // NaN if not assigned
            
            // Check that values are defined
            if (!checkFormData()){
                return false;
            }
            
            var valuefilters = _.map(valuefilter_ids, function(v){ return "/api/v1/participantfilter/" + v + "/"; })
            var metafilters = _.map(metafilter_ids, function(v){ return "/api/v1/participantmetafilter/" + v + "/"; })
            
            var filter_data = JSON.stringify({
                name: filter_name,
                description: filter_desc,
                action: $(".meta-create-block .operator :selected").val(),
                filters: valuefilters,
                metafilters: metafilters,
                groups: {}
            })
            
            $.ajax({
                url: "/api/v1/participantmetafilter/",
                type: "POST",
                contentType: 'application/json',
                data: filter_data,
                complete: function(d){
                    // Grab new filter id
                    var new_filter_id = d.getResponseHeader("Location").split("participantmetafilter")[1].split("/")[1];
                    postLoadMetaFilterForm(new_filter_id);
                    
                    // Code to handle addition of filter into dom
                    var new_filter_html = "<div class='filter meta' filter-id='" + new_filter_id + "'>";
                    new_filter_html += "<span class='filter-tag-title'>" + filter_name + "</span>";
                    new_filter_html += "<p>" + filter_desc + "</p>";
                    new_filter_html += "</div>";

                    middle_pane.find(".display-box").prepend(new_filter_html); // left_pane
                    middle_pane.find(".display-list .meta-filters").prepend(new_filter_html); // middle pane
                    right_pane.find(".display-box .meta-filters").prepend(new_filter_html); // right pane
                    activateMiddlepaneDragDrop();
                },
                dataType: 'json',
                processData: false
            })
        }
    }
    
    function clearMetaFilterForm(){
        $("#edit-meta-filter-display > .label-block > h2").html("Create New Meta Filter");
        middle_pane.find(".btn.save").html("Create");
        middle_pane.find(".btn.cancel").html("Clear");
        
        // reset droppables to original state
        middle_pane.find(".meta-create-block .meta").removeClass("ui-drop-dropped");
        middle_pane.find(".meta-create-block .meta").removeAttr("filter-id");
        middle_pane.find(".meta-create-block .meta").removeAttr("filter-type");
        
        // Add back in original html
        middle_pane.find(".meta-create-block .meta.left").html("<span>Filter 1</span>")
        middle_pane.find(".meta-create-block .meta.right").html("<span>Filter 2</span>")
        
        // Unset values
        middle_pane.find("input[name=filter-id]").val(null)
        $("#inputMetaName").val(null)
        $("#inputMetaDescription").val(null)
        middle_pane.find("textarea.idPreview").val(null);
        
        // Disable or hide buttons
        middle_pane.find("button.preview").addClass("disabled");
        middle_pane.find("button.saveas").addClass("hidden");
        middle_pane.find("button.btn-danger").addClass("hidden");
        
        // Unset/hide warnings
        $("#inputMetaName").closest("div.control-group").removeClass("error");
        $("#inputMetaName").parent().find(".help-inline").addClass("hidden");
        middle_pane.find(".meta-create-block").closest("div.control-group").removeClass("error");
        middle_pane.find(".meta-create-block").parent().find(".help-inline").addClass("hidden");
    }
    
    // called after save or load of a saved metafilter
    function postLoadMetaFilterForm(new_filter_id){
        middle_pane.find(".btn.save").html("Save Changes");
        middle_pane.find(".btn.cancel").html("Close");
        middle_pane.find("input[name=filter-id]").val(new_filter_id)
        middle_pane.find("button.preview").removeClass("disabled");
        middle_pane.find("button.saveas").removeClass("hidden");
        middle_pane.find("button.btn-danger").removeClass("hidden");
    }
    
    // Used for auto naming
    // call when option is toggled on or when a new filter is dropped and option is on
    function getMetaFilterName(){
        var name_divs = $(".meta-create-block > div")
        return  "(" + name_divs.eq(0).attr("filter-type") + "_" +  name_divs.eq(0).attr("filter-id") + ")" +
                name_divs.eq(1).find(":selected").val() + 
                "(" + name_divs.eq(2).attr("filter-type") + "_" + name_divs.eq(2).attr("filter-id") + ")";
    }
    
    /*
     * Redisplay meta-filter
     */
    middle_pane.on("click", ".display-box .meta.filter", function(){
        var filter_id = $(this).attr("filter-id");
        
        // Clear
        middle_pane.find(".btn.cancel").trigger('click');
        
        $.ajax({
            url: "/api/v1/participantmetafilter/" + filter_id + "/",
            dataType: 'json',
            data: {'format': 'json'},
            success: function(d){
                $("#edit-meta-filter-display > .label-block > h2").html("Edit Existing Meta Filter");
                
                $("#inputMetaName").val(d.name)
                $("#inputMetaDescription").val(d.description)                        
                postLoadMetaFilterForm(d.id);
                
                // Load HTML of matching elements
                var urls = d.filters.concat(d.metafilters);
                
                var loadable_divs = $("#edit-meta-filter-display .meta-create-block .meta.ui-droppable");
                _.each(urls, function(v,k){
                    var target_div = loadable_divs.eq(k);
                    $.getJSON(v,{'format':'json'},function(d){
                        new_filter_html = "<span class='filter-tag-title'>" + d.name + "</span>";
                        new_filter_html += "<p>" + d.description + "</p>";
                        target_div.html(new_filter_html);
                        target_div.addClass("ui-drop-dropped");
                        target_div.attr("filter-id", d.id); // break into id
                        target_div.attr("filter-type", (v.indexOf("meta") !== -1) ? "meta": "value");
                        if (k == (urls.length - 1)){
                            $("#edit-meta-filter-display img").addClass("hidden");
                        }
                    })
                })
            },
            beforeSend: function(){
                $("#edit-meta-filter-display img").removeClass("hidden");
            }
        })
    })
    

    /**********************************************************************
     * RIGHT PANE
     */
    right_pane.on("click", ".display-box .filter", function(){
        if ($(this).hasClass("meta")){
            load_matching_participants($(this).attr('filter-id'), true);
        } else {
            load_matching_participants($(this).attr('filter-id'), false);
        }
        
    })
    
    right_pane.on("click", "#participant-data-table .label-block a", function(){
        load_matching_participants();
    })

    /*
     * Load into right pane
     */
    function load_matching_participants(filter_id, is_meta){
        var server_data = {};
        if (filter_id !== undefined){
            if (is_meta){
                server_data.meta_filter_id = filter_id;
            } else {
                server_data.filter_id = filter_id;
            }
            $("#participant-data-table h2 > span:nth-child(3)").html(" Matching Participants");
        } else {
            $("#participant-data-table h2 > span:nth-child(3)").html(" Total Participants in Study");
        }
        
        var table_div = $("#participant-data-table .participant-table");
        
        $("#participant-data-table h2 > span:first").addClass("hidden");
        $("#participant-data-table h2 > img").removeClass("hidden");
        
        $.get("/browser/filter/participants/", server_data, function(data){
            table_div.html(data);
        }).done(function(){
            var n_matching_participants = table_div.find("tr").length - 1;
            $("#participant-data-table h2 > span:first").html(n_matching_participants);
            $("#participant-data-table h2 > span:first").removeClass("hidden");
            $("#participant-data-table h2 > img").addClass("hidden");
        });
    }

    /**********************************************************************
     * GENERIC FUNCTIONS FOR MULTIPLE PANES
     */
    $("#accordian-div").on("click","button.preview",function(event){
        if($(this).hasClass("disabled")){
            return false;
        }
        event.preventDefault();
        
        var typeobj = getFilterTypeForButton(this)
        var filter_id_name = (typeobj.type == "value") ? "filter_id" : 'meta_filter_id';
        var parent_form = typeobj.parent_form;
        
        var filter_id = parseInt(parent_form.find(":input[name=filter-id]").val());
        server_data = {'format': 'json'}
        server_data[filter_id_name] = filter_id;
        loadPreview(server_data);
    })
    
    /*
     * @param server_data - an object pf params to be passed to the server
     */
    function loadPreview(server_data){
        if (server_data.hasOwnProperty('filter_id')){
            var working_area = left_pane;
        } else {
            var working_area = middle_pane;
        }
        
        $.ajax({
            url: "/browser/filter/participants/",
            data: server_data,
            beforeSend: function(){
                working_area.find("button.preview").addClass("disabled");
                working_area.find("button.preview").html("Loading ids of matching participants....");
            },
            complete: function(d){
                working_area.find("button.preview").removeClass("disabled");
                working_area.find("button.preview").html("Preview Selected IDs");
            },
            success: function(d){
                console.log(d);
                if (d.length == 0){
                    working_area.find("textarea.idPreview").val("No participants in your current dataset match this query");
                } else {
                    working_area.find("textarea.idPreview").val(String(d));
                }
            },
            dataType: 'json'
        })
    }

    /*
     * @param button - a dom object of the button clicked
     * @returns obj
     *          type: 'meta' or 'value' depending on the type of filter being edited
     *          parent-form: a jquery object of the form associated with that type
     */
    function getFilterTypeForButton(button){
        var ret_obj = {};
        ret_obj.parent_form = $(button).parents("#new-filter-form")
        
        if (ret_obj.parent_form.length){
            ret_obj.type = "value";                    
        } else {
            ret_obj.parent_form = $(button).parents("#new-meta-filter-form");
            ret_obj.type = "meta";
        }
        return ret_obj;                
    }
})();
