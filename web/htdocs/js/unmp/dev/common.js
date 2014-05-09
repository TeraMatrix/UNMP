var global_log = "False";
var tactical_call = null;
var isLogged_in = 0;
var last_accessed = Date.now();
//@TODO: get these variables from server.
var IDLE_TIMEOUT = 5 * 60;
var GRACE_PERIOD = 60;

// prototype tabs with jquery object
$.fn.yoTabs = function (tabs) {
    this.each(function () {
        var $this = $(this);
        var firstLi = $this.find(">ul").find("li:first");
        var allA = $this.find(">ul").find("a");
        allA.removeClass("active");
        allA.click(function (e) {
            e.preventDefault();
            var $$this = $(this);
            var parentA = $$this.parent().parent().find("a");
            var parentTab = $$this.parent().parent().parent();
            parentTab.find("> div.tab-content").hide();
            parentA.removeClass("active");
            $$this.addClass("active");
            var hrefArr = $$this.attr('href').split('#');
            var divId = "#" + hrefArr[hrefArr.length - 1];
            parentTab.find(divId).show();
        });
        firstLi.find("a").click();
    });
    return this;
};

// prototype spin loading with jquery object
$.fn.spin = function (opts) {
    this.each(function () {
        var $this = $(this),
            data = $this.data();

        if (data.spinner) {
            data.spinner.stop();
            delete data.spinner;
        }
        if (opts !== false) {
            data.spinner = new Spinner($.extend({color: $this.css('color')}, opts)).spin(this);
        }
    });
    return this;
};

// start spin loading
function spinStart(obj, objContainer, css, lines, length, width, radius, color, speed, trail, shadow) {
    lines = lines != null ? lines : 12;
    length = length != null ? length : 14;
    width = width != null ? width : 4;
    radius = radius != null ? radius : 14;
    color = color != null ? color : '#FFF';
    speed = speed != null ? speed : 1;
    trail = trail != null ? trail : 30;
    shadow = shadow != null ? shadow : true;
    var opts = {
        lines: lines, 			// The number of lines to draw
        length: length,		// The length of each line
        width: width, 			// The line thickness
        radius: radius, 		// The radius of the inner circle
        color: color, 		// #rgb or #rrggbb
        speed: speed, 			// Rounds per second
        trail: trail, 			// Afterglow percentage
        shadow: shadow 		// Whether to render a shadow
    };
    objContainer.show();
    obj.show();
    obj.spin(opts);
    if (css != null) {
        obj.find("> div").css(css);
    }
}

// stop spin loading
function spinStop(obj, objContainer) {
    objContainer.hide();
    obj.hide();
    obj.stop();
}

// To start spin loading function call like that
// spinStart(spinLoading,spinMainLoading);

// To stop spin loading function call like that
// spinStop(spinLoading,spinMainLoading);


//prototype dasboard with jquery object
$.fn.yoDashboard = function (options) {
    var options = $.extend({
        title: "My Dashboard Graph",						// use this if you want to change title of dashboard graph or dashboard table
        width: "100%",										// use this if you want to change width of dashboard graph or dashboard table
        height: "180px",									// use this if you want to change height of dashboard graph or dashboard table
        className: "",										// use this if you want to add new class
        style: {},											// use this if you want to add new style sheet
        showNextPreButton: false,							// use this if you want to show/hide next previous button on dashboard graph or dashboard table
        autoRefresh: false,									// use this if you want dashboard make auto refresh
        showRefreshButton: false,							// use this if you want to show/hide refresh button on dashboard graph or dashboard table
        getTotalItem: function () {
            return 0;
        },					// call function that return number of items
        totalItem: 0,
        startFrom: 0,										// use this if you want to change start range
        itemLimit: 5,										// use this if you want to change item limit
        showTabOption: false,								// use this if you want to show/hide tab option
        tabList: {value: [], name: [], selected: null},			// use this to add tab options
        ajaxRequest: function (div_obj, start, limit, tab_value) {
            return true
        },	// ajax request that create your dashboard graph or dashboard table
        //spinStart(obj,objContainer,css,lines,length,width,radius,color,speed,trail,shadow)
        //spinStart($("#dashboard1").find("div.sm-spin"),$("#dashboard1").find("div.sm-loading"),{"left":"30px","top":"30px"},12,8,3,7,'#FFF',1,30,true);
        loadingSpinCss: {"left": "30px", "top": "30px"},
        loadingSpinLines: 12,
        loadingSpinLength: 8,
        loadingSpinWidth: 3,
        loadingSpinRadius: 7,
        loadingSpinColor: '#FFF',
        loadingSpinSpeed: 1,
        loadingSpinTrail: 30,
        loadingSpinShadow: true,
        errorMsg: "Some server problem occurred, Please try again later."
    }, options);
    //alert(options.height);
    //alert(options.title);
    this.options = options;
    options.totalItem = options.getTotalItem();
    return this.each(function () {
        var $this = $(this);
        $this.options = options;

        // create dashboard head
        var $dbHead = $("<div/>");
        $dbHead.addClass("db-head");

        // create title span
        var $span = $("<span/>");
        $span.html($this.options.title);
        $span.appendTo($dbHead);

        // create button container
        var $aDiv = $("<div/>");
        $aDiv.addClass("db-menu");

        // create button options
        // previous button
        var $prevA = $("<a/>");
        $prevA.addClass("ds");
        $prevA.attr("href", "#");

        var $prevASpan = $("<span/>");
        $prevASpan.addClass("prv");
        $prevASpan.appendTo($prevA);

        if ($this.options.showNextPreButton) {
            $prevA.addClass("ft");
            $prevA.appendTo($aDiv);
        }

        // next button
        var $nextA = $("<a/>");
        $nextA.addClass("ds");
        $nextA.attr("href", "#");

        var $nextASpan = $("<span/>");
        $nextASpan.addClass("nxt");
        $nextASpan.appendTo($nextA);

        if (!$this.options.showRefreshButton)
            $nextA.addClass("lt");

        if ($this.options.showNextPreButton)
            $nextA.appendTo($aDiv);


        // refresh button
        var $refeshA = $("<a/>");
        $refeshA.addClass("ds");
        $refeshA.attr("href", "#");

        var $refeshASpan = $("<span/>");
        $refeshASpan.addClass("rf2");
        $refeshASpan.appendTo($refeshA);

        if ($this.options.showRefreshButton) {
            if ($this.options.showNextPreButton)
                $refeshA.addClass("lt");
            else
                $refeshA.addClass("ftlt");
            $refeshA.removeClass("ds");
            $refeshA.addClass("en");
            $refeshA.appendTo($aDiv);
        }

        // next-prev button enable or disable
        $.yoDashboard.changeNextPrevState($this, $nextA, $prevA);

        // bind Event with next button
        $nextA.click(function (e) {
            e.preventDefault();
            if ($(this).hasClass("en")) {
                $.yoDashboard.ajaxCall($this, true, 1);
            }
        });

        // bind Event with previous button
        $prevA.click(function (e) {
            e.preventDefault();
            if ($(this).hasClass("en")) {
                $.yoDashboard.ajaxCall($this, true, 2);
            }
        });

        // bind Event with refresh button
        $refeshA.click(function (e) {
            e.preventDefault();
            // ajax call
            $.yoDashboard.ajaxCall($this, true, 0);
        });

        // bind Event with body
        $(document).click(function (event) {
            $.yoDashboard.clickOnBody($this);
        });

        if ($this.options.showTabOption && $this.options.tabList.value.length > 0) {
            // Create Tabs
            var $tabs = $("<div/>");
            $tabs.addClass("db-tab");

            var $aTabs = $("<a/>");
            $aTabs.attr("href", "#");

            // Create Tab List
            var $tabList = $("<div/>");
            $tabList.addClass("db-tab-list");

            var $ul = $("<ul/>");
            for (var i = 0; i < $this.options.tabList.value.length; i++) {
                var $li = $("<li/>");
                var $aLi = $("<a/>");
                $aLi.attr("href", "#");
                $aLi.attr("value", $this.options.tabList.value[i]);
                $aLi.html($this.options.tabList.name[i]);
                if ($this.options.tabList.value[i] == $this.options.tabList.selected) {
                    $aLi.addClass("selected");
                    $aTabs.attr("value", $this.options.tabList.value[i]);
                    $aTabs.html($this.options.tabList.name[i]);
                    var $spanATabs = $("<span/>");
                    $spanATabs.addClass("dwn");
                    $spanATabs.appendTo($aTabs);
                }
                $aLi.click(function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    $aThis = $(this)
                    $aThis.parent().parent().find("a").removeClass("selected");
                    $aThis.addClass("selected");
                    $.yoDashboard.updateSelectedValue($this, $aThis.attr("value"), $aThis.html());
                    // ajax call
                    $.yoDashboard.ajaxCall($this, true, 0);
                    $.yoDashboard.clickOnBody($this);
                });
                $aLi.appendTo($li);
                $li.appendTo($ul);
            }
            $li.addClass("lt");
            $ul.appendTo($tabList);
            $tabList.hide();
            $tabList.appendTo($dbHead);

            // bind Event on tabs
            $aTabs.click(function (e) {
                e.preventDefault();
                e.stopPropagation();
                $.yoDashboard.showTabList($this);
            });
            $aTabs.appendTo($tabs);
            $tabs.appendTo($dbHead);
        }

        $aDiv.appendTo($dbHead);

        // dashboard body
        $dbBody = $("<div/>");
        $dbBody.addClass("db-body");

        // dashboard body container
        $dbBodyContainer = $("<div/>");
        $dbBodyContainer.addClass("db-container");
        $dbBodyContainer.attr("id", "ccpl_" + $this.attr("id"));
        $dbBodyContainer.css("height", $this.options.height);
        $dbBodyContainer.appendTo($dbBody);

        // dashboard main loading
        $dbMainLoading = $("<div/>");
        $dbMainLoading.addClass("sm-loading");
        $dbMainLoading.hide();

        // dashboard spin loading
        $dbSpinLoading = $("<div/>");
        $dbSpinLoading.addClass("sm-spin");
        $dbSpinLoading.hide();

        // render html
        $this.html("");
        $dbHead.appendTo($this);
        $dbBody.appendTo($this);
        $dbMainLoading.appendTo($this);
        $dbSpinLoading.appendTo($this);

        // ajax call
        $.yoDashboard.ajaxCall($this, false, 0);
    });
};


var ccplDashboard = $.yoDashboard = {
    changeNextPrevState: function ($this, $nextA, $prevA) {
        var nextSlotStartFrom = $this.options.startFrom + $this.options.itemLimit;
        if ($this.options.totalItem > nextSlotStartFrom) {
            $nextA.removeClass("ds");
            $nextA.addClass("en");
        }
        else {
            $nextA.removeClass("en");
            $nextA.addClass("ds");
        }
        if ($this.options.startFrom > 0) {
            $prevA.removeClass("ds");
            $prevA.addClass("en");
        }
        else {
            $prevA.removeClass("en");
            $prevA.addClass("ds");
        }
    },
    clickOnNextChangeNextPrevValue: function ($this) {
        var nextStart = $this.options.startFrom + $this.options.itemLimit;
        if (nextStart < $this.options.totalItem)
            $this.options.startFrom = nextStart;
    },
    clickOnPrevChangeNextPrevValue: function ($this) {
        $this.options.startFrom = $this.options.startFrom - $this.options.itemLimit;
        if ($this.options.startFrom < 0)
            $this.options.startFrom = 0;
    },
    clickOnBody: function ($this) {
        $this.find("div.db-head > div.db-tab-list").hide();
    },
    showTabList: function ($this) {
        $this.find("div.db-head > div.db-tab-list").slideDown();
    },
    updateSelectedValue: function ($this, value, text) {
        var $a = $this.find("div.db-head > div.db-tab > a");
        $a.attr("value", value);
        $a.html(text + "<span class=\"dwn\"></span>");
        $this.options.tabList.selected = value;
    },
    showLoading: function ($this) {
        var $loading = $this.find("div.sm-loading");
        var $spin = $this.find("div.sm-spin");
        spinStart($spin, $loading, $this.options.loadingSpinCss, $this.options.loadingSpinLines, $this.options.loadingSpinLength, $this.options.loadingSpinWidth, $this.options.loadingSpinRadius, $this.options.loadingSpinColor, $this.options.loadingSpinSpeed, $this.options.loadingSpinTrail, $this.options.loadingSpinShadow);
    },
    hideLoading: function ($this) {
        var $loading = $this.find("div.sm-loading");
        var $spin = $this.find("div.sm-spin");
        spinStop($spin, $loading);
    },
    ajaxCall: function ($this, showMsg, button, update) {
        $.yoDashboard.showLoading($this);
        var start = $this.options.startFrom;
        var limit = $this.options.itemLimit;
        if (button == 1) // for next
        {
            start = start + limit;
        }
        else if (button == 2) // for previous
        {
            start = start - limit;
        }
        if (!$this.options.ajaxRequest($this.find("div.db-body > div.db-container"), start, limit, $this.options.tabList.selected)) {
            if (showMsg) {
                $.prompt($this.options.errorMsg, {prefix: 'jqismooth'});
                //$.yoDashboard.hideLoading($this);
            }
        }
        else {
            if (button == 1) {
                $.yoDashboard.clickOnNextChangeNextPrevValue($this);
                $.yoDashboard.changeNextPrevState($this, $this.find("div.db-head > div.db-menu > a:eq(1)"), $this.find("div.db-head > div.db-menu > a:eq(0)"));
            }
            else if (button == 2) {
                $.yoDashboard.clickOnPrevChangeNextPrevValue($this);
                $.yoDashboard.changeNextPrevState($this, $this.find("div.db-head > div.db-menu > a:eq(1)"), $this.find("div.db-head > div.db-menu > a:eq(0)"));
            }
            //$.yoDashboard.hideLoading($this);
        }
    }
};

// generic dashboard api
$.fn.yoAllGenericDashboard = function (options) {
    var options = $.extend({
        graphs: [],
        graphColumn: 2,
        otherData: [],
        db: {},
        afterComplete: function (dbId) {
        }
    }, options);
    this.options = options;
    var dbVar = {};
    this.each(function () {
        var $this = $(this);
        $this.options = options;
        //alert($this.options.graphColumn);
        var $table = $("<table/>");
        $table.attr({"cellspacing": "10px", "cellpadding": "0", "width": "100%"});
        var $tr = $("<tr/>");
        var tdWith = 100 / options.graphColumn;
        //alert($this.options.graphs.length);
        for (var i = 0; i < $this.options.graphs.length; i++) {
            if (i % $this.options.graphColumn == 0) {
                if (i != 0) {
                    $tr.appendTo($table);
                }
                $tr = $("<tr/>");
            }
            var $td = $("<td/>");
            $td.css("width", String(tdWith) + "%");
            var $div = $("<div/>");
            $div.attr("id", "graph_" + String($this.options.graphs[i].name));
            $div.attr("class", "db-box");
            $this.options.graphs[i]["otherData"] = $this.options.otherData;
            $this.options.graphs[i]["afterComplete"] = $this.options.afterComplete;
            // stop specific loading IF TABLE & not GRAPH
            /*try{
             if($this.options.otherData[7].name)
             {

             if(isTableFunc != undefined || isTableFunc != null)
             {
             $this.options.graphs[i]["showSpinLoad"] = false;
             }
             }


             }
             catch(ex)
             {
             $this.options.graphs[i]["showSpinLoad"] = true;
             }*/
            //
            dbVar[String($this.options.graphs[i].name)] = $div.yoGenericDashboard($this.options.graphs[i]);
            $div.appendTo($td);
            $td.appendTo($tr);
        }
        var extraTdCount = $this.options.graphs.length % $this.options.graphColumn;

        for (var j = 0; j < extraTdCount; j++) {
            var $td = $("<td/>");
            var $div = $("<div/>");
            $div.appendTo($td);
            $td.appendTo($tr);
        }
        $tr.appendTo($table);
        $this.html("");
        $table.appendTo($this);
    });
    this.options.db = dbVar;
    return this;
};

// prototype generic dashboard with jquery object
$.fn.yoGenericDashboard = function (options) {
    var options = $.extend({
        name: "my_graph",
        displayName: "My Dashboard Graph",				// use this if you want to change Display Name of dashboard graph or dashboard table
        type: [],
        fields: [],
        calType: [],
        ajax: {
            method: "get",
            url: null,
            data: {},
            cache: false
        },
        totalItemAjax: {
            method: "get",
            url: null,
            data: {},
            cache: false
        },
        otherOption: {
            width: "100%",
            height: "180px",
            showRefreshButton: false,	// use this if you want to show/hide refresh button on dashboard graph or dashboard table
            showNextPreButton: false,	// use this if you want to show/hide next previous button on dashboard graph or dashboard table
            showTabOption: false,								// use this if you want to show/hide tab option
            showOption: false,
            showType: false,
            showFields: false,
            showCalType: false,
            autoRefresh: false					// use this if you want dashboard make auto refresh
        },
        onRefreshAjax: {
            method: "get",
            url: null,
            data: {},
            cache: false
        },
        className: "",										// use this if you want to add new class
        style: {},											// use this if you want to add new style sheet
        totalItem: -1,
        startFrom: 0,										// use this if you want to change start range
        itemLimit: 5,										// use this if you want to change item limit
        tabList: {value: [], name: [], selected: null},			// use this to add tab options
        ajaxRequest: function (div_obj, start, limit, tab_value) {
            return true
        },	// ajax request that create your dashboard graph or dashboard table
        //spinStart(obj,objContainer,css,lines,length,width,radius,color,speed,trail,shadow)
        //spinStart($("#dashboard1").find("div.sm-spin"),$("#dashboard1").find("div.sm-loading"),{"left":"30px","top":"30px"},12,8,3,7,'#FFF',1,30,true);
        showSpinLoad: true,

        loadingSpinCss: {"left": "30px", "top": "30px"},
        loadingSpinLines: 12,
        loadingSpinLength: 8,
        loadingSpinWidth: 3,
        loadingSpinRadius: 7,
        loadingSpinColor: '#FFF',
        loadingSpinSpeed: 1,
        loadingSpinTrail: 30,
        loadingSpinShadow: true,
        errorMsg: "Some server problem occurred, Please try again later.",
        otherData: [],
        setTimeoutVar: null,
        isTable: false,
        afterComplete: function (dbId) {
        }
    }, options);
    //alert(options.height);
    //alert(options.displayName);root
    this.options = options;
    return this.each(function () {
        var tabRightPosition = 3;

        var $this = $(this);
        $this.options = options;

        if ($this.options.otherOption.showRefreshButton == true) {
            tabRightPosition += 20;
        }
        if ($this.options.otherOption.showNextPreButton == true) {
            tabRightPosition += 40;
        }
        if (tabRightPosition > 3) {
            tabRightPosition += 3;
        }
        // create dashboard head
        var $dbHead = $("<div/>");
        $dbHead.addClass("db-head");

        // create title span
        var $span = $("<span/>");
        $span.html($this.options.displayName);

        // create button container
        var $aDiv = $("<div/>");
        $aDiv.addClass("db-menu");

        // create button options
        // previous button
        var $prevA = $("<a/>");
        $prevA.addClass("ds");
        $prevA.attr("href", "#");

        var $prevASpan = $("<span/>");
        $prevASpan.addClass("prv");
        $prevASpan.appendTo($prevA);

        if ($this.options.otherOption.showNextPreButton) {
            $prevA.addClass("ft");
            $prevA.appendTo($aDiv);
        }

        // next button
        var $nextA = $("<a/>");
        $nextA.addClass("ds");
        $nextA.attr("href", "#");

        var $nextASpan = $("<span/>");
        $nextASpan.addClass("nxt");
        $nextASpan.appendTo($nextA);

        if (!$this.options.otherOption.showRefreshButton)
            $nextA.addClass("lt");

        if ($this.options.otherOption.showNextPreButton)
            $nextA.appendTo($aDiv);


        // refresh button
        var $refeshA = $("<a/>");
        $refeshA.addClass("ds");
        $refeshA.attr("href", "#");

        var $refeshASpan = $("<span/>");
        $refeshASpan.addClass("rf2");
        $refeshASpan.appendTo($refeshA);

        if ($this.options.otherOption.showRefreshButton) {
            if ($this.options.otherOption.showNextPreButton) {
                $refeshA.addClass("lt");
            }
            else {
                $refeshA.addClass("ftlt");
            }
            $refeshA.removeClass("ds");
            $refeshA.addClass("en");
            $refeshA.appendTo($aDiv);
        }

        // other option button
        var $otherOptionDiv = $("<div/>");
        $otherOptionDiv.addClass("opt-btn");

        var $otherOptionIns = $("<ins/>");
        $otherOptionIns.addClass("oo");
        $otherOptionIns.appendTo($otherOptionDiv);


        // other options button list
        var $optionListDiv = $("<div/>");

        if ($this.options.otherOption.showOption && (($this.options.otherOption.showType && $this.options.type.length > 0) || ($this.options.otherOption.showFields && $this.options.fields.length > 0) || ($this.options.otherOption.showCalType && $this.options.calType.length > 0))) {
            $otherOptionDiv.appendTo($dbHead);

            // for IE Browser Support
            $span.appendTo($dbHead);

            // click event
            $otherOptionDiv.click(function (e) {
                e.stopPropagation();
                var $this = $(this);
                $this.next().next().show();
            });

            // create options in the options button list
            $optionListDiv.addClass("yo-contextmenu");

            // click event
            $optionListDiv.click(function (e) {
                e.stopPropagation();
            });
            // option list ul
            var $ul = $("<ul/>");


            // li separator
            var $li = $("<li/>");
            $li.addClass("yo-separator");
            $li.addClass("yo-separator-before");
            $li.appendTo($ul);

            // create graph type menu
            if ($this.options.otherOption.showType && $this.options.type.length > 0) {
                var $li = $("<li/>");

                var $ins = $("<ins/>");
                $ins.html("&nbsp;");
                $ins.appendTo($li);

                var $liA = $("<a/>");
                $liA.attr({"href": "#", "rel": "graph_type"});
                $liA.html("Graph Type");

                var $liArrow = $("<span/>");
                $liArrow.css({"line-height": "17px", "position": "relative", "right": "-20px"});
                $liArrow.html("&raquo;");
                $liArrow.appendTo($liA);

                $liA.appendTo($li);

                // li A click Event
                $liA.click(function (e) {
                    e.preventDefault();
                    var $this = $(this);
                    $this.parent().parent().find("ul").hide();
                    $this.next().show();

                });
                // graph type sub menu
                var $gtUl = $("<ul/>");
                for (var gtI = 0; gtI < $this.options.type.length; gtI++) {
                    var $gtLi = $("<li/>");
                    var $gtIns = $("<ins/>");
                    $gtIns.html("&nbsp;");
                    $gtIns.appendTo($gtLi);

                    var $gtLiA = $("<a/>");
                    $gtLiA.attr({"href": "#", "rel": $this.options.type[gtI].value});
                    $gtLiA.html($this.options.type[gtI].name);

                    // Click Event for anchor
                    $gtLiA.click(function (e) {
                        e.preventDefault();
                        var $thisA = $(this);
                        var isUpdate = "";
                        $thisA.parent().parent().find("div.ch").hide();
                        for (var gtII = 0; gtII < $this.options.type.length; gtII++) {
                            if ($this.options.type[gtII].isChecked == 1) {
                                if ($this.options.type[gtII].value != $thisA.attr("rel")) {
                                    isUpdate = "type";
                                }
                            }
                            $this.options.type[gtII].isChecked = 0;
                            if ($this.options.type[gtII].value == $thisA.attr("rel")) {
                                $this.options.type[gtII].isChecked = 1;
                                $thisA.find("div.ch").show();
                            }
                        }
                        // ajax call
                        $.yoGenericDashboard.ajaxCall($this, true, 0, isUpdate);
                        $.yoGenericDashboard.clickOnBody($this);
                    });
                    var $liCheck = $("<div/>");
                    $liCheck.css({"width": "16px", "height": "16px", "position": "absolute", "top": "0", "right": "3px"});
                    $liCheck.addClass("ch");
                    if ($this.options.type[gtI].isChecked == 1) {
                        $liCheck.show();
                    }
                    else {
                        $liCheck.hide();
                    }
                    $liCheck.appendTo($gtLiA);
                    $gtLiA.appendTo($gtLi);
                    $gtLi.appendTo($gtUl);
                }
                $gtUl.appendTo($li);
                $li.appendTo($ul);
                // li separator
                var $li = $("<li/>");
                $li.addClass("yo-separator");
                $li.addClass("yo-separator-before");
                $li.appendTo($ul);
            }
            $ul.appendTo($optionListDiv);
            $optionListDiv.appendTo($dbHead);

            // create fields menu
            if ($this.options.otherOption.showFields && $this.options.fields.length > 0) {
                var $li = $("<li/>");

                var $ins = $("<ins/>");
                $ins.html("&nbsp;");
                $ins.appendTo($li);

                var $liA = $("<a/>");
                $liA.attr({"href": "#", "rel": "fields"});
                $liA.html("Fields");

                var $liArrow = $("<span/>");
                $liArrow.css({"line-height": "17px", "position": "relative", "right": "-20px"});
                $liArrow.html("&raquo;");
                $liArrow.appendTo($liA);

                $liA.appendTo($li);

                // li A click Event
                $liA.click(function (e) {
                    e.preventDefault();
                    var $this = $(this);
                    $this.parent().parent().find("ul").hide();
                    $this.next().show();

                });
                // fields menu
                var $gtUl = $("<ul/>");
                if ($this.options.fields.length > 8) {
                    $gtUl.css({"height": '150px'})
                }
                for (var gtI = 0; gtI < $this.options.fields.length; gtI++) {
                    var $gtLi = $("<li/>");
                    var $gtIns = $("<ins/>");
                    $gtIns.html("&nbsp;");
                    $gtIns.appendTo($gtLi);

                    var $gtLiA = $("<a/>");
                    $gtLiA.attr({"href": "#", "rel": $this.options.fields[gtI].name});
                    $gtLiA.html($this.options.fields[gtI].displayName);

                    // Click Event for anchor
                    $gtLiA.click(function (e) {
                        e.preventDefault();
                        var $thisA = $(this);
                        for (var gtII = 0; gtII < $this.options.fields.length; gtII++) {
                            if ($this.options.fields[gtII].name == $thisA.attr("rel")) {
                                if ($this.options.fields[gtII].isChecked == 1) {
                                    $this.options.fields[gtII].isChecked = 0
                                    $thisA.find("div.ch").hide();
                                }
                                else {
                                    $this.options.fields[gtII].isChecked = 1
                                    $thisA.find("div.ch").show();
                                }
                            }
                        }
                        // ajax call
                        $.yoGenericDashboard.ajaxCall($this, true, 0, "fields");
                        $.yoGenericDashboard.clickOnBody($this);
                    });

                    var $liCheck = $("<div/>");
                    $liCheck.css({"width": "16px", "height": "16px", "position": "absolute", "top": "0", "right": "3px"});
                    $liCheck.addClass("ch");
                    if ($this.options.fields[gtI].isChecked == 1) {
                        $liCheck.show();
                    }
                    else {
                        $liCheck.hide();
                    }
                    $liCheck.appendTo($gtLiA);
                    $gtLiA.appendTo($gtLi);
                    $gtLi.appendTo($gtUl);
                }
                $gtUl.appendTo($li);
                $li.appendTo($ul);


                // li separator
                var $li = $("<li/>");
                $li.addClass("yo-separator");
                $li.addClass("yo-separator-before");
                $li.appendTo($ul);
            }

            // create calcutation menu
            if ($this.options.otherOption.showCalType && $this.options.calType.length > 0) {
                var $li = $("<li/>");

                var $ins = $("<ins/>");
                $ins.html("&nbsp;");
                $ins.appendTo($li);

                var $liA = $("<a/>");
                $liA.attr({"href": "#", "rel": "calc"});
                $liA.html("Calc");

                var $liArrow = $("<span/>");
                $liArrow.css({"line-height": "17px", "position": "relative", "right": "-20px"});
                $liArrow.html("&raquo;");
                $liArrow.appendTo($liA);

                $liA.appendTo($li);

                // li A click Event
                $liA.click(function (e) {
                    e.preventDefault();
                    var $this = $(this);
                    $this.parent().parent().find("ul").hide();
                    $this.next().show();

                });
                // graph type sub menu
                var $gtUl = $("<ul/>");
                for (var gtI = 0; gtI < $this.options.calType.length; gtI++) {
                    var $gtLi = $("<li/>");
                    var $gtIns = $("<ins/>");
                    $gtIns.html("&nbsp;");
                    $gtIns.appendTo($gtLi);

                    var $gtLiA = $("<a/>");
                    $gtLiA.attr({"href": "#", "rel": $this.options.calType[gtI].name});
                    $gtLiA.html($this.options.calType[gtI].displayName);

                    // Click Event for anchor
                    $gtLiA.click(function (e) {
                        e.preventDefault();
                        var $thisA = $(this);
                        $thisA.parent().parent().find("div.ch").hide();
                        var isUpdate = "";
                        for (var gtII = 0; gtII < $this.options.calType.length; gtII++) {
                            if ($this.options.calType[gtII].isChecked == 1) {
                                if ($this.options.calType[gtII].name != $thisA.attr("rel")) {
                                    isUpdate = "calType";
                                }
                            }
                            $this.options.calType[gtII].isChecked = 0;
                            if ($this.options.calType[gtII].name == $thisA.attr("rel")) {
                                $this.options.calType[gtII].isChecked = 1;
                                $thisA.find("div.ch").show();
                                // add calc type with graph name
                                $this.find("div.db-head").find("span").eq(0).html($this.options.displayName + " <label style='font-size:9px;color:#555;'> - " + String($this.options.calType[gtII].displayName) + "</label>")
                            }
                        }
                        // ajax call
                        $.yoGenericDashboard.ajaxCall($this, true, 0, isUpdate);
                        $.yoGenericDashboard.clickOnBody($this);
                    });
                    var $liCheck = $("<div/>");
                    $liCheck.css({"width": "16px", "height": "16px", "position": "absolute", "top": "0", "right": "3px"});
                    $liCheck.addClass("ch");
                    if ($this.options.calType[gtI].isChecked == 1) {
                        $liCheck.show();
                        // add calc type with graph name
                        $dbHead.find("span").eq(0).html($this.options.displayName + " <label style='font-size:9px;color:#555;'> - " + String($this.options.calType[gtI].displayName) + "</label>")
                    }
                    else {
                        $liCheck.hide();
                    }
                    $liCheck.appendTo($gtLiA);
                    $gtLiA.appendTo($gtLi);
                    $gtLi.appendTo($gtUl);
                }
                $gtUl.appendTo($li);
                $li.appendTo($ul);

                // li separator
                var $li = $("<li/>");
                $li.addClass("yo-separator");
                $li.addClass("yo-separator-before");
                $li.appendTo($ul);
            }
        }


        // next-prev button enable or disable
        $.yoGenericDashboard.changeNextPrevState($this, $nextA, $prevA);

        // bind Event with next button
        $nextA.click(function (e) {
            e.preventDefault();
            if ($(this).hasClass("en")) {
                $.yoGenericDashboard.ajaxCall($this, true, 1, "");
            }
        });

        // bind Event with previous button
        $prevA.click(function (e) {
            e.preventDefault();
            if ($(this).hasClass("en")) {
                $.yoGenericDashboard.ajaxCall($this, true, 2, "");
            }
        });

        // bind Event with refresh button
        $refeshA.click(function (e) {
            e.preventDefault();
            //$.yoGenericDashboard.ajaxCall($this,true,0,"");

            // ajax call
            if ($this.options.onRefreshAjax == undefined) {
                $.yoGenericDashboard.ajaxCall($this, true, 0, "");
            }
            else {
                $.ajax({
                    type: $this.options.onRefreshAjax.method,
                    url: $this.options.onRefreshAjax.url,
                    data: $this.options.onRefreshAjax.data,
                    cache: $this.options.onRefreshAjax.cache,
                    success: function (result) {
                        if (result.success == 0) {
                            $.yoGenericDashboard.ajaxCall($this, true, 0, "");
                        }
                        else {
                            if (result.msg == undefined) {
                                $().toastmessage('showErrorToast', "Device not responding.");
                                $.yoGenericDashboard.ajaxCall($this, true, 0, "");
                            }
                            else {
                                $().toastmessage('showErrorToast', String(result.msg));
                                $.yoGenericDashboard.ajaxCall($this, true, 0, "");
                            }
                        }
                    }
                });
            }
        });

        // bind Event with body
        $(document).click(function (event) {
            $.yoGenericDashboard.clickOnBody($this);
        });

        if ($this.options.otherOption.showTabOption && $this.options.tabList.value.length > 0) {
            // Create Tabs
            var $tabs = $("<div/>").css({"right": String(tabRightPosition) + "px"});
            $tabs.addClass("db-tab");

            var $aTabs = $("<a/>");
            $aTabs.attr("href", "#");

            // Create Tab List
            var $tabList = $("<div/>").css({"right": String(tabRightPosition) + "px"});
            $tabList.addClass("db-tab-list");

            var $ul = $("<ul/>");
            for (var i = 0; i < $this.options.tabList.value.length; i++) {
                var $li = $("<li/>");
                var $aLi = $("<a/>");
                $aLi.attr("href", "#");
                $aLi.attr("value", $this.options.tabList.value[i]);
                $aLi.html($this.options.tabList.name[i]);
                if ($this.options.tabList.value[i] == $this.options.tabList.selected) {
                    $aLi.addClass("selected");
                    $aTabs.attr("value", $this.options.tabList.value[i]);
                    $aTabs.html($this.options.tabList.name[i]);
                    var $spanATabs = $("<span/>");
                    $spanATabs.addClass("dwn");
                    $spanATabs.appendTo($aTabs);
                }
                $aLi.click(function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    $aThis = $(this)
                    if (!$aThis.hasClass("selected")) {
                        $aThis.parent().parent().find("a").removeClass("selected");
                        $aThis.addClass("selected");
                        $.yoGenericDashboard.updateSelectedValue($this, $aThis.attr("value"), $aThis.html());
                        $.yoGenericDashboard.ajaxCall($this, true, 0, "");
                    }
                    $.yoGenericDashboard.clickOnBody($this);

//					$aThis.parent().parent().find("a").removeClass("selected");
//					$aThis.addClass("selected");
//					$.yoGenericDashboard.updateSelectedValue($this,$aThis.attr("value"),$aThis.html());
                    // ajax call
//					$.yoGenericDashboard.ajaxCall($this,true,0,"");
                    $.yoGenericDashboard.clickOnBody($this);
                });
                $aLi.appendTo($li);
                $li.appendTo($ul);
            }
            $li.addClass("lt");
            $ul.appendTo($tabList);
            $tabList.hide();
            $tabList.appendTo($dbHead);

            // bind Event on tabs
            $aTabs.click(function (e) {
                e.preventDefault();
                e.stopPropagation();
                $.yoGenericDashboard.showTabList($this);
            });
            $aTabs.appendTo($tabs);
            $tabs.appendTo($dbHead);
        }
        $aDiv.appendTo($dbHead);

        // dashboard body
        $dbBody = $("<div/>");
        $dbBody.addClass("db-body");

        // dashboard body container
        $dbBodyContainer = $("<div/>");
        $dbBodyContainer.addClass("db-container");
        $dbBodyContainer.attr("id", "ccpl_" + $this.attr("id"));
        $dbBodyContainer.css("height", $this.options.otherOption.height);
        $dbBodyContainer.appendTo($dbBody);

        // dashboard main loading
        $dbMainLoading = $("<div/>");
        $dbMainLoading.addClass("sm-loading");
        $dbMainLoading.hide();

        // dashboard spin loading
        $dbSpinLoading = $("<div/>");
        $dbSpinLoading.addClass("sm-spin");
        $dbSpinLoading.hide();

        // render html
        $this.html("");
        $dbHead.appendTo($this);
        $dbBody.appendTo($this);
        $dbMainLoading.appendTo($this);
        $dbSpinLoading.appendTo($this);
        // stop spin loading for table
        if ($this.options.showSpinLoad == true) {
            $dbSpinLoading.appendTo($this);
        }
        // ajax call
        $.yoGenericDashboard.ajaxCall($this, false, 0, "");
    });
};

var ccplGenericDashboard = $.yoGenericDashboard = {
    changeNextPrevState: function ($this, $nextA, $prevA) {
        var nextSlotStartFrom = $this.options.startFrom + $this.options.itemLimit;
        if ($this.options.totalItem > nextSlotStartFrom) {
            $nextA.removeClass("ds");
            $nextA.addClass("en");
        }
        else {
            $nextA.removeClass("en");
            $nextA.addClass("ds");
        }
        if ($this.options.startFrom > 0) {
            $prevA.removeClass("ds");
            $prevA.addClass("en");
        }
        else {
            $prevA.removeClass("en");
            $prevA.addClass("ds");
        }
    },
    clickOnNextChangeNextPrevValue: function ($this) {
        var nextStart = $this.options.startFrom + $this.options.itemLimit;
        if (nextStart < $this.options.totalItem)
            $this.options.startFrom = nextStart;
    },
    clickOnPrevChangeNextPrevValue: function ($this) {
        $this.options.startFrom = $this.options.startFrom - $this.options.itemLimit;
        if ($this.options.startFrom < 0)
            $this.options.startFrom = 0;
    },
    clickOnBody: function ($this) {
        $this.find("div.db-head > div.db-tab-list").hide();
        $this.find("div.yo-contextmenu").hide();
        $this.find("div.yo-contextmenu > ul").find("ul").hide();
    },
    showTabList: function ($this) {
        $this.find("div.db-head > div.db-tab-list").slideDown();
    },
    updateSelectedValue: function ($this, value, text) {
        var $a = $this.find("div.db-head > div.db-tab > a");
        $a.attr("value", value);
        $a.html(text + "<span class=\"dwn\"></span>");
        $this.options.tabList.selected = value;
    },
    showLoading: function ($this) {
        var $loading = $this.find("div.sm-loading");
        var $spin = $this.find("div.sm-spin");
        spinStart($spin, $loading, $this.options.loadingSpinCss, $this.options.loadingSpinLines, $this.options.loadingSpinLength, $this.options.loadingSpinWidth, $this.options.loadingSpinRadius, $this.options.loadingSpinColor, $this.options.loadingSpinSpeed, $this.options.loadingSpinTrail, $this.options.loadingSpinShadow);
    },
    hideLoading: function ($this) {
        var $loading = $this.find("div.sm-loading");
        var $spin = $this.find("div.sm-spin");
        spinStop($spin, $loading);
    },
    ajaxCall: function ($this, showMsg, button, update) {
        $.yoDashboard.showLoading($this);
        var start = $this.options.startFrom;
        var limit = $this.options.itemLimit;
        if (button == 1) // for next
        {
            start = start + limit;
        }
        else if (button == 2) // for previous
        {
            start = start - limit;
        }
        var data = $this.options.ajax.data;
        if (data == undefined)
            data = {}
        data["start"] = start;
        data["limit"] = limit;
        data["tab"] = $this.options.tabList.selected;
        for (var i = 0; i < $this.options.type.length; i++) {
            if ($this.options.type[i].isChecked == 1) {
                data["type"] = $this.options.type[i].value;
                data["typeName"] = $this.options.type[i].name;
            }
        }
        var fieldArr = new Array();

        for (var i = 0; i < $this.options.fields.length; i++) {
            if ($this.options.fields[i].isChecked == 1) {
                fieldArr[fieldArr.length] = $this.options.fields[i].name;
            }
        }
        data["field"] = String(fieldArr);
        for (var i = 0; i < $this.options.calType.length; i++) {
            if ($this.options.calType[i].isChecked == 1) {
                data["calType"] = $this.options.calType[i].name;
            }
        }
        for (var i = 0; i < $this.options.otherData.length; i++) {
            data[$this.options.otherData[i].name] = $this.options.otherData[i].value();
            if ($this.options.otherData[i].name == "is_table") {
                $this.options.isTable = true;
            }

        }
        data["update"] = update;
        if ($this.options.ajax.url != null) {
            if ($this.options.totalItem == -1 && $this.options.totalItemAjax.url != null && $this.options.totalItemAjax.url != undefined) {
                var count = 0;
                $.ajax({
                    type: $this.options.totalItemAjax.method,
                    url: $this.options.totalItemAjax.url,
                    data: $this.options.totalItemAjax.data,
                    cache: $this.options.totalItemAjax.cache,
                    success: function (result) {
                        try {
                            count = parseInt(result);
                        }
                        catch (err) {
                            count = 0;
                        }
                        $this.options.totalItem = count;
                        data["total"] = String($this.options.totalItem);
                        $.yoDashboard.changeNextPrevState($this, $this.find("div.db-head > div.db-menu > a:eq(1)"), $this.find("div.db-head > div.db-menu > a:eq(0)"));
                        $.yoGenericDashboard.ajaxCallForGraph($this, showMsg, button, update, data);
                    }
                });
            }
            else {
                //$this.options.totalItem = 0;
                data["total"] = String($this.options.totalItem);
                $.yoGenericDashboard.ajaxCallForGraph($this, showMsg, button, update, data);
            }
        }
    },
    ajaxCallForGraph: function ($this, showMsg, button, update, data) {
        $.ajax({
            method: $this.options.ajax.method,
            url: $this.options.ajax.url,
            data: data,
            cache: $this.options.ajax.cache,
            success: function (result) {
                //alert(result);
                if (result["success"] == 0 || true) {
                    // plote graph
                    //result = {"success": 0, "timestamp": ["12:05","12:10","12:15","12:20","12:25","12:30","12:35","12:40","12:45"], "graph_sub_title": "statistics", "graph_title": "Network Bandwidth Statistics", "data": [{"data": [45,1,23,88,11,55,23,56,23], "name": ["TX Packets"," (Kbps)"]}, {"data": [12,34,2,45,67,45,34,11,56], "name": ["TX Packets"," (Kbps)"]}]};
                    var idObject = $this.find("div.db-body > div.db-container");
                    var drawType = data["typeName"];
                    if ($this.options.isTable != undefined && $this.options.isTable == true) {
                        var tableData = result["data"];
                        var $table = $("<table/>").addClass("yo-table").css({"width": "100%"}).attr({"cellspacing": "0px", "cellpadding": "0px"});
                        var $tr = $("<tr/>");
                        for (var thI = 0; thI < tableData["th"].length; thI++) {
                            $("<th/>").html(tableData["th"][thI]).appendTo($tr);
                        }
                        $tr.appendTo($table);
                        if (tableData["td"].length == 0) {
                            var $tr = $("<tr/>");
                            $("<td/>").attr({"colspan": tableData["th"].length}).html("No data exist.").appendTo($tr);
                            $tr.appendTo($table);
                        }
                        else {
                            for (var trI = 0; trI < tableData["td"].length; trI++) {
                                var $tr = $("<tr/>");
                                for (var tdI = 0; tdI < tableData["td"][trI].length; tdI++)
                                    $("<td/>").html(tableData["td"][trI][tdI]).appendTo($tr);
                                $tr.appendTo($table);
                            }
                        }
                        idObject.html("").css({"overflow": "auto"});
                        $table.appendTo(idObject);
                    }
                    else {
                        Highcharts.setOptions({
                            global: {
                                useUTC: false
                            }
                        });

                        $this.options.highChart = new Highcharts.Chart({
                            chart: {
                                zoomType: 'x',
                                spacingRight: 20,
                                renderTo: idObject.attr("id"),
                                defaultSeriesType: drawType
                                //marginRight: 10,
                                //marginBottom: 25
                            },
                            title: {
                                text: ""	//result.graph_title,
                                //x: 20 //center
                            },
                            subtitle: {
                                text: ""	//result.graph_sub_title,
                                //x: -20
                            },
                            xAxis: {
//								type: 'datetime',
                                labels: {
                                    formatter: function () {
                                        var hh = Highcharts.dateFormat('%H:%M:%S', this.value);
                                        if (hh == "00:00:00") {
                                            return Highcharts.dateFormat('%e %b %Y', this.value);
                                        }
                                        return Highcharts.dateFormat('%H:%M', this.value);
                                    },
                                    style: {
                                        color: (result.timestamp.length < 29) ? 'rgb(102,102,102)' : '#FFF',
                                        font: '10px Trebuchet MS, Verdana, sans-serif'
                                    }
                                },
                                //								labels: {
//									rotation: 0
//									},
                                tickLength: 20,
                                reversed: true,
                                categories: result.timestamp
                            },
                            yAxis: {
                                min: (result.range_min == undefined || result.range_min) ? null : result.range_min,
                                max: (result.range_max == undefined || result.range_max || result.range_max == 0) ? null : result.range_max,
                                title: {
                                    text: ''
                                }
                                /*							plotLines: [{
                                 value: 0,
                                 width: 1,
                                 color: '#808080'
                                 }]*/
                            },
                            tooltip: {
                                crosshairs: true,
                                shared: true,
                                formatter: function () {
                                    var s = '<b>' +
                                        (Highcharts.dateFormat('%H:%M', this.x) == "00:00" ? Highcharts.dateFormat('%e. %b %Y', this.x) : Highcharts.dateFormat('%e. %b %Y, %H:%M', this.x));
                                    //Highcharts.dateFormat('%e. %b %Y, %H:%M', this.x)+
                                    '</b>';
                                    $.each(this.points, function (i, point) {
                                        s += '<br/><span style="color: ' + String(point.series.color) + '">' + point.series.name + '</span>: ' +
                                            point.y;
                                    });
                                    return s;
                                }
                            },
                            plotOptions: {
                                spline: {
                                    marker: {
                                        radius: 4,
                                        lineColor: '#666666',
                                        lineWidth: 1
                                    }
                                }
                            },
                            /*						tooltip: {
                             crosshairs: true,
                             shared: true,
                             formatter: function() {
                             return '<b>'+ this.series.name[0] +'</b><br/>'+
                             ''+this.x+'<br/>' +' '+ this.y +' '+this.series.name[1];
                             }
                             },*/

                            legend: {
                                labelFormatter: function () {
                                    return this.name[0];
                                }
                            },
                            series: result.data
                        });
                    }
                }
                else if (showMsg) {
                    $.prompt($this.options.errorMsg, {prefix: 'jqismooth'});
                }
                if (button == 1) {
                    $.yoDashboard.clickOnNextChangeNextPrevValue($this);
                    $.yoDashboard.changeNextPrevState($this, $this.find("div.db-head > div.db-menu > a:eq(1)"), $this.find("div.db-head > div.db-menu > a:eq(0)"));
                }
                else if (button == 2) {
                    $.yoDashboard.clickOnPrevChangeNextPrevValue($this);
                    $.yoDashboard.changeNextPrevState($this, $this.find("div.db-head > div.db-menu > a:eq(1)"), $this.find("div.db-head > div.db-menu > a:eq(0)"));
                }
                $.yoDashboard.hideLoading($this);
            },
            complete: function () {
                if ($this.options.otherOption.autoRefresh != 0 && $this.options.otherOption.autoRefresh) {
                    if ($this.options.setTimeoutVar) {
                        clearTimeout($this.options.setTimeoutVar);
                    }
                    $this.options.setTimeoutVar = setTimeout(function () {
                        $.yoGenericDashboard.ajaxCall($this, true, 0, "");
                    }, ($this.options.otherOption.autoRefresh * 1000));
                    $this.options.afterComplete("graph_" + String($this.options.name));
                }
            }
        });
    }
};
// end prototype generic dashboard with jquery object


// firefox debug
$.debug = function (log_txt) {
    if (window.console != undefined) {
        console.log(log_txt);
    }
}
// firefox debug

// firefox debug
function getOffset(el) {
    var _x = 0;
    var _y = 0;
    while (el && !isNaN(el.offsetLeft) && !isNaN(el.offsetTop)) {
        _x += el.offsetLeft - el.scrollLeft;
        _y += el.offsetTop - el.scrollTop;
        el = el.offsetParent;
    }
    return { top: _y, left: _x };
}
var serverDate = new Date();

$(function () {
    var spinLoading = $("div#spin_loading");		// create object that hold loading circle
    var spinMainLoading = $("div#main_loading");	// create object that hold loading squire

    if ($(window).width() < 1100) {
        $("#container_body").css({"left": "0px"});
        $("#container_nav").css({"z-index": 100}).hide();
        $("#header3_text").css({"left": "0px"});
        $("#version_no", "#footer").css("margin-left", "100px");
        var sideBarDiv = $("<div/>").addClass("sidebar-btn-div").attr({"title": "Show"});
        if ($().tipsy != undefined) {
            sideBarDiv.tipsy({gravity: 'w'});
        }
        $("<a/>").html("Side Menu").appendTo(sideBarDiv);
        sideBarDiv.toggle(function (event) {
            event.stopPropagation();
            $("#container_nav").show();
            $("#container_body").css({"left": "260px"});
            $("#header3_text").css({"left": "260px"});
            sideBarDiv.attr({"original-title": "Hide"});
        }, function (event) {
            event.stopPropagation();
            $("#container_nav").hide();
            $("#container_body").css({"left": "0px"});
            $("#header3_text").css({"left": "0px"});
            sideBarDiv.attr({"original-title": "Show"});
        });
        sideBarDiv.appendTo($("#footer"));
        $("#container_body").show();
        $("body").click(function () {
            if ($("#container_nav").is(":visible")) {
                sideBarDiv.click();
            }
        });
    }
    else {
        $("#container_nav").show();
        $("#container_body").show();
    }
    //login_user event
    $("#login_user").click(function (e) {
        e.stopPropagation();
        $("#user_options").show();
    });	//sub sub menu events
    $("a.menu-link", "div#header2").click(function (e) {
        e.stopPropagation();
        $("div.sub-sub-menu").hide();
        var subSubDiv = $("div" + $(this).attr("href"));
        subSubDiv.show();
        var pos = getOffset(this);
        subSubDiv.css({top: pos.top + 30, left: pos.left});
    });
    //logout
    $("#logout").click(function () {
        try {
            spinStart(spinLoading, spinMainLoading);
        }
        catch (err) {
            spinLoading.hide();
            spinMainLoading.hide();
        }
        $.ajax({
            type: "post",
            url: "unmp_logout.py",
            cache: false,
            success: function (result) {
                if (result == 0 || result == "0") {
                    //window.location.reload();
                    //parent.location.href =	parent.location.href;
                    top.top.location.reload();
                }
                else {
                    //$.prompt(String("There is some error in logout. Please Contact Your Administrator."),{prefix:'jqismooth'});
                    console.log("logout error");
                    parent.location.href = parent.location.href;
                }
            }
        });
    });

    // Default Selected Link
    defaultSelectedLink = $("div#icons_div div.active");
    var defaultLinkHref = defaultSelectedLink.find("a").attr("href");
    if (defaultLinkHref != undefined) {
        $("div[rel='" + defaultLinkHref.split("\.py")[0] + "']", "#container_nav").show();
    }

    //menu functionality
    $("div#page_header a").click(function (e) {
        //e.preventDefault();
        e.stopPropagation();
        $(".header2_menu_div").hide();
        $($(this).attr("href")).show();
        $("#icons_div div.icon").removeClass("active");
        $(this).parent().addClass("active");
    });
    $("div.header2_menu_div > a").click(function (e) {
        //e.preventDefault();
        e.stopPropagation();
    });
    //show default selected menu
    $("body").click(function () {
        $("div#icons_div div.icon").removeClass("active");
        defaultSelectedLink.addClass("active");
        $("div.header2_menu_div").hide();
        $(defaultSelectedLink.find("a").attr("href")).show();

        // hide user options
        $("#user_options,div.sub-sub-menu").hide();
    });

    $("#toggle_events_logs_box").toggle(
        function () {
            $("#events_logs_box").slideDown();
            global_log = "True";
            $(this).attr("src", "images/new_icons/round_minus.png");
            get_log_data(1);
        },
        function () {
            $("#events_logs_box").slideUp();
            $(this).attr("src", "images/new_icons/round_plus.png");
            global_log = "False";
        });

    // close event and logs box @ footer
    $("#close_events_logs_box").click(function () {
        $("#toggle_events_logs_box").click();
    });

    // show tactical view
    tacticalView("#tactical_view");


    get_server_time();

    servertime = setInterval(function () {
        get_server_time();
    }, 15000);


    idleTimer();

    // tool tip
    if ($().tipsy != undefined) {
        $('.n-tip-image').tipsy({gravity: 'n'}); // n | s | e | w
        $('.s-tip-image').tipsy({gravity: 's'}); // n | s | e | w
        $('.e-tip-image').tipsy({gravity: 'e'}); // n | s | e | w
        $('.w-tip-image').tipsy({gravity: 'w'}); // n | s | e | w
    }
    sideBarToggle();
});

function idleTimer() {
    $(document).click(function () {
        last_accessed = Date.now();
    });

    $(document).keydown(function () {
        last_accessed = Date.now();
    });
}


function showWillLogoutMsg(seconds) {
    $().toastmessage('showToast', {
        text: '<div id="session_timeout" >\
			<table class="display" style="margin-left: 5px;">\
				<thead>\
					<tr>\
						<th colspan="2" class="ui-state-default">\
							Your Session is about to expire\
						</th>\
					</tr>\
				</thead>\
			<table>"\
        	There has been no activity on the UNMP interface, this session will be terminated in ' + seconds + ' seconds.<br> \
        	Please choose from the options below to - <br/><br/>\
        	<input type=button',
        sticky: true,
        position: 'top-center',
        type: 'warning',
        closeText: '',
        close: function () {
            last_accessed = Date.now();
            console.log("toast is closed ...");
        }
    });
}


function showBox(seconds) {
    if (seconds < 1)
        seconds = 1;

    box_html = "<div id=\"session_timeout\" style=\"width:440px;\"> \
		<table class=\"display\" style=\"margin-left: 5px;\"> \
		    <thead> \
		    <tr>\
		        <th class=\"ui-state-default\"> \
		            Your Session is about to expire \
		        </th> \
		    </tr> \
		    </thead> \
		    <tr> \
		        <th style=\"font-size: 11px;\"> \
		        	<br/>\
		            <img src=\"images/new/alert.png\" alt=\"\"/> \
		            There has been no activity on the UNMP interface, <br/>\
		            this session will be terminated in <span id=\"timeout_seconds\">" + seconds + "<span> seconds.\
		            <br/>  \
		        </th> \
		    </tr> \
		</table> \
		<div style=\"margin: 5px;\"> \
			<br/><br/> \
			<div style=\"border-bottom: 2px solid #73747B; color: #333;line-height: 1.6em;font-size: 12px; font-weight: bold;\"> \
				Please choose from the options below to - \
			<div> \
			<div style=\"float:right;margin: 5px;\" > \
				<button class=\"yo-small\" style=\"margin: 5px;margin-left: 10px;\" onclick=\"boxClose()\" type=\"button\"> \
					<span>Yes, keep working</span> \
				</button> \
			    <button class=\"yo-small\" style=\"margin: 5px;margin-right: 15px;\" onclick=\"logmeout()\" type=\"button\"> \
			    	<span>No, Logoff</span> \
			    </button> \
		    </div> \
		</div> \
		</div>"


    $.colorbox({onLoad: function () {
        $('#cboxClose').remove();
    },
        html: box_html,
//		html: "<div id=\"session_timeout\" > <table class=\"display\" style=\"margin-left: 5px;\"> <thead> <tr> <th class=\"ui-state-default\"> Your Session is about to expire </th> </tr> </thead> <tr> <th> <img src=\"images/new/alert.png\" alt=\"\"/> There has been no activity on the UNMP interface, this session will be terminated in <span id=\"timeout_seconds\">"+seconds+"<span> seconds.<br> Please choose from the options below to - <br/><br/> </th> </tr> <tr> <th> </th> </tr> <tr> <th class=\"ui-state-default\"> <table> <div> <button style=\"margin-left: 100px;\" type=\"button\" onclick=\"boxClose()\" disabled=\"\" value=\"Yes, keep working\"> </button> <button style=\"margin-left: 15px;\" type=\"button\" onclick=\"logmeout()\" disabled=\"\" value=\"No, Logoff\"> </button>  </div> </div>",
        opacity: 0.4,
        width: "480px",
        height: "246px"
    });

}

function logmeout() {
    $("#logout").click();
}
function boxClose() {
    last_accessed = Date.now();
    $.colorbox.close();
}


function get_server_time() {
    var idleTime = parseInt((Date.now() - last_accessed) / 1000);
    if (idleTime > (IDLE_TIMEOUT - GRACE_PERIOD)) {
        //$('div.toast-container').remove();
        //showWillLogoutMsg(135-idleTime);
        showBox(IDLE_TIMEOUT - idleTime);
    }
    else {
        // var taost_div = $('div.toast-container');
        // if(taost_div != null)
        // 	$('div.toast-container').remove();

    }

    $.ajax({//serverDate
        type: "get",
        url: "server_time.py?&idle_time=" + idleTime,
        cache: false,
        success: function (result_complete) {
            try {
                if (typeof result_complete == "string") {
                    if (result_complete.length > 400 && isLogged_in) {
                        isLogged_in = 0;
                        window.location = '';
                        //$("#logout").click();
                    }
                    else {
                        if (!isLogged_in) {
                            var result_data = result_complete.split("\n");
                            result = JSON.parse(result_data[1]).date_time_server;
                            serverDate = new Date(result[0], result[1] - 1, result[2], result[3], result[4], result[5]);
                            date_time($("#tactical_view"));
                        }

                        //mahipal's code
                        if (JSON.parse(result_data[0]).nagios == "stop")
                            $().toastmessage('showNoticeToast', "Nagios is stopped. Please start it.");
                        isLogged_in = 1;
                    }
                }
                else {
                    if (!isLogged_in) {
                        result = result_complete.date_time_server;
                        serverDate = new Date(result[0], result[1] - 1, result[2], result[3], result[4], result[5]);
                        date_time($("#tactical_view"));
                    }
                    isLogged_in = 1;
                }
            }
            catch (e) {

            }
            /////
            if (!isLogged_in) {
                clearInterval(servertime);
            }

        }
    });
}


function toggle_log_data(a) {
    if (a == 1) {
        get_log_data(1);
    }
    else {
        get_alarm_log_data(1);
    }
}
function get_log_data(a) {
    if (a != 1 && !($("#user_log_a").hasClass("head-link-active"))) {
        return false;
    }
    $("#user_log_a").addClass("head-link-active");
    $("#alarm_log_a").removeClass("head-link-active");
    var $fromObj = $("#get_current_log_data_form");
    var url = $fromObj.attr("action");
    var method = $fromObj.attr("method");
    var data = $fromObj.serialize();
    $.ajax({
        type: method,
        url: url,
        data: data,
        cache: false,
        success: function (result) {
            try {
                $("#log_user").html(result);
                //result2=result.data;
                //last_execution_time=result.last_execution_time;
            }
            catch (err) {
                $().toastmessage('showErrorToast', err);
            }
        }

    });
    if (global_log == "True" && $("#user_log_a").hasClass("head-link-active"))
        setTimeout(function () {
            get_log_data(2);
        }, 5000);
}


function get_alarm_log_data(a) {
    if (a != 1 && !($("#alarm_log_a").hasClass("head-link-active"))) {
        return false;
    }
    $("#user_log_a").removeClass("head-link-active");
    $("#alarm_log_a").addClass("head-link-active");
    var $fromObj = $("#get_current_log_data_form");
    var url = "get_alarm_log_data_form.py";	//$fromObj.attr("action");
    var method = $fromObj.attr("method");
    var data = $fromObj.serialize();
    $.ajax({
        type: method,
        url: url,
        data: data,
        cache: false,
        success: function (result) {
            try {
                $("#log_user").html(result);
                //result2=result.data;
                //last_execution_time=result.last_execution_time;
            }
            catch (err) {
                $().toastmessage('showErrorToast', err);
            }
        }

    });
    if (global_log == "True" && $("#alarm_log_a").hasClass("head-link-active"))
        setTimeout(function () {
            get_alarm_log_data(2);
        }, 5000);
}


function date_time(tacticalDivObj) {
    var date = serverDate;
    serverDate.setSeconds(serverDate.getSeconds() + 1);
    var year = date.getFullYear();
    var month = date.getMonth();
    var months = new Array('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December');
    var d = date.getDate();
    var day = date.getDay();
    var days = new Array('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday');
    var h = date.getHours();
    if (h < 10) {
        h = "0" + h;
    }
    var m = date.getMinutes();
    if (m < 10) {
        m = "0" + m;
    }
    var s = date.getSeconds();
    if (s < 10) {
        s = "0" + s;
    }
    var result = '' + days[day] + ' ' + months[month] + ' ' + d + ' ' + year + ' ' + h + ':' + m + ':' + s;
    tacticalDivObj.html("<div style=\"margin-top:13px;\">" + result + "</div>");
    setTimeout(function () {
        date_time(tacticalDivObj)
    }, '1000');
    return true;
}

function tacticalView(tacticalDivObj) {
    // call ajax function
    /*$.ajax({
     type:"get",
     url:"tactical_overview.py",
     cache:false,
     success:function(result){
     try
     {
     result = eval("(" + result + ")");
     }
     catch(err)
     {
     result = { "hosts":[0,0,0,0,0], "services":[0,0,0,0,0] };
     }
     tacticalViewHtml = "\
     <table width=\"100%\" cellspacing=\"0\" cellpadding=\"0\">\
     <colgroup>\
     <col width=\"62px\" style=\"width:62px;\"/>\
     <col style=\"width:auto;\"/>\
     </colgroup>\
     <tr>\
     <td class=\"label\">Hosts</td>\
     <td>\
     <a class=\"service-bar\" href=\"#\">\
     <span class=\"s-bar s-small-bar s-0\"><span class=\"text\">" + result["hosts"][1] + "</span><span class=\"ss\"></span></span>\
     <span class=\"s-bar s-small-bar s-1\"><span class=\"text\">0</span><span class=\"ss\"></span></span>\
     <span class=\"s-bar s-small-bar s-2\"><span class=\"text\">" + (result["hosts"][2]+result["hosts"][3]+result["hosts"][4]) + "</span><span class=\"ss\"></span></span>\
     <span class=\"s-bar s-small-bar s-3\"><span class=\"text\">0</span><span class=\"ss\"></span></span>\
     </a>\
     </td>\
     </tr>\
     <tr>\
     <td class=\"label\">Services</td>\
     <td>\
     <a class=\"service-bar\" href=\"#\">\
     <span class=\"s-bar s-small-bar s-0\"><span class=\"text\">" + result["services"][1] + "</span><span class=\"ss\"></span></span>\
     <span class=\"s-bar s-small-bar s-1\"><span class=\"text\">" + result["services"][2] + "</span><span class=\"ss\"></span></span>\
     <span class=\"s-bar s-small-bar s-2\"><span class=\"text\">" + result["services"][3] + "</span><span class=\"ss\"></span></span>\
     <span class=\"s-bar s-small-bar s-3\"><span class=\"text\">" + result["services"][4] + "</span><span class=\"ss\"></span></span>\
     </a>\
     </td>\
     </tr>\
     </table>";
     $(tacticalDivObj).html(tacticalViewHtml);
     tactical_call = setTimeout(function(){tacticalView(tacticalDivObj);},30000);
     }
     });*/
}

function sideBarToggle() {
    var sideBarConts = $("div.content", "#container_nav");
    var sideBarHeads = $("div.head", "#container_nav");
    //sideBarConts.hide();
    $("#container_nav").click(function (event) {
        event.stopPropagation();
    });
    sideBarHeads.click(function () {
        var $this = $(this);
        if ($this.hasClass("closed")) {
            sideBarConts.slideUp();
            sideBarHeads.removeClass("open").addClass("closed");
            $this.parent().find("div.content").slideDown();
            $this.removeClass("closed").addClass("open");
        }
        else {
            $this.parent().find("div.content").slideUp();
            $this.removeClass("open").addClass("closed");
        }
    });
    $("li a[href$='" + $("input#selected_link").val() + "']", "#container_nav").parent().addClass("selected");
}
// parseUri 1.2.2
// (c) Steven Levithan <stevenlevithan.com>
// MIT License

function parseUri(str) {
    var o = parseUri.options,
        m = o.parser[o.strictMode ? "strict" : "loose"].exec(str),
        uri = {},
        i = 14;

    while (i--) uri[o.key[i]] = m[i] || "";

    uri[o.q.name] = {};
    uri[o.key[12]].replace(o.q.parser, function ($0, $1, $2) {
        if ($1) uri[o.q.name][$1] = $2;
    });

    return uri;
};

parseUri.options = {
    strictMode: false,
    key: ["source", "protocol", "authority", "userInfo", "user", "password", "host", "port", "relative", "path", "directory", "file", "query", "anchor"],
    q: {
        name: "queryKey",
        parser: /(?:^|&)([^&=]*)=?([^&]*)/g
    },
    parser: {
        strict: /^(?:([^:\/?#]+):)?(?:\/\/((?:(([^:@]*)(?::([^:@]*))?)?@)?([^:\/?#]*)(?::(\d*))?))?((((?:[^?#\/]*\/)*)([^?#]*))(?:\?([^#]*))?(?:#(.*))?)/,
        loose: /^(?:(?![^:@]+:[^:@\/]*@)([^:\/?#.]+):)?(?:\/\/)?((?:(([^:@]*)(?::([^:@]*))?)?@)?([^:\/?#]*)(?::(\d*))?)(((\/(?:[^?#](?![^?#\/]*\.[^?#\/.]+(?:[?#]|$)))*\/?)?([^?#\/]*))(?:\?([^#]*))?(?:#(.*))?)/
    }
};

function pageTip() {
    var fileName = parseUri(document.URL);

    var pageTipMapping = {
        "manage_host": "page_tip_host",
        "manage_login": "view_page_tip_manage_login",
        "manage_group": "help_users_group",
        "manage_hostgroup": "page_tip_hostgroup",
        "discovery": "page_tip_discovery",
        "manage_service": "page_tip_service",
        "odu_scheduling": "view_page_tip_scheduling",
        "manage_user": "help_users_main",
        "trapreport": "page_tip_trap",
        "main_report": "page_tip_main_reporting",
        "analyzed_report": "page_tip_analyzed_reporting",
        "main_report_idu4": "page_tip_main_reporting",
        "main_report_odu16": "page_tip_main_reporting",
        "main_report_odu100": "page_tip_main_reporting",
        "inventory_report": "page_tip_for_inventory",
        "main_report_ap25": "page_tip_main_reporting",
        "history_report": "page_tip_history_reporting",
        "user_settings": "page_tip_change_user_setting",
        "alarm_mapping": "page_tip_alarm_mapping",
        "device_details_example": "page_tip_device_detail",
        "circle_graph": "page_tip_circle_graph",
        "daemons_controller": "page_tip_daemons",
        //"manage_license":"page_tip_license", //error
        //"manage_events":"view_page_tip_log_user",
        //"manage_logs":"view_page_tip_log_user",
        "log_user": "view_page_tip_log_user",
        "odu_listing": "page_tip_odu_listing",
        "idu_listing": "page_tip_idu_listing",
        "ap_listing": "page_tip_ap_listing",
        "ap_profiling": "page_tip_ap_listing",
        "sp_dashboard_profiling": "page_tip_sp_monitor_dashboard",
        "get_ap_advanced_graph_value": "page_tip_ap_advanced_dashboard",
        //"ap_profiling":"page_tip_ap_profiling",
        "ccu_listing": "page_tip_ccu_listing",
        "localhost_dashboard": "view_page_tip_local_dashboard",
        "status_snmptt": "page_tip_event_details",
        "googlemap": "page_tip_google_map",
        "live_monitoring": "page_tip_live_monitoring"
    };

    var ptip = $("#page_tip");
    var pageNow = fileName["file"].split("\.py")[0];
    if (ptip.length) {
        var pageHelp = pageTipMapping[pageNow];
        try {
            if (pageHelp != undefined && pageHelp !== "page_tip_google_map") {
                pageHelp = "locale/" + pageTipMapping[pageNow] + ".html";
                console.log(pageHelp, pageNow);
                ptip.colorbox(
                    {
                        href: pageHelp,
                        title: "Page Tip",
                        opacity: 0.4,
                        maxWidth: "80%",
                        width: "650px",
                        height: "450px"
//                        onComplte:function(){}
                    }
                );
            }
            else {
                return false;
            }
        }
        catch (pageTipException) {
            console.log(pageTipException);
        }
    }
    else {
        console.log("No Documentation Found");
    }
}
$(function () {
    try {
        pageTip();
    }
    catch (pageTipException) {
        console.log(pageTipException);
    }

});