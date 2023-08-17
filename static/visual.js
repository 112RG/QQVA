class VisualCommandBuilder {
    constructor(textboxId) {
      this.textbox = document.getElementById(textboxId);
      this.count = 0;
      this.socket = new WebSocket('ws://localhost:8000/listen')
    }

    appendText(text) {
      this.textbox.value += text;
    }

    increaseCount(){
        if(this.count == 10){
            alert("Max 10 commands")
            return false
        } else {
            this.count++
            return true
        }
    }

    sendCommands(){
        var lines = this.textbox.value.split('\n');
        var command_block = []
        for(var i = 0;i < lines.length;i++){
            if (lines[i].length > 1){
                command_block.push({command: lines[i], sub_command: 5})
            }
        }
        this.socket.send(JSON.stringify({commands: command_block}))
    }
}

$(document).ready(function() {
    const commandBuilder = new VisualCommandBuilder($("#command_text").attr('id'))
    commandBuilder.socket.onopen = () => {
        console.log({ event: 'onopen' })
    }
    $("#up").click(function(event) {
      if(commandBuilder.increaseCount()) {
        commandBuilder.appendText(event.target.id + "\n")
      }
      console.log("got_up");
    });
    $("#down").click(function(event) {
      if(commandBuilder.increaseCount()) {
        commandBuilder.appendText(event.target.id + "\n")
      }
      console.log("got_down");
    });
    $("#left").click(function(event) {
      if(commandBuilder.increaseCount()) {
        commandBuilder.appendText(event.target.id + "\n")
      }
      console.log("got_left");
    });
    $("#right").click(function(event) {
      if(commandBuilder.increaseCount()) {
        commandBuilder.appendText(event.target.id + "\n")
      }
      console.log("got_right");
    });
    $("#spin").click(function(event) {
      if(commandBuilder.increaseCount()) {
        commandBuilder.appendText(event.target.id + "\n")
      }
      console.log("got_spin");
    });
    $("#send_command").click(function(event) {
        commandBuilder.sendCommands();
        console.log("got_send");
      });
})
