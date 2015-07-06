/**
 * Created by Tadej on 6.7.2015.
 */

function dragStart(e){
    e.dataTransfer.setData("text/plain", this.href);
}

function dragEnd(e){
    e.preventDefault();
    e.stopPropagation();
    var data = e.dataTransfer.getData("text/plain");
    var ids = data.split('=');
    var id = ids[ids.length-1];
    var children = this.children;
    var row = -1;
    var col = -1;
    for (var child of children){
        if (child.tagName == 'INPUT'){
            if (child.name == 'row'){
                row = child.value;
            }
            if (child.name == 'col'){
                col = child.value;
            }
        }
    }
    var request = $.ajax({
        method: "POST",
        url: "/app/papers/add_to_schedule/",
        data: { row:row, col:col, id:id},
    });
    request.done(function(msg){
        $("#mydiv").load(location.href+" #myDiv>*","");
    });
    request.fail(function() {
        alert( "Request failed ");
    });

}

function dragOver(e){
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
    return false
}

 $(document).ready(function() {
     var papers = document.getElementsByName('paper');
     for (var paper of papers) {
         paper.addEventListener('dragstart', dragStart, false);
     }
     var slots = document.getElementsByName('slot');
     for (var slot of slots){
         slot.addEventListener('dragover', dragOver, false);
         slot.addEventListener('drop', dragEnd, false);
     }
 })