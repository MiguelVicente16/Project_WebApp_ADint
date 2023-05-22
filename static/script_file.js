const dropdownElementList = document.querySelectorAll('.dropdown-toggle')

const dropdownList = [...dropdownElementList].map(dropdownToggleEl => new bootstrap.Dropdown(dropdownToggleEl))

const radioButtons = document.querySelectorAll("input[name='flexRadioDefault']");

function changeStatus(){
  var status = document.getElementById("service");
  if(status.value == "nenhuma")
  {
    document.getElementById("evaluation").style.visibility="hidden";
    document.getElementById("label_txt").style.visibility="hidden";
  }
  else
  {
    document.getElementById("evaluation").style.visibility="visible";
    document.getElementById("label_txt").style.visibility="visible";
  }
}

radioButtons.forEach(radio => {
radio.addEventListener("click", handleRadioClick);
});

function changeStatus_activity(aux){

  if(aux == 5)
  {
    document.getElementById("appear_txt_area").style.display="block";
    
  }
  else
  {
    document.getElementById("appear_txt_area").style.display="none";
  }
}

function hide_show_checkbox(aux) {
  var x;
  x = document.getElementById("Courses_check");
  if (aux === 1) {
    x.style.display = "block";
  } else {
    document.getElementById('Courses_check').style.display = "none"
    $('input[name="Courses"]').prop('checked', false);
    $('input[name="Courses"]').val('')
    x.style.display = "none";
  }
}

function openTab(show_tab, hide_tab2, hide_tab3, button_id_active, button_id2, button_id3) {
  if(document.getElementById(show_tab).style.display == "none"){
    document.getElementById(show_tab).style.display = "block"
    document.getElementById(hide_tab2).style.display = "none"
    document.getElementById(hide_tab3).style.display = "none"
    document.getElementById(button_id_active).style.backgroundColor = "#E1E6FF"
    document.getElementById(button_id_active).style.color = "black"
    document.getElementById(button_id_active).style.borderColor = "black"
    document.getElementById(button_id2).style.backgroundColor = "#000be4"
    document.getElementById(button_id2).style.color = "#fff"
    document.getElementById(button_id_active).style.borderColor = "fff"
    document.getElementById(button_id3).style.backgroundColor = "#000be4"
    document.getElementById(button_id3).style.color = "#fff"
    document.getElementById(button_id_active).style.borderColor = "fff"
    document.getElementById('Courses_check').style.display = "none"
    $('input[name="Administrative"]').prop('checked', false);
    $('input[name="Courses"]').prop('checked', false);
    $('input[name="Academic"]').prop('checked', false);
    $('input[name="Personal"]').prop('checked', false);
  } else{
    document.getElementById(show_tab).style.display = "none"
    document.getElementById(button_id_active).style.backgroundColor = "#000be4"
    document.getElementById(button_id_active).style.color = "#fff"
    document.getElementById(button_id_active).style.borderColor = "fff"
  }
}

function myFunction(dropdown) {
/* When the user clicks on the button, toggle between hiding and showing the dropdown content */
document.getElementById(dropdown).classList.toggle("show");
}

window.onclick = function(event) {
  // Close the dropdown menu if the user clicks outside of it
  if (!event.target.matches('.drop')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

$(document).ready(function(){

  $("#home").click(function(){
    document.getElementById('Create_Activity').style.display = "none"
    document.getElementById('List_Courses').style.display = "none"
    document.getElementById('home_div').style.display = "block"
    document.getElementById('Create_evaluation').style.display = "none"
    document.getElementById('top').scrollIntoView(); 
    $("#button_activity").addClass("ghost")
    $("#button_evaluation").addClass("ghost")
    $("#button_course").addClass("ghost")
    $("#home").removeClass("ghost")
  })
  
  $("#button_evaluation, #butao_avaliacao").click(function(){
    document.getElementById('Create_Activity').style.display = "none"
    document.getElementById('List_Courses').style.display = "none"
    document.getElementById('home_div').style.display = "none"
    document.getElementById('Create_evaluation').style.display = "block"
    document.getElementById('Create_evaluation').scrollIntoView(); 
    $("#button_activity").addClass("ghost")
    $("#home").addClass("ghost")
    $("#button_course").addClass("ghost")
    $("#button_evaluation").removeClass("ghost")
    $.ajax({
            url: '/evaluations/new',
            type: "GET",
            dataType: "json",
            success: function (data_1) {
                listbox = document.querySelector('#service');
                $('#service').empty()
                $('#service').append('<option value = "nenhuma"  selected class="form-control">Click and pick a service to evaluate</option>')
                for (var i = 0;  i < Object.keys(data_1["lista"]).length; i++){
                    option = new Option(data_1["lista"][i], data_1["lista"][i]);
                    listbox.add(option, undefined);
                }
            }
      });
      
  })

  $("#submit_evaluation").click(function(e){
    e.preventDefault();
         $.ajax({
          url : '/evaluations/new',
          type : 'POST',
          dataType: "json",
          contentType: 'application/json',
          data :  JSON.stringify({
               service : $('#service').val(),
               evaluation : $('#evaluation').val()
             }),
             success:function(){
              alert("You cant evaluate a non existent Service")
             }
      });
     $('#service').val("nenhuma").attr('selected','selected');
     $('#evaluation').val('');
  });

  $("#button_course, #butao_curso").click(function(){
    document.getElementById('Create_Activity').style.display = "none"
    document.getElementById('List_Courses').style.display = "block"
    document.getElementById('home_div').style.display = "none"
    document.getElementById('Create_evaluation').style.display = "none"
    document.getElementById('List_Courses').scrollIntoView(); 
    $("#button_activity").addClass("ghost")
    $("#home").addClass("ghost")
    $("#button_evaluation").addClass("ghost")
    $("#button_course").removeClass("ghost")
    $.ajax({
            url: '/courses',
            type: "GET",
            dataType: "json",
            success: function (data_1) {
                var list = document.getElementById('course_list');
                $('#course_list').empty()
                for (var i = 0;  i < Object.keys(data_1["courses"]).length; i++){
                    var string = "<li id = 'list_course_" + i + "'"+" class='list-group-item d-flex justify-content-between align-items-start'>"
                    var lista = "#list_course_"+i
                    var div = "#div_course_"+i
                    var string_2 = "<div style = 'width:60%;' id ='div_course_" +i+"'"+"class='ms-2 me-auto'></div>"
                    var div_2 = "div_bold_"+i
                    var string_3 = "<div style= 'margin:auto' class='fw-bold' id ='div_bold_"+i+"'"+ "></div>"
                    $("#course_list").append($(string))
                    $(lista).append($(string_2))
                    $(div).append($(string_3))
                    text = data_1["courses"][i]["acron"] + "    |    " + data_1["courses"][i]["nome"]
                    document.getElementById(div_2).appendChild(document.createTextNode(text));
                    var button = "<a style ='margin:auto' href='"+ data_1["courses"][i]["url"]+"'"+" ><button style ='width: 100%; height:70%; font-size:12px; ' class='btn btn-primary' type='button'>Go to</button></a>"
                    $(lista).append($(button))
              }
            }
      });
  })

  $("#button_activity, #butao_atividade").click(function(){
    plot()
    table()
    document.getElementById('Create_evaluation').style.display = "none"
    document.getElementById('List_Courses').style.display = "none"
    document.getElementById('home_div').style.display = "none"
    document.getElementById('Create_Activity').style.display = "block"
    document.getElementById('Create_Activity').scrollIntoView(); 
    $("#home").addClass("ghost")
    $("#button_course").addClass("ghost")
    $("#button_activity").removeClass("ghost")
    $("#button_evaluation").addClass("ghost")
    $.ajax({
            url: '/activities/new',
            type: "GET",
            dataType: "json",
            success: function (data_1) {
                $('#Courses_check').empty()
                for (var i = 0;  i < Object.keys(data_1["courses"]).length; i++){
                    var string = "<div class='form-check' style= 'margin: 5px 70px 5px ;' id = 'div_id_list_courses_"+i+"'>"+"</div>"
                    var div = "#div_id_list_courses_"+i
                    var string_2 = "<input class='form-check-input' type = 'radio'style = 'border: 1px solid black; position: relative;' name='Courses' id='Courses' value =' "+data_1["courses"][i]["acron"]+"'"+">"
                    var label =  "<label class='form-check-label' style = 'position: absolute; left: 50%;' for='Courses'>"+data_1["courses"][i]["acron"] +"</label>"
                    $("#Courses_check").append($(string))
                    $(div).append($(string_2))
                    $(div).append($(label))
              }
              $('#Administrative_check').empty()
              for (var i = 0;  i < Object.keys(data_1["lista"]).length; i++){
                var string = "<div class='form-check' style= 'margin: 3px 15px 5px;' id = 'div_check_"+i+"'>"+"</div>"
                var div = "#div_check_"+i
                var string_2 = "<input class='form-check-input'  style = ' border: 1px solid black; position: relative; ' type='radio' name='Administrative' id='Administrative' value ='"+ data_1["lista"][i]+"'  required>"
                var label =  "<label class='form-check-label' for='Administrative'>"+data_1["lista"][i] +"</label>"
                $("#Administrative_check").append($(string))
                $(div).append($(string_2))
                $(div).append($(label))
              }
            }
      });
  })

  $("#button_administrative").click(function(e){
    e.preventDefault();
    $('input[name="Personal"]').prop('checked', false);
    $('input[name="Academic"]').prop('checked', false);
    $('#Personal').val('')
    $('#Academic').val('')
    if(($('input[name="Administrative"]:checked').val() != '')  && ($('#date_Administrative_start').val() != '') && ($('#date_Administrative_end').val() != '')){
         $.ajax({
          url : '/activities/new',
          type : 'POST',
          dataType: "json",
          contentType: 'application/json',
          data :  JSON.stringify({
              Administrative : $('input[name="Administrative"]:checked').val(),
              Personal : $('#Personal').val(),
              Academic: $('#Academic').val(),
              date_Administrative_start:  $('#date_Administrative_start').val(),
              date_Administrative_end: $('#date_Administrative_end').val(),
             }),
             success:function(){
              plot()
              table()
              alert("New activity created successfully")
             }
      });
    }else{
      alert("!To submit you must choose an Option of activity and a Start and End Date!")
    }
    document.getElementById('Courses_check').style.display = "none"
    $('input[name="Administrative"]').val('')
    $('input[name="Administrative"]').prop('checked', false);
    $('input[name="Courses"]').prop('checked', false);
    $('input[name="Courses"]').val('')
    $('#date_Administrative_start').val('');
    $('#date_Administrative_end').val('');
   });
  
  $("#button_academic").click(function(e){
    e.preventDefault();
    $('input[name="Personal"]').prop('checked', false);
    $('input[name="Administrative"]').prop('checked', false);
    $('#Personal').val('')
    $('#Administrative').val('')
    if(($('input[name="Academic"]:checked').val() != '')  && ($('#date_Academic_start').val() != '') && ($('#date_Academic_end').val() != '')){
         $.ajax({
          url : '/activities/new',
          type : 'POST',
          dataType: "json",
          contentType: 'application/json',
          data :  JSON.stringify({
              Academic : $('input[name="Academic"]:checked').val(),
              Personal : $('#Personal').val(),
              Administrative: $('#Administrative').val(),
              Courses: $('input[name="Courses"]:checked').val(),
              date_Academic_start:  $('#date_Academic_start').val(),
              date_Academic_end: $('#date_Academic_end').val(),
             }),
             success:function(){
              plot()
              table()
              alert("New activity created successfully")
             }
      });
    }else{
      alert("!To submit you must choose an Option of activity and a Start and End Date!")
    }
    document.getElementById('Courses_check').style.display = "none"
    $('input[name="Academic"]').val('')
    $('input[name="Academic"]').prop('checked', false);
    $('input[name="Courses"]').prop('checked', false);
    $('input[name="Courses"]').val('')
    $('#date_Academic_start').val('');
    $('#date_Academic_end').val('');

   });
  
  $("#button_personal").click(function(e){
    e.preventDefault();
    $('input[name="Academic"]').prop('checked', false);
    $('input[name="Administrative"]').prop('checked', false);
    $('#Academic').val('')
    $('#Administrative').val('')
    if(($('input[name="Personal"]:checked').val() != '')  && ($('#date_Personal_start').val() != '') && ($('#date_Personal_end').val() != '')){
         $.ajax({
          url : '/activities/new',
          type : 'POST',
          dataType: "json",
          contentType: 'application/json',
          data :  JSON.stringify({
               Personal : $('input[name="Personal"]:checked').val(),
               Academic : $('#Academic').val(),
               Administrative: $('#Administrative').val(),
               newactivity: $('#newactivity').val(),
               date_Personal_start:  $('#date_Personal_start').val(),
               date_Personal_end: $('#date_Personal_end').val(),
             }),
             success:function(){
              plot()
              table()
              alert("New activity created successfully")
             }
      });
    } else{
      alert("!To submit you must choose an Option of activity and a Start and End Date!")
    }
    $('input[name="Personal"]').val('')
    $('input[name="Personal"]').prop('checked', false);
    $('#newactivity').val('');
    $('#date_Personal_start').val('');
    $('#date_Personal_end').val('');
   });
});

/**
 *  Send a AJAX request to server to obtain plot information and next print it
 */
function plot(){
  $('#plot').empty()
  $.ajax({
            url: '/output',
            type: "GET",
            dataType: "json",
            success: function (data_1) {
              var string = "<img src='data:image/png;base64, "+data_1["plot_url"]+"' alt='Chart' class = 'plot'>"
              $("#plot").append($(string))
            }
          })
}

/**
 *  Send a AJAX request to server to obtain table information and next print it
 */
function table(){
  $.ajax({
            url: '/table',
            type: "GET",
            dataType: "json",
            success: function (data_1) {
              
              $('#table').empty()
              $('#table tbody').empty()
              var string = "<tr id= row'></tr>"
              $("#table").append($(string))
              $("#table tr").append($("<th>Activity</th>"))
              $("#table tr").append($("<th>Type</th>"))
              $("#table tr").append($("<th>Start</th>"))
              $("#table tr").append($("<th>End</th>"))
              for (var i = 0;  i < Object.keys(data_1["table"]).length; i++){
                var string = "<tr id= row_'"+i+"'></tr>"
                var div = "#row_"+i
                $("#table tr:last").after(string)
                var row = "<td>"+data_1["table"][i]["activity"]+"</td> <td>"+data_1["table"][i]["area"]+"</td> <td>"+data_1["table"][i]["start"]+"</td> <td>"+data_1["table"][i]["end"]+"</td>"
                $("#table tr:last").append($(row))
              }
            }
          })
}