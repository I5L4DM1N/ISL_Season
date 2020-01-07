var add = (function () {
  var counter = 0;
  return function () {counter += 1; return counter;}
})();

/*function myFunction(){
  document.getElementById("demo").innerHTML = add();
}*/

function myFunction() {
  setInterval(function(){document.getElementById("demo").innerHTML = add(); }, 1000);
}


/*
HTML-kod

<button type="button" onclick="myFunction()">Count!</button>

	<p id="demo">0</p>
*/