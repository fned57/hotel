"use strict";

$(document).ready(function () {
            $("#btnsubmit").click(function (event) {
                event.preventDefault();
                var form = $('#send_data')[0];
                var data = new FormData(form);
                $("#btnSubmit").prop("disabled", true);

                $.ajax({
                    type: "POST",
                    enctype: 'multipart/form-data',
                    url: "/bookings",
                    data: data,

                    processData: false,
                    contentType: 'application/json',
                    cache: false,
                    timeout: 800000,
                    success: function (data) {
                        console.log(data);
                    },
                    error: function (e) {
                        console.log("ERROR : ", e);
                        $("#btnSubmit").prop("disabled", false);
                    }
                });
            });
        });
