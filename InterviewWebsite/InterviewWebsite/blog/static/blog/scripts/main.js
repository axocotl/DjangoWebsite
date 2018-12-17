function shuffle(id)
{
    var elements = $("#"+id);
    var shuffle_order = get_shuffle_order(Array.apply(null, {length: elements[0].children.length}).map(Number.call, Number));
    var new_order = document.createElement('div');
    for(var i = 0; i < shuffle_order.length; i++)
    {
        new_order.appendChild(elements[0].children[shuffle_order[i]].cloneNode(true));
    }
    elements[0].innerHTML = new_order.innerHTML;
}

function get_shuffle_order (array)
{
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}