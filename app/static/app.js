$(document).ready(function(){
$("form").submit(function(event){
  event.preventDefault();
  var prompt = $("#prompt").val();
  var words = prompt.split(" ");
  if(words.length > 5){
  $("#prompt").val(words.slice(0,5).join(" "));
  alert("You can only enter 5 words");
  return;
  }
  $("#loading").css("color", "#c6a54f");

  $.ajax({
    type: "POST",
    url: "/response",
    data: {prompt: prompt},
    success: function(response){
      $("#response").text(response);
      $("#loading").width("50%");
      $("#loading").css("color", "#f2f2f2");
    }
  });

const response = document.getElementById("response");
const downloadButton = document.getElementById("download-button");


downloadButton.addEventListener("click", () => {

  var habit_name = $("#prompt").val();
  const text = response.textContent;
  const blob = new Blob([text], { type: "text/plain" });
  downloadButton.href = URL.createObjectURL(blob);
  downloadButton.download = "Zbuduj nawyk" + habit_name + ".txt";
});
});
});