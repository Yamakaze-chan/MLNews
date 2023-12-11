function active_nav_curr()
{
  var header = document.getElementById("nav_btn");
  var btns = header.getElementsByClassName("button");
  for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
    });
  }
  document.getElementById("frame_content").src = "./Change_currency";
}

function active_nav_gold()
{
  var header = document.getElementById("nav_btn");
  var btns = header.getElementsByClassName("button");
  for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
    });
  }
  document.getElementById("frame_content").src = "./Change_gold";
}

function active_nav_stock()
{
  var header = document.getElementById("nav_btn");
  var btns = header.getElementsByClassName("button");
  for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
    });
  }
  document.getElementById("frame_content").src = "./Change_stock";
}