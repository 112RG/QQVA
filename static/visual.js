class VisualCommandBuilder {
    constructor(textboxId) {
      this.textbox = document.getElementById(textboxId);
    }

    appendText(text) {
      this.textbox.value += text;
    }
}

$(document).ready(function() {
    $("#up").click(function() {
        console.log("got_up");
      });
      $("#down").click(function() {
        console.log("got_up");
      });
      $("#left").click(function() {
        console.log("got_up");
      });
      $("#right").click(function() {
        console.log("got_up");
      });
      $("#spin").click(function() {
        console.log("got_up");
      });
})
