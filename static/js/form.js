

$(document).ready(function() {
    $("#myForm").submit(function(event) {
        event.preventDefault();
        
        var formData = {
            "message": $("#message").val()
        };

        $.ajax({
            type: "POST",
            url: "/submit_form",
            data: JSON.stringify(formData),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data) {
                $("#response").text(data.response);
            },
            error: function(errMsg) {
                console.error("Error:", errMsg);
            }
        });
    });
});