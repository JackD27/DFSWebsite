
function getPermutations(array, size2) {
    function p(t, i) {
        if (t.length === size2) {
             result.push(t);
                return;
                  }
                  if (i + 1 > array.length) {
                      return;
                  }
                  p(t.concat(array[i]), i + 1);
                  p(t, i + 1);
              }
            
              var result = [];
              p([], 0);
              return result;
            }

let players = [];

document.onkeydown=function(){
    if(window.event.keyCode=='13'){
        addText();
    }
}

size = 2

function addText() {
    
    let text = document.getElementById('text').value;
    if (text.length > 1){
        players.push(text);
    }

    var str = ""
    var pval = ""
    

    players.forEach(function(player) {
        pval += '<li>'+ player + '</li>';
      }); 
      
      pval += '</ul>';
      document.getElementById("result-text").innerHTML = pval;

    document.getElementById('text').value = "";
    combos = getPermutations(players, size);

    combos.forEach(function(combo) {
        str += '<li>'+ combo + '</li>';
      }); 
      
      str += '</ul>';
      document.getElementById("comboContainer").innerHTML = str;
    
    var items = document.querySelectorAll("#result-text li")
    for (var i = 0; i < items.length; i++) {
        items[i].onclick = function() {
            document.getElementById("text").value = this.innerHTML
            
        }

        };

    }


function deleteWord(){
    let text = document.getElementById('text').value;
    for (var i = 0; i < players.length; i++) {
        if (players[i] === text) {
            players.splice(i, 1);
            document.getElementById('text').value = "";
            addText()
            }
        }
}

function deleteAll(){
    while (players.length) {
        players.pop();
    }
    addText()
}


    


