<script type="text/javascript">
/* function get_fac_name() {
    let fac = $("#selFac option:selected" ).val();
    $("#txtFac").val(fac);
}

function get_fac_name_s() {
    let fac = $("#selFacSearch option:selected" ).val();
    $("#txtFacSearch").val(fac);
}

function validateForm() {
    let dateReport = $('#dateReport').val();
    let dateOccur = $('#dateOccur').val();
    let selFac = $("#selFac option:selected" ).text().trim();
    let txtPatient = $('#txtPatient').val().trim();
    let txtPerRept = $('#txtPerRept').val();
    let txtPhone = $('#txtPhone').val();
    let selPerComp= $('#selPerComp').val();
    let selIntake = $('#selIntake').val();
    let selMed = $('#selMed').val();
    let selShipping = $('#selShipping').val();
    let selDelivery = $('#selDelivery').val();
    let selBilling= $('#selBilling').val();
    let selCooking = $('#selCooking').val();
    let selOther = $('#selOther').val();
    let selTechInv = $('#selTechInv').val();
    let selRphInv = $('#selRphInv').val();
    let txtExp = $('#txtExp').val();
    let opcode =  $('#opcode').val();
    let id = "0";

    let msg = "";
    let type_count = 0;
    console.log(txtPatient);

    if(dateReport.trim() === "") {
        msg += "A date for discovery or reporting is required<br />";
    }
    if(dateOccur.trim() === "") {
        msg += "An occurence date is required<br />";
    }
    if(selFac.trim() === "0") {
        msg += "A Facility code is required<br />";
    }

    $('.selType').each(function(index, item){
        if ($(this).val() !== "0") {
            type_count += 1;
        }
    });

    if (type_count === 0){
        msg += "At least one reason from the 'Types of Occurences' is required<br />";
    }

    if(txtExp.trim() === "") {
        msg += "A explanation of the occurence is required<br />";
    }

    
    if (msg !== "") {
        $('#errMsg').html(msg);
        $('#mError').modal('show');
        return false;    
    }
    else {
        if (opcode === 'update'){
            id = $("#txtID").val();
        }
    
        $.ajax({
            type: "POST",
            url: "{{url_for('occur')}}",
            dataType: 'json',
            data: {
                'dateReport': dateReport,
                'dateOccur': dateOccur,
                'selFac': selFac,
                'txtPatient': txtPatient,
                'txtPerRept': txtPerRept,
                'txtPhone': txtPhone,
                'selPerComp': selPerComp,
                'selIntake': selIntake,
                'selMed': selMed,
                'selShipping': selShipping,
                'selDelivery': selDelivery,
                'selBilling': selBilling,
                'selCooking': selCooking,
                'selOther': selOther,
                'selTechInv': selTechInv,
                'selRphInv': selRphInv,
                'txtExp': txtExp,
                'op-code': opcode,
                'id': id
            },
            async: false,
            success: function (data) {
            },
            complete: function (data) {
                if (opcode === 'update'){
                    $('#tmInfo').html("Update Complete");
                    $('#pmInfo').html("Update completed for Occurence with ID: " + id )
                    $('#mInfo').modal('show');
                }
                //location.reload();
            }
        });
    }


}

function search() {
    $('#errMsgSearch').html("");
    let facility = $("#selFacSearch option:selected" ).text().trim();
    let startDate = $('#txtDateStart').val().trim();
    let endDate = $('#txtDateEnd').val().trim();
    let dateType = $("input[name='optDate']:checked").val().trim();
    let dates = "", filter = "", facSearch = "", where = " WHERE ";
    let html = '';

    if (facility === "" && startDate === '' && endDate === '') {
        $('#errMsgSearch').html("A search term must be entered");
        return false;
    }
    
    if (!compareDates(startDate, endDate) && (startDate !== '' && endDate !== '')) {
        $('#errMsgSearch').html("The starting date cannot be later than the ending date");
        return false;
    }

    if (startDate !== '' && endDate  === ""){
        dates =  dateType + " = '" + startDate + "'"
    }
    else if ( startDate !== '' && endDate  !== ""){
        dates = " ( " + dateType + " >= '" + startDate + "' AND " + dateType + " <= '" + endDate + "' ) " 
    }

    if (facility != '') {
        facSearch = "FACILITY_CODE = '" + facility + "'"
    }

    if (facility != '' && (startDate === '' && endDate === '')) {
        filter = where + facSearch;
    }
    else if(facility != '') {
        filter = where + facSearch + " AND " + dates;
    }
    else {
        filter = where  + dates;
    }

    $.ajax({
        data: {
            sql: `SELECT ID
                ,CONVERT(char(10)
                ,DISCOVER_DATE,126) as DISCOVER_DATE
                ,CONVERT(char(10), OCCUR_DATE,126) as OCCUR_DATE
                ,FACILITY_CODE, CREATED_BY
                ,USERNAME
                FROM dbo.RPT_OCCUR 
            `+ filter
        },
        type: 'POST',
        url: '/getSearch',
        dataType: 'json'
    })
    .done(function (data) {
        $.each(data, function (index, item) {
            let id = item.ID
            let dateDiscover = item.DISCOVER_DATE;
            let dateOccur = item.OCCUR_DATE;
            let facCode = item.FACILITY_CODE;
            let createdBy = item.USERNAME;
            let facName = $("#txtFacSearch").val();
            html += '<tr><td>' + dateDiscover + '</td>';
            html += '<td>' + dateOccur + '</td>';
            html += '<td>' + facCode + '</td>';
            html += '<td>' + createdBy + '</td>';
            html += `<td><a id="edit-user" href="#" onclick="edit_occurence(` + id + `,'` + facName +  `')" >Edit</a></td></tr>`;
            
        });
        $("#tbSearch").html(html);
    });
    console.log(filter);
    // console.log(dateType);
}

function edit_occurence(id, facName){
    $.ajax({
        data: {
            sql: `SELECT ID
                ,CONVERT(char(10),[DISCOVER_DATE],126) as DISCOVER_DATE
                ,CONVERT(char(10), [OCCUR_DATE],126) as OCCUR_DATE
                ,[USERNAME]
                ,[FACILITY_CODE]
                ,[CREATED_BY]
                ,[USERNAME]
                ,[FACILITY_CODE]
                ,[PATIENT_NAME]
                ,[PERSON_REPORTING]
                ,[PHONE]
                ,[PERSON_COMPLETING]
                ,[ORDER_INTAKE]
                ,[MEDICATION]
                ,[SHIPPING]
                ,[DELIVERY]
                ,[BILLING]
                ,[COOKING]
                ,[OTHER]
                ,[TECH_ID]
                ,[RPH_ID]
                ,[EXPLANATION]
                FROM dbo.[RPT_OCCUR] WHERE [ID] = `+ id
        },
        type: 'POST',
        url: '/getSearch',
        dataType: 'json'
    })
    .done(function (data) {
        $.each(data, function (index, item) {
            $('#dateReport').val(item.DISCOVER_DATE);
            $('#dateOccur').val(item.OCCUR_DATE);
            //$("#selFac option:selected").text(item.FACILITY_CODE);
            $("#selFac").val(facName);
            $("#txtFac").val(facName);
            $('#txtPatient').val(item.PATIENT_NAME);
            $('#txtPerRept').val(item.PERSON_REPORTING);
            $('#txtPhone').val(item.PHONE);
            $('#selPerComp').val(item.PERSON_COMPLETING);
            $('#selIntake').val(item.ORDER_INTAKE); 
            $('#selMed').val(item.MEDICATION);
            $('#selShipping').val(item.SHIPPING);
            $('#selDelivery').val(item.DELIVERY);
            $('#selBilling').val(item.BILLING);
            $('#selCooking').val(item.COOKING);
            $('#selOther').val(item.OTHER);
            $('#selTechInv').val(item.TECH_ID);
            $('#selRphInv').val(item.RPH_ID);
            $('#txtExp').val(item.EXPLANATION);
            $('#opcode').val('update');
            $('#dMode').html("Update Mode");
            $("#txtID").val(item.ID);
        });
    });
    $('#mSearch').modal('hide');
}

function compareDates(start, end){
    try {
        let dStart = Date.parse(start);
        let dEnd = Date.parse(end);
        console.log(start);

        if (dStart > dEnd) {
            return false
        }
        return true;
    }
    catch(err){
        alert(err.message)
        return false;
    }
}

function openSearch() {
    $('#mSearch').modal('show');
    $('#rbStart').prop("checked", true);;
    $('#txtDateStart').val("");
    $('#txtDateEnd').val("");
    $('#txtFacSearch').val("");
    $('#selFacSearch').val("0");
    $("#tbSearch").html("");
    $('#errMsgSearch').html("");
}

function clearForm() {
    $('#dateReport').val("");
    $('#dateOccur').val("");
    $("#selFac" ).val("0")
    $("#txtFac" ).val("")
    $('#txtPatient').val("")
    $('#txtPerRept').val("");
    $('#txtPhone').val("");
    $('#selPerComp').val("0");
    $('#selIntake').val("0");
    $('#selMed').val("0");
    $('#selShipping').val("0");
    $('#selDelivery').val("0");
    $('#selBilling').val("0");
    $('#selCooking').val("0");
    $('#selOther').val("0");
    $('#selTechInv').val("0");
    $('#selRphInv').val("0");
    $('#txtExp').val("");
    $("#txtID").val("0");
    $("#txtID").val("insert");
    $("#dMode").html("Add Mode");
}  */

</script>