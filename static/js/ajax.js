$("#generate").click(() => {
    $.ajax({
        url: "/generate",
        success: (data) => {
            $("#generate").prop('disabled', true);
            $("#punchline").html("");
            $("#joke").html(data["joke"]).hide().fadeIn(2000, () =>  {
                $("#punchline").html(data["punchline"]).hide().fadeIn(2000);
                $("#generate").prop('disabled', false);
            });
            $('#favorites').val(data["id"]);
            $("#generate").html("Generate another");
        }
    });
});

$("#favorites").click(() => {
    $.ajax({
        type: "POST",
        url: "/favorites",
        data: {jokeId: $("#favorites").val()},
        success: function(data){
            alert(data["message"]);
        },
        error: () => {
            alert("An error has occurred or you didn't log in");
        }
    });
});

$("#delete").click(() => {
    var jokeId = "#" + $("#delete").val();
    $.ajax({
        type: "POST",
        url: "/delete",
        data: {joke: $(jokeId).html()},
        success: () => {
            location.reload();
        },
        error: () => {
            location.reload();
        }
    });
});
